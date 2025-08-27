# Ansible Device Change Logger Callback Plugin

## Overview

The `device_change_logger` callback plugin for Ansible logs changes made by playbook tasks to a CSV file. It captures details about tasks that report `changed=True`, including the timestamp, host, task name, playbook, invoking user, and changes in two columns: a human-readable summary (`Changes - Summarized`) and the full JSON task result (`Changes - Detailed`). The plugin is designed for tracking configuration changes on systems and network devices, supporting modules like `ansible.builtin.file`, `ansible.builtin.lineinfile`, and `cisco.ios.ios_config`.

## Features

- Logs changes to a CSV file, with a default path of `~/.ansible/changes/change_logs.csv` for normal runs and `~/.ansible/changes/change_logs_check.csv` for check mode (`-C`).
- Supports a custom CSV path via the `ANSIBLE_CHANGE_LOG_FILE` environment variable.
- Captures:
  - **Timestamp**: When the change occurred (ISO format).
  - **Host**: The target host or device.
  - **Task**: The name of the task that made the change.
  - **Playbook**: The name of the playbook file.
  - **Invoked By**: The user or system that ran the playbook.
  - **Changes - Summarized**: A human-readable summary of changes (e.g., file permission changes, configuration lines applied).
  - **Changes - Detailed**: The full JSON output of the task result for detailed inspection.
- Supports common Ansible modules (`ansible.builtin`) and network modules (e.g., `cisco.ios.ios_config`).
- Handles check mode (`-C` or `--check`), logging predicted changes with a `Check mode: `prefix in the `Changes - Summarized` column.
- Automatically migrates existing CSV files to include `Invoked By`, `Changes - Summarized`, and `Changes - Detailed` columns if missing.
- Provides human-readable summaries for supported modules, with JSON fallback for others.

## Requirements

- Ansible 2.9 or later.
- Python 3.6 or later.
- The plugin must be enabled in `ansible.cfg`.
- Write permissions to the CSV directory (default: `~/.ansible/changes/` or specified via `ANSIBLE_CHANGE_LOG_FILE`).

## Installation

1. **Place the Plugin**:

   - Copy `device_change_logger.py` to your Ansible callback plugins directory, typically:
     - `~/.ansible/plugins/callback/` for user-specific installation.
     - `/usr/share/ansible/plugins/callback/` for system-wide installation.
     - Or, within an Ansible collection under `plugins/callback/`.

2. **Enable the Plugin**:

   - Edit your `ansible.cfg` file (e.g., `~/.ansible.cfg` or in your project directory) to enable the plugin:

     ```ini
     [defaults]
     callbacks_enabled = device_change_logger
     ```
   - If using a custom callback directory, set the path:

     ```ini
     [defaults]
     callback_plugins = /path/to/your/callback_plugins
     callbacks_enabled = device_change_logger
     ```

3. **Verify Permissions**:

   - Ensure the user running Ansible has write permissions to the CSV directory (default: `~/.ansible/changes/` or specified via `ANSIBLE_CHANGE_LOG_FILE`).

## Usage

1. **Run a Playbook**:

   - Execute your playbook as usual:

     ```bash
     ansible-playbook configure_router.yml
     ```
   - For check mode (dry-run), use `-C`:

     ```bash
     ansible-playbook -C configure_router.yml
     ```

2. **Configure CSV Path** (Optional):

   - To use a custom CSV path, set the `ANSIBLE_CHANGE_LOG_FILE` environment variable:

     ```bash
     export ANSIBLE_CHANGE_LOG_FILE=/path/to/custom/changes.csv
     ansible-playbook configure_router.yml
     ```
   - In check mode without a custom path, logs go to `~/.ansible/changes/change_logs_check.csv`.

3. **Check the Log**:

   - The plugin creates or appends to the specified CSV file (or default paths) for tasks where `changed=True`.
   - Open the CSV file to view the logged changes, including both summarized and detailed outputs.

## Supported Modules

The plugin formats change summaries for:

- **System Modules** (e.g., `ansible.builtin.file`, `ansible.builtin.template`, `ansible.builtin.lineinfile`):
  - Logs attribute changes (e.g., `mode: 0644 -> 0755`) or line changes (e.g., `Line changed: Listen 80 -> Listen 8080`) in `Changes - Summarized`.
- **Network Modules** (e.g., `cisco.ios.ios_config`):
  - Logs applied commands (e.g., `Applied commands: interface GigabitEthernet0/1; description Connected to core switch`) in `Changes - Summarized`.
- **Other Modules**:
  - Falls back to JSON or a truncated string in `Changes - Summarized` for modules with non-standard result structures (e.g., `ansible.builtin.command`, some cloud modules).
  - Always logs the full JSON task result in `Changes - Detailed`.

## Configuration

- **Default CSV Paths**:
  - Normal runs: `~/.ansible/changes/change_logs.csv`
  - Check mode (`-C`): `~/.ansible/changes/change_logs_check.csv` (unless overridden by `ANSIBLE_CHANGE_LOG_FILE`).
