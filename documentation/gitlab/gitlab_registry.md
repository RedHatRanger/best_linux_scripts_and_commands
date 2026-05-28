# Registry Configuration
## Edit GitLab Config File:
```bash
sudo cp /etc/gitlab/gitlab.rb /etc/gitlab/gitlab.rb.bak-2026-05-27
sudo cat << EOF >> /etc/gitlab/gitlab.rb
## GitLab Container Registry
registry_external_url 'https://gitlab.example.com:5050'
registry_nginx['ssl_certificate'] = "/etc/gitlab/ssl/gitlab.example.com.crt"
registry_nginx['ssl_certificate_key'] = "/etc/gitlab/ssl/gitlab.example.com.key"
# Allow large image uploads
registry_nginx['client_max_body_size'] = '0'
EOF
```

## Restart GitLab to incorporate the changes
```bash
sudo gitlab-ctl reconfigure
```

## Install `gitlab-runner` on the gitlab server
```bash
sudo yum install gitlab-runner --enablerepo *gitlab-runner*
```

## Start and Enable gitlab-runner service (if required)
```bash
sudo systemctl enable --now gitlab-runner
```

## Open the firewall port 5050/tcp:
```bash
sudo firewall-cmd --add-port=5050/tcp --permanent
sudo firewall-cmd --reload
```

## Create a Project-level Access Token called `WIKI_TOKEN` and save the variable:
- Click on the desired Project, e.g. `Autobot Inventory`>`Settings`>`Access Tokens`>`Add new token`.
- Name it `WIKI_TOKEN` with the `Developer` Role, and it it `read/write repository/registry (4 checkboxes)`.
  - Token name: `WIKI_TOKEN`.
  - Token Description: `Token to read and write to the Autobot Inventory Project`.
  - Expiration date: `2027-05-21`  # 1 year from nows
  - Click `Create project access token`.
  - Copy the token.
  - Click `Settings`>`CI/CD`>`Variables`>`Add variable`.
  - Leave the defaults except for the Key and Value:
    - Key: `WIKI_TOKEN`
    - Value: `<the token value you copied from a few moments ago>`


## Create the podman-user in GitLab and generate the PAT Token to podman login with that token

## On Server1,
# Edit the registries.conf:
```bash
sudo mkdir -p /opt/podman-user/< team >-ee # transfer the <team>-ee.tar> image here
sudo vim /etc/containers/registries.conf
# Ensure this line is as follows:
unqualified-search-registries = ["gitlab.example.com:5050"]
# then login
su - podman-user
podman load -i <team>-ee.tar
podman login gitlab.example.com:5050
podman images
podman tag <old_image_name> <new_image_name>
podman push gitlab.example.com:5050/<team>/autobot_inventory/<team>-ee:2.1
```

## Optionally on Server1, save the podman-user creds from /run/user/<id>/containers/auth.json to ~/.config/containers/auth.json

## Configure a CI/CD Runner in GitLab:
- Navigate to your Project>Settings>CI/CD>Runners>Create project runner
- Fill in:
  - Tags: `<team>`
  - Check the `Run untagged jobs` box.
  - Runner Description:
    - Execution Node
    - Check `Lock to current project`
    - Maximum job timeout: 3600
  - Save the changes by creating the runner  # this will generate a command to run to register the runner

