# What is Redis?
- High-performance backend plug-in to speed up playbooks and handle automation data, such as `ios facts`.
- Ansible leverages it to optimize its own operations.
- Fact Caching (Most Common)
  - By default, Ansible gathers device details ("facts") from your devices at the start of every playbook run, which takes time.
  - You can configure Ansible to store these gathered facts inside a Redis database.
    - The Benefit: On subsequent playbook runs, Ansible pulls the facts instantly from Redis memory instead of logging into the remote servers to gather them again.
    - This slashes playbook execution times, especially across hundreds or thousands of inventory hosts.

| Feature | Redis | PostgreSQL|
| --- | --- | --- |
Primary Storage | RAM (Memory) | Hard Drive / SSD (Disk)
Data Model | Key-Value / NoSQL | Relational / SQL Tables
Speed | Sub-millisecond (Ultra-fast) | Fast, but limited by disk I/O
Primary Use Case | Caching, sessions, real-time queues | Primary application data and financial records

## Step 1: Install Redis
Install the package directly from the RHEL 8 AppStream repository:
```bash
sudo yum install -y redis
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
# rename-command FLUSHDB ""      # commented out for testing
rename-command FLUSHALL ""
rename-command DEBUG ""
rename-command CONFIG ""
```

## Step 3: Enable and Start the Service
Start the native systemd service so it handles persistence and boots automatically:
```bash
sudo systemctl enable --now redis  # Or `systemctl restart redis.service` if you changed any settings in /etc/redis.conf
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
Remove `fact_caching_connection` from your `ansible.cfg` file, leaving only the plugin declaration:
```ini
[defaults]
...
gathering = explicit                  # Only collect ios_facts, not Linux facts
fact_caching = redis                  # community.general collection is required
fact_caching_timeout = 86400
...
```

THEN in ~/.bashrc
```bash
export ANSIBLE_CACHE_PLUGIN_CONNECTION="localhost:6379:0:StrongRedisPassword123!"
export REDIS_PW="StrongRedisPassword123!"
```

1. Get the facts for a device:
```bash
redis-cli -a $REDIS_PW --scan    # Copy one of the output entries
redis-cli -a $REDIS_PW get <paste entry here> | jq -r
```

## Troubleshooting
- I had to `pip3 install "redis<8.0"` for it to work (redis 7.3.0)
- To drop these warnings: `Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.`
```bash
echo "alias redis-cli='redis-cli 2>/dev/null'" >> ~/.bashrc
. ~/.bashrc
```

- To Flush the database:
```bash
redis-cli -a $REDIS_PW -n 0 flushdb       # This flushes the entire database 0
```

---

# Tests
## For testing purposes only, add `callbacks_enabled = profile_tasks` for a timed output:
```yaml
[defaults]
...
callbacks_enabled = profile_tasks
...
```

## SAMPLE PLAYBOOK & Hosts:
```yaml
---
# ansible-playbook -i inventory/testy.redis.ini playbooks/testy.redis.yml -f 25 -e use_cache=False
- name: Gather Facts Using Facts Caching
  hosts: "{{ target | default('redis') }}"  # Default target host or group
  gather_facts: false
  vars:
    use_cache: false                        # Optionally, set this var in inventory/group_vars/all.yml

  tasks:
    - name: Gather Live IOS Facts
      cisco.ios.ios_facts:
        gather_subset:
          - "{{ ios_gather_subset | default('min') }}"
      when: not use_cache | bool

    - name: Display a comprehensive set of cached facts
      ansible.builtin.debug:
        msg: >-
          Device Name: {{ inventory_hostname }}
          Model: {{ ansible_net_model }}
          Serial: {{ ansible_net_serialnum }}
          OS Version: {{ ansible_net_version }}

```

```ini
[redis]
router1     ansible_host=192.168.1.2    # arbitrary example host, assuming you can connect via SSH
```

## Run the Playbook
```bash
ansible-playbook -i inventory/testy.redis.ini playbooks/testy.redis.yml -f 25 -e use_cache=false

# NOW Test with
ansible-playbook -i inventory/testy.redis.ini playbooks/testy.redis.yml -f 25 -e use_cache=true
```

## If you want to mess around with `redis-cli` in general:
```bash
redis-cli -a $REDIS_PW $ # This authorizes the login
# OR
# redis-cli
# THEN at the prompt: AUTH StrongRedisPassword123!
# Manually set key-value pairs:
redis-cli -a $REDIS_PW set user1 "Gary"
redis-cli -a $REDIS_PW mset user2 "Chris" user3 "Jacob" user4 "Jason" user5 "Brian"
redis-cli -a $REDIS_PW mget user1 user2 user3 user4 user5

# To store multiple fields for a single call:
redis-cli -a $REDIS_PW hset user:1000 name "Alice" email "alice@example.com" age "30"

# Then to fetch:
redis-cli -a $REDIS_PW hget user:100 name
```
