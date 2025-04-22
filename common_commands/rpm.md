To list all packages AND versions which are currently installed on the system:
```
rpm -qa

# To count the packages:
rpm -qa | wc -l
```

To list all packages (names only) and save them to a file:
```
rpm -qa --qf "%{NAME}\n" | sort -u | tee -a installed_packages.txt
```

If you want to know the history of an installed package:
```
rpm -q --changelog <package>
```

If you want to determine what package is installed based on the filepath of the binary:
```
rpm -qf /usr/bin/<package_name>
```
