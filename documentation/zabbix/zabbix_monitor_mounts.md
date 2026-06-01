### User
how do I get it to monitor for a share /ncm to see if it is mounted and if not email an alert

### Model
To monitor if the `/share` share is mounted on your RHEL 8 server and receive an email alert if it drops, you need to create a **Custom Item** using Zabbix Agent 2's built-in filesystem tools, build a **Trigger** to look for missing mount criteria, and configure an **Email Media Type** Action.

#### Step 1: Create the Monitoring Item in the Zabbix Web UI
We will use the native `vfs.fs.mounted` key, which returns `1` if the folder is an active mount point and `0` if it is unmounted or a regular directory.

1. Go to **Data collection** → **Hosts** and click on your RHEL 8 host.
2. Click **Items** at the top of the host's overview page, then click **Create item**.
3. Fill out the item properties:
   * **Name**: `Mount Status of /share`
   * **Type**: `Zabbix agent` or `Zabbix agent (active)` (Choose the mode matching your firewall/config).
   * **Key**: `vfs.fs.mounted[/share]`
   * **Type of information**: `Numeric (unsigned)`
   * **Update interval**: `1m` (Checks every minute).
4. Click **Add** to save the item.

#### Step 2: Create the Trigger to Detect an Unmount Event
Next, we must tell Zabbix to generate a problem alert when the value of the item drops to `0`.

1. While still on your host's configuration screen, click the **Triggers** tab at the top.
2. Click **Create trigger**.
3. Set the following properties:
   * **Name**: `/share Share is NOT Mounted on {HOST.NAME}`
   * **Severity**: `High` or `Average`
   * **Expression**: Click **Add** next to the field, choose your `Mount Status of /ncm` item, select the function `last()` (most recent value) T, and set it to **= 0**. 
     * *The final string looks like this:* `last(/YourHostName/vfs.fs.mounted[/ncm])=0`
4. Click **Add** to save your trigger.

#### Step 3: Configure Email Delivery (Media Type)
If you have not already configured your Zabbix server to send emails, you need to define your SMTP server.

1. Go to **Alerts** → **Media types**.
2. Click on **Email**.
3. Input your corporate or local SMTP details:
   * **SMTP server**: e.g., `://yourdomain.com` or `localhost`
   * **SMTP hello**: `yourdomain.com`
   * **SMTP email**: `zabbix@yourdomain.com`
4. Click **Update**.
5. Assign this media type to your user profile under **Users** → **Users** → select your user profile → **Media** tab → **Add** your email address.

#### Step 4: Create the Action to Email the Alert
Now, link the trigger to the email media delivery system.

1. Go to **Alerts** → **Actions** → **Trigger actions**.
2. Click **Create action** in the top right.
3. In the **Action** tab:
   * **Name**: `Email Alert for Unmounted Shares`
   * **Conditions**: Click **Add**, select **Trigger**, and locate your `/share Share is NOT Mounted` trigger.
4. In the **Operations** tab:
   * Look for the **Operations** block and click **Add**.
   * Under **Send to users**, add your Zabbix user account.
   * Under **Send only to**, select **Email**.
   * Click **Add** to confirm the operation settings.
5. Click **Add** at the bottom of the screen to save the global action rule.

#### Alternative: Troubleshooting Deadlocks via Agent Configuration
If `/ncm` is an **NFS or CIFS network share** and the remote server completely drops off the network, the native `vfs.fs.mounted` item can occasionally hang while attempting to scan the kernel mount table. 

If you notice your Zabbix agent items going into an "Unsupported" state rather than triggering during an outage, you can add a lightweight **UserParameter script** fallback directly on your RHEL 8 host. 

1. Open a custom configuration snippet file on the RHEL 8 server:
   ```bash
   sudo vi /etc/zabbix/zabbix_agent2.d/mount_check.conf
   ```
2. Add the following line to leverage system systemd/mount tables safely without triggering hard hangs:
   ```text
   UserParameter=custom.share.mounted,mountpoint -q /ncm && echo 1 || echo 0
   ```
3. Restart the agent:
   ```bash
   sudo systemctl restart zabbix-agent2
   ```
4. Update your Zabbix Web UI item **Key** from Step 1 to match your custom parameter: `custom.ncm.mounted`.