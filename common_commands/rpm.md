To list all packages which are currently installed on the system:
```
rpm -qa
```

If you want to know the history of an installed package:
```
rpm -q --changelog <package>
```

If you want to determine what package is installed based on the filepath of the binary:
```
rpm -qf /usr/bin/<package_name>
```
