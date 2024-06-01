![Screenshot from 2024-06-01 09-28-06](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/8be37a4d-bf0f-470b-8080-5e26d9b69542)

* LAB for special permissions:
```
[root@ctrl ~]# mkdir -p /perms/dir{1..4}
[root@ctrl ~]# cd /perms
[root@ctrl perms]# ll
total 0
drwxr-xr-x. 2 root root 6 Jun  1 09:33 dir1
drwxr-xr-x. 2 root root 6 Jun  1 09:33 dir2
drwxr-xr-x. 2 root root 6 Jun  1 09:33 dir3
drwxr-xr-x. 2 root root 6 Jun  1 09:33 dir4

# Set the Sticky Bit for dir1:
[root@ctrl perms]# chmod -v 1777 /perms/dir1
mode of '/perms/dir1' changed from 0755 (rwxr-xr-x) to 1777 (rwxrwxrwt)

# Set the SGID Bit for dir2:
[root@ctrl perms]# chmod -v 2777 /perms/dir2
mode of '/perms/dir2' changed from 0755 (rwxr-xr-x) to 2777 (rwxrwsrwx)

# Set the Sticky Bit and SGID Bit for dir3:
[root@ctrl perms]# chmod -v 3777 /perms/dir3
mode of '/perms/dir3' changed from 0755 (rwxr-xr-x) to 3777 (rwxrwsrwt)

# Set the Sticky Bit but no permissions allowed to other users:
[root@ctrl perms]# chmod -v 1770 /perms/dir4
mode of '/perms/dir4' changed from 0755 (rwxr-xr-x) to 1770 (rwxrwx--T)
```

* You can use the find command to locate files with special permissions:
```
# Find either SGID or Sticky Bit set:
[root@ctrl perms]# find /perms -type d -perm /g=s,o=t 
/perms/dir1
/perms/dir2
/perms/dir3
/perms/dir4

# Find directories where both SGID and Sticky Bit are set:
[root@ctrl perms]# find /perms -type d -perm -g=s,o=t 
/perms/dir3

# Find directories where only the Sticky Bit is set:
[root@ctrl perms]# find /perms -type d -perm /o=t 
/perms/dir1
/perms/dir3
/perms/dir4
```

![Screenshot from 2024-06-01 09-47-37](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/26c2e34c-c240-4929-a4fb-46d4f99dd8ab)

* LAB for Groups and Collaboration:
```

```
