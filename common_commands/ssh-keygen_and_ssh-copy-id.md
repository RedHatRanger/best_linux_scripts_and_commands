* Generate a private and public key exchange:
```
ssh-keygen -t rsa -b 4096 -N ""
ssh-copy-id -i ~/.ssh/id_rsa.pub ansible@192.168.122.100
<ENTER PASSWORD>
```

* Try using SSH to the remote system without a password (You may create the alias for ssh command to make shorter):
```
ssh -Xq -o ServerAliveInterval=60 ansible@192.168.122.100
```


* Success!!
