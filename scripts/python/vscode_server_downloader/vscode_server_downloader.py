#!/usr/bin/env python3

# This script is kicked off from a Windows Machine and installs vscode-server to the remote Linux machine
# Sample run: python vscode_server_downloader.py --user rhel --host server1

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path


COMMIT_PATTERN = re.compile(r"^[0-9a-fA-F]{40}$")
SUPPORTED_REMOTE_ARCHITECTURES = {"x86_64", "amd64"}
SCRIPT_VERSION = "1.0.1"



def format_command(command):
    """Return a readable representation of a command."""
    return subprocess.list2cmdline([str(item) for item in command])


def run_command(command, *, capture_output=False):
    """Run a local command and raise an error if it fails."""
    command = [str(item) for item in command]

    print(f"\n> {format_command(command)}")

    try:
        return subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=capture_output,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            f"Required command was not found: {command[0]}"
        ) from exc
    except subprocess.CalledProcessError as exc:
        if capture_output:
            if exc.stdout:
                print(exc.stdout, file=sys.stderr)

            if exc.stderr:
                print(exc.stderr, file=sys.stderr)

        raise RuntimeError(
            f"Command failed with exit code {exc.returncode}: "
            f"{format_command(command)}"
        ) from exc


def require_commands(command_names):
    """Ensure the required commands are available in PATH."""
    missing = []

    for command_name in command_names:
        if shutil.which(command_name) is None:
            missing.append(command_name)

    if missing:
        raise RuntimeError(
            "Required command(s) were not found in PATH: "
            + ", ".join(missing)
        )


def validate_commit_id(commit_id):
    """Validate and normalize a VS Code commit ID."""
    commit_id = commit_id.strip()

    if not COMMIT_PATTERN.fullmatch(commit_id):
        raise ValueError(
            "The commit ID must contain exactly 40 hexadecimal characters."
        )

    return commit_id.lower()


def detect_commit_id():
    """
    Detect the commit ID from the locally installed VS Code.

    On Windows, VS Code commonly provides code.cmd. Batch files need to be
    invoked through cmd.exe. Using CALL also handles paths containing spaces.
    """
    code_command = shutil.which("code")

    if code_command is None:
        raise RuntimeError(
            "The VS Code 'code' command was not found in PATH."
        )

    if os.name == "nt" and code_command.lower().endswith((".cmd", ".bat")):
        # Let cmd.exe resolve `code` from PATH. Avoid quoting the full
        # code.cmd path under Program Files; that causes nested-quote errors.
        command = [
            os.environ.get("COMSPEC", r"C:\Windows\System32\cmd.exe"),
            "/d",
            "/c",
            "code",
            "--version",
        ]
    else:
        command = [
            code_command,
            "--version",
        ]

    result = run_command(
        command,
        capture_output=True,
    )

    for line in result.stdout.splitlines():
        value = line.strip()

        if COMMIT_PATTERN.fullmatch(value):
            return value.lower()

    raise RuntimeError(
        "Could not find a 40-character commit ID in the output of "
        "'code --version'."
    )


def wait_for_browser_download(url):
    """Show the download link and wait until the archive is available."""
    label = "Download vscode-server-linux-x64.tar.gz"
    download_directory = Path.home() / "Downloads"
    archive_path = download_directory / "vscode-server-linux-x64.tar.gz"

    print("\nThe VS Code Server archive must be downloaded in your browser.")

    # OSC 8 hyperlinks work in Windows Terminal and other modern terminals.
    if sys.stdout.isatty():
        print(f"Download link: \033]8;;{url}\033\\{label}\033]8;;\033\\")
    else:
        print(f"Download link: {label}")

    # Always show the URL so it can be copied when hyperlinks are unsupported.
    print(f"URL: {url}")
    print(f"Expected file: {archive_path}")
    print("Use Ctrl+click on the link if your terminal requires it.")

    while True:
        input("\nAfter the download finishes, press Enter to continue...")

        if archive_path.is_file() and archive_path.stat().st_size > 0:
            print(f"Found archive: {archive_path}")
            return archive_path.resolve()

        print("\nThe expected archive was not found or is empty.", file=sys.stderr)
        print(f"Save the download as: {archive_path}", file=sys.stderr)
        print("Then press Enter to check again, or Ctrl+C to cancel.", file=sys.stderr)



