```
- name: Get Distribution
  ansible.builtin.debug:
    msg:
      - "Distribution and Version: {{ ansible_facts.distribution }} {{ ansible_facts.distribution_version }}"
```
