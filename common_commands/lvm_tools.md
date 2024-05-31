* LAB using fallocate, looping devices, and LVM Tools:
```
# Make this directory if you haven't already:
[root@ctrl disks]# mkdir -p /var/disks

# Now let's create our virtual raw disks:
[root@ctrl disks]# fallocate -l 1G /var/disks/disk1
[root@ctrl disks]# fallocate -l 2G /var/disks/disk2
[root@ctrl disks]# losetup /dev/loop1 /var/disks/disk1
[root@ctrl disks]# losetup /dev/loop2 /var/disks/disk2

# Let's setup our physical volumes:
[root@ctrl disks]# pvcreate /dev/loop1 /dev/loop2
  Physical volume "/dev/loop1" successfully created.
  Physical volume "/dev/loop2" successfully created.
[root@ctrl disks]# pvs
  PV                                                    VG Fmt  Attr PSize    PFree
  /dev/loop1                                               lvm2 ---     1.00g 1.00g
  /dev/loop2                                               lvm2 ---     2.00g 2.00g
  /dev/mapper/luks-0c47695d-f0a2-491e-bb5b-b6f2295e84ef rl lvm2 a--  <236.81g    0 


# Next, let's set up our volume group:
[root@ctrl disks]# vgcreate -v vg1 /dev/loop1 /dev/loop2 
  Wiping signatures on new PV /dev/loop1.
  Wiping signatures on new PV /dev/loop2.
  Adding physical volume '/dev/loop1' to volume group 'vg1'
  Adding physical volume '/dev/loop2' to volume group 'vg1'
  Creating volume group backup "/etc/lvm/backup/vg1" (seqno 1).
  Volume group "vg1" successfully created
[root@ctrl disks]# vgs
  VG  #PV #LV #SN Attr   VSize    VFree
  rl    1   8   0 wz--n- <236.81g    0 
  vg1   2   0   0 wz--n-    2.99g 2.99g
[root@ctrl disks]# vgdisplay
  --- Volume group ---
  VG Name               vg1
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               2.99 GiB
  PE Size               4.00 MiB
  Total PE              766
  Alloc PE / Size       0 / 0   
  Free  PE / Size       766 / 2.99 GiB
  VG UUID               fVYv06-23m2-mnWE-mWnp-swNc-vZ4S-HvT1hY


# To remove the Volume Group VG1 and the two looping Physical Volumes:
[root@ctrl disks]# vgremove vg1
  Volume group "vg1" successfully removed
[root@ctrl disks]# pvremove /dev/loop1 /dev/loop2
  Labels on physical volume "/dev/loop1" successfully wiped.
  Labels on physical volume "/dev/loop2" successfully wiped.


# To change the default Extant size from 4M to 8M:
[root@ctrl disks]# pvcreate /dev/loop1 /dev/loop2
  Physical volume "/dev/loop1" successfully created.
  Physical volume "/dev/loop2" successfully created.
[root@ctrl disks]# vgcreate -v -s 8m VG1 /dev/loop1 /dev/loop2
  Wiping signatures on new PV /dev/loop1.
  Wiping signatures on new PV /dev/loop2.
  Adding physical volume '/dev/loop1' to volume group 'VG1'
  Adding physical volume '/dev/loop2' to volume group 'VG1'
  Creating volume group backup "/etc/lvm/backup/VG1" (seqno 1).
  Volume group "VG1" successfully created
[root@ctrl disks]# vgdisplay VG1
  --- Volume group ---
  VG Name               VG1
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               2.98 GiB
  PE Size               8.00 MiB
  Total PE              382
  Alloc PE / Size       0 / 0   
  Free  PE / Size       382 / 2.98 GiB
  VG UUID               BpdyAk-Rz3T-bJNc-hP3e-DR8i-JqvN-n6DMwI


# Next, let's use the lvcreate command:
[root@ctrl disks]# lvcreate -n LV1 -L 1.5G VG1
  Logical volume "LV1" created.
[root@ctrl disks]# lvdisplay VG1
  --- Logical volume ---
  LV Path                /dev/VG1/LV1
  LV Name                LV1
  VG Name                VG1
  LV UUID                j0tmFQ-cMf0-7FWU-vPN0-IPke-h8QN-yEAcIj
  LV Write Access        read/write
  LV Creation host, time ctrl.example.com, 2024-05-31 09:24:54 -0500
  LV Status              available
  # open                 0
  LV Size                1.50 GiB
  Current LE             192
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:9

# Next, let's create LV2 using 100 more extants from VG1:
[root@ctrl disks]# vgdisplay VG1
  --- Volume group ---
  VG Name               VG1
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  2
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                1
  Open LV               0
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               2.98 GiB
  PE Size               8.00 MiB
  Total PE              382
  Alloc PE / Size       192 / 1.50 GiB
  Free  PE / Size       190 / 1.48 GiB
  VG UUID               BpdyAk-Rz3T-bJNc-hP3e-DR8i-JqvN-n6DMwI
[root@ctrl disks]# lvcreate -n LV2 -l 100 VG1
WARNING: xfs signature detected on /dev/VG1/LV2 at offset 0. Wipe it? [y/n]: y
  Wiping xfs signature on /dev/VG1/LV2.
  Logical volume "LV2" created.
[root@ctrl disks]# vgdisplay VG1
  --- Volume group ---
  VG Name               VG1
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  3
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               0
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               2.98 GiB
  PE Size               8.00 MiB
  Total PE              382
  Alloc PE / Size       292 / 2.28 GiB
  Free  PE / Size       90 / 720.00 MiB
  VG UUID               BpdyAk-Rz3T-bJNc-hP3e-DR8i-JqvN-n6DMwI
# As you can see there are 90 Physical Extants (720MB) remaining after creating 2 logical partitions (2.28GB)
```
![Screenshot from 2024-05-31 09-32-42](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/6c100b49-6842-4786-9a2f-05c891c0096a)

