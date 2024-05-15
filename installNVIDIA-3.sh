#!/bin/bash

# This script is optional and you will only need it if the graphics doesn't come up after script #2

# Backup these two files
\cp /etc/X11/xorg.conf /etc/X11/xorg.conf.bak
\cp /etc/X11/xorg.conf.nvidia-xconfig-original /etc/X11/xorg.conf.nvidia-xconfig-original.bak
\cp /etc/X11/xorg.conf.nvidia-xconfig-original /etc/X11/xorg.conf
systemctl restart gdm
