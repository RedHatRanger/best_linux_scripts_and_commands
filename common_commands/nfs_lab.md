* LAB for NFS Server Setup:
```
# Install the package and start the service:
[root@ctrl ~]# yum -y install nfs-utils
Package nfs-utils-1:2.5.4-25.el9.x86_64 is already installed.
Dependencies resolved.
Nothing to do.
Complete!
[root@ctrl ~]# 
[root@ctrl ~]# systemctl enable --now nfs-server
Created symlink /etc/systemd/system/multi-user.target.wants/nfs-server.service → /usr/lib/systemd/system/nfs-server.service.
```
