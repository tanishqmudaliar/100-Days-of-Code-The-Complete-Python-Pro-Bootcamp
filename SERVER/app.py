"""Flask application for the Python project portfolio."""

from __future__ import annotations

import random
import uuid
from urllib.parse import quote

from flask import Flask, abort, jsonify, render_template, request, send_from_directory

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
GUI_STATE: dict[str, dict] = {}


def load_flashy_deck(project):
    import pandas
    try:
        data = pandas.read_csv(project.path / "data" / "words_to_learn.csv")
    except FileNotFoundError:
        fr = pandas.read_csv(project.path / "data" / "french_words.csv").rename(columns={"French": "Word"})
        fr["Language"] = "French"
        hi = pandas.read_csv(project.path / "data" / "hindi_words.csv").rename(columns={"Hindi": "Word"})
        hi["Language"] = "Hindi"
        data = pandas.concat([fr, hi], ignore_index=True)
    return data.to_dict(orient="records")


def render_gui_project(project):
    guide = project.guide or {}
    if project.name == "Day 31":
        session_id = request.args.get("session_id") or str(uuid.uuid4())
        state = GUI_STATE.setdefault(session_id, {"deck": load_flashy_deck(project)})
        card = random.choice(state["deck"])
        state["current"] = card
        return render_template(guide["template"], title=guide.get("title", project.name),
                               project=project, card=card, session_id=session_id)
    return render_template(guide["template"], title=guide.get("title", project.name), project=project)


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
        "mail_merge.html", title=guide.get("title", project.name), project=project, guide=guide,
        github_url=github_folder_url(project), letter=letter, names=names, letters=letters,
    )


@app.get("/")
def index():
    return render_template("index.html", title="Live Python Demos",
                           projects=[project for project in discover_projects() if project.runnable])


@app.route("/<slug>", methods=["GET", "POST"])
def project_page(slug: str):
    project = get_project(slug)
    if project is None or not project.runnable:
        abort(404)
    if project.kind == "gui":
        return render_gui_project(project)
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
        "project.html", title=(project.guide or {}).get("title", project.name), project=project, guide=project.guide or {},
        github_url=github_folder_url(project), output=output, waiting=waiting, session_id=session_id,
    )

@app.post("/<slug>/next")
def gui_next(slug: str):
    project = get_project(slug)
    if project is None or project.kind != "gui":
        abort(404)
    payload = request.get_json(force=True)
    session_id = payload.get("session_id") or str(uuid.uuid4())
    state = GUI_STATE.setdefault(session_id, {"deck": load_flashy_deck(project)})
    card = random.choice(state["deck"])
    state["current"] = card
    return jsonify(session_id=session_id, card=card)


@app.post("/<slug>/known")
def gui_known(slug: str):
    project = get_project(slug)
    if project is None or project.kind != "gui":
        abort(404)
    payload = request.get_json(force=True)
    session_id = payload.get("session_id") or str(uuid.uuid4())
    state = GUI_STATE.setdefault(session_id, {"deck": load_flashy_deck(project)})
    current = state.get("current")
    if current in state["deck"]:
        state["deck"].remove(current)
    if not state["deck"]:
        state["deck"] = load_flashy_deck(project)
    card = random.choice(state["deck"])
    state["current"] = card
    return jsonify(session_id=session_id, card=card)


@app.get("/<slug>/assets/<path:filename>")
def project_asset(slug: str, filename: str):
    project = get_project(slug)
    if project is None:
        abort(404)
    return send_from_directory(project.path, filename)


if __name__ == "__main__":
    app.run(debug=True)
