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
    Logs changed tasks and ensures the CSV header contains 'Invoked By'.
    If an older CSV exists without that column, it is migrated automatically.
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
        self.log_file = os.path.join(self.log_dir, 'change_logs.csv')

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        if not os.path.exists(self.log_file):
            # create a fresh file with the expected header
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.EXPECTED_HEADER)
        else:
            # ensure existing file header contains "Invoked By" and migrate if needed
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

        try:
            details = json.dumps(result._result, sort_keys=True)
        except Exception:
            details = str(result._result)

        # Append a row matching EXPECTED_HEADER order
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, host, task, self.playbook, invoked_by, details])

    def _ensure_invoked_by_column(self):
        # Read existing CSV
        with open(self.log_file, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # If the file is empty, write the expected header
        if not rows:
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.EXPECTED_HEADER)
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
        for r in rows[1:]:
            # pad row to expected length before inserting
            if len(r) < idx:
                r = r + [''] * (idx - len(r))
            new_r = r[:idx] + [''] + r[idx:]
            new_rows.append(new_r)

        # Write to a temp file then atomically replace the original file
        fd, temp_path = tempfile.mkstemp(dir=self.log_dir)
        os.close(fd)
        try:
            with open(temp_path, 'w', newline='') as tf:
                writer = csv.writer(tf)
                writer.writerows(new_rows)
            os.replace(temp_path, self.log_file)
        finally:
            # cleanup if something went wrong and temp file still exists
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass