# PythonAnywhere server

This Flask app publishes each top-level folder next to `SERVER` as a project.
For example, a folder named `day-1` is available at `/day-1`; `Day 20 & 21`
becomes `/day-20-21`. The folder list is discovered on each request, so new
folders do not require a code change.

## Excluding a folder

Edit `SERVER/config.py` and add its exact folder name to `EXCLUDED_FOLDERS`.
The original course archive is excluded by default because it contains lesson
materials rather than portfolio projects. `EXCLUDED_PROJECTS` is provided for
projects that are too small or unfinished.

Desktop projects using turtle, Tkinter, or pygame are shown as source-only
because PythonAnywhere cannot display their desktop windows. Console projects
can be run from their project page with optional input, subject to the timeout.

## PythonAnywhere setup

1. Upload/clone this repository.
2. Create a PythonAnywhere web app using Flask.
3. Set the working directory to the repository root and the WSGI file to:
   `SERVER/pythonanywhere_wsgi.py`.
4. Install dependencies in the web app virtualenv with `pip install -r requirements.txt`.

The WSGI file adds `SERVER` to `sys.path`, so the app works without moving any
project folders.