* But what if we want to extend these volumes?:
```
# Let's destroy and recreate VG1 using our loop1 and loop2 raw disks:
[root@ctrl disks]# vgremove VG1
  Volume group "VG1" successfully removed
[root@ctrl disks]# vgcreate -v -s 8m VG1 /dev/loop1 /dev/loop2
  Wiping signatures on new PV /dev/loop1.
  Wiping signatures on new PV /dev/loop2.
  Adding physical volume '/dev/loop1' to volume group 'VG1'
  Adding physical volume '/dev/loop2' to volume group 'VG1'
  Creating volume group backup "/etc/lvm/backup/VG1" (seqno 1).
  Volume group "VG1" successfully created
[root@ctrl disks]# vgdisplay VG1
  --- Volume group ---
  VG Name               VG1
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               2.98 GiB
  PE Size               8.00 MiB
  Total PE              382
  Alloc PE / Size       0 / 0   
  Free  PE / Size       382 / 2.98 GiB
  VG UUID               Ad7dR4-nU6c-z18z-SoeY-kv17-4iwd-ISVjTu

# Now, let's create the logical volume LV1:
[root@ctrl disks]# lvcreate -n LV1 -L +1G VG1
  Logical volume "LV1" created.
[root@ctrl disks]# lvdisplay /dev/VG1/LV1
  --- Logical volume ---
  LV Path                /dev/VG1/LV1
  LV Name                LV1
  VG Name                VG1
  LV UUID                q2r8sW-TRAu-mStU-Ugh1-xEwA-fG21-7b1TRb
  LV Write Access        read/write
  LV Creation host, time ctrl.example.com, 2024-05-31 09:49:41 -0500
  LV Status              available
  # open                 0
  LV Size                1.00 GiB
  Current LE             128
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:9

# Let's create a filesystem type XFS and extend it 1.5GB:
[root@ctrl disks]# mkfs.xfs /dev/VG1/LV1
meta-data=/dev/VG1/LV1           isize=512    agcount=4, agsize=65536 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=1, sparse=1, rmapbt=0
         =                       reflink=1    bigtime=1 inobtcount=1 nrext64=0
data     =                       bsize=4096   blocks=262144, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0, ftype=1
log      =internal log           bsize=4096   blocks=16384, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
Discarding blocks...Done.
[root@ctrl disks]#
[root@ctrl disks]# lvextend -r -L +1.5G LV1 VG1
  Volume group "LV1" not found
  Cannot process volume group LV1
[root@ctrl disks]#
[root@ctrl disks]# lvextend -r -L +1.5G /dev/VG1/LV1
  Size of logical volume VG1/LV1 changed from 1.00 GiB (128 extents) to 2.50 GiB (320 extents).
  File system xfs found on VG1/LV1.
  File system mount is needed for extend.
Continue with xfs file system extend steps: mount, xfs_growfs? [y/n]:y
  Extending file system xfs to 2.50 GiB (2684354560 bytes) on VG1/LV1...
mount /dev/VG1/LV1 /tmp/tmp.O1iaVXsfTY_lvresize_102695
mount done
xfs_growfs /dev/VG1/LV1
meta-data=/dev/mapper/VG1-LV1    isize=512    agcount=4, agsize=65536 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=1, sparse=1, rmapbt=0
         =                       reflink=1    bigtime=1 inobtcount=1 nrext64=0
data     =                       bsize=4096   blocks=262144, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0, ftype=1
log      =internal log           bsize=4096   blocks=16384, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
data blocks changed from 262144 to 655360
xfs_growfs done
cleanup unmount /tmp/tmp.O1iaVXsfTY_lvresize_102695
cleanup unmount done
  Extended file system xfs on VG1/LV1.
  Logical volume VG1/LV1 successfully resized.
[root@ctrl disks]# lvdisplay /dev/VG1/LV1
  --- Logical volume ---
  LV Path                /dev/VG1/LV1
  LV Name                LV1
  VG Name                VG1
  LV UUID                q2r8sW-TRAu-mStU-Ugh1-xEwA-fG21-7b1TRb
  LV Write Access        read/write
  LV Creation host, time ctrl.example.com, 2024-05-31 09:49:41 -0500
  LV Status              available
  # open                 0
  LV Size                2.50 GiB
  Current LE             320
  Segments               2
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:9


# To make /dev/VG1/LV1 mounted persistently:
mkdir -p /lv/lv1
vim /etc/fstab

# Add this line
/dev/VG1/LV1 /lv/lv1      xfs       defaults 0 0

:wq

systemctl daemon-reload
mount -a
```

