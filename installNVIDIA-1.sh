```
#!/bin/bash

# This script has several parts but it will install the NVIDIA driver from the share to the host

# Set the initial variables
driver1="535.129.03"
driver2="470.82.01"
driver3="470.223.02"

# Test to see if NVIDIA cards are present
lspci | grep -i nvidia &>/dev/null
if [[ $? -eq 1 ]]; then
  clear
  echo -e "\nThis machine does not have an NVIDIA graphics card so NO NEED TO RUN THIS\n"
  exit
fi

# See which NVIDIA card is present
gcard=$(lspci | grep -i nvidia | awk -F: 'NR==1{print $0}')
if [[ $gcard =~ "P2000" ]] || [[ $gcard =~ "P6000" ]] || [[ $gcard =~ "K2200" ]]; then
  clear
  echo -e "\nCopying the necessary NVIDIA INstaller file to /root...Please wait...\n"
  rsync -av --progress /<some network share path>/NVIDIA-Linux-x86_64-${driver1}.run /root &>/dev/null
elif [[ $gcard =~ "2235" ]]; then
  clear
  echo -e "\nCopying the necessary NVIDIA INstaller file to /root...Please wait...\n"
  rsync -av --progress /<some network share path>/NVIDIA-Linux-x86_64-${driver2}.run /root &>/dev/null
else
```
