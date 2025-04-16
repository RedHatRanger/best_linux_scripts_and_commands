```
- name: Get list of YUM repos
  ansible.builtin.yum:
    list: repos
  register: yum_repo

- name: Show enabled YUM repos and count
  ansible.builtin.debug:
    msg:
      - "Number of Enabled Repos: {{ yum_repo.results | selectattr('enabled', 'equalto', 1) | list | length }}"
      - "Enabled Repos: {{ yum_repo.results | selectattr('enabled', 'equalto', 1) | map(attribute='repoid') | list }}"
```
