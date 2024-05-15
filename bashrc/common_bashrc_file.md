### For Admin Computer

* You must first create a "platform" folder in your home directory, and then copy the /etc/ansible/ stuff to there

# For the Admin user:
```
export ANSIBLE_CONFIG=/home/<myusername>/platform/ansible.cfg
export IBUS_NO_SNOOPER_APPS=python3

alias task='ansible --become --ask-become-pass -m shell -a'
alias go='ssh -Xq -o ServerAliveInterval=60'
alias rocky1='go rky-node1'
alias rocky2='go rky-node2'

rhname=$(hostname -s)
if [[ $rhname == "rky-node1" ]]; thne
  PS1="\u@\h(Rocky1)[\W]$ "
elif [[ $rhname == "rky-node2" ]]; thne
  PS1="\u@\h(Rocky2)[\W]$ "
.
.
.
fi
```

# For the root user:
```
umask 077
alias which='alias | /usr/bin/which --tty-only --read-alias --show-dot --show-tilde'

PS1="\[\033[01;31m\][\u@RockyAdmin\[\033[01;31m\] [\[\033[01;31m\]\W]\\$ \[\033[00m\]"
```
