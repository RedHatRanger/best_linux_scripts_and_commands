* To start or restart a service, or multiple services:
```
systemctl restart crond
systemctl stop chronyd.service
systemctl start chronyd
systemctl restart crond.service chronyd.service
```

* To start and enable a service simultaneously:
```
systemctl enable --now crond
```

* To check the status of a service, or multiple services:
```
systemctl status sshd
systemctl status sshd crond chronyd
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
