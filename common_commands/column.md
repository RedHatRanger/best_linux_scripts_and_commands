If you are tired of scrolling and scrolling the output of a command, simply pipe it to column:
```
cat /var/log/messages | column
```

If you need to sort through a mess of an output, use the column command:
```
cat /etc/passwd | column -t -s ":" -N USERNAME,PW,UID,GUID,COMMENT,HOME,INTERPRETER
```

And if you want to convert it all into JSON format:
```
cat /etc/passwd | column -t -s ":" -N USERNAME,PW,UID,GUID,COMMENT,HOME,INTERPRETER -J -n passwordfile
```
