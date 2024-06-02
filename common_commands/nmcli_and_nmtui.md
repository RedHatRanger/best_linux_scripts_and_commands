* nmcli demonstration:
```
[root@ctrl ~]# nmcli con
NAME                 UUID                                  TYPE      DEVICE 
lo                   19dc588a-3360-4168-b581-bb1445d14fbf  loopback  lo     
enp2s0               203037ce-37ee-4565-aa7a-790ebcfc49fe  ethernet  --     

# If you need to bring a connection down and up again:
[root@ctrl ~]# nmcli con down lo
Connection 'lo' successfully deactivated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/1)
[root@ctrl ~]# nmcli con up lo
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/10)

# If you need to add a connection:
[root@ctrl ~]# nmcli con add type ethernet ifname eth1 ipv4.method manual ipv4.addresses 192.168.122.250/24 connection.id cafe
Connection 'cafe' (9d337292-36ee-459e-b5da-2168477696ac) successfully added.
[root@ctrl ~]# nmcli con
NAME                 UUID                                  TYPE      DEVICE
lo                   19dc588a-3360-4168-b581-bb1445d14fbf  loopback  lo  
cafe                 9d337292-36ee-459e-b5da-2168477696ac  ethernet  --     
enp2s0               203037ce-37ee-4565-aa7a-790ebcfc49fe  ethernet  --

# You can delete a connection using nmcli:
[root@ctrl ~]# nmcli con delete cafe
Connection 'cafe' (3901da63-db82-4078-81a4-2e69505f5e2a) successfully deleted.     
```

* You can optionally use NMTUI or nmtui for the graphical configuration to add, activate, and deactivate connections:
```
nmtui
```
