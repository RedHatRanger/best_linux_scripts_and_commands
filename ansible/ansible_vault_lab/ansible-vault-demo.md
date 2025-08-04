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
        msg: "API Key: {{ google.api_key }}"

    - name: Print crypto_wallet_passports
      debug:
        msg: "Crypto Wallets: {{ crypto_wallet_passports }}"

    - name: Print masked credit card info
      debug:
        msg:
          - "Cardholder: {{ credit_card.name_on_card }}"
          - "Credit Card#: {{ credit_card.number }}"
          - "Expiration: {{ credit_card.expire_date }}"

    - name: Print Zabbix API key
      debug:
        msg: "Zabbix API Key: {{ zabbix.api_key }}"

    - name: Print switch service account
      debug:
        msg:
          - "Switch Service Account: {{ cisco_service_account }}"
          - "Service Account Password: {{ cisco_service_password }}"
EOF
```

---

## 3. Encrypt the Data Files

```bash
ansible-vault encrypt encrypted_vars/nunya.yml encrypted_vars/zabbix.yml
```

---

## 4. Vault File Management (OPTIONAL)

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
cat << EOF > roles/vault_role/tasks/main.yml
# tasks file for vault_role
- name: Render sensitive data template to file
  template:
    src: template.j2
    dest: "/tmp/sensitive_data_output.txt"

- name: Read rendered content and print
  command: cat /tmp/sensitive_data_output.txt
  register: rendered_output

- name: Display rendered secrets
  debug:
    msg: "{{ rendered_output.stdout_lines }}"

- name: Remove temporary file
  file:
    path: "/tmp/sensitive_data_output.txt"
    state: absent
EOF
```

### 5.3. Template File: `roles/vault_role/templates/template.j2`

```yaml
cat << EOF > roles/vault_role/templates/template.j2
# Rendered Secrets Output

Google API Key: {{ google.api_key }}
Zabbix API Key: {{ zabbix.api_key }}
Cisco Standard User: Username: {{ cisco.username }} / Password: {{ cisco.password }}
Switch Service Account: Username: {{ cisco_service_account }} / Password: {{ cisco_service_password }}
Crypto Wallet Passport: {{ crypto_wallet_passports }}
Credit Cardholder: {{ credit_card.name_on_card }}
Last 4 of Credit Card: {{ credit_card.number[-4:] }}
Credit Card CVV: {{ credit_card.cvv }}
EOF
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

## 7. Run the `vault_roles.yml` Playbook

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
