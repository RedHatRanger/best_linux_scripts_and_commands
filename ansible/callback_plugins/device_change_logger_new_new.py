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
    Ansible callback plugin that logs tasks reporting changes (changed=True) to a CSV file.
    Captures timestamp, host, task name, playbook name, invoking user, and human-readable change details.
    Supports custom CSV paths via the ANSIBLE_CHANGE_LOG_FILE environment variable.
    In check mode (-C), logs to a separate '_check' CSV file by default and prefixes change details with 'Check mode: '.
    Automatically migrates older CSVs to include the 'Invoked By' column if missing.
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'device_change_logger'
    CALLBACK_NEEDS_ENABLED = True

    # Define the expected CSV header
    EXPECTED_HEADER = ['Timestamp', 'Host', 'Task', 'Playbook', 'Invoked By', 'Change Details']

    def __init__(self):
        """
        Initialize the plugin, setting up the CSV log file path and directory.
        Checks for a custom path via ANSIBLE_CHANGE_LOG_FILE; defaults to ~/.ansible/changes/change_logs.csv.
        Creates the log directory and initializes or migrates the CSV file.
        """
        super(CallbackModule, self).__init__()
        self.playbook = None  # Store playbook name, set in v2_playbook_on_start
        self.log_dir = os.path.expanduser('~/.ansible/changes')  # Default log directory
        # Set log file path from environment variable or default
        default_log_file = os.path.join(self.log_dir, 'change_logs.csv')
        self.log_file = os.environ.get('ANSIBLE_CHANGE_LOG_FILE', default_log_file)

        # Ensure the log directory exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        # Create new CSV with header or migrate existing CSV if needed
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.EXPECTED_HEADER)
        else:
            self._ensure_invoked_by_column()

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
        """
        Log a task's changes to the CSV file.
        Captures host, task, playbook, user, and change details.
        In check mode (-C), logs to a separate '_check' CSV (if using default path) and prefixes details with 'Check mode: '.
        Args:
            result: Ansible result object with task and host details.
        """
        host = result._host.get_name()  # Get target host (e.g., router1.example.com)
        task = result._task.get_name()  # Get task name (e.g., Configure interface and SNMP)
        timestamp = datetime.now().isoformat()  # Current time in ISO format
        invoked_by = self._get_invoking_user()  # Identify who ran the playbook

        # Determine log file path: use '_check' suffix in check mode if default path
        log_file = self.log_file
        if result._result.get('check_mode', False) and log_file == os.path.join(self.log_dir, 'change_logs.csv'):
            log_file = os.path.join(self.log_dir, 'change_logs_check.csv')
            # Initialize check mode CSV if it doesn't exist
            if not os.path.exists(log_file):
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                with open(log_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(self.EXPECTED_HEADER)
            else:
                self._ensure_invoked_by_column(log_file)

        # Format change details (e.g., file permissions, config lines)
        details = self._format_change_details(result._result)
        if result._result.get('check_mode', False):
            details = f"Check mode: {details}"  # Indicate dry-run changes

        # Append row to CSV: [Timestamp, Host, Task, Playbook, Invoked By, Change Details]
        with open(log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, host, task, self.playbook, invoked_by, details])

    def _format_change_details(self, result_dict):
        """
        Format task changes into a human-readable string.
        Processes 'before'/'after' (e.g., file attributes), 'diff' (e.g., line changes), or 'commands' (e.g., cisco.ios.ios_config).
        Falls back to JSON or truncated string if no known structure is found.
        Args:
            result_dict: Dictionary containing task result data (result._result).
        Returns:
            str: Readable change summary or fallback output.
        """
        try:
            # Handle 'before' and 'after' keys (common in ansible.builtin.file, template)
            before = result_dict.get('before')
            after = result_dict.get('after')
            if before is not None and after is not None:
                # Dictionary-based: compare attributes (e.g., mode, owner)
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
                # String-based: compare content (e.g., config snippets)
                elif isinstance(before, str) and isinstance(after, str):
                    if before == after:
                        return "No content changes detected"
                    return f"Config changed (before: {len(before)} chars, after: {len(after)} chars)"

            # Handle 'diff' key (common in lineinfile, ios_config with diff=True)
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

            # Fallback to JSON for unrecognized result structures
            return json.dumps(result_dict, sort_keys=True)
        except Exception as e:
            # Fallback to truncated string if parsing fails
            return f"Error formatting changes: {str(e)}; Raw result: {str(result_dict)[:100]}"

    def _ensure_invoked_by_column(self, log_file=None):
        """
        Ensure the CSV file includes the 'Invoked By' column.
        Migrates older CSVs by adding the column and padding rows with empty values.
        Uses atomic writes to prevent corruption.
        Args:
            log_file: Path to the CSV file (optional; defaults to self.log_file).
        """
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
        # If Invoked By already present, no migration needed
        if 'Invoked By' in header:
            return

        # Determine insert index: before 'Change Details' if present, else append
        if 'Change Details' in header:
            idx = header.index('Change Details')
        else:
            idx = len(header)

        # Build new header with 'Invoked By'
        new_header = header[:idx] + ['Invoked By'] + header[idx:]

        # Update rows: insert empty value at idx, padding shorter rows
        new_rows = [new_header]
        modified_rows = 0
        for r in rows[1:]:
            if len(r) < idx:
                r = r + [''] * (idx - len(r))
                modified_rows += 1
            new_r = r[:idx] + [''] + r[idx:]
            new_rows.append(new_r)

        # Write to a temp file then atomically replace the original
        fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(log_file))
        os.close(fd)
        try:
            with open(temp_path, 'w', newline='') as tf:
                writer = csv.writer(tf)
                writer.writerows(new_rows)
            os.replace(temp_path, log_file)
            
            # Output summary of migration
            change_summary = [
                f"Modified CSV file: {log_file}",
                f"Added column: 'Invoked By' at position {idx + 1}",
                f"Updated header: {', '.join(new_header)}",
                f"Rows modified (padded): {modified_rows}",
                f"Total rows processed: {len(rows) - 1}"
            ]
            print("\n".join(change_summary))
        finally:
            # Clean up temp file if it still exists
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass