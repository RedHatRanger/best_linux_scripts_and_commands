* Example using sed editor to replace something in a configuration file (you may use ? instead of / if desired):
```
sed -i 's/#Storage=auto/Storage=persistent/g' /etc/systemd/journald.conf
```

* Inside a file, when using vim:
```
:1,$s/#Storage=auto/Storage=persistent/g
```