## Registering the Runner on the GitLab Server
```bash
# Copy the gitlab-registry.crt or create one
### the fix on Server1:
openssl s_client -showcerts -connect gitlab.example.com:5050 </dev/null 2>/dev/null | openssl x509 -outform PEM > gitlab-registry.crt
sudo cp gitlab-registry.crt /etc/pki/ca-trust/source/anchors/gitlab-registry.crt
sudo update-ca-trust

# SCP the cert to the gitlab server
ssh gitlab
mkdir -p /etc/gitlab-runner/certs
sudo cp gitlab-registry.crt /etc/gitlab-runner/certs/gitlab.example.com.crt

# Run the registration script
sudo gitlab-runner register --url "https://gitlab.example.com" --token "<token>" --executor "docker" --docker-host "unix:///run/podman/podman.sock" --name="execution-node" --tls-ca-file="/etc/gitlab-runner/certs/gitlab.example.com.crt"

# Enter  the information and paste the default image: `gitlab.example.com:5050/<team>/autobot_inventory/<team>-ee:2.1`
# Your `/etc/gitlab-runner/config.toml` needs to look like this (this example has two registered runners):

concurrent = 1
check_interval = 0
connection_max_age = "15m0s"
shutdown_timeout = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "execution-node"
  request_concurrency = 4
  url = "https://gitlab.example.com/"
  id = 1
  token = "<token>"
  token_obtained_at = 2026-05-08T19:56:18Z
  token_expires_at = 0001-01-01T00:00:00Z
  executor = "docker"
  [runners.cache]
    MaxUploadedArchiveSize = 0
  [runners.docker]
    host = "unix:///run/podman/podman.sock"
    tls_verify = false
    image = "gitlab.example.com:5050/<team>/autobot_inventory/<team>-ee:2.0"
    privileged = false
    disable_entrypoint_overwrite = false
    group_add = ["10018"]   # Group ID for the team
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache", "/<team>/logs/inventory_checker:/<team>/logs/inventory_checker:ro,z", "/etc/gitlab-runner/certs:/etc/gitlab-runner/certs:ro"]
    volume_keep = false
    pull_policy = ["if-not-present"]
    shm_size = 0
    network_mtu = 0

[[runners]]
  name = "server_checks"
  url = "https://gitlab.example.com"
  id = 7
  token = "<token>"
  token_obtained_at = 2026-05-26T19:12:13Z
  token_expires_at = 0001-01-01T00:00:00Z
  executor = "shell"
  request_concurrency=4
  [runners.cache]
    MaxUploadedArchiveSize = 0
    [runners.cache.s3]
      AssumeRoleMaxConcurrency = 0
    [runners.cache.gcs]
    [runners.cache.azure]
```

## Restart the gitlab-runner service and install podman on the gitlab server:
```bash
sudo systemctl restart gitlab-runner
sudo yum install podman -y
sudo systemctl enable --now podman.socket
```

## Append the GitLab server's `/etc/containers/registries.conf` with this:
```bash
# ON the GitLab Server
sudo cat << EOF >> /etc/containers/registries.conf
[[registry]]
location = "gitlab.example.com:5050"
insecure = true
EOF

sudo chmod 644 /etc/pki/ca-trust/source/anchors/gitlab-registry.crt
sudo update-ca-trust extract
sudo systemctl restart gitlab-runner

sudo cat /etc/gitlab-runner/certs/gitlab.example.com.crt  # You will add the contentss to the GIT_SSL_CAINFO project CI/CD Variable as a File.
```

## Pipeline Scheduling
- Description: `Hourly Autobot Inventory Sync`
- Cron timezone: `Central Time US`
- Interval Pattern: `Custom`
  - `0 * * * *`
- Check `Activated`
- Save the Changes

## Troubleshooting
```bash
sudo gitlab-runner list
```

## THIS IS NECESSARY:
- Ran into SSL local certificates issue:
  - Copy the contents of the `gitlab-registry.crt`
  - In your project, navigate to `Settings>CI/CD>Variables`, click `Add variable`.
  - Change the `Type` dropdown to `File`.
  - Change `Masked` to `Visible`.
  - In the `Key` field, type: `GIT_SSL_CAINFO`.
  - Paste the copied certificate contents in the `Value` field.
  - Leave `Protected Variable` and `Mask Variable` unchecked.  Masking will fail on certificates due to new lines.

## Edit the .gitlab-ci.yml in the Autobot Inventory project:
```bash
stages:
  - execute

run_inventory_audit:
  stage: execute
  image: gitlab.example.com:5050/<team>/autobot_inventory/<team>-ee:2.1
  script:
    # 1. Process data and generate files
    - python3 process_inventory.py
    
    # 2. Configure Git for Wiki push
    - git config --global user.email "runner@gitlab.example.com"
    - git config --global user.name "Autobot Runner"
    
    # 3. Clone and update the Wiki
    # Ensure WIKI_TOKEN is set as a Masked Variable in Settings > CI/CD
    - git clone https://oauth2:${WIKI_TOKEN}@gitlab.example.com/<team>/autobot_inventory.wiki.git wiki_repo
    - cp home.md wiki_repo/home.md
    - cd wiki_repo
    - git add home.md
    - git commit -m "Automated Inventory Update v1.0.4 [skip ci]" || echo "No changes found"
    - git push origin main
    - cd ..

  artifacts:
    name: "Interactive_Inventory_Audit"
    paths:
      - inventory_dashboard.html
    expire_in: 1 month
    expose_as: 'Interactive Dashboard'

  tags:
    - <team>
```

