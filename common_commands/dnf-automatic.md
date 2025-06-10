The dnf-automatic RPM package as a DNF component provides a service which is started automatically.

Install and settings of dnf-automatic
On a fresh install of Fedora with default options, the dnf-automatic RPM is not installed. The first command below installs this RPM:

```
sudo dnf install dnf-automatic
```

By default, dnf-automatic runs from the configurations in the /etc/dnf/automatic.conf file. These configurations only download, but do not apply any of the packages. In order to change or add any configurations, open the .conf file as the root user (or using sudo) from a terminal window.

```
sudo vim /etc/dnf/automatic.conf
```
A modification to automatic.conf to download all updates, apply them, and reboot could be:
```
[commands]
apply_updates=True
reboot=when-needed
```

Omit reboot=when-needed to manually reboot. A full and detailed description of dnf-automatic settings is provided on the dnf-automatic page.

Run dnf-automatic

Once you are finished with the configuration, execute:

```
systemctl enable --now dnf-automatic.timer
```

to enable and start the systemd timer.

Check status of dnf-automatic:

```
systemctl status dnf-automatic.timer
```
