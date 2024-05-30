* To view the man pages for logrotate:
```
man 5 logrotate.conf
```

* To make a custom logrotate configuration:
```
vim /etc/logrotate.conf

/var/log/my.log
{
  weekly
  rotate 4
  size 100
  dateext
  compress
  copytruncate
}

:wq

logrotate /etc/logrotate.conf
ls -l /var/log/my*
```
![Screenshot from 2024-05-30 08-44-06](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/d4538a2b-18bb-4cea-8165-c24df9f4a964)
![Screenshot from 2024-05-30 08-44-06](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/d4538a2b-18bb-4cea-8165-c24df9f4a964)