## Edit the process_inventory.py
```bash
__version__ = "1.0.7"

import pandas as pd
import os
import sys
from datetime import datetime

INPUT_FILE = "/<team>/logs/inventory_checker/inv_check_output.csv"
WIKI_FILE = "home.md"
HTML_FILE = "inventory_dashboard.html"

def process_inventory():
    try:
        if not os.path.exists(INPUT_FILE):
            print(f"Error: {INPUT_FILE} not found.")
            sys.exit(1)

        # 1. Load Data
        df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig', sep=None, engine='python')
        df.columns = df.columns.str.strip()
        
        # 2. Generate Wiki Content
        markdown_table = df.to_markdown(index=False, tablefmt="pipe")
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        wiki_content = f"# Inventory Audit Dashboard\n> **Last Sync:** {current_time}\n\n{markdown_table}"
        
        with open(WIKI_FILE, "w") as f:
            f.write(wiki_content)

        # 3. Generate Styled HTML
        html_table_headers = "".join([f"<th>{col}</th>" for col in df.columns])
        html_rows = ""
        for _, row in df.iterrows():
            html_rows += "<tr>" + "".join([f"<td>{val}</td>" for val in row]) + "</tr>"

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Inventory Dashboard v{__version__}</title>
            <style>
                body {{ 
                    font-family: "Segoe UI", Arial, sans-serif; 
                    padding: 30px; 
                    background-color: #f0f2f5; 
                    color: #333; 
                }}
                .container {{
                    background: white;
                    padding: 20px;
                    border-radius: 4px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header-section {{ 
                    border-bottom: 3px solid #002d5b; 
                    margin-bottom: 20px; 
                    padding-bottom: 10px; 
                }}
                h2 {{ color: #002d5b; margin: 0; }}
                
                #search-input {{ 
                    width: 100%; 
                    padding: 12px; 
                    border: 2px solid #d1d9e0; 
                    border-radius: 4px;
                    font-size: 14px; 
                    margin-bottom: 20px;
                    box-sizing: border-box;
                }}
                #search-input:focus {{
                    outline: none;
                    border-color: #0056b3;
                }}

                table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
                
                /* Header Styling: Deep Navy */
                th {{ 
                    background-color: #002d5b; 
                    color: #ffffff; 
                    padding: 12px 10px; 
                    border: 1px solid #001a35; 
                    text-align: left; 
                    cursor: pointer;
                    text-transform: uppercase;
                    font-size: 12px;
                }}
                th:hover {{ background-color: #004080; }}

                td {{ padding: 10px; border: 1px solid #d1d9e0; }}

                /* Zebra Striping: Soft Azure */
                tr:nth-child(even) {{ background-color: #eef4fb; }}
                tr:nth-child(odd) {{ background-color: #ffffff; }}
                
                tr:hover {{ background-color: #d6e4f3 !important; }}

                .metadata {{ font-size: 12px; color: #666; margin-top: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header-section">
                    <h2>Network Inventory Dashboard</h2>
                    <div class="metadata">Sync: {current_time} | Records: {len(df)}</div>
                </div>

                <input type="text" id="search-input" placeholder="Filter by IP, Hostname, OS, or Date...">

                <table id="inventory-table">
                    <thead>
                        <tr>{html_table_headers}</tr>
                    </thead>
                    <tbody>
                        {html_rows}
                    </tbody>
                </table>
            </div>

            <script>
                document.getElementById('search-input').addEventListener('keyup', function() {{
                    const filter = this.value.toUpperCase();
                    const trs = document.querySelectorAll('#inventory-table tbody tr');
                    trs.forEach(tr => {{
                        tr.style.display = tr.textContent.toUpperCase().includes(filter) ? "" : "none";
                    }});
                }});

                document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {{
                    const table = th.closest('table');
                    const tbody = table.querySelector('tbody');
                    const index = Array.from(th.parentNode.children).indexOf(th);
                    const asc = th.asc = !th.asc;
                    Array.from(tbody.querySelectorAll('tr'))
                        .sort((a, b) => {{
                            const aCol = a.children[index].textContent.trim();
                            const bCol = b.children[index].textContent.trim();
                            return aCol.localeCompare(bCol, undefined, {{numeric: true, sensitivity: 'base'}}) * (asc ? 1 : -1);
                        }})
                        .forEach(tr => tbody.appendChild(tr));
                }})));
            </script>
        </body>
        </html>
        """
        
        with open(HTML_FILE, "w") as f:
            f.write(html_content)
            
        print(f"Successfully generated v{__version__}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    process_inventory()
```