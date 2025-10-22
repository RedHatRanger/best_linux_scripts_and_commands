## Open PowerShell and type:
```bash
New-Item -ItemType File -Path $PROFILE -Force
```

## Then, paste this into the .ps1 file that is created:
```
function ll { Get-ChildItem -Force }
```

## Now, `ll` works all the time!