Place this in ansible.cfg:
```
[defaults]
callbacks_enabled = device_change_logger
```

Then:
```
mkdir -p ~/ansible/callback_plugins
```
