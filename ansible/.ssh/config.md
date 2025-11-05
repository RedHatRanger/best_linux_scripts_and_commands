## Paste this into your `~/.ssh/config` file:
```bash
Host <my_server_alias>                         # Alias of the server
    Hostname 192.168.1.100
    User <my_username>
    Port 22
    IdentityFile ~/.ssh/id_rsa
```
