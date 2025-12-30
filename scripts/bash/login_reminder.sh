#!/bin/bash

# This script will alert the user for them to take action about something if 28 days have elapsed.

USER_NAME="<your username>"

# Check if 28 days have elapsed since the last time the user logged in.
if [ ! -f /home/$USER_NAME/.last_login_reminder ] || [[ $(find /home/$USER_NAME/.last_login_reminder -mtime +28 -print) ]]; then
  # Display the reminder
  DISPLAY=:0 su $USER_NAME -c 'zenity --warning --text="Please be sure to log into your account soon to avoid lockout."'
  # Update the last reminder file
  touch /home/$USER_NAME/.last_login_reminder
fi


### Open the cron table for editing:
# crontab -e
# Add the following line to run the script daily at a specific time (e.g., 8:00 AM):
# 0 8 * * * /path/to/login_reminder.sh
