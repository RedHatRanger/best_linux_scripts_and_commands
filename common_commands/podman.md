[See this other lab for more practice](https://github.com/RedHatRanger/rhcsa9vagrant/blob/main/rhcsa-practice-questions/21_container_service.md)

* First install the required packages (as root):
```bash
yum install @"Container Management"
```

* TO ALLOW ROOTLESS PODMAN (as root):
```bash
# Create the file if it doesn't exist, then add the information
touch /etc/sysctl.d/99-sysctl.conf
echo "user.max_user_namespaces=100000" >> /etc/sysctl.d/99-sysctl.conf

# Rebuild sysctl profile
sysctl -a

# Add the user (in this case it is `testuser`) to /etc/subuid and /etc/subgid
usermod --add-subuids 100000-165535 --add-subgids 100000-165535 testuser

# Enable linger:
loginctl enable-linger testuser
```

* Then, try to podman pull rockylinux for example (as the testuser):
```
ssh testuser@localhost
podman pull rockylinux:latest
podman images  # fetches the image_id
podman run -it --name rocky --hostname rockylinux <image_id>
```

* To remove the container (as the testuser):
```
podman rm rocky
```

* To add software to the pod and backup for exporting it (as the testuser):
```
podman rm rocky
podman run -it --name rocky --hostname rockylinux <image_id>
yum install ansible-core -y

# HIT CTRL+p then CTRL+q to exit the container but keep it running in the background
podman ps  # fetch the CONTAINER ID

# Export the container to a file:
podman commit <CONTAINER_ID> > "rockylinux.tar"
```

* To get back into the container (as the testuser):
```
podman attach <CONTAINER_ID>
```
