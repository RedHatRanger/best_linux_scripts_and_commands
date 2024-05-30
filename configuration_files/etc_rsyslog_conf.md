* To view the rsyslog man pages:
```
man 3 rsyslog
man 5 rsyslog.conf
```

* Let's modify the /etc/rsyslog.conf configuration as a test:
```
vim /etc/rsyslog.d/my.conf

local1.warn /var/log/my.log


:wq


systemctl restart rsyslogd
logger -p local1.warn "Hellllpppppppppp!"
```
