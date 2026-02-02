## To revert to a previous working directory via the command:
```bash
pushd <directory>   # This changes to the new directory, but saves the current working directory in a temporary memory to be recalled by popd
```

```bash
popd                # This returns to the temporary saved directory from the pushd command
```

### OPTIONALLY YOU MAY USE `dirs` command to view the previous folders stored in memory
EXAMPLE:
```bash
cd ~/
pushd /tmp
pushd /opt
popd         # Returns to /tmp

#### USE `dirs` to list the saved directories (`dirs -c` clears the memory stack)
pushd /opt
dirs         # lists /opt /tmp ~
popd +1      # takes you back to the 2nd index (/tmp) from the list, so you can take a step back in time skipping a previous one in the stack     
```
