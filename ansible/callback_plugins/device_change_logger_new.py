from ansible.plugins.callback import CallbackBase
from datetime import datetime
import os
import csv
import json
import getpass
import pwd
import tempfile

class CallbackModule(CallbackBase):
    """
    Logs changed tasks to a CSV file and ensures the CSV header contains 'Invoked By'.
    If an older CSV exists without that column, it is migrated automatically.
    Outputs a readable summary of changes made to the CSV file and device changes in a human-readable format.
    Supports a custom CSV path via the ANSIBLE_CHANGE_LOG_FILE environment variable, with a '_check' suffix in check mode if not specified.
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'device_change_logger'
    CALLBACK_NEEDS_ENABLED = True

    EXPECTED_HEADER = ['Timestamp', 'Host', 'Task', 'Playbook', 'Invoked By', 'Change Details']

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.playbook = None
        self.log_dir = os.path.expanduser('~/.ansible/changes')
        # Default log file path
        default_log_file = os.path.join(self.log_dir, 'change_logs.csv')
        # Check for custom log file path from environment variable
        self.log_file = os.environ.get('ANSIBLE_CHANGE_LOG_FILE', default_log_file)

        # Ensure the log directory exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        # Create or migrate the CSV file
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.EXPECTED_HEADER)
        else:
            self._ensure_invoked_by_column()

    def v2_playbook_on_start(self, playbook):
        self.playbook = os.path.basename(playbook._file_name)

    def v2_runner_on_ok(self, result, **kwargs):
        if result._result.get('changed', False):
            self._log_change(result)

    def v2_runner_on_failed(self, result, **kwargs):
        if result._result.get('changed', False):
            self._log_change(result)

    def _get_invoking_user(self):
        # 1) Sudo original user (common when someone runs with sudo)
        sudo_user = os.environ.get('SUDO_USER')
        if sudo_user:
            return sudo_user

        # 2) Common CI/orchestration variables
        for envname in ('INVOKED_BY', 'GITHUB_ACTOR', 'GITLAB_USER_LOGIN', 'BUILD_USER'):
            v = os.environ.get(envname)
            if v:
                return v

        # 3) AWX/Tower or other automation platform variables (extend as needed)
        for envname in ('AWX_USERNAME', 'TOWER_USERNAME', 'ANSIBLE_RUNNER'):
            v = os.environ.get(envname)
            if v:
                return v

        # 4) Fallbacks
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
        task = result._task.get_name()
        timestamp = datetime.now().isoformat()
        invoked_by = self._get_invoking_user()

        # Use a different log file in check mode if no custom path is specified
        log_file = self.log_file
        if result._result.get('check_mode', False) and log_file == os.path.join(self.log_dir, 'change_logs.csv'):
            log_file = os.path.join(self.log_dir, 'change_logs_check.csv')
            # Ensure the check mode CSV exists with the correct header
            if not os.path.exists(log_file):
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                with open(log_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(self.EXPECTED_HEADER)
            else:
                self._ensure_invoked_by_column(log_file)

        # Extract and format change details in a readable way
        details = self._format_change_details(result._result)
        if result._result.get('check_mode', False):
            details = f"Check mode: {details}"

        # Append a row matching EXPECTED_HEADER order
        with open(log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, host, task, self.playbook, invoked_by, details])

    def _format_change_details(self, result_dict):
        """
        Format the changes from result_dict into a human-readable string.
        Focuses on 'before' and 'after' states, 'diff', or 'commands' for cisco.ios.ios_config.
        """
        try:
            # Check for 'before' and 'after' keys (common in some modules)
            before = result_dict.get('before')
            after = result_dict.get('after')
            if before is not None and after is not None:
                # Handle dictionary-based before/after (e.g., file attributes)
                if isinstance(before, dict) and isinstance(after, dict):
                    changes = []
                    for key in set(before.keys()) | set(after.keys()):
                        old_val = before.get(key, '<not set>')
                        new_val = after.get(key, '<not set>')
                        if old_val != new_val:
                            changes.append(f"{key}: {old_val} -> {new_val}")
                    if changes:
                        return "; ".join(changes)
                    return "No attribute changes detected"
                # Handle string-based before/after (e.g., config snippets)
                elif isinstance(before, str) and isinstance(after, str):
                    if before == after:
                        return "No content changes detected"
                    return f"Config changed (before: {len(before)} chars, after: {len(after)} chars)"

            # Handle 'diff' key (common in lineinfile or ios_config with diff mode)
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

            # Handle 'commands' key (common in cisco.ios.ios_config)
            commands = result_dict.get('commands')
            if commands and isinstance(commands, list):
                return "Applied commands: " + "; ".join(str(cmd) for cmd in commands)

            # Fallback to JSON if no specific structure is found
            return json.dumps(result_dict, sort_keys=True)
        except Exception as e:
            # Fallback to string representation if parsing fails
            return f"Error formatting changes: {str(e)}; Raw result: {str(result_dict)[:100]}"

    def _ensure_invoked_by_column(self, log_file=None):
        # Use the specified log file or the default
        log_file = log_file or self.log_file
        # Read existing CSV
        with open(log_file, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # If the file is empty, write the expected header
        if not rows:
            with open(log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.EXPECTED_HEADER)
            print(f"Created new CSV file {log_file} with header: {', '.join(self.EXPECTED_HEADER)}")
            return

        header = rows[0]
        # If Invoked By already present and header matches expected, nothing to do
        if 'Invoked By' in header:
            return

        # Determine insert index: before 'Change Details' if present, otherwise append at end
        if 'Change Details' in header:
            idx = header.index('Change Details')
        else:
            idx = len(header)

        # Build new header
        new_header = header[:idx] + ['Invoked By'] + header[idx:]

        # Update existing rows: insert empty value at idx for each data row, padding shorter rows if needed
        new_rows = [new_header]
        modified_rows = 0
        for r in rows[1:]:
            # Pad row to expected length before inserting
            if len(r) < idx:
                r = r + [''] * (idx - len(r))
                modified_rows += 1
            new_r = r[:idx] + [''] + r[idx:]
            new_rows.append(new_r)

        # Write to a temp file then atomically replace the original file
        fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(log_file))
        os.close(fd)
        try:
            with open(temp_path, 'w', newline='') as tf:
                writer = csv.writer(tf)
                writer.writerows(new_rows)
            os.replace(temp_path, log_file)
            
            # Output readable summary of changes
            change_summary = [
                f"Modified CSV file: {log_file}",
                f"Added column: 'Invoked By' at position {idx + 1}",
                f"Updated header: {', '.join(new_header)}",
                f"Rows modified (padded): {modified_rows}",
                f"Total rows processed: {len(rows) - 1}"
            ]
            print("\n".join(change_summary))
        finally:
            # Cleanup if something went wrong and temp file still exists
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass