# Pi-hole Deployment Guide for Podman on CachyOS / Arch Linux

This comprehensive guide covers the end-to-end setup of the official Pi-hole container using **Podman** and **podman-compose** on **CachyOS** (Arch Linux base). It handles critical configurations including rootless networking, freeing up host port 53, timezone configuration, and persistent volumes.
## Technical Prerequisites & System Prep
Before running the container, CachyOS needs specific adjustments. By default, standard Linux systems restrict rootless users from binding to ports below 1024, and network resolution services usually occupy DNS port 53.
### 1. Free Up Port 53 on the Host
CachyOS typically utilizes systemd-resolved or NetworkManager, which binds to port 53. This will cause a conflict when Pi-hole tries to listen for DNS traffic.
 1. Check if port 53 is currently occupied:
   ```bash
   sudo ss -tulnp | grep :53
   
   ```
 2. If systemd-resolved is holding the port, disable its stub listener by editing /etc/systemd/resolved.conf:
   ```bash
   sudo nano /etc/systemd/resolved.conf
   
   ```
 3. Ensure or add the following line inside the [Resolve] section:
   ```ini
   DNSStubListener=no
   
   ```
 4. Create a symlink to ensure your local resolution switches over to the proper runtime file, then restart the network resolution service:
   ```bash
   sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
   sudo systemctl restart systemd-resolved
   
   ```
### 2. Enable Rootless Podman Port Bindings
To run Pi-hole safely as an unprivileged, rootless user (highly recommended), lower the unprivileged port threshold to 53 so Podman can map the DNS server ports without requiring sudo container invocation.
 1. Adjust the sysctl threshold for the active session:
   ```bash
   sudo sysctl net.ipv4.ip_unprivileged_port_start=53
   
   ```
 2. Persist this setting across reboots by saving it to a system configuration file:
   ```bash
   echo "net.ipv4.ip_unprivileged_port_start=53" | sudo tee /etc/sysctl.d/99-podman-pihole.conf
   
   ```
### 3. Install Podman Compose
Ensure the compose orchestrator tool is installed on your CachyOS system:
```bash
sudo pacman -S podman-compose

```
## Compose Configuration (docker-compose.yml)
Create a clean directory for your configuration, navigate into it, and save the block below as docker-compose.yml.
This setup configuration locks down your requested parameters:
 * **Timezone:** America/Chicago (Central Time)
 * **Web Admin Password:** redhat
 * **Local Loopback Overrides:** Addressed via FTLCONF_LOCAL_IPV4 to bypass loop loops inherent to some rootless container engine environments.
```yaml
version: "3"

services:
  pihole:
    container_name: pihole
    image: docker.io/pihole/pihole:latest
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "8080:80/tcp"
    environment:
      TZ: 'America/Chicago'
      WEBPASSWORD: 'redhat'
      FTLCONF_LOCAL_IPV4: '127.0.0.1'
    volumes:
      - 'pihole_config:/etc/pihole'
      - 'dnsmasq_config:/etc/dnsmasq.d'
    restart: unless-stopped

volumes:
  pihole_config:
  dnsmasq_config:

```
## Deployment and Lifecycle Commands
Execute these deployment commands in the same directory where your docker-compose.yml file is saved.
### Launch / Update the Deployment
If you are starting the container for the first time or updating environment variables (like a password or timezone change), pull down old contexts and instantiate the fresh layer:
```bash
# Tear down any running context
podman-compose down

# Spin up the infrastructure in detached background mode
podman-compose up -d

```
### Verification Checks
 1. Verify that the container runtime status reads healthy/active:
   ```bash
   podman ps
   
   ```
 2. Confirm that the timezone variable accurately initialized the internal environment to Central Time:
   ```bash
   podman exec -it pihole date
   
   ```
   *Expected output: The current time stamped with a CST or CDT zone marker.*
## Post-Installation Access
 1. **Admin Dashboard Login:** Open your web browser and target your local interface:
   * **URL:** http://localhost:8080/admin
   * **Password:** redhat
 2. **Network Integration:** To route your system's traffic or entire network through this engine, update the primary DNS server entry inside your CachyOS NetworkManager configurations (or router settings) to map directly to loopback (127.0.0.1) or the local IP address of your CachyOS system.
