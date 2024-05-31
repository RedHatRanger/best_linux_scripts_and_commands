* LAB using parted (Continuing from the fdisk lab):
```
# As the root user:
parted /dev/loop1 print

# Next, lets wipe the previous stuff from the other lab using parted:
parted /dev/loop1 mklabel msdos
# Type "yes"
parted /dev/loop1 mkpart primary 0% 25%

# Print the newly created partition:
parted /dev/loop1 print
```
