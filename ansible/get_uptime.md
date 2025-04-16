```
- name: Fetch Server Uptime
  ansible.builtin.debug:
    msg: "Server Uptime: {{ ansible_facts.uptime_seconds / 86400) | round }} days."
```
