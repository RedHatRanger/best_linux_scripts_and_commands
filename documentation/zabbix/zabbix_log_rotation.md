Here is a complete, streamlined runbook for your optimized Zabbix log rotation setup. You can copy and paste this directly into your internal documentation or wiki.
# Runbook: Zabbix Log Rotation Optimization
## Purpose
Configures /var/log/zabbix/zabbix_server.log to rotate and compress as soon as it reaches **1 GB**, and upgrades the system-wide logrotate frequency from daily to **hourly** to prevent sudden log spikes from filling up disk space.
## Step 1: Logrotate Profile Configuration
Create or modify the Zabbix server logrotate configuration file.
 * **File Path:** /etc/logrotate.d/zabbix-server
 * **Configuration:**
```text
/var/log/zabbix/zabbix_server.log {
        size 1G
        rotate 3
        copytruncate
        missingok
        compress
        delaycompress
        notifempty
}

```
### Directive Quick-Reference:
 * **size 1G**: Triggers rotation immediately when the file reaches or exceeds 1 GB.
 * **rotate 3**: Retains a maximum of 3 old log files before purging.
 * **copytruncate**: Safely truncates the active log file to 0 bytes without forcing a Zabbix service restart.
 * **delaycompress**: Delays compression by one cycle. log.1 remains raw text; log.2 and log.3 are zipped into .gz files.
## Step 2: Elevate Systemd Timer to Hourly
By default, systemd only triggers logrotate once a day at midnight. Run the following commands to create a systemd drop-in override file that changes the interval to hourly.
### 1. Apply the Systemd Override
```bash
sudo mkdir -p /etc/systemd/system/logrotate.timer.d/
sudo tee /etc/systemd/system/logrotate.timer.d/override.conf << 'EOF'
[Timer]
OnCalendar=
OnCalendar=hourly
EOF

```
*(Note: The blank OnCalendar= line is required to clear the default daily schedule).*
### 2. Reload and Restart the Timer
```bash
sudo systemctl daemon-reload
sudo systemctl restart logrotate.timer

```
## Step 3: Verification & Operational Commands
### Verify the Hourly Schedule
To confirm systemd is successfully checking the logs every hour, list the active timers:
```bash
systemctl list-timers --all | grep logrotate

```
*Verify that the NEXT column shows the top of the upcoming hour.*
### Force a Manual Dry-Run / Debug
If you want to test the configuration or force an immediate rotation regardless of the file size, run logrotate in verbose/force mode:
```bash
sudo logrotate -v -f /etc/logrotate.d/zabbix-server

```
 * -v: Enables verbose output (displays the exact logic being applied).
 * -f: Forces immediate rotation for testing purposes.
