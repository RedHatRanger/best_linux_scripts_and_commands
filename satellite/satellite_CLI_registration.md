```
export REGISTRATION_SCRIPT=$(hammer host-registration generate-command --hostgroup "Application Servers" --insecure 1 --setup-insights 1 --force 1)
ssh -o StrictHostKeyChecking=no rhel1 $REGISTRATION_SCRIPT
ssh -o StrictHostKeyChecking=no rhel2 $REGISTRATION_SCRIPT
```
