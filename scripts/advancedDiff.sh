#!/bin/bash

# This script compares the contents of two files and \
# outputs the items from the reference file (file1) that \
# are missing in the comparison file (file2)

for i in $(cat /path/to/file1); do 
  grep -i $i /path/to/file2 &>/devnull
  if [[ $? -ne 0 ]]; then
    echo "$i"
  fi
done
