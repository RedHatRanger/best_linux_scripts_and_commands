Here’s how you can configure your `ansible.cfg` to specify a custom Galaxy server list and keep the API keys out of the config by using environment variables (which you set dynamically from your encrypted vault via the script):

---

### Step 1: Configure `ansible.cfg` with `server_list` and environment variable tokens

```ini
[galaxy]
server_list = my_galaxy

[galaxy_server.my_galaxy]
url = https://my.galaxy.server/api/
token = ${MY_GALAXY_API_TOKEN}
```

- `server_list` defines the named servers you want to use.
- Each server section uses `token = ${ENV_VAR}` syntax to pull the token from an environment variable instead of hardcoding it.

---

### Step 2: Keep your API tokens encrypted in `vault.yml`

```yaml
galaxy_api_token: "your_actual_api_token_here"
```

Encrypt it with:

```bash
ansible-vault encrypt vault.yml
```

---

### Step 3: Use a wrapper script to decrypt and export the token before running ansible-galaxy

Example `install_collections.sh`:

```bash
#!/bin/bash

# Decrypt vault file and extract token using yq
GALAXY_TOKEN=$(ansible-vault view vault.yml | yq '.galaxy_api_token' -r)

# Export token as environment variable expected by ansible.cfg
export MY_GALAXY_API_TOKEN="$GALAXY_TOKEN"

# Run collection install with ansible-galaxy
ansible-galaxy collection install -r requirements.yml --force
```

Make sure this script is executable:

```bash
chmod +x install_collections.sh
```

Run it instead of calling `ansible-galaxy` directly:

```bash
./install_collections.sh
```

---

### Why this is good practice

- Your API token is **never stored in plain text** in `ansible.cfg`.
- The token is **only decrypted in memory** during the script execution.
- You can safely commit `ansible.cfg` and `requirements.yml` to version control without exposing secrets.
- You can extend this pattern for multiple Galaxy servers by adding more tokens and environment variables.

# Controlling where the collections are installed
You can control where Ansible installs collections by specifying the **collections path**. There are a few ways to do this:

---

### 1. Set `collections_paths` in `ansible.cfg`

Add this under the `[defaults]` section in your `ansible.cfg`:

```ini
[defaults]
collections_paths = /path/to/custom/collections:/another/path
```

- Ansible will look for collections in these directories in order.
- When installing collections with `ansible-galaxy collection install`, it will install into the **first writable path** listed here.
- If the directory doesn’t exist, Ansible will create it.

# Using Ansible-Navigator to containerize collections:
To get collections and Python libraries installed **inside your Execution Environment (container image)** for use with `ansible-navigator` or Ansible Automation Platform, you typically build a custom EE image using **`ansible-builder`**.

Here’s how to do it step-by-step:

---

### 1. Create a `requirements.yml` for your Ansible collections

Example `requirements.yml`:

```yaml
---
collections:
  - name: ansible.posix
  - name: community.general
  - name: cisco.ios
```

---

### 2. Create a `requirements.txt` for your Python libraries (if any)

Example `requirements.txt`:

```
netaddr
pyyaml
requests
```

---

### 3. Create an `execution-environment.yml` file to define your EE build

Example `execution-environment.yml`:

```yaml
version: 1

dependencies:
  galaxy: requirements.yml
  python: requirements.txt
```

This tells `ansible-builder` to install the listed collections and Python packages inside the EE.

---

### 4. Build the Execution Environment image

Run this command in the directory with your files:

```bash
ansible-builder build -t my-custom-ee:latest
```

This will create a container image named `my-custom-ee:latest` with your collections and Python libraries installed.

---

### 5. Use your custom EE with `ansible-navigator`

In your `ansible-navigator.yml` or via CLI, specify your custom EE image:

```yaml
execution-environment:
  enabled: true
  image: my-custom-ee:latest
```

Or run directly:

```bash
ansible-navigator run playbook.yml --ee-image my-custom-ee:latest
```

---

### Summary

- Use `requirements.yml` for collections.
- Use `requirements.txt` for Python packages.
- Define both in `execution-environment.yml`.
- Build with `ansible-builder`.
- Use the resulting image with `ansible-navigator` or AAP.


---

