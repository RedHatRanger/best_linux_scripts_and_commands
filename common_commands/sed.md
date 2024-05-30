* Example using sed editor to replace something in a configuration file (you may use ? instead of / if desired):
```
sed -i 's/#Storage=auto/Storage=persistent/' /etc/systemd/journald.conf
```
