* LAB for fallocate and setup LVMs:

## Create Virtual Hard Disks using fallocate
- sudo su
- mkdir -p /var/disks
- for i in {1..2}; do touch /var/disks/disk${i}; done
- fallocate -l 1G /var/disks/disk1
- fallocate -l 2G /var/disks/disk2
- losetup /dev/loop1 /var/disks/disk1
- losetup /dev/loop2 /var/disks/disk2

## Using Parted to format the drives
- lsblk
- parted -s /dev/loop1 mklabel gpt
- parted -s /dev/loop1 mkpart primary 0% 100%
- parted -s /dev/loop1 set 1 lvm on
- partprobe /dev/loop1 \
(Repeat the `parted` steps for /dev/loop2)

## Verify the partitionins is correct
- fdisk -l /dev/loop1

## Create the Physical Volume for LVM
- pvcreate /dev/loop1 /dev/loop2
- vgcreate data_vg /dev/loop1 /dev/loop2
- lvcreate -L 1.5G -n data_files data_vg
- lvcreate -l 100%FREE -n data_migration data_vg

## Verify the LVMs have been created (Optional)
- lvs
- for i in {files,migration}; do lvdisplay /dev/data_vg/data_${i}; done

## Format the LVMs with XFS
- mkfs.xfs /dev/data_vg/data_files
- mkfs.xfs /dev/data_vg/data_migration
OR
- for i in {files,migration}; do mkfs.xfs /dev/data_vg/data_${i}; done
  
## Create the directories for mapping the LVMs
- mkdir -p /opt/data/files /opt/data/migration

## Map the LVMs in /etc/fstab
- echo "/dev/data_vg/data_files     /opt/data/files      xfs       defaults 0 0" >> /etc/fstab
- echo "/dev/data_vg/data_migration     /opt/data/migration      xfs       defaults 0 0" >> /etc/fstab
- systemctl daemon-reload
- mount -a
- lsblk
```
NAME                     MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
loop1                      7:1    0    1G  0 loop 
└─data_vg-data_migration 253:1    0  1.5G  0 lvm  /opt/data/migration
loop2                      7:2    0    2G  0 loop 
├─data_vg-data_files     253:0    0  1.5G  0 lvm  /opt/data/files
└─data_vg-data_migration 253:1    0  1.5G  0 lvm  /opt/data/migration
sda                        8:0    0   20G  0 disk 
├─sda1                     8:1    0  200M  0 part /boot/efi
└─sda2                     8:2    0 19.8G  0 part /
```
