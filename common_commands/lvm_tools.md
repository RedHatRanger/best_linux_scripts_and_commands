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





```
