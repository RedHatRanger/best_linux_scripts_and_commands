* To list all block devices in a tree layout:
```
lsblk
```

* To list all block devices, including how they are formatted (xfs, ext4, etc.), and their UUIDs:
```
lsblk -f
```

* To list only the tree from the second partition of a "SCSI" disk or hard drive:
```
lsblk /dev/sda2
```
