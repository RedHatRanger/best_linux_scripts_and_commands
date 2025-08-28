from ansible.plugins.callback import CallbackBase
from datetime import datetime
import os
import csv
import json
import getpass
import pwd
import tempfile
import sys

class CallbackModule(CallbackBase):
    """
    Ansible callback plugin that logs tasks reporting changes (changed=True) to a CSV file.
    Captures timestamp, host, task name, playbook name, invoking user, and changes in two columns:
    - Changes - Summarized: Human-readable summary of changes (e.g., file attributes, config lines).
    - Changes - Detailed: Filtered JSON of the task result for detailed inspection, excluding large fields like ansible_facts.
    Supports custom CSV paths via the ANSIBLE_CHANGE_LOG_FILE environment variable.
    In check mode (-C or --check), logs to '~/.ansible/changes/checks_only.csv' unless overridden by ANSIBLE_CHANGE_LOG_FILE.
    In normal mode, logs to '~/.ansible/changes/change_logs.csv' unless overridden.
    Prefixes summarized changes with 'Check mode: ' in check mode.
    Automatically migrates older CSVs to include 'Invoked By', 'Changes - Summarized', and 'Changes - Detailed' columns.
    Ensures both CSVs and the check mode directory (~/.ansible/changes/) persist across runs.
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'device_change_logger'
    CALLBACK_NEEDS_ENABLED = True

    # Define the expected CSV header with two change columns
    EXPECTED_HEADER = ['Timestamp', 'Host', 'Task', 'Playbook', 'Invoked By', 'Changes - Summarized', 'Changes - Detailed']

    def __init__(self):
        """
        Initialize the plugin, setting up the CSV log file path and directory.
        Checks for a custom path via ANSIBLE_CHANGE_LOG_FILE; defaults to ~/.ansible/changes/change_logs.csv.
        Creates the log directory and initializes or migrates the CSV file for normal mode only.
        """
        super(CallbackModule, self).__init__()
        self.playbook = None
        self.log_dir = os.path.expanduser('~/.ansible/changes')
        self.default_log_file = os.path.normpath(os.path.join(self.log_dir, 'change_logs.csv'))
        self.check_log_file = os.path.normpath(os.path.join(self.log_dir, 'checks_only.csv'))
        self.log_file = os.path.normpath(os.environ.get('ANSIBLE_CHANGE_LOG_FILE', self.default_log_file))

        # Ensure the normal mode log directory exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        # Initialize or migrate normal mode CSV only if using default path
        if self.log_file == self.default_log_file:
            if not os.path.exists(self.log_file):
                with open(self.log_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(self.EXPECTED_HEADER)
            else:
                self._ensure_invoked_by_column(self.log_file)

    def v2_playbook_on_start(self, playbook):
        """
        Called when the playbook starts. Stores the playbook's filename for logging.
        Args:
            playbook: Ansible playbook object containing metadata.
        """
        self.playbook = os.path.basename(playbook._file_name)

    def v2_runner_on_ok(self, result, **kwargs):
        """
        Called when a task completes successfully. Logs the task if it reports changed=True.
        Args:
            result: Ansible result object containing task execution details.
        """
        if result._result.get('changed', False):
            self._log_change(result)

    def v2_runner_on_failed(self, result, **kwargs):
        """
        Called when a task fails. Logs the task if it reports changed=True (e.g., partial changes).
        Args:
            result: Ansible result object containing task execution details.
        """
        if result._result.get('changed', False):
            self._log_change(result)

    def _get_invoking_user(self):
        """
        Determine the user or system running the playbook.
        Checks environment variables (sudo, CI/CD, automation platforms) and system fallbacks.
        Returns:
            str: Username or identifier (e.g., 'admin', 'github_actor', 'unknown').
        """
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
        """
        Log a task's changes to the CSV file.
        Captures host, task, playbook, user, summarized changes, and filtered JSON result.
        In check mode (-C or --check), logs to ~/.ansible/changes/checks_only.csv unless overridden by ANSIBLE_CHANGE_LOG_FILE.
        In normal mode, logs to ~/.ansible/changes/change_logs.csv unless overridden.
        Prefixes summarized changes with 'Check mode: ' in check mode.
        Args:
            result: Ansible result object with task and host details.
        """
        host = result._host.get_name()
        task = result._task.get_name()
        timestamp = datetime.now().isoformat()
        invoked_by = self._get_invoking_user()

        # Detect check mode by checking command-line arguments
        is_check_mode = '-C' in sys.argv or '--check' in sys.argv
        log_file = self.log_file
        if is_check_mode and 'ANSIBLE_CHANGE_LOG_FILE' not in os.environ:
            log_file = self.check_log_file
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            if not os.path.exists(log_file):
                with open(log_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(self.EXPECTED_HEADER)
            self._ensure_invoked_by_column(log_file)
        else:
            if log_file == self.default_log_file and not os.path.exists(log_file):
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                with open(log_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(self.EXPECTED_HEADER)
                self._ensure_invoked_by_column(log_file)

        # Format changes
        summarized = self._format_change_details(result._result)
        if is_check_mode:
            summarized = f"Check mode: {summarized}"
        filtered_result = {k: v for k, v in result._result.items() if k not in ['ansible_facts', 'invocation']}
        detailed = json.dumps(filtered_result, sort_keys=True)

        # Append to CSV
        with open(log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, host, task, self.playbook, invoked_by, summarized, detailed])

    def _format_change_details(self, result_dict):
        """
        Format task changes into a human-readable string for the 'Changes - Summarized' column.
        Processes 'commands' (e.g., network modules), 'before'/'after' (e.g., file attributes), 'diff' (e.g., line changes),
        'snmp', 'community', or 'snmp_server' (e.g., cisco.ios.ios_snmp_server settings).
        Falls back to a generic summary of key-value pairs for unrecognized structures.
        Args:
            result_dict: Dictionary containing task result data (result._result).
        Returns:
            str: Readable change summary or fallback output with debug info.
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

        try:
            commands = result_dict.get('commands')
            if commands and isinstance(commands, (list, str)):
                if isinstance(commands, str):
                    commands = [commands]
                if commands:
                    return "Applied commands: " + "; ".join(str(cmd) for cmd in commands)
                return "No commands applied"

            before = result_dict.get('before')
            after = result_dict.get('after')
            if before is not None and after is not None:
                if isinstance(before, dict) and isinstance(after, dict):
                    changes = recursive_diff(before, after)
                    if changes:
                        return "; ".join(changes)
                    return "No attribute changes detected"
                elif isinstance(before, list) and isinstance(after, list):
                    changes = recursive_diff(before, after)
                    if changes:
                        return "; ".join(changes)
                    return "No list changes detected"
                elif isinstance(before, str) and isinstance(after, str):
                    if before == after:
                        return "No content changes detected"
                    return f"Config changed (before: {len(before)} chars, after: {len(after)} chars)"

            diff = result_dict.get('diff')
            if diff and isinstance(diff, list):
                changes = []
                for item in diff:
                    before = item.get('before', '').strip()
                    after = item.get('after', '').strip()
                    if before != after:
                        changes.append(f"Line changed: {before} -> {after}")
                if changes:
                    return "; ".join(changes)
                return "No diff changes detected"

            snmp = result_dict.get('snmp')
            if snmp and isinstance(snmp, dict):
                changes = []
                if 'community' in snmp:
                    for comm in snmp.get('community', []):
                        name = comm.get('name', 'unknown')
                        access = comm.get('access', 'unknown')
                        changes.append(f"SNMP community: {name} ({access})")
                if changes:
                    return "; ".join(changes)
                return "No SNMP community changes detected"

            community = result_dict.get('community')
            if community and isinstance(community, (list, dict)):
                changes = []
                if isinstance(community, list):
                    for comm in community:
                        name = comm.get('name', 'unknown')
                        access = comm.get('access', 'unknown')
                        changes.append(f"SNMP community: {name} ({access})")
                elif isinstance(community, dict):
                    name = community.get('name', 'unknown')
                    access = community.get('access', 'unknown')
                    changes.append(f"SNMP community: {name} ({access})")
                if changes:
                    return "; ".join(changes)
                return "No SNMP community changes detected"

            snmp_server = result_dict.get('snmp_server')
            if snmp_server and isinstance(snmp_server, dict):
                changes = []
                if 'community' in snmp_server:
                    for comm in snmp_server.get('community', []):
                        name = comm.get('name', 'unknown')
                        access = comm.get('access', 'unknown')
                        changes.append(f"SNMP community: {name} ({access})")
                if changes:
                    return "; ".join(changes)
                return "No SNMP server changes detected"

            # Generic fallback for any remaining keys
            changes = []
            for k, v in result_dict.items():
                if k not in ['changed', 'check_mode', 'msg', 'invocation', 'before', 'after', 'diff', 'commands', 'snmp', 'community', 'snmp_server']:
                    # Truncate long values for readability
                    value_str = str(v)[:100] + '...' if len(str(v)) > 100 else str(v)
                    changes.append(f"{k}: {value_str}")
            if changes:
                return "Changes: " + "; ".join(changes)

            debug_info = f"Unrecognized result structure. Keys found: {list(result_dict.keys())}"
            return f"No recognized changes detected; Debug: {debug_info}"
        except Exception as e:
            return f"Error formatting changes: {str(e)}; Raw result: {str(result_dict)[:100]}"

    def _ensure_invoked_by_column(self, log_file):
        """
        Ensure the CSV file includes 'Invoked By', 'Changes - Summarized', and 'Changes - Detailed' columns.
        Migrates older CSVs by adding missing columns and padding rows with empty values.
        Uses atomic writes to prevent corruption.
        Args:
            log_file: Path to the CSV file to migrate.
        """
        try:
            with open(log_file, 'r', newline='') as f:
                reader = csv.reader(f)
                rows = list(reader)
        except Exception:
            rows = []

        if not rows:
            with open(log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.EXPECTED_HEADER)
            return

        header = rows[0]
        if all(col in header for col in ['Invoked By', 'Changes - Summarized', 'Changes - Detailed']):
            return

        new_header = header[:]
        modified_rows = 0

        if 'Invoked By' not in new_header:
            if 'Change Details' in new_header:
                idx = new_header.index('Change Details')
            else:
                idx = len(new_header)
            new_header = new_header[:idx] + ['Invoked By'] + new_header[idx:]
            if 'Change Details' in new_header:
                new_header.remove('Change Details')
            new_header.extend(['Changes - Summarized', 'Changes - Detailed'])
        elif 'Changes - Summarized' not in new_header or 'Changes - Detailed' not in new_header:
            if 'Change Details' in new_header:
                idx = new_header.index('Change Details')
                new_header = new_header[:idx] + ['Changes - Summarized', 'Changes - Detailed'] + new_header[idx+1:]
                new_header.remove('Change Details')
            else:
                new_header.extend(['Changes - Summarized', 'Changes - Detailed'])

        new_rows = [new_header]
        for r in rows[1:]:
            if len(r) < len(header):
                r = r + [''] * (len(header) - len(r))
                modified_rows += 1
            new_r = []
            for col in new_header:
                if col == 'Invoked By' and col not in header:
                    new_r.append('')
                elif col == 'Changes - Summarized':
                    new_r.append(r[header.index('Change Details')] if 'Change Details' in header else '')
                elif col == 'Changes - Detailed':
                    new_r.append('')
                elif col in header:
                    new_r.append(r[header.index(col)])
                else:
                    new_r.append('')
            new_rows.append(new_r)

        fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(log_file))
        os.close(fd)
        try:
            with open(temp_path, 'w', newline='') as tf:
                writer = csv.writer(tf)
                writer.writerows(new_rows)
            os.replace(temp_path, log_file)
        finally:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
