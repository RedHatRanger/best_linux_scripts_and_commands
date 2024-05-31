* LAB for mkfs.ext4:
```
# First, let's create our virtual raw disk:
[root@ctrl disks]# fallocate -l 3G /var/disks/disk3
[root@ctrl disks]# losetup /dev/loop3 /var/disks/disk3

# Next, let's format a primary partition:
[root@ctrl disks]# fdisk /dev/loop3

Welcome to fdisk (util-linux 2.37.4).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table.
Created a new DOS disklabel with disk identifier 0x4302a9e0.

Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1): 
First sector (2048-6291455, default 2048): 
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-6291455, default 6291455): +250M

Created a new partition 1 of type 'Linux' and of size 250 MiB.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Re-reading the partition table failed.: Invalid argument

The kernel still uses the old table. The new table will be used at the next reboot or after you run partprobe(8) or partx(8).

[root@ctrl disks]# partprobe /dev/loop3
[root@ctrl disks]#
[root@ctrl disks]# mkfs.ext4 /dev/loop3p1
mke2fs 1.46.5 (30-Dec-2021)
Discarding device blocks: done                            
Creating filesystem with 256000 1k blocks and 64000 inodes
Filesystem UUID: c1e7792a-cdfa-43bf-a322-6b5258fa201e
Superblock backups stored on blocks: 
	8193, 24577, 40961, 57345, 73729, 204801, 221185

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (4096 blocks): done
Writing superblocks and filesystem accounting information: done 

[root@ctrl disks]# lsblk
NAME                                          MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINTS
loop1                                           7:1    0     1G  0 loop  
└─VG1-LV1                                     253:9    0   2.5G  0 lvm   
loop2                                           7:2    0     2G  0 loop  
└─VG1-LV1                                     253:9    0   2.5G  0 lvm   
loop3                                           7:3    0     3G  0 loop  
└─loop3p1                                     259:0    0   250M  0 part  
sda                                             8:0    0 238.5G  0 disk  
├─sda1                                          8:1    0   600M  0 part  /boot/efi
├─sda2                                          8:2    0     1G  0 part  /boot
└─sda3                                          8:3    0 236.8G  0 part  
  └─luks-0c47695d-f0a2-491e-bb5b-b6f2295e84ef 253:0    0 236.8G  0 crypt 
    ├─rl-root                                 253:1    0    59G  0 lvm   /
    ├─rl-swap                                 253:2    0   7.8G  0 lvm   [SWAP]
    ├─rl-var_tmp                              253:3    0    10G  0 lvm   /var/tmp
    ├─rl-var_log_audit                        253:4    0    10G  0 lvm   /var/log/audit
    ├─rl-var                                  253:5    0    70G  0 lvm   /var
    ├─rl-home                                 253:6    0    40G  0 lvm   /home
    ├─rl-var_log                              253:7    0    30G  0 lvm   /var/log
    └─rl-tmp                                  253:8    0    10G  0 lvm   /tmp
sr0                                            11:0    1  1024M  0 rom   
[root@ctrl disks]# 
[root@ctrl disks]# blkid | grep loop3
/dev/loop3p1: UUID="c1e7792a-cdfa-43bf-a322-6b5258fa201e" TYPE="ext4" PARTUUID="4302a9e0-01"
```
