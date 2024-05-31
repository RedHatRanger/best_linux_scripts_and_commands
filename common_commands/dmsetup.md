* Standard view:
```
[root@ctrl disks]# dmsetup ls
luks-0c47695d-f0a2-491e-bb5b-b6f2295e84ef	(253:0)
rl-home	(253:6)
rl-root	(253:1)
rl-swap	(253:2)
rl-tmp	(253:8)
rl-var	(253:5)
rl-var_log	(253:7)
rl-var_log_audit	(253:4)
rl-var_tmp	(253:3)
```

* Tree view:
```
[root@ctrl disks]# dmsetup ls --tree
rl-home (253:6)
 └─luks-0c47695d-f0a2-491e-bb5b-b6f2295e84ef (253:0)
    └─ (8:3)
rl-root (253:1)
 └─luks-0c47695d-f0a2-491e-bb5b-b6f2295e84ef (253:0)
    └─ (8:3)
rl-swap (253:2)
 └─luks-0c47695d-f0a2-491e-bb5b-b6f2295e84ef (253:0)
    └─ (8:3)
rl-tmp (253:8)
 └─luks-0c47695d-f0a2-491e-bb5b-b6f2295e84ef (253:0)
    └─ (8:3)
rl-var (253:5)
 └─luks-0c47695d-f0a2-491e-bb5b-b6f2295e84ef (253:0)
    └─ (8:3)
rl-var_log (253:7)
 └─luks-0c47695d-f0a2-491e-bb5b-b6f2295e84ef (253:0)
    └─ (8:3)
rl-var_log_audit (253:4)
 └─luks-0c47695d-f0a2-491e-bb5b-b6f2295e84ef (253:0)
    └─ (8:3)
rl-var_tmp (253:3)
 └─luks-0c47695d-f0a2-491e-bb5b-b6f2295e84ef (253:0)
    └─ (8:3)
```

* Turn on LVM on automatically and create partitions using parted:
```
parted /dev/loop1 mkpart primary 0% 25% set 1 lvm on
parted /dev/loop1 mkpart primary 25% 50% set 2 lvm on
parted /dev/loop1 mkpart primary 50% 75% set 3 lvm on
parted /dev/loop1 mkpart primary 75% 100% set 4 lvm on
parted /dev/loop1 print
```
