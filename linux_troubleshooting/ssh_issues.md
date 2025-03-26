* If you keep having to input a password even after copying the id_ecdsa.pub key to the host…
```
chmod 644 ~/.ssh/authorized_keys

# Execute this one the destination host.
```

* If you need to fix your .ssh/known_hosts file:
```
ssh-keyscan <IP_address>  >> ~/.ssh/known_hosts
```
