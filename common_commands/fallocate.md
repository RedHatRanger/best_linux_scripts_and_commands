* LAB for fallocate:
```
[root@ctrl disks]# fallocate -l 1G /var/disks/disk1
[root@ctrl disks]# fallocate -l 2G /var/disks/disk2
[root@ctrl disks]# losetup /dev/loop1 /var/disks/disk1
[root@ctrl disks]# losetup /dev/loop2 /var/disks/disk2
```
