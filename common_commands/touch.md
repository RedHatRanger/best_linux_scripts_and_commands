* To prevent standard users from logging in during maintenance mode:
```
touch /etc/nologin
```

* when you are all done and want standard users to login again:
```
rm -rf /etc/nologin
```
