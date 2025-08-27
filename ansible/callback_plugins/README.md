Place this in ansible.cfg:
```
[defaults]
callbacks_enabled = device_change_logger
```

Then:
```
mkdir -p ~/ansible/callback_plugins
```

# Ansible Device Change Logger Callback Plugin

## Overview

The `device_change_logger` callback plugin for Ansible logs changes made by playbook tasks to a CSV file. It captures details about tasks that report `changed=True`, including the timestamp, host, task name, playbook, invoking user, and a human-readable summary of the changes. The plugin is particularly useful for tracking configuration changes on systems and network devices, such as those managed by modules like `ansible.builtin.file`, `ansible.builtin.lineinfile`, and `cisco.ios.ios_config`.

## Features

- Logs changes to a CSV file at `~/.ansible/changes/change_logs.csv`.
- Captures:
  - **Timestamp**: When the change occurred (ISO format).
  - **Host**: The target host or device.
  - **Task**: The name of the task that made the change.
  - **Playbook**: The name of the playbook file.
  - **Invoked By**: The user or system that ran the playbook.
  - **Change Details**: A readable summary of the changes (e.g., file permission changes, configuration lines applied).
- Supports common Ansible modules (`ansible.builtin`) and network modules (e.g., `cisco.ios.ios_config`).
- Handles check mode (`-C` or `--check`), logging predicted changes.
- Automatically migrates existing CSV files to include an `Invoked By` column if missing.
- Provides human-readable change details instead of raw JSON for supported modules.

## Requirements

- Ansible 2.9 or later.
- Python 3.6 or later.
- The plugin must be enabled in `ansible.cfg`.

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

   - Ensure the `callback_plugins` path is correctly set if using a custom directory:

     ```ini
     [defaults]
     callback_plugins = /path/to/your/callback_plugins
     callbacks_enabled = device_change_logger
     ```

3. **Verify Permissions**:

   - Ensure the user running Ansible has write permissions to `~/.ansible/changes/` for creating and updating the CSV file.

## Usage

1. **Run a Playbook**:

   - Execute your playbook as usual, e.g.:

     ```bash
     ansible-playbook configure_router.yml
     ```

   - Use `-C` or `--check` for dry-run mode to log predicted changes:

     ```bash
     ansible-playbook -C configure_router.yml
     ```

2. **Check the Log**:

   - The plugin creates or appends to `~/.ansible/changes/change_logs.csv` for tasks where `changed=True`.
   - Open the CSV file to view the logged changes.

## Supported Modules

The plugin formats change details for:

- **System Modules** (e.g., `ansible.builtin.file`, `ansible.builtin.template`, `ansible.builtin.lineinfile`):
  - Logs attribute changes (e.g., `mode: 0644 -> 0755`) or line changes (e.g., `Line changed: Listen 80 -> Listen 8080`).
- **Network Modules** (e.g., `cisco.ios.ios_config`):
  - Logs applied commands (e.g., `Applied commands: interface GigabitEthernet0/1; description Connected to core switch`).
- **Other Modules**:
  - Falls back to JSON or a truncated string for modules with non-standard result structures (e.g., `ansible.builtin.command`, some cloud modules).

## Example CSV Output

Below is a sample `change_logs.csv` after running a playbook `configure_router.yml` with `cisco.ios.ios_config` and `ansible.builtin.file` tasks:

```csv
Timestamp,Host,Task,Playbook,Invoked By,Change Details
2025-08-26T22:35:00.123456,router1.example.com,Configure interface and SNMP,configure_router.yml,admin,Applied commands: interface GigabitEthernet0/1; description Connected to core switch; snmp-server enable traps
2025-08-26T22:35:01.234567,router2.example.com,Configure interface and SNMP,configure_router.yml,admin,Applied commands: interface GigabitEthernet0/1; description Connected to core switch; snmp-server enable traps
2025-08-26T22:35:02.345678,web1.example.com,Set file permissions,configure_router.yml,admin,mode: 0644 -> 0755; owner: nobody -> admin
```

In check mode (`-C`), the output is similar but reflects predicted changes:

```csv
Timestamp,Host,Task,Playbook,Invoked By,Change Details
2025-08-26T22:35:00.123456,router1.example.com,Configure interface and SNMP,configure_router.yml,admin,Applied commands: interface GigabitEthernet0/1; description Connected to core switch; snmp-server enable traps
```

## Notes

- **Check Mode**: The plugin logs predicted changes in check mode (`-C`) if tasks report `changed=True`. Be aware that these are simulated, not actual changes.
- **Limitations**:
  - Modules with non-standard result structures (e.g., `ansible.builtin.command`, some cloud modules) may log less readable JSON output.
  - Large configuration diffs (e.g., in `cisco.ios.ios_config`) may produce verbose output unless `diff=True` is used.
- **CSV Migration**: If an existing `change_logs.csv` lacks the `Invoked By` column, the plugin migrates it automatically, padding existing rows with empty values.
- **User Detection**: The plugin identifies the invoking user via environment variables (`SUDO_USER`, CI variables) or system fallbacks (`getpass.getuser`, `pwd.getpwuid`).

## Troubleshooting

- **No CSV Entries**:
  - Ensure `callbacks_enabled = device_change_logger` is set in `ansible.cfg`.
  - Verify tasks report `changed=True` (check mode may still log if supported by the module).
  - Check write permissions for `~/.ansible/changes/`.
- **Unreadable Change Details**:
  - If JSON is logged, the module may not provide `before`/`after`, `diff`, or `commands`. Consider enabling `diff=True` for network modules or reviewing module documentation.
- **CSV File Issues**:
  - If the CSV is malformed, check for concurrent playbook runs or manual edits. The plugin uses atomic writes to minimize corruption.

## Contributing

To contribute improvements (e.g., support for additional modules, better diff handling), submit a pull request or open an issue in the repository. Suggestions for handling specific module outputs are welcome!

## License

MIT License. See `LICENSE` for details.