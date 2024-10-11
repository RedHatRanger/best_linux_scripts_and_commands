If you want to write 2G of blank information (Caution: This will wipe the drive's first 2G of data):
```
dd if=/dev/zero of=/dev/sda count=1 bs=2G
```
