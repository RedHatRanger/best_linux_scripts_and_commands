#!/bin/bash

# This script reads the home directories and changes the group name to match the user's home folder

# Iterate over each directory in /home
for i in $(ls /home | sort -u); do 
  # Change the group name recursively to match the user's home folder
  chgrp -Rh $i /home/$i/
done
