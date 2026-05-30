## Open PowerShell as Admin, and type:
```bash
New-Item -ItemType File -Path $PROFILE -Force
```

## Then, type `ise $PROFILE`, press ENTER, and paste these contents:
```
function ll { Get-ChildItem -Force }
```

## Now, `ll` works all the time!
