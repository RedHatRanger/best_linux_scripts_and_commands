To test lag to a home drive on Linux:
```
time dd if=/dev/zero of=~/testfile bs=1M count=1024 oflag=direct
```

If you want to write 2G of blank information (Caution: This will wipe the drive's first 2G of data):
```
dd if=/dev/zero of=/dev/sdb count=1 bs=2G
```

If you want to wipe a hard drive with all zeros:
```
lsblk
dd if=/dev/zero of=/dev/sdb bs=1M status=progress
```

If you want to wipe a hard drive with all random numbers:
```
lsblk
dd if=/dev/urandom of=/dev/sdb bs=1M status=progress
```
