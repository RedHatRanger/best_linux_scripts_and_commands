# RHEL 8 Execution Environment Lab Setup and Usage

This guide demonstrates how to run Ansible playbooks inside a RHEL 8–based Execution Environment (EE) container, pulled from Private Automation Hub (PAH) or Red Hat registry, using Podman and Ansible Navigator.

---

## 1. Introduction

RHEL 9 introduces stricter OpenSSH defaults which can break legacy network device support (e.g., older Cisco switches). By using a RHEL 8 EE, you ensure compatibility with older crypto algorithms and still leverage a supported containerized environment for Ansible automation.

---

## 2. Prerequisites

- Control node running RHEL 9
- Podman installed (`sudo dnf install -y podman`)
- Ansible Navigator (optional) installed (`sudo dnf install -y ansible-navigator`)
- PAH URL or Red Hat registry credentials
- Local user or root privileges for container operations

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
└── execution-environment.yml  
# ansible-builder definition (optional)
```

```
mkdir -p ee_lab/{inventories,playbooks}

cd ee_lab
```

---

4. Configure Ansible

Create an `ansible.cfg` file:
```
[defaults]
inventory = ./inventories/hosts
# If using Ansible CLI directly (not Navigator):
# stdout_callback = yaml

[execution_environment]
# Use Podman as container engine
container_engine = podman
eei = pah.example.com/ansible-automation-platform/ee-supported-rhel8:latest
```