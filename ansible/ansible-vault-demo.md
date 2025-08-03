# Ansible Vault Lab Setup and Usage

This document provides a step-by-step guide to setting up and using Ansible Vault to encrypt and manage sensitive data on **Red Hat Enterprise Linux 9 (RHEL 9)**.

## 1. Introduction to Ansible Vault

Ansible Vault is a feature of Ansible that allows you to keep sensitive data such as passwords, API keys, and private keys in encrypted files, rather than as plaintext in your playbooks or roles. These encrypted files can then be used in your Ansible playbooks, and Ansible will automatically decrypt them at runtime when needed.

## 2. Lab Setup

This section details the steps to set up the lab environment.

### 2.1. Install Ansible

First, you need to have Ansible installed. On a RHEL 9 system, you can install it using the following commands:

```bash
sudo dnf install -y ansible
```

To verify the installation, you can run:

```bash
ansible --version
```

### 2.2. Create the Directory Structure

For this lab, we will use the following directory structure:

```
ansible_vault_lab/
├── ansible.cfg
├── encrypted_vars/
│   ├── nunya.yml
│   └── zabbix.yml
├── keyfile.txt
└── vault_test.yml
```

Create the directories with the following commands:

```bash
mkdir -p ansible_vault_lab/encrypted_vars
```

### 2.3. Create the Unencrypted Data Files

Create a YAML file named `nunya.yml` inside the `encrypted_vars/` directory with the following content. This file contains the sensitive data that we want to encrypt.

```yaml
# nunya.yml (unencrypted)
---
api_key: "GOOGLE-API-1234-ZEBRA-LOL-5678"
username: "cisco_admin"
crypto_wallet_passports: "moose-unicorn-dragon@zebrabank"
credit_card:
  number: "4111 1111 1111 1111"
  expiry: "12/34"
  cvv: "123"
  name_on_card: "John Doe"
```

Create another YAML file named `zabbix.yml` with content specific to a Zabbix monitoring environment:

```yaml
# zabbix.yml (unencrypted)

zabbix_api_key: "ZBX-API-KEY-PURPLE-PENGUIN-9876"
cisco_service_account: "Penguin_admin"
cisco_service_password: "P3ngu1nsRul3!"
```

### 2.4. Create the Vault Password File

Create a file named `keyfile.txt` in the `ansible_vault_lab` directory. This file will contain the password for the vault.

```
super_secret_vault_password_123
```

**Note:** In a real-world scenario, you should restrict the permissions of this file to prevent unauthorized access.

```bash
chmod 600 ansible_vault_lab/keyfile.txt
```

### 2.5. Configure `ansible.cfg` for Vault Password File

To avoid repeatedly specifying the `--vault-password-file` option with every `ansible-vault` command, you can configure Ansible to automatically use a vault password file by creating an `ansible.cfg` file in your project directory. This file will tell Ansible where to find the vault password.

Create a file named `ansible.cfg` in the `ansible_vault_lab` directory with the following content:

```ini
[defaults]
vault_password_file = ./keyfile.txt
```

This configuration tells Ansible to look for the vault password in `keyfile.txt` located in the same directory as the `ansible.cfg` file.

### 2.6. Create a Test Playbook to Use Vault Variables

Create a playbook named `vault_test.yml` in the root of the lab directory:

```yaml
---
- name: Test encrypted variables
  hosts: localhost
  gather_facts: false

  vars_files:
    - encrypted_vars/nunya.yml
    - encrypted_vars/zabbix.yml

  tasks:
    - name: Print funny Google API key
      debug:
        msg: "API Key: {{ api_key }} | Username: {{ username }}"

    - name: Print crypto_wallet_passports
      debug:
        msg: "Crypto Wallets: {{ crypto_wallet_passports }}"

    - name: Print masked credit card info
      debug:
        msg: "Card ending in: **** **** **** {{ cc_info.number[-4:] }}"

    - name: Print Zabbix API key
      debug:
        msg: "Zabbix API Key: {{ zabbix_api_key }}"

    - name: Print switch service account
      debug:
        msg: "Switch SA: {{ switch_service_account }} / {{ switch_service_password }}"
```

## 3. Encrypting Data with Ansible Vault

Now, we will encrypt the `nunya.yml` and `zabbix.yml` files using `ansible-vault encrypt`.

```bash
ansible-vault encrypt ansible_vault_lab/encrypted_vars/nunya.yml
ansible-vault encrypt ansible_vault_lab/encrypted_vars/zabbix.yml
```

After running these commands, the content of both files will be encrypted.

## 4. Working with Encrypted Files

Ansible Vault provides several commands to work with encrypted files.

### 4.1. Viewing Encrypted Files

```bash
ansible-vault view ansible_vault_lab/encrypted_vars/nunya.yml
ansible-vault view ansible_vault_lab/encrypted_vars/zabbix.yml
```

### 4.2. Editing Encrypted Files

```bash
ansible-vault edit ansible_vault_lab/encrypted_vars/nunya.yml
ansible-vault edit ansible_vault_lab/encrypted_vars/zabbix.yml
```

### 4.3. Decrypting Files

```bash
ansible-vault decrypt ansible_vault_lab/encrypted_vars/nunya.yml
ansible-vault decrypt ansible_vault_lab/encrypted_vars/zabbix.yml
```

### 4.4. Changing the Vault Password (Rekey)

```bash
echo "another_super_secret_password_456" > new_keyfile.txt
ansible-vault rekey ansible_vault_lab/encrypted_vars/nunya.yml --new-vault-password-file new_keyfile.txt
ansible-vault rekey ansible_vault_lab/encrypted_vars/zabbix.yml --new-vault-password-file new_keyfile.txt
```

## 5. Conclusion

This lab has demonstrated the basic workflow of using Ansible Vault to secure sensitive data. By using a vault password file and `ansible.cfg`, you can streamline secret management securely and repeatably.

## 6. [Link](https://docs.ansible.com/ansible/2.8/user_guide/vault.html) to the Official Ansible-Vault Documentation.\

[Rootless Podman](https://developers.redhat.com/blog/2020/09/25/rootless-containers-with-podman-the-basics#)