- **Custom CSV Path**:
  - Set the `ANSIBLE_CHANGE_LOG_FILE` environment variable to specify a different path:

    ```bash
    export ANSIBLE_CHANGE_LOG_FILE=/tmp/logs/custom_changes.csv
    ```
  - The plugin creates the directory if it doesnâ€™t exist.
  - Applies to both normal and check mode runs unless changed.
- **Ansible Configuration**:
  - Ensure `callbacks_enabled = device_change_logger` is set in `ansible.cfg`.

## Example CSV Output

Below is a sample `change_logs.csv` after running a playbook `configure_router.yml` with `cisco.ios.ios_config` and `ansible.builtin.file` tasks:

```csv
Timestamp,Host,Task,Playbook,Invoked By,Changes - Summarized,Changes - Detailed
2025-08-27T05:30:00.123456,router1.example.com,Configure interface and SNMP,configure_router.yml,admin,Applied commands: interface GigabitEthernet0/1; description Connected to core switch; snmp-server enable traps,"{""changed"": true, ""commands"": [""interface GigabitEthernet0/1"", ""description Connected to core switch"", ""snmp-server enable traps""], ...}"
2025-08-27T05:30:01.234567,web1.example.com,Set file permissions,configure_router.yml,admin,mode: 0644 -> 0755; owner: nobody -> admin,"{""changed"": true, ""before"": {""mode"": ""0644"", ""owner"": ""nobody""}, ""after"": {""mode"": ""0755"", ""owner"": ""admin""}, ...}"
```

In check mode (`-C`), using the default path, the output goes to `change_logs_check.csv`:

```csv
Timestamp,Host,Task,Playbook,Invoked By,Changes - Summarized,Changes - Detailed
2025-08-27T05:30:02.345678,router1.example.com,Configure interface and SNMP,configure_router.yml,admin,Check mode: Applied commands: interface GigabitEthernet0/1; description Connected to core switch; snmp-server enable traps,"{""changed"": true, ""check_mode"": true, ""commands"": [""interface GigabitEthernet0/1"", ""description Connected to core switch"", ""snmp-server enable traps""], ...}"
```

With a custom path (`ANSIBLE_CHANGE_LOG_FILE=/tmp/logs/custom_changes.csv`):

```csv
Timestamp,Host,Task,Playbook,Invoked By,Changes - Summarized,Changes - Detailed
2025-08-27T05:30:03.456789,router1.example.com,Configure interface and SNMP,configure_router.yml,admin,Check mode: Applied commands: interface GigabitEthernet0/1; description Connected to core switch; snmp-server enable traps,"{""changed"": true, ""check_mode"": true, ""commands"": [""interface GigabitEthernet0/1"", ""description Connected to core switch"", ""snmp-server enable traps""], ...}"
```

## Notes

- **Check Mode**: The plugin logs predicted changes in check mode (`-C`) if tasks report `changed=True`, with a `Check mode: `prefix in the `Changes - Summarized` column. The `Changes - Detailed` column contains raw JSON, including `"check_mode": true`.
- **Custom Path**: Setting `ANSIBLE_CHANGE_LOG_FILE` overrides the default paths for both normal and check mode runs. Use different paths to separate logs as needed.
- **Limitations**:
  - Modules with non-standard result structures (e.g., `ansible.builtin.command`, some cloud modules) may log less readable JSON in `Changes - Summarized`.
  - Large JSON outputs in `Changes - Detailed` (e.g., for cloud modules) may increase CSV size.
  - Large configuration diffs (e.g., in `cisco.ios.ios_config`) may produce verbose summaries unless `diff=True` is used.
- **CSV Migration**: If an existing CSV lacks `Invoked By`, `Changes - Summarized`, or `Changes - Detailed`, the plugin migrates it by adding the missing columns, copying `Change Details` to `Changes - Summarized` (if present), and padding rows with empty values.
- **User Detection**: The plugin identifies the invoking user via environment variables (`SUDO_USER`, CI variables) or system fallbacks (`getpass.getuser`, `pwd.getpwuid`).

## Troubleshooting

- **No CSV Entries**:
  - Ensure `callbacks_enabled = device_change_logger` is set in `ansible.cfg`.
  - Verify tasks report `changed=True` (check mode may still log if supported by the module).
  - Check write permissions for the CSV directory (default: `~/.ansible/changes/` or specified path).
- **Unreadable Summarized Changes**:
  - If JSON is logged in `Changes - Summarized`, the module may not provide `before`/`after`, `diff`, or `commands`. Consider enabling `diff=True` for network modules or reviewing module documentation.
- **CSV File Issues**:
  - If the CSV is malformed, check for concurrent playbook runs or manual edits. The plugin uses atomic writes to minimize corruption.
  - Ensure unique `ANSIBLE_CHANGE_LOG_FILE` paths for concurrent runs to avoid conflicts.
- **Large Detailed Changes**:
  - The `Changes - Detailed` column may contain large JSON outputs for some modules. Review the JSON for debugging or filter specific fields if needed.

## Contributing

To contribute improvements (e.g., support for additional modules, better diff handling, JSON truncation), submit a pull request or open an issue in the repository. Suggestions for handling specific module outputs are welcome!

## License

Apache2 Free Licence. See `LICENSE` for details.