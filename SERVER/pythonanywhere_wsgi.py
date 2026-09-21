"""PythonAnywhere WSGI entrypoint."""

import sys
from pathlib import Path

server_directory = Path(__file__).resolve().parent
if str(server_directory) not in sys.path:
    sys.path.insert(0, str(server_directory))

from app import app as application
