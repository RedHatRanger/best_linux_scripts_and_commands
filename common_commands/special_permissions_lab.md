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

* LAB for Sticky Bit and Collaboration (This next part is the demo of how this works):

![Screenshot from 2024-06-01 09-51-29](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/369b72b4-d251-4d1f-99e6-8deb4506c791)

![Screenshot from 2024-06-01 09-52-30](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/b0074389-30ca-4b38-b05b-2732a88f15b3)


* This next part is where we get to see how SGID works on Collaborative Directories (Demo):
![Screenshot from 2024-06-01 09-55-20](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/a2c2a0b9-b385-4a40-b5c1-28ccffcf4ffc)

![Screenshot from 2024-06-01 09-57-16](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/feae7fb5-ee2c-4542-904c-3f7ddfc37400)

![Screenshot from 2024-06-01 09-59-06](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/365a0b4b-167a-4b00-9e21-d71fa418b9ac)

![Screenshot from 2024-06-01 09-59-51](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/798c541b-11f8-4633-81fa-3de762926638)
