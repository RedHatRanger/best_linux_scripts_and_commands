# Ansible Device Change Logger Callback Plugin

## Overview

The `device_change_logger` callback plugin for Ansible logs changes made by playbook tasks to a CSV file. It captures details about tasks that report `changed=True`, including the timestamp, host, task name, playbook, invoking user, and changes in two columns: a human-readable summary (`Changes - Summarized`) and a filtered JSON task result (`Changes - Detailed`). The plugin is designed for tracking configuration changes on systems and network devices, supporting modules like `ansible.builtin.file`, `ansible.builtin.lineinfile`, and `cisco.ios.ios_config`.

## Features

- Logs changes to a CSV file, with a default path of `~/.ansible/changes/change_logs.csv` for normal runs and `~/.ansible/changes/check/changes.csv` for check mode (`-C`).
- Supports a custom CSV path via the `ANSIBLE_CHANGE_LOG_FILE` environment variable.
- Captures:
  - **Timestamp**: When the change occurred (ISO format).
  - **Host**: The target host or device.
  - **Task**: The name of the task that made the change.
  - **Playbook**: The name of the playbook file.
  - **Invoked By**: The user or system that ran the playbook.
  - **Changes - Summarized**: A human-readable summary of changes (e.g., file permission changes, configuration lines applied).
  - **Changes - Detailed**: Filtered JSON output of the task result (excluding large fields like `ansible_facts` and `invocation`) for detailed inspection.
- Supports common Ansible modules (`ansible.builtin`) and network modules (e.g., `cisco.ios.ios_config`).
- Handles check mode (`-C` or `--check`), logging predicted changes with a `Check mode: ` prefix in the `Changes - Summarized` column.
- Automatically migrates existing CSV files to include `Invoked By`, `Changes - Summarized`, and `Changes - Detailed` columns if missing.
- Provides human-readable summaries for supported modules, with JSON fallback for others.

## Requirements

- Ansible 2.9 or later.
- Python 3.6 or later.
- The plugin must be enabled in `ansible.cfg`.
- Write permissions to the CSV directory (default: `~/.ansible/changes/` or specified via `ANSIBLE_CHANGE_LOG_FILE`).

## Installation

1. **Place the Plugin**:

   - Copy `device_change_logger.py` to your Ansible callback plugins directory. For project-specific use within `~/ansible`:
     ```bash
     mkdir -p ~/ansible/callback_plugins/
     cp device_change_logger.py ~/ansible/callback_plugins/
     ```
   - Alternatively, for user-specific use:
     ```bash
     mkdir -p ~/ansible/plugins/callback/
     cp device_change_logger.py ~/ansible/plugins/callback/
     ```
   - For system-wide use (requires root):
     ```bash
     sudo mkdir -p /usr/share/ansible/plugins/callback/
     sudo cp device_change_logger.py /usr/share/ansible/plugins/callback/
     ```

2. **Enable the Plugin**:

   - Edit your `ansible.cfg` file (e.g., `~/ansible/ansible.cfg`) to enable the plugin:
     ```ini
     [defaults]
     callbacks_enabled = device_change_logger
     ```
   - If using `~/ansible/plugins/callback/` (not `callback_plugins/`), specify the path:
     ```ini
     [defaults]
     callbacks_enabled = device_change_logger
     callback_plugins = ~/ansible/plugins/callback
     ```

3. **Verify Permissions**:

   - Ensure the plugin file is readable:
     ```bash
     chmod 644 ~/ansible/callback_plugins/device_change_logger.py
     ```
   - Ensure the CSV directory is writable:
     ```bash
     mkdir -p ~/.ansible/changes/check/
     chmod u+w ~/.ansible/changes/ ~/.ansible/changes/check/
     ```

## Usage

1. **Run a Playbook**:

   - Execute your playbook from the `~/ansible` directory:
     ```bash
     cd ~/ansible
     ansible-playbook configure_router.yml
     ```
   - For check mode (dry-run):
     ```bash
     ansible-playbook -C configure_router.yml
     ```

2. **Configure CSV Path** (Optional):

   - To use a custom CSV path (e.g., within `~/ansible`):
     ```bash
     export ANSIBLE_CHANGE_LOG_FILE=~/ansible/changes/custom_changes.csv
     mkdir -p ~/ansible/changes/
     ansible-playbook configure_router.yml
     ```
   - In check mode without a custom path, logs go to `~/.ansible/changes/check/changes.csv`.

3. **Check the Log**:

   - The plugin creates or appends to the specified CSV file (or default paths) for tasks where `changed=True`.
   - View the CSV:
     ```bash
     cat ~/.ansible/changes/change_logs.csv
     cat ~/.ansible/changes/check/changes.csv
     ```

## Supported Modules

The plugin formats change summaries for:

- **System Modules** (e.g., `ansible.builtin.file`, `ansible.builtin.template`, `ansible.builtin.lineinfile`):
  - Logs attribute changes (e.g., `mode: 0644 -> 0755`) or line changes (e.g., `Line changed: Listen 80 -> Listen 8080`) in `Changes - Summarized`.
- **Network Modules** (e.g., `cisco.ios.ios_config`):
  - Logs applied commands (e.g., `Applied commands: interface GigabitEthernet0/1; description Connected to core switch`) in `Changes - Summarized`.
- **Other Modules**:
  - Falls back to JSON or a truncated string in `Changes - Summarized` for modules with non-standard result structures (e.g., `ansible.builtin.command`, some cloud modules).
  - Logs filtered JSON (excluding `ansible_facts`, `invocation`) in `Changes - Detailed`.

## Configuration

- **Default CSV Paths**:
  - Normal runs: `~/.ansible/changes/change_logs.csv`
  - Check mode (`-C`): `~/.ansible/changes/check/changes.csv` (unless overridden by `ANSIBLE_CHANGE_LOG_FILE`).

