#!/usr/bin/env python3

__version__ = "1.4"

from ansible.plugins.callback import CallbackBase
from datetime import datetime, timezone
import os
import csv
import json
import getpass
import pwd
import tempfile
import sys
import subprocess

class CallbackModule(CallbackBase):
    """
    Ansible callback plugin (v1.4) that logs tasks reporting changes (changed=True) to a CSV file.
    Aligned to match the expected schema for the consolidation script.
    - Filters out 'localhost' to log only managed infrastructure devices.
    - Captures the complete execution context of multi-command prompts and strings universally.
    - Filters loop entries to ONLY log individual items that actually produced a change.
    - Cleans up loop string formatting to strictly print 'Commands: [configure terminal -> no...; configure terminal -> ...]'.
    - Logs WHAT was invoked (commands/configs) and completely omits execution output.
    """
    CALLBACK_VERSION = 1.4
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'device_change_logger'
    CALLBACK_NEEDS_ENABLED = True

    # Exact layout expected by the csv herder script
    EXPECTED_HEADER = ['Timestamp', 'Invoked By', 'Host', 'Playbook', 'Task', 'Changes - Summarized']

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.playbook = None
        self.group = "ems"

        self.log_dir = '/ncm/common/ansible/changes'
        playbook_timestamp = datetime.now().isoformat()
        username = getpass.getuser()
        if "@" in username:
            username = username.split("@")[0]
            
        self.default_log_file = os.path.normpath(os.path.join(self.log_dir, f'change_{username}_{playbook_timestamp}.csv'))
        self.check_log_file = os.path.normpath(os.path.join(self.log_dir, f'checks_{username}_{playbook_timestamp}.csv'))
        
        self.log_file = os.path.normpath(os.environ.get('ANSIBLE_CHANGE_LOG_FILE', self.default_log_file))

        # Ensure the normal mode log directory exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        if self.log_file == self.default_log_file:
            if not os.path.exists(self.log_file):
                self._initialize_csv(self.log_file)
            else:
                self._ensure_invoked_by_column(self.log_file)

    def _initialize_csv(self, path):
        """Helper to create an empty CSV file cleanly with correct headers and permissions."""
        old_umask = os.umask(0)
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o0660)
            with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.EXPECTED_HEADER)
        finally:
            os.umask(old_umask)
        try:
            subprocess.run(["chgrp", self.group, path], check=False)
        except Exception:
            pass

    def v2_playbook_on_start(self, playbook):
        self.playbook = os.path.basename(playbook._file_name)

    def v2_runner_on_ok(self, result, **kwargs):
        if result._result.get('changed', False):
            self._log_change(result)

    def v2_runner_on_failed(self, result, **kwargs):
        if result._result.get('changed', False):
            self._log_change(result)

    def _get_invoking_user(self):
        sudo_user = os.environ.get('SUDO_USER')
        if sudo_user:
            return sudo_user
        for envname in ('INVOKED_BY', 'GITHUB_ACTOR', 'GITLAB_USER_LOGIN', 'BUILD_USER', 'AWX_USERNAME', 'TOWER_USERNAME', 'ANSIBLE_RUNNER'):
            v = os.environ.get(envname)
            if v:
                return v
        try:
            return getpass.getuser()
        except Exception:
            pass
        try:
            return pwd.getpwuid(os.geteuid()).pw_name
        except Exception:
            pass
        return 'unknown'

    def _log_change(self, result):
        host = result._host.get_name()
        
        # Filter out local execution tracking steps completely
        if host.lower() == 'localhost' or host == '127.0.0.1':
            return

        task = result._task.get_name()
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
        invoked_by = self._get_invoking_user()

        is_check_mode = '-C' in sys.argv or '--check' in sys.argv
        log_file = self.check_log_file if (is_check_mode and 'ANSIBLE_CHANGE_LOG_FILE' not in os.environ) else self.log_file

        # Defensive dynamic file check if directories swap midway
        if not os.path.exists(log_file):
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            self._initialize_csv(log_file)
        else:
            self._ensure_invoked_by_column(log_file)

        # Format changes
        summarized = self._format_change_details(result._result)
        if is_check_mode:
            summarized = f"Check mode: {summarized}"

        # Append data row strictly mapped to the EXPECTED_HEADER layout
        with open(log_file, 'a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, invoked_by, host, self.playbook, task, summarized])

    def _format_change_details(self, result_dict):
        """
        Format task changes into a human-readable string for the 'Changes - Summarized' column.
        Strictly logs WHAT was invoked, skipping any looped actions that did not make a change.
        """
        def recursive_diff(old, new, path=""):
            changes = []
            if isinstance(old, dict) and isinstance(new, dict):
                for key in set(old.keys()) | set(new.keys()):
                    old_val = old.get(key, '<not set>')
                    new_val = new.get(key, '<not set>')
                    changes.extend(recursive_diff(old_val, new_val, path + key + "."))
            elif isinstance(old, list) and isinstance(new, list):
                if len(old) != len(new):
                    changes.append(f"{path[:-1]}: list length {len(old)} -> {len(new)}")
                else:
                    for i in range(len(old)):
                        changes.extend(recursive_diff(old[i], new[i], path + f"[{i}]."))
            elif old != new:
                changes.append(f"{path[:-1]}: {old} -> {new}")
            return changes

        def extract_command_lines(raw_cmds):
            """Helper to safely extract command text whether it's a string or a dictionary list."""
            extracted = []
            if isinstance(raw_cmds, list):
                for c in raw_cmds:
                    if isinstance(c, dict) and 'command' in c:
                        extracted.append(str(c['command']))
                    elif isinstance(c, str):
                        extracted.append(c)
            elif isinstance(raw_cmds, str):
                extracted.append(raw_cmds)
            return extracted

        try:
            # --- 1. Handle nested loops/results (e.g., Sledgehammer or looping secrets) ---
            if 'results' in result_dict and isinstance(result_dict['results'], list):
                looped_cmds = []
                for res in result_dict['results']:
                    if not isinstance(res, dict):
                        continue
                    
                    # Target item filter: bypass entries that did not alter device configurations
                    if not res.get('changed', False):
                        continue
                    
                    # 1a. Check module invocation arguments first to catch exact multi-commands list per loop execution
                    if 'invocation' in res and 'module_args' in res['invocation']:
                        args = res['invocation']['module_args']
                        target_cmds = args.get('commands') or args.get('command') or args.get('lines')
                        found_cmds = extract_command_lines(target_cmds)
                        if found_cmds:
                            # Cleaned up layout: dropped individual "Command: " prefixes
                            looped_cmds.append(" -> ".join(found_cmds))
                            continue

                    # 1b. Fallback to standard loop item logging if invocation blocks are missing
                    if 'item' in res:
                        if isinstance(res['item'], dict):
                            item_val = res['item'].get('item', res['item'])
                            looped_cmds.append(str(item_val))
                        else:
                            looped_cmds.append(str(res['item']))

                if looped_cmds:
                    # Fixed: Corrected string concatenation syntax error on closing bracket
                    return "Commands: [" + "; ".join(looped_cmds) + "]"

            # --- 2. Handle standard cisco.ios.ios_config or top-level commands lists (Non-Looped) ---
            commands = result_dict.get('commands')
            if commands:
                found_cmds = extract_command_lines(commands)
                if found_cmds:
                    return "Commands: [" + ", ".join(found_cmds) + "]"

            # Fallback parsing directly inside top-level module arguments tree
            if 'invocation' in result_dict and 'module_args' in result_dict['invocation']:
                args = result_dict['invocation']['module_args']
                target_lines = args.get('lines') or args.get('commands') or args.get('command')
                found_cmds = extract_command_lines(target_lines)
                if found_cmds:
                    return "Commands: [" + ", ".join(found_cmds) + "]"

            # --- 3. Diffs / Attribute changes fallback (e.g., SNMP state changes) ---
            before = result_dict.get('before')
            after = result_dict.get('after')
            if before is not None and after is not None:
                if isinstance(before, dict) and isinstance(after, dict):
                    changes = recursive_diff(before, after)
                    if changes:
                        return "Invoked Changes: " + "; ".join(changes)
                    return "No attribute changes detected"

            diff = result_dict.get('diff')
            if diff and isinstance(diff, list):
                changes = []
                for item in diff:
                    before = item.get('before', '').strip()
                    after = item.get('after', '').strip()
                    if before != after:
                        changes.append(f"Line changed: {before} -> {after}")
                if changes:
                    return "Invoked Diffs: " + "; ".join(changes)

            # --- 4. Generic fallback metadata tracker ---
            changes = []
            for k, v in result_dict.items():
                if k not in ['changed', 'check_mode', 'msg', 'invocation', 'before', 'after', 'diff', 'commands', 'snmp', 'community', 'snmp_server', 'results', 'stdout', 'stdout_lines']:
                    val_str = str(v).replace('\n', ' ').replace('\r', '')
                    changes.append(f"{k}: {val_str[:120]}")
            if changes:
                return "Invoked Attributes: " + "; ".join(changes)

            return f"Change detected (Details omitted)"
        except Exception as e:
            return f"Error formatting changes: {str(e)}"

    def _ensure_invoked_by_column(self, log_file):
        """Legacy migration engine using structural header mappings to match herder schema"""
        try:
            with open(log_file, 'r', newline='', encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)
        except Exception:
            return

        if not rows:
            self._initialize_csv(log_file)
            return

        header = rows[0]
        if header == self.EXPECTED_HEADER:
            return

        # Build migration dictionary map of row indexes based on existing names
        new_rows = [self.EXPECTED_HEADER]
        for r in rows[1:]:
            if len(r) < len(header):
                r = r + [''] * (len(header) - len(r))
            
            row_data = {}
            for idx, name in enumerate(header):
                row_data[name] = r[idx]

            # Standardize fallback translations for column renaming migrations
            if 'Change Details' in row_data and 'Changes - Summarized' not in row_data:
                row_data['Changes - Summarized'] = row_data['Change Details']

            new_r = [
                row_data.get('Timestamp', ''),
                row_data.get('Invoked By', ''),
                row_data.get('Host', ''),
                row_data.get('Playbook', ''),
                row_data.get('Task', ''),
                row_data.get('Changes - Summarized', '')
            ]
            new_rows.append(new_r)

        fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(log_file))
        os.close(fd)
        try:
            with open(temp_path, 'w', newline='', encoding="utf-8") as tf:
                writer = csv.writer(tf)
                writer.writerows(new_rows)
            os.replace(temp_path, log_file)
        except Exception:
            pass
        finally:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass