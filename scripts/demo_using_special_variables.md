```
#!/bin/bash
echo "This program is called $0 and it has $# args"
echo "This program is $(basename $0) and it has $# args"
PID=${*:-"1"}
ps -f -p $PID
```

![Screenshot from 2024-05-29 09-06-16](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/5474da55-a89e-4a5d-98da-63ed06f89d34)

![Screenshot from 2024-05-29 08-52-12](https://github.com/RedHatRanger/best_linux_scripts_and_commands/assets/90477448/bb0f3cb0-4459-47aa-8e98-6e8a6a7c2d73)
