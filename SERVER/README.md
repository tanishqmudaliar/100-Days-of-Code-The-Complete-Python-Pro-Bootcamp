# PythonAnywhere server

This Flask app publishes each runnable top-level folder next to `SERVER` as a project.
For example, a folder named `day-1` is available at `/day-1`; `Day 20 & 21`
becomes `/day-20-21`. The folder list is discovered on each request, so new
folders do not require a code change.

## Excluding a folder

Edit `SERVER/config.py` and add its exact folder name to `EXCLUDED_FOLDERS`.
The original course archive is excluded by default because it contains lesson
materials rather than portfolio projects. `EXCLUDED_PROJECTS` is provided for
projects that are too small or unfinished.

Desktop projects using turtle, Tkinter, or pygame are hidden because
PythonAnywhere cannot display their desktop windows. Runnable console projects
have project-specific instructions on their page. The process stays alive while
you answer one prompt at a time, just like a terminal: the next real prompt is
shown only after you submit the current response. Projects that do not need
input run immediately and report the files they generated. They run with the
project folder as the working directory, and requests are subject to the
timeout.

The current runnable projects are Days 16, 17, 24, 26, and 30. Their custom
titles, descriptions, and examples are in `SERVER/config.py`.

Day 24 has a custom web interface: visitors can edit temporary copies of
`starting_letter.txt` and `invited_names.txt`, then generate and read each
personalized letter in the browser. The repository files are never changed.
Days 18–23 are omitted because their projects require desktop windows or
keyboard-controlled GUI loops.

## PythonAnywhere setup

1. Upload/clone this repository.
2. Create a PythonAnywhere web app using Flask.
3. Set the working directory to the repository root and the WSGI file to:
   `SERVER/pythonanywhere_wsgi.py`.
4. Install dependencies in the web app virtualenv with `pip install -r requirements.txt`.

The WSGI file adds `SERVER` to `sys.path`, so the app works without moving any
project folders.
