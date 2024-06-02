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

# Find all files in /usr/share/doc that are of the PDF type (For Testing):
[root@ctrl ~]# find /usr/share/doc -name "*pdf"
/usr/share/doc/adobe-mappings-pdf
/usr/share/doc/pigz/pigz.pdf
/usr/share/doc/sil-padauk-fonts/documentation/Padauk-features.pdf
/usr/share/doc/sil-padauk-fonts/documentation/Padauk-typesample.pdf
/usr/share/doc/paktype-naskh-basic-fonts/PakTypeNaskhBasicFeatures.pdf
/usr/share/doc/gutenprint-doc/gutenprint-users-manual.pdf

# Now copy those "test" files to /opt/sales:
[root@ctrl ~]# mkdir -p /opt/sales; find /usr/share/doc -name "*pdf" -exec cp -rf {} /opt/sales \;

# Next, let's edit the /etc/exports file:
[root@ctrl ~]# vim /etc/exports.d/sales.exports

/opt/sales 192.168.122.*(rw,sync,no_root_squash)

:wq


# Finally, let's export the NFS Share:
[root@ctrl ~]# exportfs -avr
exporting 192.168.122.0/24:/opt/sales

# Now, from the other client computers:
mount -t nfs4 <IP Address of the NFS Server>:/opt/sales /mnt
ls -l /mnt

# Optionally, you may add the proper line in /etc/fstab on the flient:
<IP Address of the NFS Server>:/opt/sales /mnt       nfs4       defaults 0 0
```

* Now we could possibly use autofs to auto mount the share to the clients:
```
yum install -y autofs
vim /etc/auto.master.d/data.autofs

/data /etc/auto.data

:wq


vim /etc/auto.data

sales -rw,soft,intr <IP Address of the NFS Server>:/opt/sales

:wq
```
