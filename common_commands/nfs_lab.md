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

# Setup the Firewall:
[root@ctrl ~]# firewall-cmd --state
running
[root@ctrl ~]# firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: virbr0 virbr1 virbr2 wlp1s0
  sources: 
  services: cockpit ntp ssh
  ports: 
  protocols: 
  forward: yes
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
[root@ctrl ~]# firewall-cmd --permanent --add-service=nfs; firewall-cmd --reload; firewall-cmd --list-all
success
success
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: virbr0 virbr1 virbr2 wlp1s0
  sources: 
  services: cockpit nfs ntp ssh
  ports: 
  protocols: 
  forward: yes
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules:
```