def build_ssh_arguments(port, identity_file):
    """Build common SSH and SCP argument lists."""
    ssh_options = [
        "-p",
        str(port),
    ]

    scp_options = [
        "-P",
        str(port),
    ]

    if identity_file:
        identity_path = Path(identity_file).expanduser().resolve()

        if not identity_path.is_file():
            raise FileNotFoundError(
                f"SSH identity file does not exist: {identity_path}"
            )

        ssh_options.extend([
            "-i",
            str(identity_path),
        ])

        scp_options.extend([
            "-i",
            str(identity_path),
        ])

    return ssh_options, scp_options


def run_ssh(
    destination,
    ssh_options,
    remote_script,
    remote_arguments=(),
    *,
    capture_output=False,
):
    """
    Send a shell script to the remote host as UTF-8 bytes.

    Byte-mode input prevents Windows subprocess text mode from converting
    Unix LF line endings into CRLF during SSH transmission.
    """
    command = [
        "ssh",
        *ssh_options,
        destination,
        "/bin/sh",
        "-s",
        "--",
        *[str(argument) for argument in remote_arguments],
    ]

    print(f"\n> {format_command(command)}")

    script_bytes = (
        remote_script
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .encode("utf-8")
    )

    try:
        result = subprocess.run(
            command,
            input=script_bytes,
            check=True,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None,
        )

        if capture_output:
            result.stdout = result.stdout.decode("utf-8", errors="replace")
            result.stderr = result.stderr.decode("utf-8", errors="replace")

        return result

    except FileNotFoundError as exc:
        raise RuntimeError(
            "The SSH command was not found."
        ) from exc

    except subprocess.CalledProcessError as exc:
        stdout = (
            exc.stdout.decode("utf-8", errors="replace")
            if isinstance(exc.stdout, bytes)
            else exc.stdout
        )
        stderr = (
            exc.stderr.decode("utf-8", errors="replace")
            if isinstance(exc.stderr, bytes)
            else exc.stderr
        )

        if capture_output:
            if stdout:
                print(stdout, file=sys.stderr)

            if stderr:
                print(stderr, file=sys.stderr)

        raise RuntimeError(
            f"Remote command failed with exit code {exc.returncode}."
        ) from exc


def check_remote_architecture(destination, ssh_options):
    """Verify that the remote host can use the Linux x64 archive."""
    result = run_ssh(
        destination,
        ssh_options,
        "uname -m\n",
        capture_output=True,
    )

    architecture = result.stdout.strip()

    if architecture not in SUPPORTED_REMOTE_ARCHITECTURES:
        raise RuntimeError(
            "This script installs the server-linux-x64 package, but "
            f"the remote architecture is {architecture!r}."
        )

    print(f"Remote architecture: {architecture}")


def download_file(url, destination):
    """Download the archive while calculating its SHA-256 digest."""
    print("\nDownloading VS Code Server:")
    print(f"  URL:  {url}")
    print(f"  File: {destination}")

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "offline-vscode-server-installer/1.0",
        },
    )

    digest = hashlib.sha256()
    total_bytes = 0

    try:
        with urllib.request.urlopen(request) as response:
            with destination.open("wb") as output_file:
                while True:
                    chunk = response.read(1024 * 1024)

                    if not chunk:
                        break

                    output_file.write(chunk)
                    digest.update(chunk)
                    total_bytes += len(chunk)

    except Exception:
        destination.unlink(missing_ok=True)
        raise

    if total_bytes == 0:
        destination.unlink(missing_ok=True)
        raise RuntimeError("The downloaded archive is empty.")

    print(f"Downloaded: {total_bytes:,} bytes")
    print(f"SHA-256:   {digest.hexdigest()}")


