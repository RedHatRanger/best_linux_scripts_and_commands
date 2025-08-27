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
    Captures timestamp, host, task name, playbook name, invoking user, and changes in two columns:
    - Changes - Summarized: Human-readable summary of changes (e.g., file attributes, config lines).
    - Changes - Detailed: Full JSON of the task result for detailed inspection.
    Supports custom CSV paths via the ANSIBLE_CHANGE_LOG_FILE environment variable.
    In check mode (-C), logs to a separate '_check' CSV file by default and prefixes summarized changes with 'Check mode: '.
    Automatically migrates older CSVs to include 'Invoked By', 'Changes - Summarized', and 'Changes - Detailed' columns.
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
        Captures host, task, playbook, user, summarized changes, and detailed JSON result.
        In check mode (-C), logs to a separate '_check' CSV (if using default path) and prefixes summarized changes with 'Check mode: '.
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

        # Format summarized changes (human-readable) and detailed changes (full JSON)
        summarized = self._format_change_details(result._result)
        if result._result.get('check_mode', False):
            summarized = f"Check mode: {summarized}"  # Indicate dry-run for summarized changes
        detailed = json.dumps(result._result, sort_keys=True)  # Full task result as JSON

        # Append row to CSV: [Timestamp, Host, Task, Playbook, Invoked By, Changes - Summarized, Changes - Detailed]
        with open(log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, host, task, self.playbook, invoked_by, summarized, detailed])

    def _format_change_details(self, result_dict):
        """
        Format task changes into a human-readable string for the 'Changes - Summarized' column.
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
        Ensure the CSV file includes 'Invoked By', 'Changes - Summarized', and 'Changes - Detailed' columns.
        Migrates older CSVs by adding missing columns and padding rows with empty values.
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
        # If all expected columns are present, no migration needed
        if all(col in header for col in ['Invoked By', 'Changes - Summarized', 'Changes - Detailed']):
            return

        # Determine insert indices for new columns
        new_header = header[:]
        modified_rows = 0

        # Add 'Invoked By' before 'Change Details' or at the end
        if 'Invoked By' not in new_header:
            if 'Change Details' in new_header:
                idx = new_header.index('Change Details')
            else:
                idx = len(new_header)
            new_header = new_header[:idx] + ['Invoked By'] + new_header[idx:]
            if 'Change Details' in new_header:
                new_header.remove('Change Details')  # Remove old column if present
            new_header.extend(['Changes - Summarized', 'Changes - Detailed'])
        # Add 'Changes - Summarized' and 'Changes - Detailed' if missing
        elif 'Changes - Summarized' not in new_header or 'Changes - Detailed' not in new_header:
            if 'Change Details' in new_header:
                idx = new_header.index('Change Details')
                new_header = new_header[:idx] + ['Changes - Summarized', 'Changes - Detailed'] + new_header[idx+1:]
                new_header.remove('Change Details')  # Replace old column
            else:
                new_header.extend(['Changes - Summarized', 'Changes - Detailed'])

        # Update rows: pad and insert values
        new_rows = [new_header]
        for r in rows[1:]:
            # Pad row to match original header length
            if len(r) < len(header):
                r = r + [''] * (len(header) - len(r))
                modified_rows += 1
            # Insert values based on new header
            new_r = []
            for col in new_header:
                if col == 'Invoked By' and col not in header:
                    new_r.append('')  # Empty for old rows
                elif col == 'Changes - Summarized' and 'Change Details' in header:
                    new_r.append(r[header.index('Change Details')])  # Copy old Change Details
                elif col == 'Changes - Detailed' and 'Change Details' in header:
                    new_r.append('')  # No detailed data for old rows
                elif col in header:
                    new_r.append(r[header.index(col)])
                else:
                    new_r.append('')
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