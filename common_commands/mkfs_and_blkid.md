* Why do we use UUIDs to map disks?:
![Screenshot from 2024-05-31 08-30-19](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/cbe9f3fe-25a0-41d9-9c23-f5bd6cae6917)

* LAB for mkfs and blkid (Continuing from parted lab OR fdisk lab):
```
# As the root user (The -L is for label):
mkfs.xfs -L "DATA" /dev/loop1p1
mount LABEL=DATA /mnt
mount -t XFS

# Now, let's try mounting using the UUID (The -l is for "lazy" umount):
umount -l /mnt
blkid /dev/loop1

# Here is the output:
/dev/loop1p1: LABEL="DATA" UUID="3cd17692-ba06-40a6-839f-637896ba3f51" TYPE="xfs" PARTUUID="f7643882-7566-584c-99f7-4513a937be75"

mkdir /data
vim /etc/fstab

# Add this line:
UUID=3cd17692-ba06-40a6-839f-637896ba3f51      /data     xfs      defaults 0 0

:wq


# Next, let's automount all partitions in /etc/fstab:
systemctl daemon-reload
mount -a
```
