* To copy the contents of a folder to another folder on another system or the local file system:
```
rsync -av --progress --log-file /var/log/rsync.log /root/ root@192.168.122.100:/root
```

* To copy the folder AND all of its contents:
```
rsync -av --progress --log-file /var/log/rsync.log /root root@192.168.122.100:/
```
