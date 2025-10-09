# GitLab Installation Instructions
## Install the required RHEL package:
```bash
sudo yum install gitlab-ee -y
```

## Backup the original GitLab Configuration:
```bash
sudo cp /etc/gitlab/gitlab.rb /etc/gitlab/gitlab.rb.bak 
```

## Setup the cname on IPA to point to the actual fqdn <fqdn>

## Create the new GitLab Configuration file:
```bash
sudo cat << EOF > /etc/gitlab/gitlab.rb
external_url 'https://<fqdn>'
gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = "smtp.<domain>"
gitlab_rails['smtp_port'] = 25
gitlab_rails['smtp_domain'] = "<domain>"
gitlab_rails['smtp_openssl_verify_mode'] = 'none'
gitlab_rails['gitlab_email_from'] = 'teamgitlab@<domain>'
gitlab_rails['gitlab_email_display_name'] = 'GitLab'
gitlab_rails['impersonation_enabled'] = false
gitlab_rails['manage_backup_path'] = true
gitlab_rails['backup_path'] = "/var/opt/gitlab/backups"
gitlab_rails['backup_keep_time'] = 604800
prometheus['enable'] = false
node_exporter['enable'] = false
letsencrypt['enable'] = false
EOF
```

## Restart the GitLab-CTL Service after making the changes to the configuration:
```bash
sudo gitlab-ctl reconfigure
```

## Configure the Firewall:
```bash
sudo firewall-cmd --permanent --add-service={http,https}; sudo firewall-cmd --reload
sudo mkdir -p /etc/gitlab/ssl
sudo chmod 777 /etc/gitlab/ssl # Temp and then change back to 600
sudo cd /etc/gitlab/ssl
```

## Generate the SSL Certificate for HTTPS:
```bash
openssl req -new -newkey rsa:2048 -nodes -keyout <fqdn>.key -out newcsrrequest.csr

# Answers:
# US
# <your_state>
# <your_city>
# <organization>
# NMU
# <fqdn>
# PRESS ENTER
# PRESS ENTER
# PRESS ENTER 
```

## Cat the CSR you just created:
```bash
cat newcsrrequest.csr

## Download the certificate in Base64 on the next page.

## Hand the certificate over to the GitLab Server:
- In Windows: 
  - Make sure you can see file extensions, then rename the file certnew.cer to <fqdn>.crt
  - Open Terminal (PowerShell):

```bash
cd Downloads
scp .\<domain>.crt <your_adm_account>@<actual_fqdn>:/tmp
```

## Then on the Linux Server:
```bash
# In the /etc/gitlab/ssl directory:
sudo mv /tmp/<cname_fqdn>.crt .
sudo chown -R root: /etc/gitlab/ssl
sudo chmod -R 600 /etc/gitlab/ssl
sudo sed -i 's/http/https/g' /etc/gitlab/gitlab.rb  # Changes this line to: external_url 'https://<cname_fqdn>'
```

## Backups:
```bash
sudo gitlab-rake gitlab:backup:create
sudo gitlab-ctl backup-etc

# GitLab Backup Schedule (6pm EST daily):
0 18 * * * /usr/bin/gitlab-rake gitlab:backup:create CRON=1 > /dev/null 2>&1
```

## Reconfigure GitLab: Anytime the /etc/gitlab/gitlab.rb file is changed:
```bash
sudo gitlab-ctl reconfigure
sudo gitlab-ctl status
```

