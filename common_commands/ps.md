* To show all running processes on a system:
```
[ansible@ctrl ~]$ ps -elf
```

* To list just the sleep process:
```
[ansible@ctrl ~]$ ps -elf | grep sleep
```

* To list the process number (PID) of the command:
```
[ansible@ctrl ~]$ pgrep sleep
30516
```

* A simple demo of creating a test process and then searching for it using pgrep:
```
[ansible@ctrl ~]$ sleep 1000&
[1] 30516
[ansible@ctrl ~]$ ps -lp $(pgrep sleep)
F S   UID     PID    PPID  C PRI  NI ADDR SZ WCHAN  TTY          TIME CMD
0 S  1001   30516    8973  0  80   0 - 55238 hrtime pts/0    00:00:00 sleep

[ansible@ctrl ~]$ sudo pkill sleep
[1] 30516 Terminated       sleep 1000 
```
