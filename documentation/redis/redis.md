## Step 1: Install Redis
Install the package directly from the RHEL 8 AppStream repository:
```bash
sudo dnf install -y redis
```

## Step 2: Configure Hardening Directives (/etc/redis.conf)
Open the configuration file and apply the baseline security settings (locking down network exposure, setting a password, and configuring memory limits for caching):  
```ini
bind 127.0.0.1
protected-mode yes
port 6379

# Authentication
requirepass StrongRedisPassword123!

# Memory management (turns Redis into a proper LRU cache for facts)
maxmemory 512mb
maxmemory-policy volatile-lru

# Disable high-privilege/dangerous commands
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command DEBUG ""
rename-command CONFIG ""
```

## Step 3: Enable and Start the Service
Start the native systemd service so it handles persistence and boots automatically:
```bash
sudo systemctl enable --now redis
```

## Step 4: Point Ansible to the Cache
1. Securing the Password in Redis (/etc/redis.conf)
Redis does not natively support hashed passwords in redis.conf; it reads requirepass as a plaintext string. Instead of encrypting the file itself, security is enforced at the OS level by restricting read access to authorized users only.

ENSURE the file ownership to the redis service user and root:
```bash
sudo chown redis:root /etc/redis.conf
```

```bash
sudo chmod 640 /etc/redis.conf
```

2. Securing the Password in Ansible (ansible.cfg)
Hardcoding the password into a shared or git-tracked `ansible.cfg` file is a security risk. You can keep the password out of the configuration file entirely by using Environment Variables.

Remove fact_caching_connection from your `ansible.cfg` file, leaving only the plugin declaration:
```ini
[defaults]
gathering = explicit # Only collect ios_facts, not Linux facts
fact_caching = redis # community.general collection is required
fact_caching_timeout = 86400
```

THEN in ~/.bashrc
```bash
export ANSIBLE_CACHE_PLUGIN_CONNECTION="localhost:6379:0:StrongRedisPassword123!"
```

3. If you want to play with redis-cli:

```bash
redis-cli -a "StrongRedisPassword123!" # This authorizes the login
# OR
# redis-cli
# THEN at the prompt: AUTH StrongRedisPassword123!
```

4. Get the facts for a device:

```bash
redis-cli -a "StrongRedisPassword123!" keys --scan
redis-cli -a "StrongRedisPassword123!" get ansible_facts<device_name> | jq -r
```



## Troubleshooting

- had to `pip3 install "redis<8.0"` for it to work (redis 7.3.0)
