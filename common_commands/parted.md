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
parted -s /dev/sdb mklabel gpt
parted -s /dev/sdb mkpart primary 0% 100%
parted -s /dev/sdb set 1 lvm on
```
