* To view the man pages:
```
man 4 loop
```

* Example download ISO:
```
wget https://archive.org/download/tiny-iso-test/TinyIsoTest.iso
```

* Mount the ISO and view its contents (use -f will find the next available loop device):
```
losetup -f TinyIsoTest.iso
lsblk | grep loop
mount /dev/loop0 /mnt
cd /mnt
```
* If you are sure that the loop device is available:
```
losetup /dev/loop6 TinyIsoTest.iso

# Then run losetup to see the loop devices:
losetup
```

* To unmount the ISO:
```
# Exit the directory in use:
cd

# Unmount and delete the loop device:
umount -l /mnt
losetup -d /dev/loop0
losetup -d /dev/loop6

# To delete a single instance:
losetup -d /dev/loop0

* To delete all loop instances:
losetup -D
```

* To create a service which makes losetup persistent:
```
# As the root user:
systemctl edit --full --force losetup.service

[Unit]
Description=Set up loop device
DefaultDependencies=no
Before=local-fs.target
After=systemd-udevd.service
Required=systemd-udevd.service

[Service]
Type=oneshot
ExecStart=/sbin/losetup /dev/loop1 /var/disks/disk1
ExecStart=/sbin/partprobe /dev/loop1
Timeout=60
RemainAfterExit=no

[Install]
WantedBy=local-fs.target

:wq

systemctl daemon-reload
systemctl enable --now losetup.service
```
