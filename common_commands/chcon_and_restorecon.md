### /etc/shadow sample:
* To change the SELinux File Context:
```
chcon -t system_u:object_r:shadow_t:s0 /etc/shadow
```

### Apache HTTPD examples:
* To change the SELinux File Context using a known-good reference:
```
chcon --reference /var/www/html /var/www/html/index.html
```

* OR revert SELinux back to normal:
```
restorecon -vR /var/www/html
```
