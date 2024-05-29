#!/bin/bash
if [[ "$#" -lt 1 ]]; then
  echo "usage: $0 <username>"
  exit 1
elif getent passwd "$1"; then
  echo "The user $1 already exists on the system"
  exit 2
fi
