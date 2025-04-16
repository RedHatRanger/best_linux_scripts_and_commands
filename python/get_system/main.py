```
# pip3 install uv
# uv python install 3.8
# uv python install 3.9.21
# uv run --python 3.8 main.py
# uv run --with rich --with requests --python 3.8 main.py
# uv init --script main.py --python 3.9.21

import sys
from rich import print
import requests

print(sys.version)
```
