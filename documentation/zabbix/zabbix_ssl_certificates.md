# Zabbix Certificate Installation

## Install the mod_ssl package on the Linux Server:
```bash
sudo yum clean all
sudo yum install mod_ssl dos2unix
```
## Generate the CSR on the Linux Server:
```bash
sudo chmod 777 /etc/pki/tls/private /etc/pki/tls/certs
cd /etc/pki/tls/private 
openssl req -new -newkey rsa:3072 -nodes -keyout {{ hostname }}.key -out newcsrrequest.csr

# Answer the Questions
```

## CAT the contents of the newrrequest.csr output:
```bash
cat newcsrrequest.csr # copy this
```

## Go to the Certificate Generating Site on your Windows Workstation:
<Here is where you generate the certificate from your organization>

# DO NOT SCP the certificate...COPY THE CONTENTS
```

## Save the Generated Certificate on the Linux Server:
```bash
cd /etc/pki/tls/certs
sudo vim {{ hostname }}.crt
# (paste the contents of the .cer file from VSCode on your Windows Workstation), :wq to save

sudo chown root: {{ hostname }}.crt
sudo chmod 644 /etc/pki/tls/certs
sudo chmod 600 /etc/pki/tls/private
```
```bash
sudo vim /etc/httpd/conf.d/ssl.conf

# FIX THESE LINES TO MATCH:
SSLCertificateFile /etc/pki/tls/certs/{{ hostname }}.crt
SSLCertificateKeyFile /etc/pki/tls/private/{{ hostname }}.key
```

## Reboot the Server:
```bash
sudo reboot
```
