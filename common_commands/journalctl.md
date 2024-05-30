* To see a live running log of the system
```
journalctl -f
```
OR
```
tail -f /var/log/messages
```

* Other Journalctl commands:
```
journalctl -n5
journalctl --since yesterday
journalctl --since 6h --unit sshd
```

* To make journalctl persistent across reboots:
```
sed -i 's/#Storage=auto/Storage=persistent/' /etc/systemd/journald.conf
```

