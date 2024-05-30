* Example download ISO:
```
wget https://archive.org/download/tiny-iso-test/TinyIsoTest.iso
```

* Mount the ISO and view its contents:
```
losetup -f TinyIsoTest.iso
lsblk | grep loop
mount /dev/loop0 /mnt
cd /mnt
```
