* To change the SELinux File Context:
```
chcon -t system_u:object_r:shadow_t:s0 /etc/shadow
```

* To revert SELinux back to normal:
```
restorecon -v /etc/shadow
```
