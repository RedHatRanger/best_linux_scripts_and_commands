#!/bin/bash

# This script measures the time taken to run the dd command which creates a 1GB 
# file filled with random data from /dev/urandom

# Measure and display the time taken to execute the dd command
time dd if=/dev/urandom of=/opt/testfile.txt bs=1G count=1
