# Linux Home Backup to Windows

This project provides a Python script to back up NFS-mounted Linux home directories to a Windows machine.
The script connects via SSH, creates a compressed `.tar.gz` archive of `/home`, transfers it to Windows, and manages retention of old backups.

## Features
- Full tar+gzip archive of the Linux `/home` directory
- Transfer via `scp` to a Windows folder
- SSH keepalive options (prevents timeouts during large archives)
- Checkpoint dots printed during tar creation (keeps logs alive, shows progress)
- Excludes transient/junk files:
  - `.cache/`, `.local/share/Trash/`, `.gvfs/`, `.dbus/`, `.X11-unix/`
  - Sockets (`*.sock`)
  - Temporary files (`*.tmp`, `*.swp`, `*.lock`)
- Keeps last N backups (default: 7)
- Logs activity to `backup_tar.log`

---

## Requirements

- On Windows:
  - Python 3.x installed (e.g., `C:\\Python311\\python.exe`)
    - Anaconda/PowerShell setup on Windows:
      1. Use Windows Search to find and open `Anaconda Prompt`.
      2. Initialize Conda for PowerShell by running this:
        ```
        conda init
        Setx PYTHONUTF8 1
        ```
      3. Restart PowerShell (close all PowerShell windows, then open a new one). Now you should see (base) automatically.
  
  - OpenSSH client (available on modern Windows)
  - In the example, I downloaeded the python script and saved it to `C:\Users\Public\Public Documents` for ease
      with the `Weekly_Linux_Home_Backup.xml` Task Scheduler.  It can be tailored to meet the needs of the user.
- On Linux:
  - `tar`, `gzip`, and `ssh` (usually preinstalled)
  - Your public SSH key in `~/.ssh/authorized_keys` for passwordless login

---

## Configuration

At the top of `backup_linux_home.py` edit:

```python
LINUX_USER = "rheluser"          # Linux SSH user
LINUX_SERVER = "rhel-server"     # Linux host or IP
LINUX_HOME_DIR = "/home"         # Source directory on Linux
WINDOWS_BACKUP_BASE = r"D:\\LinuxBackups"   # Windows destination
KEEP_BACKUPS = 7                 # Number of archives to retain
```

---

## Running the Script Manually

```powershell
python backup_linux_home.py
```

- Output and tar progress `.` will appear in console & log file:
  - `D:\\LinuxBackups\\backup_tar.log`
- A backup archive will appear in:
  - `D:\\LinuxBackups\\home_backup_YYYYMMDD_HHMMSS.tar.gz`

---

## Automating with Task Scheduler (Weekly)

### Creating your own Task Schedule (Option #1)
1. Open Task Scheduler → Create Task
2. General tab:
   - Name: `Linux Home Weekly Backup`
   - Run whether user is logged on or not
   - Run with highest privileges
3. Triggers tab:
   - New → Weekly → choose day/time (e.g., Sunday @ 2:00 AM)
4. Actions tab:
   - Action: `Start a program`
   - Program/script: `C:\ProgramData\anaconda3\python.exe`
   - Arguments: path to the script (e.g., "C:\Users\Public\Documents\Python Scripts\backup_linux_home.py") # Keep the quotes
   - Start in: folder containing the script (e.g., `C:\Users\Public\Documents`)
5. Settings tab (recommended):
   - Allow task to be run on demand
   - Run task as soon as possible after a scheduled start is missed
6. Save (enter Windows account password if prompted)

### Using an existing Task Scheduler Template XML File ( Option #2)
1. Download the `Weekly_Linux_Home_Backup.xml`
2. Save to `C:\Users\Public\Documents\Python Scripts` (in this example both the XML and python script live here).
3. Open `Task Scheduler` in `Windows`, and click `Import Task`.
4. Browse for the XML file you saved step #1. 
5. General tab:
   - Click `Change User` and enter YOUR Domain or local Username.
6. Trigger tab:
   - Adjust the `date/time` and the frequency of the backups.
7. Then click `Ok` to save the configuration.


---

## Restoring a Backup (Full Restore)

1. Copy the archive back to Linux:

```powershell
scp D:\\LinuxBackups\\home_backup_20251003_124844.tar.gz rheluser@rhel-server:/tmp/
```

2. Extract on Linux:

- Restore everything to `/home` (overwrite existing files):

```bash
sudo tar -xzf /tmp/home_backup_20251003_124844.tar.gz -C /home
```

- OR restore to a different location (safe preview):

```bash
mkdir -p /tmp/restore_test
tar -xzf /tmp/home_backup_20251003_124844.tar.gz -C /tmp/restore_test
```

3. Clean up:

```bash
rm /tmp/home_backup_20251003_124844.tar.gz
```

## Restoring a Single User's Home Directory

Because the archive was created with `tar -czf ... -C /home .`, the top-level entries inside the tar are the usernames (e.g., `alice/`, `bob/`).

### Option A: Restore a single user directly into /home

```bash
# Replace alice with the actual username
sudo tar -xzf /tmp/home_backup_20251003_124844.tar.gz \
  -C /home \
  --wildcards \
  'alice/*'
```

Notes:
- If your tar shows entries prefixed with `./`, use `'./alice/*'` instead.
- Existing files under `/home/alice` will be overwritten. Ownership/permissions are preserved when running with sudo.

### Option B: Restore to a temp location first, then move

```bash
mkdir -p /tmp/restore_alice
# Extract only alice's home into the temp folder, keeping the alice/ prefix
tar -xzf /tmp/home_backup_20251003_124844.tar.gz \
  -C /tmp/restore_alice \
  --wildcards \
  'alice/*'

# Review files, then copy back (preserving attrs)
sudo rsync -a /tmp/restore_alice/alice/ /home/alice/
```

### Inspect the archive to confirm paths

```bash
# List the first 50 entries to see exact path formatting
tar -tzf /tmp/home_backup_20251003_124844.tar.gz | head -50
```

If entries are listed like `./alice/…`, use patterns starting with `./alice/*`.

## Notes

- Logs are written to `D:\\LinuxBackups\\backup_tar.log`.
- By default, up to `KEEP_BACKUPS` archives are kept (older ones deleted).
- SSH keepalive options can be tuned by changing `ServerAliveInterval` and `ServerAliveCountMax` in the script's `SSH_OPTS`.
- Run manually after first setup to confirm configuration before scheduling.

## Sample Configuration
```bash
# ================= Configuration =================


# =================================================
```

## Sample Output

```bash
2025-10-03 12:55:14,766 - INFO - === Starting TAR+GZ Linux Home Backup ===
2025-10-03 12:55:15,873 - INFO - SSH connection successful
2025-10-03 12:55:15,873 - INFO - Creating tar.gz on <server>:/tmp/home_backup_20251003_125515.tar.gz
2025-10-03 13:07:29,047 - INFO - Archive created successfully
2025-10-03 13:07:29,048 - INFO - Fetching archive to C:\Users\<username>\Documents\Backups\home_backup_20251003_125515.tar.gz
2025-10-03 13:09:01,996 - INFO - Archive copied successfully
```
