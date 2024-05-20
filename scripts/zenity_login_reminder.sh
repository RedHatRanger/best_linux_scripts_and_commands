#!/bin/bash

# This script will alert the user for them to take action about something if 28 days have elapsed.

USER_NAME="<your username>"

# Check if 28 days have elapsed since the last time the user logged in.
if [[ ! -f /home/$USER_NAME/last_login_reminder]] || [[ `find ~/.last_login_reminder -mtime +28 -print` ]]; then
  # Display the reminder
  DISPLAY=:0 su $USER_NAME -c zenity --info --text="Please log into your other system."
  # Update the last reminder file
  touch ~/.last_login_reminder
fi
