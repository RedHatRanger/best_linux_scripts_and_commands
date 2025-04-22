If you want to send someone a hashed password:
```
openssl passwd -6

# This will prompt you to enter your password and then confirm it.  Then it returns a hashed value.
```

If you want to see the contents of a certificate:
```
openssl x509 -in /etc/pki/tls/certs/localhost.crt -text
```

Generating a certificate:
```
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:3072 -subj='/C=XX/O=Default' -keyout /etc/pki/tls/private/localhost.key -out /etc/pki/tls/certs/localhost.crt
```