def transfer_archive(
    local_archive,
    destination,
    remote_archive,
    scp_options,
):
    """Copy the archive to the remote host with SCP."""
    run_command([
        "scp",
        *scp_options,
        str(local_archive),
        f"{destination}:{remote_archive}",
    ])


REMOTE_INSTALLER = r"""
set -eu

commit_id="$1"
archive="$2"
install_dir="$HOME/.vscode-server/bin/$commit_id"

case "$commit_id" in
    *[!0-9a-fA-F]*)
        echo "ERROR: Commit ID contains non-hexadecimal characters." >&2
        exit 1
        ;;
esac

if [ "${#commit_id}" -ne 40 ]; then
    echo "ERROR: Commit ID must contain exactly 40 characters." >&2
    exit 1
fi

architecture="$(uname -m)"

if [ "$architecture" != "x86_64" ] &&
   [ "$architecture" != "amd64" ]; then
    echo "ERROR: The x64 package cannot run on: $architecture" >&2
    exit 1
fi

if [ ! -s "$archive" ]; then
    echo "ERROR: Archive is missing or empty: $archive" >&2
    exit 1
fi

echo "Validating the uploaded archive..."
gzip -t "$archive"
tar -tzf "$archive" >/dev/null

mkdir -p "$HOME/.vscode-server/bin"

# Stop active VS Code Server processes before replacing installed commits.
# Match the installed .vscode-server path instead of the broad archive name;
# this avoids terminating this installer shell and its SSH session.
echo "Stopping active VS Code Server processes..."
pkill -9 -f '[.]vscode-server/' 2>/dev/null || true

# Remove all older commit-specific server installations.
echo "Removing older VS Code Server commit directories..."
rm -rf "$HOME/.vscode-server/bin/"*

case "$install_dir" in
    "$HOME/.vscode-server/bin/"????????????????????????????????????????)
        ;;
    *)
        echo "ERROR: Unexpected installation path: $install_dir" >&2
        exit 1
        ;;
esac

temporary_dir="${install_dir}.installing.$$"
backup_dir="${install_dir}.backup.$$"

cleanup() {
    rm -rf "$temporary_dir"

    if [ -d "$backup_dir" ] && [ ! -d "$install_dir" ]; then
        mv "$backup_dir" "$install_dir"
    fi
}

trap cleanup EXIT HUP INT TERM

rm -rf "$temporary_dir"
rm -rf "$backup_dir"
mkdir -p "$temporary_dir"

echo "Extracting VS Code Server..."
echo "Temporary directory: $temporary_dir"

tar -xzf "$archive" \
    -C "$temporary_dir" \
    --strip-components=1

if [ ! -f "$temporary_dir/package.json" ]; then
    echo "ERROR: package.json was not found after extraction." >&2
    exit 1
fi

if [ ! -d "$temporary_dir/out" ]; then
    echo "ERROR: The out directory was not found after extraction." >&2
    exit 1
fi

# Create the completion marker only after validation succeeds.
touch "$temporary_dir/0"

if [ -d "$install_dir" ]; then
    echo "Backing up the existing installation..."
    mv "$install_dir" "$backup_dir"
fi

mv "$temporary_dir" "$install_dir"

rm -rf "$backup_dir"
rm -f "$archive"

trap - EXIT HUP INT TERM

echo
echo "VS Code Server installation completed successfully."
echo "Commit:    $commit_id"
echo "Directory: $install_dir"
echo
echo "Installed content:"
ls -la "$install_dir"

echo
echo "Creating reusable VS Code Server deployment archive..."
cd "$HOME"
rm -f vscode-server.tar.gz
tar -czvf vscode-server.tar.gz .vscode-server/

if [ ! -s "$HOME/vscode-server.tar.gz" ]; then
    echo "ERROR: Deployment archive was not created or is empty." >&2
    exit 1
fi

echo
echo "Deployment archive created successfully."
echo "Archive: $HOME/vscode-server.tar.gz"
ls -lh "$HOME/vscode-server.tar.gz"
"""


