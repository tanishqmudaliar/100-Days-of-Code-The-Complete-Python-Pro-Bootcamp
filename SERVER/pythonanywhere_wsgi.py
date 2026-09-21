"""PythonAnywhere WSGI entrypoint."""

import sys
from pathlib import Path

server_directory = Path(
    "/home/YOUR_PYTHONANYWHERE_USERNAME/"
    "100-Days-of-Code-The-Complete-Python-Pro-Bootcamp/SERVER"
)

if str(server_directory) not in sys.path:
    sys.path.insert(0, str(server_directory))

from app import app as application