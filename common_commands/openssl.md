If you want to send someone a hashed password:
```
openssl passwd -6

# This will prompt you to enter your password and then confirm it.  Then it returns a hashed value.
```

If you want to see the contents of a certificate:
```
openssl x509 -in /etc/pki/tls/certs/localhost.crt -text
```
