* LAB for NFS Server Setup (The port is 2049 for use with NFS):
```
# See which port is nfs:
[root@ctrl ~]# rpcinfo -p | grep nfs
    100003    4   tcp   2049  nfs

# Install the package and start the service:
[root@ctrl ~]# yum -y install nfs-utils
Package nfs-utils-1:2.5.4-25.el9.x86_64 is already installed.
Dependencies resolved.
Nothing to do.
Complete!
[root@ctrl ~]# 
[root@ctrl ~]# systemctl enable --now nfs-server
Created symlink /etc/systemd/system/multi-user.target.wants/nfs-server.service → /usr/lib/systemd/system/nfs-server.service.

# Enable NFS Version 4 and above:
[root@ctrl ~]# nfsconf --set nfsd vers4 y
[root@ctrl ~]# nfsconf --set nfsd tcp y
[root@ctrl ~]# nfsconf --set nfsd udp n
[root@ctrl ~]# nfsconf --set nfsd vers3 n

# Verify that Version 3 is turned off:
[root@ctrl ~]# cat /proc/fs/nfsd/versions 
-3 +4 +4.1 +4.2
```