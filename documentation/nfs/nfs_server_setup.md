# Installation and Configuration Steps:
## Install the Package
Use the dnf package manager to install nfs-utils.

```bash
sudo dnf install nfs-utils
```

## Enable and Start Services
After installation, you must enable and start the required services. The nfs-server service handles the core NFS protocol, while rpcbind is a dependency that manages RPC program-to-port number mapping. You can start both with a single command.

```bash
sudo systemctl enable --now nfs-server rpcbind
```

## Configure the Firewall
By default, firewalld on RHEL 9 blocks incoming connections. You need to explicitly allow NFS traffic.

```bash
sudo firewall-cmd --permanent --add-service=nfs
sudo firewall-cmd --reload
```

## Export a Directory
Edit the /etc/exports file to define which directories you want to share and with which clients. 
For example, to share a directory named /data are with a specific IP address 192.168.1.10, 
you would add the following line to the file:

### Sample Configuration
```bash
/data 192.168.1.10(rw,sync,no_root_squash)
```

>rw: Allows read and write access.
>sync: Ensures that changes are written to disk before the server responds to a request.
>no_root_squash: Allows the root user on the client to have root-level privileges on the NFS share. Use this option with caution.

## Apply Exports
After saving the /etc/exports file, apply the changes without restarting the services.

```bash
sudo exportfs -avr
```