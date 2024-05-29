* To start or restart a service, or multiple services:
```
systemctl restart crond
systemctl stop chronyd.service
systemctl start chronyd
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
systemctl disable --now crond
systemctl mask crond

# Reverting the mask:
systemctl unmask crond
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