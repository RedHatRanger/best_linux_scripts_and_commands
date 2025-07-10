* LAB using parted (Continuing from the fdisk lab):
```
# As the root user:
parted /dev/loop1 print

# Next, lets wipe the previous stuff from the other lab using parted:
parted /dev/loop1 mklabel gpt
# Type "yes"
parted /dev/loop1 mkpart primary 0% 25%

# Print the newly created partition:
parted /dev/loop1 print
```

* LAB 2 using parted
```
# partition the drive
parted -s /dev/sdb mklabel gpt
parted -s /dev/sdb mkpart primary 0% 100%
parted -s /dev/sdb set 1 lvm on

# Create the Physical Volume
pvcreate /dev/sdb1

# Create the Volume Group
vgcreate data_vg /dev/sdb1

# Create the Logical Volume
lvcreate -L 200G -n <lvname> data_vg
OR
lvcreate -l 100%FREE -n <lvname> data_vg

# Format the drive
mkfs.xfs /dev/data_vg/<lvname>
```

* LAB 3 added physical storage, but need to extend partitions
```
# (/dev/sdX is the new drive, where 'X' represents the drive letter the OS assigns it.)
# Need to rescan the physical drives for changes:
echo 1 > /sys/block/sdX/device/rescan
parted /dev/sdX resizepart 1 100%
# Need to refresh the changes for lsblk:
partprobe
lsblk
pvresize /dev/sdX
# Extend the partition:
lvextend -r -l +100%FREE /dev/<Volume_Group_Name>/<LV_Name>
# Example: lvextend -r -l +100%FREE /dev/VG1/LV1
```
