"""A small PythonAnywhere-friendly portfolio for the course projects."""

from __future__ import annotations

import html
import os
import re
import subprocess
import sys
import queue
import threading
import time
import uuid
from urllib.parse import quote
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from flask import Flask, abort, render_template_string, request, url_for

try:
    from config import (
        EXCLUDED_FOLDERS,
        EXCLUDED_PROJECTS,
        MAX_OUTPUT_CHARACTERS,
        PROJECT_GUIDES,
        RUN_TIMEOUT_SECONDS,
        GITHUB_REPOSITORY_URL,
    )
except ImportError:
    from .config import (
        EXCLUDED_FOLDERS,
        EXCLUDED_PROJECTS,
        MAX_OUTPUT_CHARACTERS,
        PROJECT_GUIDES,
        RUN_TIMEOUT_SECONDS,
        GITHUB_REPOSITORY_URL,
    )


SERVER_DIR = Path(__file__).resolve().parent
REPOSITORY_DIR = SERVER_DIR.parent
PYTHON_SUFFIXES = {".py"}
UNSUPPORTED_IMPORTS = {
    "pygame": "pygame windows are not available on PythonAnywhere",
    "tkinter": "desktop Tkinter windows are not available on PythonAnywhere",
    "turtle": "desktop turtle windows are not available on PythonAnywhere",
}

app = Flask(__name__)
SESSIONS: dict[str, "ProjectSession"] = {}


@dataclass(frozen=True)
class Project:
    name: str
    slug: str
    path: Path
    entrypoint: Optional[Path]
    files: tuple[Path, ...]
    runnable: bool
    unavailable_reason: Optional[str] = None
    guide: dict[str, str] | None = None