- **Custom CSV Path**:
  - Set the `ANSIBLE_CHANGE_LOG_FILE` environment variable:
    ```bash
    export ANSIBLE_CHANGE_LOG_FILE=~/ansible/changes/custom_changes.csv
    ```
  - The plugin creates the directory if it doesnâ€™t exist.
  - Applies to both normal and check mode runs unless changed.

- **Ansible Configuration**:
  - Ensure `callbacks_enabled = device_change_logger` is set in `~/ansible/ansible.cfg`.
  - For `~/ansible/callback_plugins/`, no `callback_plugins` path is needed.

## Example CSV Output

Below is a sample `change_logs.csv` after running a playbook `configure_router.yml` with `cisco.ios.ios_config` and `ansible.builtin.file` tasks:

```csv
Timestamp,Host,Task,Playbook,Invoked By,Changes - Summarized,Changes - Detailed
2025-08-27T05:53:00.123456,router1.example.com,Configure interface and SNMP,configure_router.yml,admin,Applied commands: interface GigabitEthernet0/1; description Connected to core switch; snmp-server enable traps,"{""changed"": true, ""commands"": [""interface GigabitEthernet0/1"", ""description Connected to core switch"", ""snmp-server enable traps""]}"
2025-08-27T05:53:01.234567,web1.example.com,Set file permissions,configure_router.yml,admin,mode: 0644 -> 0755; owner: nobody -> admin,"{""changed"": true, ""before"": {""mode"": ""0644"", ""owner"": ""nobody""}, ""after"": {""mode"": ""0755"", ""owner"": ""admin""}}"
```

In check mode (`-C`), using the default path, the output goes to `check/changes.csv`:

```csv
Timestamp,Host,Task,Playbook,Invoked By,Changes - Summarized,Changes - Detailed
2025-08-27T05:53:02.345678,router1.example.com,Configure interface and SNMP,configure_router.yml,admin,Check mode: Applied commands: interface GigabitEthernet0/1; description Connected to core switch; snmp-server enable traps,"{""changed"": true, ""check_mode"": true, ""commands"": [""interface GigabitEthernet0/1"", ""description Connected to core switch"", ""snmp-server enable traps""]}"
```

With a custom path (`ANSIBLE_CHANGE_LOG_FILE=~/ansible/changes/custom_changes.csv`):

```csv
Timestamp,Host,Task,Playbook,Invoked By,Changes - Summarized,Changes - Detailed
2025-08-27T05:53:03.456789,router1.example.com,Configure interface and SNMP,configure_router.yml,admin,Check mode: Applied commands: interface GigabitEthernet0/1; description Connected to core switch; snmp-server enable traps,"{""changed"": true, ""check_mode"": true, ""commands"": [""interface GigabitEthernet0/1"", ""description Connected to core switch"", ""snmp-server enable traps""]}"
```

## Notes

- **Check Mode**: The plugin logs predicted changes in check mode (`-C`) if tasks report `changed=True`, with a `Check mode: ` prefix in the `Changes - Summarized` column. The `Changes - Detailed` column contains filtered JSON, including `"check_mode": true`.
- **Custom Path**: Setting `ANSIBLE_CHANGE_LOG_FILE=~/ansible/changes/custom_changes.csv` keeps logs within your `~/ansible` directory for consistency.
- **Limitations**:
  - Modules with non-standard result structures (e.g., `ansible.builtin.command`, some cloud modules) may log less readable JSON in `Changes - Summarized`.
  - The `Changes - Detailed` column is filtered to exclude `ansible_facts` and `invocation`, but large outputs may still occur for some modules.
  - Large configuration diffs (e.g., in `cisco.ios.ios_config`) may produce verbose summaries unless `diff=True` is used.
- **CSV Migration**: If an existing CSV lacks `Invoked By`, `Changes - Summarized`, or `Changes - Detailed`, the plugin migrates it by adding the missing columns, copying `Change Details` to `Changes - Summarized` (if present), and padding rows with empty values.
- **User Detection**: The plugin identifies the invoking user via environment variables (`SUDO_USER`, CI variables) or system fallbacks (`getpass.getuser`, `pwd.getpwuid`).

## Troubleshooting

- **No CSV Entries**:
  - Ensure `callbacks_enabled = device_change_logger` is set in `~/ansible/ansible.cfg`.
  - Verify tasks report `changed=True` (check mode may still log if supported by the module).
  - Check the plugin is in `~/ansible/callback_plugins/`:
    ```bash
    ls ~/ansible/callback_plugins/device_change_logger.py
    ```
- **CSV Not Written**:
  - Verify write permissions:
    ```bash
    chmod u+w ~/.ansible/changes/ ~/.ansible/changes/check/
    ```
    or for a custom path:
    ```bash
    chmod u+w ~/ansible/changes/
    ```
- **Unreadable Summarized Changes**:
  - If JSON is logged in `Changes - Summarized`, the module may not provide `before`/`after`, `diff`, or `commands`. Enable `diff=True` for network modules or check module documentation.
- **CSV File Issues**:
  - If the CSV is malformed, check for concurrent playbook runs or manual edits. The plugin uses atomic writes to minimize corruption.
  - Ensure unique `ANSIBLE_CHANGE_LOG_FILE` paths for concurrent runs.
- **Large Detailed Changes**:
  - The `Changes - Detailed` column is filtered, but large outputs may remain. Modify the filter list in the plugin (Line 152) if needed.

## Contributing

To contribute improvements (e.g., support for additional modules, better diff handling, JSON filtering), submit a pull request or open an issue in the repository. Suggestions for handling specific module outputs are welcome!

## License

MIT License. See `LICENSE` for details.