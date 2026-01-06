# Ansible AWX Configuration

## Table of Contents
1. [Credentials Management](#credentials-management)
    - [The Machine Credential](#creating-the-ansible-ssh-user-machine-credential)
    - [The Ansible Vault Credential](#creating-a-global-ansible-vault-credential)
    - [The GitLab SVC Account Credential](#creating-the-gitlab-svc-account-credential)
    - [The Private Container Registry Credential](#creating-private-container-registry-credential)
1. [Execution Environment Management](#execution-environment-management)
1. [User Management](#user-management)
1. [Projects Management](#projects-management)
1. [Inventory Management](#inventory-management)
1. [Templates Management](#templates-management)
1. [OIDC Authentication](#oidc-authentication)
1. [Enable Writing to an NFS Share](#enable-writing-to-an-nfs-share)
1. [Misc Configuration](#misc-configuration)
    - [Optionally use the Project's Ansible.cfg](#optionally-configure-awx-to-use-the-projects-ansiblecfg-instead-of-the-container-one)

<br>

## Credentials Management
- Objective: Configure the credentials for:
    - Ansible to SSH
    - Ansible Vault to encrypt/decrypt
    - GitLab SVC Account
    - Private Container Registry

### Creating the Ansible SSH User Machine Credential:
- Objective: Configure Machine Credentials to access the managed devices.

1. On the left sidebar, click `Resources` > `Credentials`.
1. Click `Add` and fill in the details:
    - Name: `Cisco SVC Account (Ansible User)`
    - Description: `The account which Ansible uses to access the Cisco devices`
    - Organization: `<Your Organization>`
    - Credential Type: Choose `Machine` from the drop-down menu.
    - Type Details:
        - Username: `<Your Ansible SSH Username>`
            >defined by ansible_user in your project's group_vars/all.yml`
        - Password: `<Your Ansible SSH Password>`
            >defined by ansible_password in your project's group_vars/all.yml
        - Privilege Escalation Method: `enable`
1. Click `Save` to confirm the setting.

### Creating a Global Ansible Vault Credential:
- Objective: Setup an Ansible Vault Credential to decrypt the Ansible user pw.

>This is required if you have used ansible-vault to encrypt the ansible_password in your Git `<project>`/group_vars/all.yml):
1. On the left sidebar, click `Resources` > `Credentials`.
1. Click `Add` and fill in the details:
    - Name: `Ansible Vault Credential`
    - Description: `Ansible Vault Credential`
    - Organization: `<LEAVE BLANK>`
    - Credential Type: Choose `Vault` from the drop-down menu.
    - Type Details:
        - Vault Password: `<Enter your vault password OR the contents of your vault pw file>`
1. Click `Save` to confirm the setting.

### Creating the GitLab SVC Account Credential:
- Objective: Configure GitLab SVC Account Credentials to pull playbooks.

1. On the left sidebar, click `Resources` > `Credentials`.
1. Click `Add` and fill in the details:
    - Name: `GitLab SVC Account`
    - Description: `AWX User GitLab Service Account`
    - Organization: `<Your Organization> OR <LEAVE BLANK>`
    - Credential Type: Choose `Source Control` from the drop-down menu.
    - Type Details:
        - Username: `awx-user` 
            >The SVC Account you created in GitLab which has access to the Ansible Config Mgmt Project
        - Password: `<The Personal Access Token generated in GitLab for the awx-user>`
1. Click `Save` to confirm the setting.

### Creating Private Container Registry Credential:
- Objective: Configure Private Registry Credentials to retrieve your EEs.

1. On the left sidebar, click `Resources` > `Credentials`.
1. Click `Add` and fill in the details:
    - Name: `<Your Registry Provider Name> Registry Creds`
    - Description: `<Your Registry Provider Name> Registry Creds`
    - Organization: `<Your Organization>`
    - Credential Type: Choose `Container Registry` from the drop-down menu.
    - Type Details:
        - Authentication URL: `<Your URL where your Execution Environment is podman-pulled from>`
        - Username: `<the team svc account name>`
        - Password: `<the team's token generated to access the registry>`
        - Options: Check `Verify SSL`.
1. Click `Save` to confirm the setting.

<br>

---

## Execution Environment Management
- Objective: Setup the team's default execution environment.

1. On the left sidebar, click `Administration` > `Execution Environments`.
1. Click `Add` and fill in the details:
    - Name: `Network Automation EE`
    - Image: `<The Image URL from your Private Registry and version number>`
        >The image URL you would podman pull from.
    - Pull: Choose `Always pull container before running` from the drop-down menu.
    - Description: `Cisco Network Automation EE`
    - Organization: `<LEAVE BLANK to make it globally available>`
    - Registry Credential: `<Your Registry Provider Name> Registry Creds`
        >We created this in a previous step.
1. Click `Save` to confirm the setting.

<br>

---

## User Management
- Objective: Setup Organizations, Teams, and Users for Least Privilege

### Creating an Organization:
1. On the left sidebar, click `Access` > `Organizations`.
1. Click `Add` and fill in the details:
    - Name
    - Description
    - Choose the Execution Environment:
        - `Network Automation EE`
    - Galaxy Credentials (optional for updates)
1. Click `Save` to confirm the setting.

### Creating Teams:
1. On the left sidebar, click `Access` > `Teams`.
1. Click `Add` and fill in the details:
    - Name: `<team title>`
    - Description: `<Create a custom>`
    - Choose the `Organization`
1. Click `Save` to confirm the setting.

### Creating Users:
1. On the left sidebar, click `Access` > `Users`.
1. Click `Add User` and fill in the details (or modify an existing user).
    - First Name
    - Last Name
    - Username
    - Password 2x
    - Normal User
    - Choose their `Organization` you created earlier.
1. Click `Save` to confirm the setting.

### Adding Users to Teams (Membership):
1. On the left sidebar, click `Access` > `Teams`.
1. In the main part of the screen, click on the `Access` Tab.
1. Click `Add` to add the user we created previously:
    - `Users` > `Next` > `<myuser>` (checkbox) > `Next` > `Member`
1. Click `Save`.

### Limiting Job Templates to Teams (Roles = Permissions):
1. On the left sidebar, click `Access` > `Teams`.
1. Click the target team name for editing.
1. In the main part of the screen, click on the `Roles` Tab.
1. Click `Add`:
    - `Job Templates` > `Next` > Check the desired Job Templates > `Next` > Check `Execute`.
1. Click `Save` to confirm the setting.

<br>

---

## Projects Management
- Objective: To Access the `Ansible Config Mgmt Project` Roles and Playbooks.

1. On the left sidebar, click `Resources` > `Projects`.
1. Click `Add` and fill in the details:
    - Name: `Ansible Config Mgmt`
    - Description: `Main Ansible Project`
    - Organization: `<Your Organization>`
    - Execution Environment: `Network Automation EE`
    - Source Control Type: `Git`
    - Type Details:
        - Source Control URL: `<The URL of your Ansible Config Mgmt Project>`
        - Source Control Branch: `devtest`
            >You can choose 'main' but for this sample we are choosing the devtest branch.
        - Source Control Credential: Click the Magnifying Glass and choose `GitLab SVC Account`.
        - Options:
            - Check the boxes:
                - `Clean`
                - `Update Revision on Launch`
1. Click `Save` to confirm the setting.

<br>

---

## Inventory Management
- Objective: To manage separate inventories in an organized way.

1. On the left sidebar, click `Resources` > `Inventories`.
1. Click `Add` and fill in the details:
    - Name: `Test Inventory`
    - Description: `The inventory from Test.ini`
    - Organization: `<Your Organization>`
1. Click `Save`.
1. In `Inventories` > `Test Inventory`, click the `Sources` Tab.
1. Click `Add` and fill in the details:
    - Name: `Test Inventory YML`
    - Description: `This was generated from the Test.ini`
    - Execution Environment: `Network Automation EE`
    - Source: Choose `Sourced from a Project` from the drop-down menu.
    - Source Details:
        - Project: `Ansible Config Mgmt`
            >Your GitLab Project Name
        - Inventory file: `inventory/test_inventory.yml`
            >Here it browses GitLab for the inventory.yml file.
        - Check the box for `Update on launch`.
1. Click `Save` to confirm the setting.

<br>

---

## Templates Management
- Objective: Create a Reusable Job Template to Run Ansible Jobs.

1. On the left sidebar, click `Resources` > `Templates`.
1. Click `Add` and fill in the details:
    - Name: `<This name should mirror the name of the playbook or role, plus the site name>`
    - Description: `<A brief description of what the playbook is doing>`
    - Job Type: Choose `Run (OR Check)` from the drop-down menu.
    - Inventory: `Test Inventory`
    - Project: `Ansible Config Mgmt`
    - Execution Environment: `Network Automation EE`
    - Playbook: `<Browse the dropdown for the desired GitLab playbook>`
    - Credentials:
        - Machine:
            - Click the radio button next to `Cisco SVC Account`.
            - Click `Select` to confirm.
        - Vault:
            - Check the box for the `Ansible Vault Credential`.
            - Click `Select` to confirm.
    - Verbosity: `<LEAVE DEFAULT OR set it higher for debugging>`
    - Show Changes: Click the slider to `On`.
    - Skip Tags: `awx` (optional)
1. Click `Save` to confirm the setting.
1. Click `Launch` when ready to kickoff the Ansible Job Run.

<br>

---

## OIDC Authentication
- Objective: Setup OIDC for authenticating users via Azure AD:

1. On the left sidebar, click `Settings` > `Generic OIDC`.
1. Click `Edit` and fill in the details:
    - OIDC Key: `<Client ID from Azure AD>`
    - OIDC Secret: `<Generated Secret from Azure AD>`
    - OIDC Provider URL: `https://login.microsoft.us/<TenantID>/v2.0`
    - Verify OIDC Provider Certificate: `On`
1. Click `Save` to confirm the setting.
1. Log out with your system admininistrative user.
1. Test OIDC Login using the button below (do not enter a username or pw).

<br>

---

## Enable Writing to an NFS share:
1. On the left sidebar, click `Administration` > `Instance Groups`.
1. Click `Add` > `Add container group` and fill in:
    - Name: `NFS Mapping Container Group`
    - Options: Check `Customize pod specification` and fill in the `YAML`:
        - Custom pod spec:
            ```bash
            apiVersion: v1
            kind: Pod
            metadata:
              namespace: <awx namespace>
            spec:
              containers:
                - name: worker
                  image: <image link and the version #>
                  securityContext:
                    runAsUser: 0
                    privileged: true
                  volumeMounts:
                    - name: nfs-volume
                      mountPath: /<mountpath>
              volumes:
                - name: nfs-volume
                  nfs:
                    server: <NFS Server IP>
                    path: /<mountpath>
            ```
<br>

---

## Misc Configuration

### Optionally configure AWX to use the Project's `ansible.cfg` instead of the container one:
1. On the left sidebar, click `Settings` > `Job settings`.
1. Click `Edit` > `Extra Environment Variables` and fill in:
    ```bash
     {
     "ANSIBLE_CONFIG": "/runner/project/ansible.cfg"
     }
    ```
    
