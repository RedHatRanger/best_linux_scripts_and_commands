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