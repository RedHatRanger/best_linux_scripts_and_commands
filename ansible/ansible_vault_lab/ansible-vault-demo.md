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

```bash
ansible_vault_lab/
├── ansible.cfg
├── encrypted_vars
│   ├── nunya.yml
│   └── zabbix.yml
├── keyfile.txt
├── roles
│   └── vault_role
│       ├── tasks
│       │   └── main.yml
│       └── templates
│           └── template.j2
├── vault_test_roles.yml
└── vault_test.yml
```

Create the directories with the following commands:

```bash
mkdir -p ansible_vault_lab/encrypted_vars
cd ansible_vault_lab/encrypted_vars
```

### 2.3. Create the Unencrypted Data Files

Create a YAML file named `nunya.yml` inside the `encrypted_vars/` directory with the following content. This file contains the sensitive data that we want to encrypt.

```yaml
cat << EOF > nunya.yml
# nunya.yml (unencrypted)
---
api_key: "GOOGLE-API-1234-ZEBRA-LOL-5678"
cisco:
  username: "cisco_admin"
  password: "RoleTide1"
crypto_wallet_passports: "moose-unicorn-dragon@zebrabank"
credit_card:
  number: "4111 1111 1111 1111"
  expire_date: "12/34"
  cvv: "123"
  name_on_card: "John Doe"
EOF
```

Create another YAML file named `zabbix.yml` with content specific to a Zabbix monitoring environment:

```yaml
cat << EOF > zabbix.yml
# zabbix.yml (unencrypted)
---
zabbix_api_key: "ZBX-API-KEY-PURPLE-PENGUIN-9876"
cisco_service_account: "Penguin_admin"
cisco_service_password: "P3ngu1nsRul3!"
EOF
```

### 2.4. Create the Vault Password File

Create a file named `keyfile.txt` in the `ansible_vault_lab` directory. This file will contain the password for the vault.

```
cd ../
cat << EOF > keyfile.txt
WhenYouWishUponAStar3!
EOF
```

**Note:** In a real-world scenario, you should restrict the permissions of this file to prevent unauthorized access.

```bash
# For this demonstration, we will give 660 permission so the owner and the group will have Read and Write Access to the File
chmod 660 keyfile.txt
```

### 2.5. Configure `ansible.cfg` for Vault Password File

To avoid repeatedly specifying the `--vault-password-file` option with every `ansible-vault` command, you can configure Ansible to automatically use a vault password file by creating an `ansible.cfg` file in your project directory. This file will tell Ansible where to find the vault password.

Create a file named `ansible.cfg` in the `ansible_vault_lab` directory with the following content:

```ini

cat << EOF > ansible.cfg
# ansible.cfg - Global config for Ansible

[defaults]
vault_password_file = ./keyfile.txt
EOF
```

This configuration tells Ansible to look for the vault password in `keyfile.txt` located in the same directory as the `ansible.cfg` file.

### 2.6. Create a Test Playbook to Use Vault Variables

Create a playbook named `vault_test.yml` in the root of the lab directory:

```yaml
cat << EOF > vault_test.yml
# vault_test.yml
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
        msg: "API Key: {{ api_key }}"

    - name: Print crypto_wallet_passports
      debug:
        msg: "Crypto Wallets: {{ crypto_wallet_passports }}"

    - name: Print masked credit card info
      debug:
        msg: |
          FAKE Credit Card \#: {{ credit_card.number }}
          Cardholder: {{ credit_card.name_on_card }}

    - name: Print Zabbix API key
      debug:
        msg: "Zabbix API Key: {{ zabbix_api_key }}"

    - name: Print switch service account
      debug:
        msg: |
          Switch Service Account: {{ cisco_service_account }}
          Service Account Password: {{ cisco_service_password }}
EOF
```

## 3. Encrypting Data with Ansible Vault

Now, we will encrypt the `nunya.yml` and `zabbix.yml` files using `ansible-vault encrypt`.

```bash
ansible-vault encrypt encrypted_vars/nunya.yml encrypted_vars/zabbix.yml
```

After running these commands, the content of both files will be encrypted.

* Done!

---

## 4. Working with Encrypted Files

Ansible Vault provides several commands to work with encrypted files.

### 4.1. Viewing Encrypted Files

```bash
ansible-vault view nunya.yml
```

### 4.2. Editing Encrypted Files

```bash
ansible-vault edit nunya.yml
```

### 4.3. Decrypting Files

```bash
ansible-vault decrypt nunya.yml
```

---

# 5. Create the Role to Render Encrypted Data (BEST OPTION)

### 5.1. Create the Role Directory Structure

```bash
ansible_vault_lab/
└── roles/
    └── vault_role/
        ├── tasks/
        │   └── main.yml
        └── templates/
            └── template.j2
```

### 5.2. `roles/vault_role/tasks/main.yml`

```yaml
---
- name: Render sensitive data template
  template:
    src: template.j2
    dest: "/tmp/sensitive_data_output.txt"
  vars:
    api_key: "{{ api_key }}"
    username: "{{ username }}"
    crypto_wallet_passports: "{{ crypto_wallet_passports }}"
    cc_info: "{{ cc_info }}"
    zabbix_api_key: "{{ zabbix_api_key }}"
    switch_service_account: "{{ switch_service_account }}"
    switch_service_password: "{{ switch_service_password }}"
```

### 5.3. `roles/vault_role/templates/template.j2`

```jinja
# Template for rendering encrypted variables

API Key: {{ api_key }}
Username: {{ username }}
Crypto Wallet Passports: {{ crypto_wallet_passports }}
Card ending in: **** **** **** {{ cc_info.number[-4:] }}
Zabbix API Key: {{ zabbix_api_key }}
Switch SA: {{ switch_service_account }} / {{ switch_service_password }}
```

## 6. Create the Final Playbook

### 6.1. `vault_test_roles.yml`

```yaml
---
- name: Test encrypted variables with role
  hosts: localhost
  gather_facts: false

  vars_files:
    - encrypted_vars/nunya.yml
    - encrypted_vars/zabbix.yml

  roles:
    - vault_role
```

## 7. Run the Playbook

Now you can run the playbook with:

```bash
ansible-playbook vault_test_roles.yml
```

Ansible will decrypt the variables from the `nunya.yml` and `zabbix.yml` files and pass them to the Jinja2 template in the `vault_role` to render the output to `/tmp/sensitive_data_output.txt`.

## 8. Review the Output

After the playbook runs successfully, you can review the rendered file at `/tmp/sensitive_data_output.txt` to ensure that everything is processed correctly.
