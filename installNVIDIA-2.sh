#!/bin/bash

# This script has several parts but it will install the NVIDIA driver from the share to the host

# Set the initial variables
driver1="535.129.03"
driver2="470.82.01"
driver3="470.223.02"

# Test to see if NVIDIA cards are present
lspci | grep -i nvidia &>/dev/null
if [[ $? -ne 0 ]]; then
  clear
  echo -e "\nThis machine does not have an NVIDIA graphics card so NO NEED TO RUN THIS\n"
  exit
fi

systemctl isolate multi-user.target
mkdir -p /mnt/media

# Install the necessary components
yum install -y gcc make kernel-headers kernel-devel acpid libglvnd* pkgconfig &>/dev/null

# Run the NVIDIA Installer
gcard=$(lspci | grep -i nvidia | awk -F: 'NR==1{print $0}')
if [[ $gcard =~ "P2000" ]] || [[ $gcard =~ "P6000" ]] || [[ $gcard =~ "K2200" ]]; then
  clear
  echo -e "\nThis will install the new $driver1 driver...Please wait...\n"
  sh /root/NVIDIA-Linux-x86_64-${driver1}.run --tmpdir /mnt/media
elif [[ $gcard =~ "2235" ]]; then
  clear
  echo -e "\nThis will install the new $driver2 driver...Please wait...\n"
  sh /root/NVIDIA-Linux-x86_64-${driver2}.run --tmpdir /mnt/media
else
  clear
  echo -e "\nThis will install the new $driver3 driver...Please wait...\n"
  sh /root/NVIDIA-Linux-x86_64-${driver3}.run --tmpdir /mnt/media
fi

# Rebuild the initramfs file
find /boot -name "*nouveau*" &>/dev/null
if [[ $? -ne 0 ]]; then
  mv /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r)-nouveau.img
  dracut /boot/initramfs-$(uname -r).img $(uname -r)
fi

# Set the default target back to graphical.target
systemctl set-default graphical.target

# Reboot the system
init 6
