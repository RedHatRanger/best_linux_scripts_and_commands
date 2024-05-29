* To start, stop, or restart a service, or multiple services:
```
systemctl start chronyd
systemctl stop chronyd.service
systemctl restart crond
systemctl restart crond.service chronyd.service
```
* To enable a service so that it starts automatically at boot:
```
systemctl enable crond
```

* To start and enable a service simultaneously:
```
systemctl enable --now crond
```

* To mask or unmask a service so that it will not enable automatically after a system upgrade:
```
systemctl mask --now crond

# Reverting the mask:
systemctl unmask crond
```

* To check the status of a service, or multiple services:
```
systemctl status sshd
systemctl status sshd crond chronyd
```

* To reload the systemctl daemon:
```
systemctl daemon-reload
```

* To get a default or set a default target:
```
systemctl get-default
systemctl set-default multi-user.target
systemctl set-default graphical.target
```

* To temporarily change a target:
```
systemctl isolate multi-user.target
```

* To list all services running on a system, with or without the given type (service/socket/target/timer):
```
systemctl list-units --type socket
systemctl list-units
```

* To cat a service:
```
[root@ansible]# systemctl cat crond
# /usr/lib/systemd/system/crond.service
[Unit]
Description=Command Scheduler
After=auditd.service nss-user-lookup.target systemd-user-sessions.service time-sync.target ypbind.service autofs.service

[Service]
EnvironmentFile=/etc/sysconfig/crond
ExecStart=/usr/sbin/crond -n $CRONDARGS
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartSec=30s

[Install]
WantedBy=multi-user.target 
```
