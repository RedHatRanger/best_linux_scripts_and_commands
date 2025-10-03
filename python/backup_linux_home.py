#!/usr/bin/env python3
# File: manual_backup.py
# Created On: 2025-10-03 14:46:26
# Version: v1.2
# Description: This script runs from Windows, creates a backup of the user's Linux /home folder, then copies it to their 'C:\...\Documents\Backups' directory
#

"""
Backup script:
 - Runs from Windows
 - Tells the Linux server to tar+gzip the /home directory
 - Copies the resulting .tar.gz file to Windows via SCP
 - Keeps only the last N archives
 - Uses SSH keepalive options to prevent timeout
 - Shows tar progress with checkpoint dots
 - Excludes common volatile/cache files and ignores non-fatal warnings
"""

import os
import sys
import subprocess
import datetime
import logging

# ================= Configuration =================
LINUX_USER = "<YOUR USERNAME HERE>"
LINUX_SERVER = "<YOUR LINUX SERVER (FQDN) HERE>"
LINUX_HOME_DIR = "<YOUR LINUX HOME DIR PATH>"
WINDOWS_BACKUP_BASE = r"C:\Users\<YOUR USERNAME>\Documents\Backups"
KEEP_BACKUPS = 7   # How many compressed archives to keep
LOG_FILE = os.path.join(WINDOWS_BACKUP_BASE, "backup_tar.log")
SSH_OPTS = ["-o", "ServerAliveInterval=60", "-o", "ServerAliveCountMax=20"]  # Keeps SSH open for 20 mins before timing out.
# =================================================

os.makedirs(WINDOWS_BACKUP_BASE, exist_ok=True)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def check_ssh():
    """Check SSH connection to Linux server"""
    try:
        cmd = ["ssh"] + SSH_OPTS + [f"{LINUX_USER}@{LINUX_SERVER}", "echo OK"]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if "OK" in result.stdout:
            logging.info("SSH connection successful")
            return True
    except Exception as e:
        logging.error(f"SSH failed: {e}")
    return False

def create_remote_archive():
    """Run tar+gzip on the Linux server with progress output & excludes"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    remote_archive = f"/tmp/home_backup_{timestamp}.tar.gz"

    # Common excludes to keep archives clean/small and avoid transient files
    excludes = [
        "--exclude=.X11-unix",
        "--exclude=.dbus",
        "--exclude=.cache",
        "--exclude=.local/share/Trash",
        "--exclude=.gvfs",
        "--exclude=*.tmp",
        "--exclude=*.swp",
        "--exclude=*.lock",
        "--exclude=*.sock",
    ]

    tar_cmd = (
        f"tar -czf {remote_archive} "
        f"--checkpoint=1000 --checkpoint-action=dot "
        f"--warning=no-file-changed --ignore-failed-read "
        + " ".join(excludes) +
        f" -C {LINUX_HOME_DIR} ."
    )

    cmd = ["ssh"] + SSH_OPTS + [f"{LINUX_USER}@{LINUX_SERVER}", tar_cmd]

    logging.info(f"Creating tar.gz on {LINUX_SERVER}:{remote_archive}")
    try:
        # Let stdout pass through so checkpoint dots appear in console/log
        subprocess.run(cmd, check=True)
        logging.info("Archive created successfully")
        return remote_archive, timestamp
    except subprocess.CalledProcessError as e:
        logging.error(f"Tar command failed: {e}")
        return None, None

def fetch_archive(remote_archive, timestamp):
    """Copy archive from Linux to Windows"""
    local_file = os.path.join(WINDOWS_BACKUP_BASE, f"home_backup_{timestamp}.tar.gz")
    cmd = ["scp"] + SSH_OPTS + [f"{LINUX_USER}@{LINUX_SERVER}:{remote_archive}", local_file]
    logging.info(f"Fetching archive to {local_file}")
    try:
        subprocess.run(cmd, check=True)
        logging.info("Archive copied successfully")
        return local_file
    except subprocess.CalledProcessError as e:
        logging.error(f"SCP failed: {e}")
        return None

def cleanup_remote(remote_archive):
    """Delete the tmp archive on Linux"""
    cmd = ["ssh"] + SSH_OPTS + [f"{LINUX_USER}@{LINUX_SERVER}", f"rm -f {remote_archive}"]
    subprocess.run(cmd)

def cleanup_local_old():
    """Keep only the most recent N archives on Windows"""
    backups = []
    for f in os.listdir(WINDOWS_BACKUP_BASE):
        if f.startswith("home_backup_") and f.endswith(".tar.gz"):
            p = os.path.join(WINDOWS_BACKUP_BASE, f)
            try:
                backups.append((p, os.path.getctime(p)))
            except FileNotFoundError:
                pass
    backups.sort(key=lambda x: x[1], reverse=True)
    for old, _ in backups[KEEP_BACKUPS:]:
        logging.info(f"Removing old backup {old}")
        try:
            os.remove(old)
        except FileNotFoundError:
            pass

def main():
    logging.info("=== Starting TAR+GZ Linux Home Backup ===")
    if not check_ssh():
        sys.exit(1)

    remote_archive, timestamp = create_remote_archive()
    if not remote_archive:
        sys.exit(1)

    local_file = fetch_archive(remote_archive, timestamp)
    cleanup_remote(remote_archive)

    if local_file:
        cleanup_local_old()
        try:
            size_mb = os.path.getsize(local_file) // (2**20)
        except FileNotFoundError:
            size_mb = "unknown"
        logging.info(f"Backup complete → {local_file} ({size_mb} MB)")
        sys.exit(0)
    else:
        logging.error("Backup failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
