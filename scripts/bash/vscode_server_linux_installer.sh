#!/usr/bin/env bash

# Description: This Bash script will remove and reapply the correct ~/.vscode-server extensions
#

# Check if the effective UID is 0 (which is the root user):
if [[ "$EUID" == 0 ]]; then
  echo "This script should not be run as root."
  echo "Please run it with a standard user account."
  exit 1 # Exit with a non-zero status code to indicate an error
fi
echo " "

# Warn the user of losing existing vscode-server sessions:
echo -e "** Warning: This will kill ALL of your running 'vscode-server' sessions... **\n"
echo "Press [Enter] to INSTALL VSCODE-SERVER..."
echo "OR"
echo "Press [Ctrl+C] to CANCEL..."
read
echo " "

# Stop vscode-server for the current logged on user
clear
echo "Stopping vscode-server sessions for the current user..."
pkill -9 -f vscode-server 2>/dev/null
sleep 3
clear
echo -e "Stopping vscode-server sessions for the current user...DONE\n"
sleep 3

# Create backup of ~/.vscode-server before removal
sleep 3
if [[ -d ~/.vscode-server ]]; then
    backup_name="$HOME/.vscode-server.backup.$(date +%Y%m%d_%H%M%S)"
    echo "Creating backup of current extensions at $backup_name..."
    mv ~/.vscode-server "$backup_name"
    clear
    echo -e "Stopping vscode-server sessions for the current user...DONE\n"
    echo -e "Creating backup of current extensions at $backup_name...DONE\n"
fi

# Execute 'Order 66' - Removing the extensions
clear
sleep 3
echo -e "Stopping vscode-server sessions for the current user...DONE\n"
echo -e "Creating backup of current extensions at $backup_name...DONE\n"
echo -e "Removing old vscode extensions..."
rm -rfv ~/.vscode-server
sleep 3
clear
echo -e "Stopping vscode-server sessions for the current user...DONE\n"
echo -e "Creating backup of current extensions at $backup_name...DONE\n"
echo -e "Removing old vscode extensions...DONE\n"

# Extract the latest extensions from /ncm/common:
echo "Extracting the new vscode extensions..."
echo "Running 'tar -xzf /share/common/vscode-server.tar.gz --no-same-owner  -C ~/' ..."
echo "Please wait...This will take approximately 5-6 minutes to complete..."
tar -xzf /share/common/vscode-server.tar.gz --no-same-owner  -C ~/
sleep 2
clear
echo "Completed installation of VSCode Extensions.  You can now connect to Remote - SSH in vscode."
