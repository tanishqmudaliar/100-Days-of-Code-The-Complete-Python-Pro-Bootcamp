"""Flask application for the Python project portfolio."""

from __future__ import annotations

import uuid
from urllib.parse import quote

from flask import Flask, abort, render_template, request

try:
    from .config import GITHUB_REPOSITORY_URL
    from .discovery import discover_projects, get_project
    from .sessions import ProjectSession
except ImportError:
    from config import GITHUB_REPOSITORY_URL
    from discovery import discover_projects, get_project
    from sessions import ProjectSession

app = Flask(__name__)
SESSIONS: dict[str, ProjectSession] = {}


def github_folder_url(project) -> str:
    return f"{GITHUB_REPOSITORY_URL}/tree/main/{quote(project.name, safe='')}"


def render_mail_merge(project):
    guide = project.guide or {}
    letter_path = project.path / "Input" / "Letters" / "starting_letter.txt"
    names_path = project.path / "Input" / "Names" / "invited_names.txt"
    letter = letter_path.read_text(encoding="utf-8")
    names = names_path.read_text(encoding="utf-8")
    letters = []
    if request.method == "POST":
        letter = request.form.get("starting_letter", "")
        names = request.form.get("invited_names", "")
        letters = [(name, letter.replace("[name]", name)) for name in names.splitlines() if name.strip()]
    return render_template(
        "mail_merge.html", title=project.name, project=project, guide=guide,
        github_url=github_folder_url(project), letter=letter, names=names, letters=letters,
    )


@app.get("/")
def index():
    return render_template("index.html", title="Python projects",
                           projects=[project for project in discover_projects() if project.runnable])


@app.route("/<slug>", methods=["GET", "POST"])
def project_page(slug: str):
    project = get_project(slug)
    if project is None or not project.runnable:
        abort(404)
    if project.name == "Day 24":
        return render_mail_merge(project)
    session_id = request.form.get("session_id") or request.args.get("session_id") or str(uuid.uuid4())
    session = SESSIONS.get(session_id)
    if session is None or session.project.slug != project.slug:
        session = ProjectSession(project)
        SESSIONS[session_id] = session
    output, waiting = session.advance(request.form.get("input", "") if request.method == "POST" else "")
    if not waiting:
        SESSIONS.pop(session_id, None)
    return render_template(
        "project.html", title=project.name, project=project, guide=project.guide or {},
        github_url=github_folder_url(project), output=output, waiting=waiting, session_id=session_id,
    )


if __name__ == "__main__":
    app.run(debug=True)
