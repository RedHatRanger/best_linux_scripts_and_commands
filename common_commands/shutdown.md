### These commands must be ran as "sudo"

* To shutdown a system 20 minutes from now and leave a logging message:
```
shutdown -h +20 "Bye Bye Folks"
```

* To reboot a system:
```
shutdown -r now
```

OR

```
init 6
```

* To cancel a scheduled shutdown:
```
shutdown -c
```

* To shutdown or reboot a system without any warning (last resort):
```
poweroff
```
OR 

```
reboot
```
