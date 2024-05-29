```
#!/bin/bash
echo "This program is called $0 and it has $# args"
echo "This program is $(basename $0) and it has $# args"
ps -f -p $1
```
