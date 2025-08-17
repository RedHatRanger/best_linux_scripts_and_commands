Here’s how you can configure your `ansible.cfg` to specify a custom Galaxy server list and keep the API keys out of the config by using environment variables (which you set dynamically from your encrypted vault via the script):

---

### Step 1: Configure `ansible.cfg` with `server_list` and environment variable tokens

```ini
[galaxy]
server_list = my_galaxy

[galaxy_server.my_galaxy]
url = https://my.galaxy.server/api/
token = ${MY_GALAXY_API_TOKEN}
```

- `server_list` defines the named servers you want to use.
- Each server section uses `token = ${ENV_VAR}` syntax to pull the token from an environment variable instead of hardcoding it.

---

### Step 2: Keep your API tokens encrypted in `vault.yml`

```yaml
galaxy_api_token: "your_actual_api_token_here"
```

Encrypt it with:

```bash
ansible-vault encrypt vault.yml
```

---

### Step 3: Use a wrapper script to decrypt and export the token before running ansible-galaxy

Example `install_collections.sh`:

```bash
#!/bin/bash

# Decrypt vault file and extract token using yq
GALAXY_TOKEN=$(ansible-vault view vault.yml | yq '.galaxy_api_token' -r)

# Export token as environment variable expected by ansible.cfg
export MY_GALAXY_API_TOKEN="$GALAXY_TOKEN"

# Run collection install with ansible-galaxy
ansible-galaxy collection install -r requirements.yml --force
```

Make sure this script is executable:

```bash
chmod +x install_collections.sh
```

Run it instead of calling `ansible-galaxy` directly:

```bash
./install_collections.sh
```

---

### Why this is good practice

- Your API token is **never stored in plain text** in `ansible.cfg`.
- The token is **only decrypted in memory** during the script execution.
- You can safely commit `ansible.cfg` and `requirements.yml` to version control without exposing secrets.
- You can extend this pattern for multiple Galaxy servers by adding more tokens and environment variables.