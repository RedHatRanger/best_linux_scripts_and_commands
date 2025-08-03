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
├── encrypted_vars/
│   └── nunya.yml
└── keyfile.txt
```

Create the directories with the following commands:

```bash
mkdir -p ansible_vault_lab/encrypted_vars
```

### 2.3. Create the Unencrypted Data File

Create a YAML file named `nunya.yml` inside the `ansible_vault_lab` directory with the following content. This file contains the sensitive data that we want to encrypt.

```yaml
# nunya.yml (unencrypted)

api_key: "GOOGLE-API-1234-ZEBRA-LOL-5678"
username: "sir_snorts_a_lot"
crypto_wallet_passports: "moose-unicorn-dragon@zebrabank"
cc_info:
  number: "4111 1111 1111 1111"
  expiry: "12/34"
  cvv: "123"
  name_on_card: "Sir Laughsalot"
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

## 3. Encrypting Data with Ansible Vault

Now, we will encrypt the `nunya.yml` file using `ansible-vault encrypt`. We will use the `--vault-password-file` option to provide the password from our `keyfile.txt`.

```bash
ansible-vault encrypt ansible_vault_lab/nunya.yml
```

After running this command, the content of `nunya.yml` will be encrypted.

## 4. Working with Encrypted Files

Ansible Vault provides several commands to work with encrypted files.

### 4.1. Viewing Encrypted Files

To view the content of an encrypted file without decrypting it permanently, you can use `ansible-vault view`:

```bash
ansible-vault view ansible_vault_lab/encrypted_vars/nunya.yml
```

This will display the original content of the file in your terminal.

### 4.2. Editing Encrypted Files

To edit an encrypted file, you can use `ansible-vault edit`. This will decrypt the file into a temporary file, open it in your default editor, and then re-encrypt it when you save and close the editor.

```bash
ansible-vault edit ansible_vault_lab/encrypted_vars/nunya.yml
```

### 4.3. Decrypting Files

To permanently decrypt a file, you can use `ansible-vault decrypt`:

```bash
ansible-vault decrypt ansible_vault_lab/encrypted_vars/nunya.yml
```

This will replace the encrypted file with its decrypted version.

### 4.4. Changing the Vault Password (Rekey)

If you need to change the password of an encrypted file, you can use `ansible-vault rekey`. This command will decrypt the file with the old password and re-encrypt it with a new password.

First, create a new password file, for example, `new_keyfile.txt`:

```
another_super_secret_password_456
```

Then, run the `rekey` command:

```bash
ansible-vault rekey ansible_vault_lab/encrypted_vars/nunya.yml --new-vault-password-file new_keyfile.txt
```

## 5. Conclusion

This lab has demonstrated the basic workflow of using Ansible Vault to secure sensitive data. By using a vault password file, you can automate the process of encrypting and decrypting files without having to manually enter the password every time.





## Expected Outputs for Vault Operations (Simulated)

Since the sandbox environment is currently unresponsive, the following are the *expected outputs* for the Ansible Vault operations described above, assuming a successful execution.

### 3. Encrypting Data with Ansible Vault - Expected Output

After running the `ansible-vault encrypt` command, you should see output similar to this:

```
Encryption successful
```

And if you were to try to `cat` the `nunya.yml` file, you would see encrypted content:

```
$ cat ansible_vault_lab/nunya.yml
$ANSIBLE_VAULT;1.1;AES256
613030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030
```

### 4.1. Viewing Encrypted Files - Expected Output

When you run `ansible-vault view`, you will see the decrypted content of the file in your terminal:

```yaml
api_key: "GOOGLE-API-1234-ZEBRA-LOL-5678"
username: "sir_snorts_a_lot"
crypto_wallet_passports: "moose-unicorn-dragon@zebrabank"
cc_info:
  number: "4111 1111 1111 1111"
  expiry: "12/34"
  cvv: "123"
  name_on_card: "Sir Laughsalot"
```

### 4.2. Editing Encrypted Files - Expected Output

When you run `ansible-vault edit`, it will open the file in your default text editor (e.g., `vi`, `nano`). After you make changes and save the file, the terminal will show something like:

```
[sudo] password for ubuntu:
Editing /home/ubuntu/ansible_vault_lab/encrypted_vars/nunya.yml
```

And then it will return to the prompt after saving and re-encrypting.

### 4.3. Decrypting Files - Expected Output

After running `ansible-vault decrypt`, you should see:

```
Decryption successful
```

And if you `cat` the file again, you will see the original unencrypted content.

### 4.4. Changing the Vault Password (Rekey) - Expected Output

After running `ansible-vault rekey`, you should see:

```
Rekey successful
```

This indicates that the file has been successfully re-encrypted with the new password. You would then need to use `new_keyfile.txt` to view or edit the file.




### 2.5. Configure `ansible.cfg` for Vault Password File

To avoid repeatedly specifying the `--vault-password-file` option with every `ansible-vault` command, you can configure Ansible to automatically use a vault password file by creating an `ansible.cfg` file in your project directory. This file will tell Ansible where to find the vault password.

Create a file named `ansible.cfg` in the `ansible_vault_lab` directory with the following content:

```ini
[defaults]
vault_password_file = ./keyfile.txt
```

This configuration tells Ansible to look for the vault password in `keyfile.txt` located in the same directory as the `ansible.cfg` file.