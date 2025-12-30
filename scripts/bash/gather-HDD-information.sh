#!/bin/bash

# This script will gather HDD serial #'s for multiple machines using smartctl, and store them on a network share.

mkdir -p /<some network share>/HDD-Info/$(hostname -s)
echo "lsblk output:" > /<some network share>/HDD-Info/$(hostname -s)/HDD_information.txt
lsblk >> /<some network share>/HDD-Info/$(hostname -s)/HDD_information.txt
echo " "
echo " "
for i in {a..z}; do echo "smartctl -i /dev/sd${i} output:"; smartctl -i /dev/sd${i}; done >> /<some network share>/HDD-Info/$(hostname -s)/HDD_information.txt
echo "df -h output:" >> /<some network share>/HDD-Info/$(hostname -s)/HDD_information.txt
df -h >> /<some network share>/HDD-Info/$(hostname -s)/HDD_information.txt