class ProjectSession:
    """Keep one real project process alive while a visitor answers prompts."""

    def __init__(self, project: Project):
        self.project = project
        self.process = subprocess.Popen(
            [sys.executable, str(project.entrypoint)],
            cwd=project.path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            env={**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONIOENCODING": "utf-8"},
        )
        self.output_queue: queue.Queue[str | None] = queue.Queue()
        self.output = ""
        threading.Thread(target=self._read_output, daemon=True).start()

    def _read_output(self):
        assert self.process.stdout is not None
        for character in iter(lambda: self.process.stdout.read(1), ""):
            self.output_queue.put(character)
        self.output_queue.put(None)

    def advance(self, answer: str = "") -> tuple[str, bool]:
        if answer:
            if self.process.stdin is None:
                return "The project input stream is unavailable.", False
            self.process.stdin.write(answer + "\n")
            self.process.stdin.flush()
            self.output += answer + "\n"

        pattern = self.project.guide.get("prompt_pattern") if self.project.guide else None
        prompt_pattern = re.compile(pattern) if pattern else None
        deadline = time.monotonic() + RUN_TIMEOUT_SECONDS
        ended = False
        while time.monotonic() < deadline:
            try:
                character = self.output_queue.get(timeout=0.1)
            except queue.Empty:
                if self.process.poll() is not None:
                    ended = True
                    break
                continue
            if character is None:
                ended = True
                break
            self.output += character
            if prompt_pattern and prompt_pattern.search(self.output):
                break
        if self.process.poll() is not None:
            ended = True
        if time.monotonic() >= deadline and not ended:
            self.process.kill()
            self.output += f"\n\nThe project exceeded the {RUN_TIMEOUT_SECONDS}-second limit."
            ended = True
        if ended and self.project.name == "Day 24":
            generated = sorted(
                file.name
                for file in (self.project.path / "Output" / "ReadyToSend").glob("letter_for_*.txt")
            )
            self.output += (
                "\n\nGenerated letters:\n" + "\n".join(generated)
                if generated
                else "\n\nNo letters were generated."
            )
        # Piped stdin does not provide a real terminal line echo. Reconstruct
        # it once, without retaining the padding some prompts acquire when
        # consecutive input() calls are rendered together.
        # A piped Python process can leave a padding space after an input
        # prompt. It is not part of the project's printed output.
        display_output = re.sub(r"\n[ \t]+", "\n", self.output)
        return display_output, not ended

    def close(self):
        if self.process.poll() is None:
            self.process.kill()


def slugify(name: str) -> str:
    """Turn a folder name into a stable URL segment."""
    value = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return value or "project"


def _entrypoint(folder: Path, files: list[Path]) -> Optional[Path]:
    for candidate in ("app.py", "main.py", "solution.py"):
        match = next((file for file in files if file.name.lower() == candidate), None)
        if match:
            return match
    return files[0] if files else None


def _unsupported_reason(entrypoint: Optional[Path]) -> Optional[str]:
    if entrypoint is None:
        return "There is no Python entrypoint in this folder."
    try:
        source = entrypoint.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        return f"Unable to inspect the entrypoint: {error}"
    lowered = source.lower()
    for module, reason in UNSUPPORTED_IMPORTS.items():
        if re.search(rf"\b(?:from|import)\s+{re.escape(module)}\b", lowered):
            return reason
    return None


def discover_projects() -> list[Project]:
    """Discover top-level project folders on every request.

    This intentionally avoids a hard-coded day list: creating a new folder
    next to SERVER is enough to make it appear at /<folder-slug>.
    """
    projects: list[Project] = []
    used_slugs: set[str] = set()
    for folder in sorted(REPOSITORY_DIR.iterdir(), key=lambda item: item.name.lower()):
        if (
            not folder.is_dir()
            or folder.name == SERVER_DIR.name
            or folder.name.startswith(".")
        ):
            continue
        if folder.name in EXCLUDED_FOLDERS or folder.name in EXCLUDED_PROJECTS:
            continue
        files = sorted(
            (
                file
                for file in folder.rglob("*")
                if file.is_file() and file.suffix.lower() in PYTHON_SUFFIXES
            ),
            key=lambda item: str(item).lower(),
        )
        slug = slugify(folder.name)
        if slug in used_slugs:
            slug = f"{slug}-{len(used_slugs) + 1}"
        used_slugs.add(slug)
        entrypoint = _entrypoint(folder, files)
        unavailable_reason = _unsupported_reason(entrypoint)
        guide = PROJECT_GUIDES.get(folder.name)
        projects.append(
            Project(
                name=folder.name,
                slug=slug,
                path=folder,
                entrypoint=entrypoint,
                files=tuple(files),
                runnable=entrypoint is not None and unavailable_reason is None,
                unavailable_reason=unavailable_reason,
                guide=guide,
            )
        )
    return projects


def get_project(slug: str) -> Project:
    project = next((item for item in discover_projects() if item.slug == slug), None)
    if project is None:
        abort(404)
    return project


def relative_file(project: Project, file: Path) -> str:
    return file.relative_to(project.path).as_posix()


def github_folder_url(project: Project) -> str:
    folder_path = quote(project.name, safe="")
    return f"{GITHUB_REPOSITORY_URL}/tree/main/{folder_path}"


def render_mail_merge(project: Project):
    guide = project.guide or {}
    letter_path = project.path / "Input" / "Letters" / "starting_letter.txt"
    names_path = project.path / "Input" / "Names" / "invited_names.txt"
    letter = letter_path.read_text(encoding="utf-8")
    names = names_path.read_text(encoding="utf-8")
    letters: list[tuple[str, str]] = []
    if request.method == "POST":
        letter = request.form.get("starting_letter", "")
        names = request.form.get("invited_names", "")
        letters = [
            (name, letter.replace("[name]", name))
            for name in names.splitlines()
            if name.strip()
        ]
    editor = f"""
      <form method="post" class="mail-merge">
        <div class="editor-grid">
          <label>starting_letter.txt
            <textarea name="starting_letter" rows="12">{html.escape(letter)}</textarea>
          </label>
          <label>invited_names.txt
            <textarea name="invited_names" rows="12">{html.escape(names)}</textarea>
          </label>
        </div>
        <p class="muted">Edit these temporary copies for this run. Your repository files are not changed.</p>
        <button type="submit">Generate letters</button>
      </form>
    """
    result = ""
    if letters:
        result = "<h2>Generated letters</h2><div class=\"letters\">" + "".join(
            f"<article><h3>letter_for_{html.escape(name)}.txt</h3><pre>{html.escape(content)}</pre></article>"
            for name, content in letters
        ) + "</div>"
    body = (
        f'<p><a class="back-link" href="{url_for("index")}">&larr; All projects</a></p>'
        f'<p class="eyebrow">Interactive project</p><h1>{html.escape(guide.get("title", project.name))}</h1>'
        f"<p>{html.escape(guide.get('description', ''))}</p>"
        f'<div class="actions"><a class="button" href="{html.escape(github_folder_url(project))}" target="_blank" rel="noopener">View folder on GitHub</a></div>'
        f"<p class=\"muted\">{html.escape(guide.get('instructions', ''))}</p>"
        f"{editor}{result}"
    )
    return page(project.name, body)


def run_project(project: Project, user_input: str) -> tuple[str, bool]:
    if not project.runnable or project.entrypoint is None:
        return project.unavailable_reason or "This project cannot be run here.", False
    try:
        completed = subprocess.run(
            [sys.executable, str(project.entrypoint)],
            cwd=project.path,
            input=user_input,
            capture_output=True,
            text=True,
            timeout=RUN_TIMEOUT_SECONDS,
            check=False,
            env={**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONIOENCODING": "utf-8"},
        )
    except subprocess.TimeoutExpired as error:
        output = (error.stdout or "") + (error.stderr or "")
        return f"{output}\n\nThe project exceeded the {RUN_TIMEOUT_SECONDS}-second limit.", False
    except OSError as error:
        return f"Could not start the project: {error}", False

    output = (completed.stdout or "") + (completed.stderr or "")
    if project.name == "Day 24":
        generated = sorted(
            file.name
            for file in (project.path / "Output" / "ReadyToSend").glob("letter_for_*.txt")
        )
        output += (
            "\n\nGenerated letters:\n"
            + "\n".join(generated)
            if generated
            else "\n\nNo letters were generated."
        )
    if len(output) > MAX_OUTPUT_CHARACTERS:
        output = output[:MAX_OUTPUT_CHARACTERS] + "\n\n[Output truncated]"
    return output or "(The project produced no output.)", completed.returncode == 0


PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }}</title>
  <style>
    :root { color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }
    body { background: radial-gradient(circle at top, #172554, #0b1120 48%); color: #e5e7eb; margin: 0; min-height: 100vh; }
    main { max-width: 1050px; margin: auto; padding: 3rem 1.25rem 5rem; }
    a { color: #58a6ff; text-decoration: none; } a:hover { color: #79c0ff; text-decoration: none; }
    a:focus-visible, button:focus-visible, input:focus-visible, textarea:focus-visible { outline: 2px solid #58a6ff; outline-offset: 3px; }
    .hero { margin-bottom: 2rem; } .eyebrow { color: #58a6ff; font-size: .8rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }
    .grid { display: grid; gap: 1.2rem; grid-template-columns: repeat(auto-fit, minmax(270px, 1fr)); }
    article, .panel { background: #161b22; border: 1px solid #30363d; border-radius: .75rem; box-shadow: 0 12px 30px rgba(0,0,0,.18); padding: 1.25rem; }
    .panel + .panel, .panel + pre, pre + .panel { margin-top: 1.5rem; }
    article { transition: transform .15s, border-color .15s, box-shadow .15s; } article:hover { border-color: #58a6ff; box-shadow: 0 16px 35px rgba(0,0,0,.28); transform: translateY(-3px); }
    article h2 a { color: #f0f6fc; } article h2 a:hover { color: #58a6ff; }
    button, .button { background: #238636; border: 1px solid rgba(240,246,252,.1); border-radius: .45rem; box-shadow: 0 1px 0 rgba(31,35,40,.1); color: #fff; cursor: pointer; display: inline-block; font-weight: 700; padding: .65rem 1rem; text-decoration: none; }
    button:hover, .button:hover { background: #2ea043; color: #fff; text-decoration: none; }
    textarea { box-sizing: border-box; min-height: 8rem; width: 100%; background: #0d1117; border: 1px solid #30363d; border-radius: .45rem; color: #e5e7eb; padding: .8rem; resize: vertical; }
    .actions { margin: 1.25rem 0; } .button { background: #334155; border-radius: .55rem; color: #e2e8f0; display: inline-block; font-weight: 700; padding: .7rem 1rem; text-decoration: none; } .button:hover { background: #475569; }
    .mail-merge { margin-top: 1.5rem; } .editor-grid { display: grid; gap: 1rem; grid-template-columns: repeat(2, minmax(0, 1fr)); } label { color: #cbd5e1; font-weight: 700; } label textarea { display: block; margin-top: .5rem; }
    .letters { display: grid; gap: 1rem; } .letters article { box-shadow: none; } .letters pre { margin: 0; }
    input { box-sizing: border-box; width: 100%; background: #0d1117; border: 1px solid #30363d; border-radius: .45rem; color: #e5e7eb; margin-top: .5rem; padding: .8rem; }
    .terminal { background: #0d1117; border: 1px solid #30363d; border-radius: .65rem; box-shadow: 0 20px 50px rgba(0,0,0,.3); margin-top: 1.5rem; overflow: hidden; }
    .terminal-bar { align-items: center; background: #161b22; border-bottom: 1px solid #30363d; color: #8b949e; display: flex; gap: .45rem; padding: .7rem 1rem; }
    .terminal-dot { border-radius: 50%; height: .65rem; width: .65rem; } .red { background: #f87171; } .yellow { background: #facc15; } .green { background: #4ade80; }
    .terminal pre { border: 0; border-radius: 0; margin: 0; min-height: 12rem; padding: 1rem; }
    .terminal-form { border-top: 1px solid #1e293b; display: flex; gap: .7rem; padding: .8rem 1rem; }
    .terminal-form input { background: #0d1117; border: 1px solid #30363d; flex: 1; margin: 0; }
    .terminal-form button { padding: .65rem 1rem; }
    pre { background: #020617; border: 1px solid #1e293b; border-radius: .6rem; overflow-x: auto; padding: 1rem; white-space: pre-wrap; margin: 1.5rem 0; }
    .muted { color: #8b949e; } .success { color: #7ee787; } .failure { color: #ff7b72; } .tag { background: #1f6feb33; border: 1px solid #1f6feb66; border-radius: 999px; color: #79c0ff; display: inline-block; font-size: .75rem; font-weight: 700; padding: .25rem .55rem; }
    .back-link { background: #21262d; border: 1px solid #30363d; border-radius: .45rem; color: #c9d1d9; display: inline-block; font-size: .9rem; font-weight: 600; margin-bottom: 1.5rem; padding: .55rem .8rem; }
    .back-link:hover { background: #30363d; color: #fff; }
    ol { padding-left: 1.25rem; } li { margin: .4rem 0; }
  </style>
</head>
<body><main>{{ body|safe }}</main></body>
</html>
"""


def page(title: str, body: str):
    return render_template_string(PAGE, title=title, body=body)


@app.get("/")
def index():
    cards = []
    runnable_projects = [project for project in discover_projects() if project.runnable]
    for project in runnable_projects:
        guide = project.guide or {}
        cards.append(
            f'<article><h2>{html.escape(guide.get("title", project.name))}</h2>'
            f'<p>{html.escape(guide.get("description", "Interactive Python project."))}</p>'
            f'<span class="tag">Runnable locally</span>'
            f'<p><a class="button" href="{url_for("project_page", slug=project.slug)}">Open project</a></p></article>'
        )
    body = (
        '<div class="hero"><p class="eyebrow">Python portfolio</p><h1>Projects you can try</h1><p class="muted">'
        "These projects run from the browser using the same Python files in this repository. "
        "Desktop-only projects are intentionally hidden.</p></div>"
        '<div class="grid">' + "".join(cards) + "</div>"
    )
    return page("Python projects", body)


@app.route("/<slug>", methods=["GET", "POST"])
def project_page(slug: str):
    project = get_project(slug)
    if not project.runnable:
        abort(404)
    if project.name == "Day 24":
        return render_mail_merge(project)
    session_id = request.form.get("session_id") or request.args.get("session_id") or str(uuid.uuid4())
    project_session = SESSIONS.get(session_id)
    if project_session is None or project_session.project.slug != project.slug:
        project_session = ProjectSession(project)
        SESSIONS[session_id] = project_session
    answer = request.form.get("input", "") if request.method == "POST" else ""
    output, waiting = project_session.advance(answer)
    guide = project.guide or {}
    terminal_form = ""
    if not waiting:
        SESSIONS.pop(session_id, None)
        terminal_form = '<div class="terminal-form"><span class="muted">Process finished. Refresh to run it again.</span></div>'
    else:
        terminal_form = f"""
          <form method="post" class="terminal-form">
            <input id="input" name="input" autocomplete="off" autofocus required
                   placeholder="Type the response to the prompt above">
            <input type="hidden" name="session_id" value="{html.escape(session_id)}">
            <button type="submit">Send</button>
          </form>
        """
    result = f"""
      <div class="terminal">
        <div class="terminal-bar">
          <span class="terminal-dot red"></span><span class="terminal-dot yellow"></span><span class="terminal-dot green"></span>
          <span>project terminal</span>
        </div>
        <pre class="{"success" if waiting else "failure"}">{html.escape(output)}</pre>
        {terminal_form}
      </div>
    """
    body = (
        f'<p><a class="back-link" href="{url_for("index")}">&larr; All projects</a></p>'
        f'<p class="eyebrow">Interactive project</p><h1>{html.escape(guide.get("title", project.name))}</h1>'
        f"<p>{html.escape(guide.get('description', ''))}</p>"
        f"<p class=\"muted\">Entry point: {html.escape(relative_file(project, project.entrypoint)) if project.entrypoint else 'none'}</p>"
        f'<div class="actions"><a class="button" href="{html.escape(github_folder_url(project))}" target="_blank" rel="noopener">View folder on GitHub</a></div>'
        f'<p class="muted">{html.escape(guide.get("instructions", ""))}</p>'
        f"{result}"
    )
    return page(project.name, body)


if __name__ == "__main__":
    app.run(debug=True)
