# RHEL 8 Execution Environment Lab Setup and Usage

This guide demonstrates how to run Ansible playbooks inside a RHEL 8–based Execution Environment (EE) container, pulled from Private Automation Hub (PAH) or Red Hat registry, using Podman and Ansible Navigator.

---

## 1. Introduction

RHEL 9 introduces stricter OpenSSH defaults which can break legacy network device support (e.g., older Cisco switches). By using a **RHEL 8 EE**, you ensure compatibility with older crypto algorithms and still leverage a supported containerized environment for Ansible automation.

---

## 2. Prerequisites

* **Control node** running RHEL 9
* **Podman** installed (`sudo dnf install -y podman`)
* **Ansible Navigator** (optional) installed (`sudo dnf install -y ansible-navigator`)
* **PAH URL** or Red Hat registry credentials
* Local user or root privileges for container operations

---

## 3. Directory Structure

Create a project directory:

```
ee_lab/
├── ansible.cfg         # Ansible config pointing to inventory and EE
├── inventories/
│   └── hosts           # Inventory file
├── playbooks/
│   └── site.yml        # Sample playbook
└── execution-environment.yml  # ansible-builder definition (optional)
```

```bash
mkdir -p ee_lab/{inventories,playbooks}
cd ee_lab
```

---

## 4. Configure Ansible

Create `ansible.cfg`:

```ini
[defaults]
inventory = ./inventories/hosts
# If using Ansible CLI directly (not Navigator):
# stdout_callback = yaml

[execution_environment]
# Use Podman as container engine
container_engine = podman
eei = pah.example.com/ansible-automation-platform/ee-supported-rhel8:latest
```

---

## 5. Inventory File

`inventories/hosts`:

```ini
[local]
localhost ansible_connection=local
```

For network devices, add groups and host entries:

```ini
[cisco]
switch1 ansible_host=192.168.1.10 ansible_user=admin
```

---

## 6. Sample Playbook

`playbooks/site.yml`:

```yaml
---
- name: Test RHEL8 EE in container
  hosts: local
  gather_facts: false
  tasks:
    - name: Show Python version inside EE
      ansible.builtin.command: python3 --version
      register: pyv
    - debug:
        msg: "EE Python: {{ pyv.stdout }}"

- name: Configure Cisco Switch (legacy SSH)
  hosts: cisco
  gather_facts: false
  connection: network_cli
  collections:
    - cisco.ios
  tasks:
    - name: Ensure interface status
      cisco.ios.ios_interface:
        name: GigabitEthernet1
        enabled: true
```

---

## 7. Pulling the EE Image

### 7.1. Login to PAH

```bash
podman login pah.example.com
```

Use SSO or service-account token.

### 7.2. Pull the RHEL 8 EE

```bash
podman pull pah.example.com/ansible-automation-platform/ee-supported-rhel8:latest
```

If using Red Hat registry:

```bash
podman login registry.redhat.io
podman pull registry.redhat.io/ansible-automation-platform/ee-supported-rhel8:latest
```

---

## 8. Running Playbooks

### 8.1. With `ansible-playbook`

```bash
ansible-playbook playbooks/site.yml --eei pah.example.com/ansible-automation-platform/ee-supported-rhel8:latest
```

### 8.2. With `ansible-navigator`

```bash
ansible-navigator run playbooks/site.yml --execution-environment true
```

> Navigator reads `ansible.cfg` and uses `eei` setting by default.

---

## 9. Rootless vs. Rootful Containers

| Mode     | Setup Requirement                                     | Notes                                  |
| -------- | ----------------------------------------------------- | -------------------------------------- |
| Rootless | Local user with `/etc/subuid` & `/etc/subgid` entries | More secure; each user isolated        |
| Rootful  | `sudo podman pull` / `sudo podman run`                | Simpler for CI; shared container store |

---

## 10. Optional: Custom EE via `ansible-builder`

`execution-environment.yml`:

```yaml
version: 1

dependencies:
  python:
    - netmiko
    - paramiko
  galaxy:
    collections:
      - cisco.ios
      - cisco.nxos

images:
  base_image:
    name: pah.example.com/ansible-automation-platform/ee-supported-rhel8:latest
```

Build it:

```bash
ansible-builder build --tag custom-rhel8-ee -f execution-environment.yml
```

---

## 11. Verification & Cleanup

* Verify image exists:

  ```bash
  podman images | grep ee-supported-rhel8
  ```
* Remove containers/images when done:

  ```bash
  podman rmi pah.example.com/ansible-automation-platform/ee-supported-rhel8:latest
  ```

---

### 🚀 Next Steps

* Extend the playbook with more network modules
* Push custom EE to your PAH for team usage
* Automate builds via CI/CD pipeline

Enjoy your containerized Ansible lab on RHEL 8! 🎉
