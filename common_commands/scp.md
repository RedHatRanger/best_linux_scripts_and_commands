* This is an SCP lab:
```
# As Ansible user:
[ansible@rhel9 ~]$ sudo useradd -m bob
[ansible@rhel9 ~]$ ssh-keygen -t rsa -b 4096 -N ""
[ansible@rhel9 ~]$ sudo su - bob

# As Ansible user:
[ansible@rhel9 ~]$ cat ~/.ssh/id_rsa.pub
ssh-rsa sdjfklsajdfklsdjflksjdflksjdflkjsdlkfjslkdjfslkdjfklsjdflk;jsdfklajdslkfjs......
.................................. ansible@rhel9.domain.com
# Copy this output

[ansible@rhel9 ~]$ sudo su - bob

# As bob:
[bob@rhel9 ~]$ mkdir -m 700 .ssh
[bob@rhel9 ~]$ vim ~/.ssh/authorized_keys
# Paste the id_rsa.pub content in this file, then type :wq
[bob@rhel9 ~]$ exit

* As Ansible user:
[ansible@rhel9 ~]$ ssh bob@localhost
# Type yes here
[bob@rhel9 ~]$ exit

# Finally, to test the secure file copy:
[ansible@rhel9 ~]$ scp file1 bob@localhost:/tmp/
```
