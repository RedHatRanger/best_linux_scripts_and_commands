#!/bin/bash

# Use this script to log your yum updates and also prepare for the nvidia driver installation

nvidiafile=/root/nvidia_configuration.txt
nvidia-smi > $nvidiafile
uname -r >> $nvidiafile
yum clean all
yum -y update | tee -a /root/$(date +%F)-yum-updates.txt

nvidia-smi &>/dev/null
if [[ $? -eq 0 ]]; then
  systemctl set-default multi-user.target
  echo "Please reboot and then install the NVIDIA driver."
else
  echo "This system doesn't use an NVIDIA driver...You are done...Please reboot."
fi
