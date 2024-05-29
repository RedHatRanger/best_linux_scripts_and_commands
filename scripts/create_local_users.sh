#!/bin/bash

# This script will take a given username input to see if the user already exists on the system
# You will need sudo permission to run this

create_user() {
  if [[ "$#" -lt 1 ]]; then
    echo "usage: $0 <username>"
    exit 1
  elif getent passwd "$1"; then
    echo "The user $1 already exists on the system"
    exit 2
  fi
  useradd -m "$1"
  getent passwd "$1"
}

set_password() {
  while ! [ -n "$USER_PASSWORD" ]; do
    read -s -p "Enter a password for the new user $1: " USER_PASSWORD
  done
  echo "$USER_PASSWORD" | passwd --stdin "$1"
}

for u in "$@"
do
  create_user "$u"
  set_password "$u"
done
