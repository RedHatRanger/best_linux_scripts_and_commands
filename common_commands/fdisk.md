![Screenshot from 2024-05-31 08-00-13](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/5141b988-ea52-4dc0-8f3d-1f78e73fb54d)

* LAB for fdisk partitioning:
```
mkdir -p /var/disks
fallocate -l 1G /var/disks/disk1
losetup

# root user:
losetup /dev/loop1 /var/disks/disk1
fdisk /dev/loop1
# Type "p" to print the partition table
# Type "m" for menu of choices
# Type "n" for new
# Type "p" for primary
# Hit Enter for Default on the next one
# Type "+250M" for 250 megabytes
# Type "p" to print the partition table

```