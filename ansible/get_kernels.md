```
- name: Display current kernel and available updates
  hosts: all
  become: true
  gather_facts: true

  tasks:
    - name: Check for available package updates
      ansible.builtin.yum:
        list: updates
      register: yum_updates

    - name: Display the Updates Info
      ansible.builtin.debug:
        msg:
          - "Current Kernel: {{ ansible_facts.kernel }}"
          - "Kernel Update: {{ (yum_updates.results | map(attribute='envra') | list | sort | select('search', 'kernel') | first)[2:] | default('N/A') }}"
          - "Number of Updates: {{ yum_updates.results | map(attribute='envra') | list | length }}"
```