* If we needed to extend our volume group to a loop3 device:
```
vgextend -v VG1 /dev/loop3
```

* To view the xfs information:
```
[root@ctrl disks]# xfs_info /dev/VG1/LV1
meta-data=/dev/VG1/LV1           isize=512    agcount=10, agsize=65536 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=1, sparse=1, rmapbt=0
         =                       reflink=1    bigtime=1 inobtcount=1 nrext64=0
data     =                       bsize=4096   blocks=655360, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0, ftype=1
log      =internal log           bsize=4096   blocks=16384, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
```
* Optionally, you can extend an LVM to 100% of the VG1:
```
lvextend -r -l +100%FREE /dev/VG1/LV1
```

* To give assign a new label to the xfs partition:
```
[root@ctrl disks]# xfs_admin -L "DATA" /dev/VG1/LV1
writing all SBs
new label = "DATA"

# We can validate this by:
[root@ctrl disks]# xfs_admin -l /dev/VG1/LV1
label = "DATA"
[root@ctrl disks]# blkid | grep LV1
/dev/mapper/VG1-LV1: LABEL="DATA" UUID="3ccb0a2d-fcd6-45a8-85f4-e94579499fe3" TYPE="xfs"
```
![Screenshot from 2024-05-31 10-35-35](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/1026aeb8-1b2a-489f-a735-eebb74e8b881)
