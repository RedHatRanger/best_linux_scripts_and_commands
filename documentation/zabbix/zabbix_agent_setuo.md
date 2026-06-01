### Model
To start monitoring your RHEL 8 host, you must configure Zabbix Agent 2 locally and add it to the Zabbix web interface.

#### Step 1: Configure Zabbix Agent 2 on RHEL 8
Open the Zabbix Agent 2 configuration file:
```bash
sudo vi /etc/zabbix/zabbix_agent2.conf
```

Update these three parameters to match your infrastructure:
* **`Server`**: Enter the IP address of your Zabbix server (for passive checks).
* **`ServerActive`**: Enter the IP address of your Zabbix server (for active checks).
* **`Hostname`**: Enter the exact hostname of your RHEL 8 machine. This must precisely match the string you enter into the Zabbix frontend.

Restart and enable the Zabbix Agent 2 service so it survives reboots:
```bash
sudo systemctl restart zabbix-agent2
sudo systemctl enable zabbix-agent2
```

#### Step 2: Add the Host in the Zabbix Web Interface
1. Go to **Data collection** → **Hosts** (or **Configuration** → **Hosts** depending on your Zabbix version).
2. Click **Create host** in the upper right.
3. On the **Host** tab, fill in:
   * **Host name**: Enter the exact hostname string you specified in the `zabbix_agent2.conf` file.
   * **Templates**: Link the official `Linux by Zabbix agent` template (this covers both agent versions).
   * **Host groups**: Select an appropriate group (e.g., `Linux servers`).
4. Under **Interfaces**:
   * Click **Add** and select **Agent**.
   * Input the **IP address** of your RHEL 8 device.
   * Keep the default port at `10050`.
5. Click **Add** to save.

#### Step 3: Verify Connection
Check the host list. The **ZBX** availability icon next to your RHEL 8 machine will turn green within a few minutes when data collection begins successfully.