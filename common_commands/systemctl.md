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
