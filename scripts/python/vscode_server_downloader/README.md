and here's the readme: # VSCode Server Downloader

Installs the matching VS Code Server on an isolated `x86_64` RHEL machine from a Windows workstation.

**Version:** 1.0.1

## Requirements

On Windows:

* Python 3

* Visual Studio Code with `code` available in `PATH`

* `ssh` and `scp`

* Access to the RHEL host

## Run

Open PowerShell in the folder containing `install_vscode_server.py`:

```powershell
python .\install_vscode_server.py --host <host> --user YOUR_RHEL_USERNAME
```

The script will:

1. Detect your VS Code commit.

2. Provide a link to the matching server archive.

3. Wait while you download the archive.

4. Transfer the archive to the RHEL host.

5. Remove older VS Code Server installations.

6. Install the matching server version.

7. Create a reusable deployment archive.

Save the downloaded file as:

```text
%USERPROFILE%\Downloads\vscode-server-linux-x64.tar.gz
```

Return to PowerShell and press Enter to continue.

## Result

The server is installed at:

```text
~/.vscode-server/bin/<commit-id>
```

A reusable archive is created at:

```text
~/vscode-server.tar.gz
```

When the script finishes, reconnect to `server1` using VS Code Remote - SSH.

## Optional: Use an existing archive

```powershell
python .\install_vscode_server.py --host server1 --user YOUR_RHEL_USERNAME --archive "$HOME\Downloads\vscode-server-linux-x64.tar.gz"
```

> **Warning:** The script stops active VS Code Server processes and deletes existing commit directories under `~/.vscode-server/bin/`.
