* Some samples:
```
time dd if=/dev/zero of=dd.disk bs=1M count=500
```

```
time dd if=/dev/urandom of=test.txt bs=1G count=1
```

```
time fallocate -l 500M fa.disk
```

```
time sleep 5
```
