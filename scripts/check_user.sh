#!/bin/bash

# This script will take a given username input to see if the user already exists on the system

if [[ "$#" -lt 1 ]]; then
  echo "usage: $0 <username>"
  exit 1
elif getent passwd "$1"; then
  echo "The user $1 already exists on the system"
  exit 2
fi

read -s -p "Enter a password for the new user $1: " USER_PASSWORD
