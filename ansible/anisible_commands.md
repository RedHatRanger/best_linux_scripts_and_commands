## To search ansible documentation for proper syntax:
```
ansible-doc -s <module name> 
```

## To TEMPORARILY enable EPEL to install a package:
```
ansible -b -k -i inventory/<myinventory> -m shell -a "yum --enablerepo=<temporary_repoid_name> install python3-ansible-pylibssh -y" all
```
