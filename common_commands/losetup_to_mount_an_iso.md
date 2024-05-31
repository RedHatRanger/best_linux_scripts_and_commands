* To view the man pages:
```
man 4 loop
```

* Example download ISO:
```
wget https://archive.org/download/tiny-iso-test/TinyIsoTest.iso
```

* Mount the ISO and view its contents (use -f will find the next available loop device):
```
losetup -f TinyIsoTest.iso
lsblk | grep loop
mount /dev/loop0 /mnt
cd /mnt
```
* If you are sure that the loop device is available:
```
losetup /dev/loop6 TinyIsoTest.iso

# Then run losetup to see the loop devices:
losetup
```

* To unmount the ISO:
```
# Exit the directory in use:
cd

# Unmount and delete the loop device:
umount -l /mnt
losetup -d /dev/loop0
losetup -d /dev/loop6

# To clear a single instance:
losetup -d /dev/loop0

* To clear all loop instances:
losetup -D
```