def install_remote_server(
    destination,
    ssh_options,
    commit_id,
    remote_archive,
):
    """Install and validate the server archive on the RHEL host."""
    run_ssh(
        destination,
        ssh_options,
        REMOTE_INSTALLER,
        [
            commit_id,
            remote_archive,
        ],
    )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "Download, transfer, and install the matching VS Code Server "
            "on an x86_64 RHEL host."
        )
    )

    parser.add_argument(
        "--host",
        required=True,
        help="SSH hostname or IP address of the RHEL host.",
    )

    parser.add_argument(
        "--user",
        required=True,
        help="Remote Linux username used by VS Code Remote-SSH.",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=22,
        help="Remote SSH port. Default: 22.",
    )

    parser.add_argument(
        "--identity-file",
        help="Optional path to an SSH private key.",
    )

    parser.add_argument(
        "--commit-id",
        help=(
            "Optional 40-character VS Code commit ID. If omitted, "
            "the script obtains it from 'code --version'."
        ),
    )

    parser.add_argument(
        "--archive",
        type=Path,
        help=(
            "Use an existing VS Code Server tar.gz archive instead of "
            "downloading one."
        ),
    )

    parser.add_argument(
        "--keep-archive",
        action="store_true",
        help=(
            "Keep a copy of the downloaded archive in the current "
            "directory after installation."
        ),
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.port < 1 or args.port > 65535:
        raise ValueError("The SSH port must be between 1 and 65535.")

    # The code command is needed only when the commit ID is not provided.
    required_commands = []

    if not args.commit_id:
        required_commands.append("code")

    required_commands.extend([
        "ssh",
        "scp",
    ])

    require_commands(required_commands)

    if args.commit_id:
        commit_id = validate_commit_id(args.commit_id)
    else:
        commit_id = detect_commit_id()

    print(f"\nVS Code Server installer version: {SCRIPT_VERSION}")
    print(f"VS Code commit: {commit_id}")

    download_url = (
        "https://update.code.visualstudio.com/"
        f"commit:{commit_id}/server-linux-x64/stable"
    )

    archive_name = (
        f"vscode-server-linux-x64-{commit_id}.tar.gz"
    )

    destination = f"{args.user}@{args.host}"

    ssh_options, scp_options = build_ssh_arguments(
        args.port,
        args.identity_file,
    )

    print(f"Remote destination: {destination}")

    check_remote_architecture(
        destination,
        ssh_options,
    )

    remote_archive = f"/tmp/{archive_name}"
    temporary_directory = None

    try:
        if args.archive:
            local_archive = args.archive.expanduser().resolve()

            if not local_archive.is_file():
                raise FileNotFoundError(
                    f"Archive does not exist: {local_archive}"
                )

            if local_archive.stat().st_size == 0:
                raise RuntimeError(
                    f"The specified archive is empty: {local_archive}"
                )

            print(f"Using existing archive: {local_archive}")

        else:
            local_archive = wait_for_browser_download(download_url)

        print(f"\nTransferring archive to {destination}...")

        transfer_archive(
            local_archive,
            destination,
            remote_archive,
            scp_options,
        )

        print("\nInstalling VS Code Server on the RHEL host...")

        install_remote_server(
            destination,
            ssh_options,
            commit_id,
            remote_archive,
        )

        if args.keep_archive and temporary_directory:
            retained_archive = Path.cwd() / archive_name
            shutil.copy2(local_archive, retained_archive)
            print(f"\nRetained archive: {retained_archive}")

        print("\nInstallation successful.")
        print(
            f"Reconnect to {args.host!r} using VS Code Remote - SSH."
        )

    finally:
        if temporary_directory is not None:
            temporary_directory.cleanup()


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(
            "\nInstallation cancelled.",
            file=sys.stderr,
        )
        raise SystemExit(130)

    except Exception as exc:
        print(
            f"\nERROR: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(1)
  
