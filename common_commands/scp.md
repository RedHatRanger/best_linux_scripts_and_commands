* This is an SCP lab:
```
[ansible@rhel9 ~]$ sudo useradd -m bob
[ansible@rhel9 ~]$ ssh-keygen -t rsa -b 4096 -N ""
[ansible@rhel9 ~]$ sudo su - bob

# As bob:
[bob@rhel9 ~]$ mkdir -m 700 .ssh
```
