* If bash doesn't work for a script with ./test.sh:
```
bash ./test.sh
```
OR If STIG is the issue:
```
mount -o remount,exec /home
```

# Summary
"When you explicitly call bash, you are leveraging the fact that bash itself is an executable that interprets text files, rather than relying on the kernel's direct execution mechanism, which is blocked by the noexec mount option".
