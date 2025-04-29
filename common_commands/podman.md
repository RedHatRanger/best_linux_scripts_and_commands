[Why Use Containers?](#Containers101)

[See this other lab for more practice](https://github.com/RedHatRanger/rhcsa9vagrant/blob/main/rhcsa-practice-questions/21_container_service.md)
<br><br>

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


---

<br><br><br><br>

# Containers101

# Rootless Containers with Podman: The Basics

As a developer, you have probably heard a lot about containers. A container is a unit of software that provides a packaging mechanism that abstracts the code and all of its dependencies to make application builds fast and reliable. An easy way to experiment with containers is with the Pod Manager tool (Podman), which is a daemonless, open source, Linux-native tool that provides a command-line interface (CLI) similar to the Docker container engine.

In this document, we will:

- Explain the benefits of using containers and Podman
- Introduce rootless containers and their importance
- Show how to use rootless containers with Podman through a practical example

---

## 1. Why Containers?

Containers isolate your applications from the underlying computing environment. They bind application logic and dependencies into a single unit, enabling developers to focus on code rather than environment discrepancies. Operations teams benefit by managing application deployment without worrying about software versions or configuration.

Containers virtualize at the operating system (OS) level, making them lightweight compared to virtual machines (VMs), which virtualize at the hardware level. Key advantages:

- **Low hardware footprint**
- **Environment isolation**
- **Quick deployment**
- **Multiple environment deployments**
- **Reusability**

---

## 2. Why Podman?

Podman simplifies finding, running, building, sharing, and deploying OCI‑compatible containers and images. Its main advantages include:

- **Daemonless**: No central service is required, unlike Docker.
- **Layer control**: Fine‑grained management of image layers.
- **Fork/exec model**: Uses a direct process model rather than client/server.
- **Rootless support**: Run containers without requiring root privileges on the host.

---

## 3. Why Rootless Containers?

Rootless containers allow unprivileged users to create, run, and manage containers without admin rights. Benefits:

- **Enhanced security**: Compromised container daemons or runtimes do not yield host root access.
- **Multi‑user support**: Multiple users can run containers on the same host safely.
- **Nested isolation**: Run containers within containers without privilege escalation.

From a security standpoint, running with fewer privileges reduces risk. Podman achieves this by spawning container processes as child processes of the user, with no central daemon.

---

## 4. Example: Using Rootless Containers with Podman

### 4.1. System Requirements

- **RHEL Enterprise Linux (RHEL) 7.7** or greater

### 4.2. Configuration

1. **Install dependencies:

   ```bash
   sudo yum install slirp4netns podman -y
   # Or install the Container Tools module:
   sudo yum install @container-tools -y
   ```
   - `slirp4netns` provides network connectivity in an unprivileged user namespace.

3. **Create a non-root user** (e.g., `rhel`):‑root user** (e.g., `rhel`):

   ```bash
   sudo useradd -c "Red Hat" rhel
   sudo passwd rhel
   ```

This new user is automatically configured for rootless Podman.

### 4.3. Connect as the User

Instead of `su -`, connect using a direct login method:

```bash
ssh rhel@localhost
```

This preserves the environment variables needed for rootless Podman.

### 4.4. Pull a RHEL Image

1. **Pull the Universal Base Image (UBI)**:

   ```bash
   podman pull registry.access.rhel.com/ubi7/ubi
   ```

2. **Inspect the image**:

   ```bash
   podman run registry.access.rhel.com/ubi7/ubi cat /etc/os-release
   ```

3. **List local images**:

   ```bash
   podman images
   ```

> Note: Creating and running containers from these images can be covered in a follow‑up guide.

### 4.5. Verify Rootless Configuration

Check UID/GID mappings inside the user namespace:

```bash
podman unshare cat /proc/self/uid_map
```

This confirms that Podman is using subordinate user IDs without root.

---

## 5. Conclusion and Tips

- **Storage location**: Rootless container data resides under the user’s home (e.g., `$HOME/.local/share/containers/storage`).
- **Privilege isolation**: Containers run with expanded UIDs/GIDs inside the namespace but have no extra host privileges.
- **Security best practice**: Fewer privileges on the host reduce the attack surface in multi‑user environments.

Enjoy experimenting with rootless containers using Podman!

* If you need to create a persistent service for the sysctl settings:
```
[Unit]
Description=Custom sysctl overrides (after sysctl loads its config)
After=sysctl.service
Wants=sysctl.service
 
[Service]
Type=oneshot
ExecStart=/usr/sbin/sysctl -w user.max_user_namespaces=28633
ExecStart=/usr/sbin/sysctl -w net.ipv4.ip_unprivileged_port_start=443
 
[Install]
WantedBy=multi-user.target
```
OR
```
cat << EOF > /etc/sysctl.d/100-custom.conf
# allow more user namespaces
user.max_user_namespaces = 28633

# let unprivileged processes bind ports ≥ 443
net.ipv4.ip_unprivileged_port_start = 443
EOF

sed -i 's/user.max_user_namespaces = 28633/#user.max_user_namespaces = 28633/g' /etc/sysctl.d/99-sysctl.conf
```
