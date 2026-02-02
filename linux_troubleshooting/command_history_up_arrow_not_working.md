## To fix your bash history issue with the up arrow not registering previous command:	
1. vim ~/.bashrc:
shopt -s histappend
PROMPT_COMMAND="history -a; history -n; history -r; $PROMPT_COMMAND"
