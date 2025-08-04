# Ansible Vault Lab Setup and Usage

This `ansible-vault` lab provides a hands-on walkthrough for securely managing sensitive data such as:
- API keys
- Credentials
- Secrets

By the end of this lab, you will:

* Understand the purpose and use cases of Ansible Vault
* Create encrypted YAML files for storing and managing sensitive data
* Integrate encrypted variables into playbooks and roles
* Render and manage secret data using Ansible templates

This is a strong security practice for DevOps and IT professionals who need to ensure sensitive automation data is not exposed in version control systems (GitLab) or logs (Splunk).

---

## 1. Introduction to Ansible Vault

Ansible Vault allows users to **encrypt entire files or individual variables** in Ansible projects. This ensures that sensitive data such as:

* Passwords
* API tokens
* Certificates
* SSH keys

...can be stored securely in source control while still being accessible to Ansible at runtime (when decrypted).

Vault files are encrypted using a password, and Ansible supports automatic decryption using a configured password file.

---

## 2. Lab Setup

Follow these steps to build the lab environment.

### 2.1. Install Ansible

```bash
sudo dnf install -y ansible
ansible --version
```

### 2.2. Create Directory Structure

```bash
mkdir -p ansible_vault_lab/encrypted_vars
cd ansible_vault_lab/encrypted_vars
```

Structure overview:

```bash
ansible_vault_lab/
├── ansible.cfg
├── encrypted_vars
│   ├── nunya.yml
│   └── zabbix.yml
├── keyfile.txt
├── roles
│   └── vault_role
│       ├── tasks
│       │   └── main.yml
│       └── templates
│           └── template.j2
├── vault_roles.yml
└── vault_test.yml
```

### 2.3. Create Sensitive Data Files (Unencrypted)

```bash
cat << EOF > nunya.yml
# nunya.yml (unencrypted)
---
google:
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

cat << EOF > zabbix.yml
# zabbix.yml (unencrypted)
---
zabbix:
  api_key: "ZBX-API-KEY-PURPLE-PENGUIN-9876"
cisco_service_account: "Penguin_admin"
cisco_service_password: "P3ngu1nsRul3!"
EOF
```

### 2.4. Create a Vault Password File

```bash
cd ../
cat << EOF > keyfile.txt
WhenYouWishUponAStar3!
EOF
chmod 660 keyfile.txt
```

### 2.5. Configure Ansible to Use Vault Password

```bash
cat << EOF > ansible.cfg
[defaults]
vault_password_file = ./keyfile.txt
EOF
```

---

### 2.6. Create a Test Playbook

```bash
cat << EOF > vault_test.yml
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
          FAKE Credit Card #: {{ credit_card.number }}
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

---

## 3. Encrypt the Data Files

```bash
ansible-vault encrypt encrypted_vars/nunya.yml encrypted_vars/zabbix.yml
```

---

## 4. Vault File Management

### View:

```bash
ansible-vault view encrypted_vars/nunya.yml
```

### Edit:

```bash
ansible-vault edit encrypted_vars/nunya.yml
```

### Decrypt:

```bash
ansible-vault decrypt encrypted_vars/nunya.yml
```

---

# 5. Create the Role to Render Encrypted Data

### 5.1. Role Directory

```bash
mkdir -p roles/vault_role/{tasks,templates}
```

### 5.2. Role Task File: `roles/vault_role/tasks/main.yml`

```yaml
- name: Render sensitive data template
  template:
    src: template.j2
    dest: "/tmp/sensitive_data_output.txt"
```

### 5.3. Template File: `roles/vault_role/templates/template.j2`

```jinja
# Rendered Secrets Output

API Key: {{ api_key }}
Username: {{ cisco.username }}
Crypto Wallet Passports: {{ crypto_wallet_passports }}
Card ending in: **** **** **** {{ credit_card.number[-4:] }}
Zabbix API Key: {{ zabbix_api_key }}
Switch SA: {{ cisco_service_account }} / {{ cisco_service_password }}
```

---

## 6. Final Playbook to Call Role: `vault_roles.yml`

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

---

## 7. Run the Playbook

```bash
ansible-playbook vault_roles.yml
```

---

## Summary

You now have a complete lab that:

* Uses **Ansible Vault** to encrypt/decrypt YAML variable files
* Integrates secrets into **Ansible roles**
* Outputs decrypted data securely via templates

This workflow mirrors real-world practicality for managing secrets securely in Ansible automation. 
For more, see the [Ansible Vault documentation](https://docs.ansible.com/ansible/latest/user_guide/vault.html).
