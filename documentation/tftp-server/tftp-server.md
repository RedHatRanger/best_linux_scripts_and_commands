# Install TFTP Server on a RHEL 8/9 System:

## Initial Setup:
```bash
sudo yum install -y tftp-server tftp # tftp server and client for testing locally
sudo systemctl enable --now tftp.socket
sudo firewall-cmd --permanent --add-service=tftp; sudo firewall-cmd --reload
sudo mkdir -p /etc/systemd/system/tftp.service.d
sudo chmod -R 755 /etc/systemd/system/tftp.service.d/
sudo vim /etc/systemd/system/tftp.service.d/allow_uploads.conf
# Fill it in the next step
```

## Create the TFTP Service in `allow_uploads.conf` (then :wq to save):
```bash
[Service]
ExecStart=
ExecStart=/usr/sbin/in.tftpd -c -p -s /var/lib/tftpboot
```

## Restart the TFTP Service and modify ownership of the shared `tftpboot` directory:
```bash
sudo systemctl daemon-reload
sudo systemctl restart tftp.service
sudo chown nobody: /var/lib/tftpboot/
sudo chmod 775 /var/lib/tftpboot/
sudo restorecon -RFv /var/lib/tftpboot/
```