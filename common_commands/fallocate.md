* LAB for fallocate and setup LVMs:
```
## Create Virtual Hard Disks using fallocate
sudo su
mkdir -p /var/disks
for i in {1..2}; do touch /var/disks/disk${i}; done
fallocate -l 1G /var/disks/disk1
fallocate -l 2G /var/disks/disk2
losetup /dev/loop1 /var/disks/disk1
losetup /dev/loop2 /var/disks/disk2

## LVM Partitioning
pvcreate /dev/loop1 /dev/loop2
vgcreate data_vg /dev/loop1 /dev/loop2
lvcreate -L 1.5G -n data_files data_vg
lvcreate -l 100%FREE -n data_migration data_vg
lvs
for i in {files,migration}; do lvdisplay /dev/data_vg/data_${i}; done

```
