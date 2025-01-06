If you are tired of scrolling and scrolling the output of a command, simply pipe it to column:
```
cat /var/log/messages | column
```

If you need to sort through a mess of an output, use the column command:
```
cat /etc/passwd | column -t -s ":"
```