Here are all three files with explanations to help you build your custom Execution Environment for Cisco device automation on RHEL 8 UBI8 base.

---

### 1. `execution-environment.yml`

```yaml
---
# Defines the Execution Environment build configuration

version: 1

# Base image: Red Hat Universal Base Image 8 (UBI8)
base_image: registry.access.redhat.com/ubi8/ubi

dependencies:
  # Python packages to install inside the EE
  python: requirements.txt

  # Ansible collections to install inside the EE
  galaxy: requirements.yml

additional_build_steps:
  prepend:
    # Install system packages needed to build Python dependencies
    - microdnf install -y gcc libffi-devel openssl-devel
    - microdnf clean all
```

**Explanation:**  
This file tells `ansible-builder` to start from the UBI8 base image, install Python packages listed in `requirements.txt`, and Ansible collections listed in `requirements.yml`. It also installs essential system libraries needed to compile Python packages like `netmiko` or `napalm`.

---

### 2. `requirements.txt`

```text
# Python libraries required for Cisco device automation

netmiko
napalm
paramiko
pyyaml
requests
```

**Explanation:**  
This file lists Python packages your EE needs. These libraries provide SSH connectivity, device drivers, YAML parsing, and HTTP requests support commonly used in network automation.

---

### 3. `requirements.yml`

```yaml
---
# Ansible collections for Cisco device automation and networking

collections:
  - name: cisco.ios
  - name: cisco.iosxr
  - name: cisco.nxos
  - name: cisco.asa
  - name: ansible.netcommon
  - name: community.network
  - name: community.general
```

**Explanation:**  
This file lists the Ansible collections to be installed inside the EE. It includes collections for various Cisco platforms (IOS, IOS-XR, NX-OS, ASA), plus common networking and general utility collections.

---

### Next Steps

1. Place these three files in the same directory.
2. Run the build command to create your custom EE image:

```bash
ansible-builder build -t my-custom-ee:latest
```

3. Use the image with `ansible-navigator` by specifying it in your config or CLI:

```bash
ansible-navigator run playbook.yml --ee-image my-custom-ee:latest
```

Here are all three files with explanations to help you build your custom Execution Environment for Cisco device automation on RHEL 8 UBI8 base.

---

### 1. `execution-environment.yml`

```yaml
---
# Defines the Execution Environment build configuration

version: 1

# Base image: Red Hat Universal Base Image 8 (UBI8)
base_image: registry.access.redhat.com/ubi8/ubi

dependencies:
  # Python packages to install inside the EE
  python: requirements.txt

  # Ansible collections to install inside the EE
  galaxy: requirements.yml

additional_build_steps:
  prepend:
    # Install system packages needed to build Python dependencies
    - microdnf install -y gcc libffi-devel openssl-devel
    - microdnf clean all
```

**Explanation:**  
This file tells `ansible-builder` to start from the UBI8 base image, install Python packages listed in `requirements.txt`, and Ansible collections listed in `requirements.yml`. It also installs essential system libraries needed to compile Python packages like `netmiko` or `napalm`.

---

### 2. `requirements.txt`

```text
# Python libraries required for Cisco device automation

netmiko
napalm
paramiko
pyyaml
requests
```

**Explanation:**  
This file lists Python packages your EE needs. These libraries provide SSH connectivity, device drivers, YAML parsing, and HTTP requests support commonly used in network automation.

---

### 3. `requirements.yml`

```yaml
---
# Ansible collections for Cisco device automation and networking

collections:
  - name: cisco.ios
  - name: cisco.iosxr
  - name: cisco.nxos
  - name: cisco.asa
  - name: ansible.netcommon
  - name: community.network
  - name: community.general
```

**Explanation:**  
This file lists the Ansible collections to be installed inside the EE. It includes collections for various Cisco platforms (IOS, IOS-XR, NX-OS, ASA), plus common networking and general utility collections.

---

### Next Steps

1. Place these three files in the same directory.
2. Run the build command to create your custom EE image:

```bash
ansible-builder build -t my-custom-ee:latest
```

3. Use the image with `ansible-navigator` by specifying it in your config or CLI:

```bash
ansible-navigator run playbook.yml --ee-image my-custom-ee:latest
```