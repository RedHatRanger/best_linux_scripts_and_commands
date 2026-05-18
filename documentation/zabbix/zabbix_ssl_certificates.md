# Zabbix Certificate Installation

On the Target Linux Server:
## Install the mod_ssl package:
```bash
sudo yum clean all
sudo yum install mod_ssl dos2unix
```
## Generate the CSR:
```bash
cd /etc/pki/tls/private
openssl req -new -newkey rsa:3072 -nodes -keyout {{ hostname }}.key -out newcsrrequest.csr
```

## CAT the contents of the newrrequest.csr output:
```bash
cat newcsrrequest.csr # copy this
```

### You will then generate the certificate with your organization and download it to your Linux Server

On the Linux Server:
```bash
sudo chmod 777 /etc/pki/tls/certs
sudo mv /tmp/{{ hostname }}.crt /etc/pki/tls/certs
cd /etc/pki/tls/certs
sudo dos2unix /etc/pki/tls/certs/{{ hostname }}.crt
sudo chown root: {{ hostname }}.crt
sudo chmod 644 {{ hostname }}.crt
cd /etc/pki/tls/private
sudo chmod 644 /etc/pki/tls/private/{{ hostname }}.key
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