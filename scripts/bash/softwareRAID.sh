#!/bin/bash

# This script will create a software raid using 12 other mounted hard drives. In this example the OS resides on /dev/sda.

for i in {b..m}; do fdisk /dev/sd${i}; done
mdadm --create /dev/md0 --level=6 --raid-devices=11 --spare-devices=1 /dev/sdb1 /dev/sdc1 /dev/sdd1 ... /dev/sdm1
mkfs.ext4 /dev/md0
mkdir /mnt/raid
echo "/dev/md0 /mnt/raid           ext4        defaults 0 0" >> /etc/fstab

# To check: mdadm --details /dev/md0
