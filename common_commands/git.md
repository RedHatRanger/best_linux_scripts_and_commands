## GIT for Windows:
1) Generate the ssh keys in Terminal (PowerShell):
```
ssh-keygen -t ecdsa
```

2) Open up GitLab portal on Google Chrome, click "Add New Key", and copy your ~/.ssh/id_ecdsa.pub contents here:
```
https://<yourdomain>/-/user_settings/ssh_keys
```

3) Open up VSCode and connect to the remote repository using the SSH git code from the gitlab site.

4) OPEN UP A GIT for Windows Bash Prompt:
```
git config --global user.name "<lastName>,<firstName> <MiddleName>"
git config --global user.email "<username>@<domainname>"
```
