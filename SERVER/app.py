"""A small PythonAnywhere-friendly portfolio for the course projects."""

from __future__ import annotations

import html
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from flask import Flask, abort, render_template_string, request, url_for

try:
    from config import (
        EXCLUDED_FOLDERS,
        EXCLUDED_PROJECTS,
        MAX_OUTPUT_CHARACTERS,
        RUN_TIMEOUT_SECONDS,
    )
except ImportError:
    from .config import (
        EXCLUDED_FOLDERS,
        EXCLUDED_PROJECTS,
        MAX_OUTPUT_CHARACTERS,
        RUN_TIMEOUT_SECONDS,
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


@dataclass(frozen=True)
class Project:
    name: str
    slug: str
    path: Path
    entrypoint: Optional[Path]
    files: tuple[Path, ...]
    runnable: bool
    unavailable_reason: Optional[str] = None


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
        projects.append(
            Project(
                name=folder.name,
                slug=slug,
                path=folder,
                entrypoint=entrypoint,
                files=tuple(files),
                runnable=entrypoint is not None and unavailable_reason is None,
                unavailable_reason=unavailable_reason,
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
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )
    except subprocess.TimeoutExpired as error:
        output = (error.stdout or "") + (error.stderr or "")
        return f"{output}\n\nThe project exceeded the {RUN_TIMEOUT_SECONDS}-second limit.", False
    except OSError as error:
        return f"Could not start the project: {error}", False

    output = (completed.stdout or "") + (completed.stderr or "")
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
    :root { color-scheme: dark; font-family: system-ui, sans-serif; }
    body { background: #111827; color: #e5e7eb; margin: 0; }
    main { max-width: 960px; margin: auto; padding: 2rem 1rem 4rem; }
    a { color: #93c5fd; } .grid { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); }
    article, .panel { background: #1f2937; border: 1px solid #374151; border-radius: .75rem; padding: 1rem; }
    button { background: #2563eb; border: 0; border-radius: .4rem; color: white; cursor: pointer; padding: .6rem 1rem; }
    textarea { box-sizing: border-box; min-height: 5rem; width: 100%; background: #030712; color: #e5e7eb; border: 1px solid #4b5563; padding: .7rem; }
    pre { background: #030712; border-radius: .5rem; overflow-x: auto; padding: 1rem; white-space: pre-wrap; }
    .muted { color: #9ca3af; } .success { color: #86efac; } .failure { color: #fca5a5; }
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
    for project in discover_projects():
        status = (
            '<span class="success">Runnable</span>'
            if project.runnable
            else f'<span class="muted">{html.escape(project.unavailable_reason or "View only")}</span>'
        )
        cards.append(
            f'<article><h2><a href="{url_for("project_page", slug=project.slug)}">'
            f"{html.escape(project.name)}</a></h2><p>{status}</p>"
            f'<p class="muted">{len(project.files)} Python file(s)</p></article>'
        )
    body = (
        "<h1>My Python projects</h1><p class=\"muted\">"
        "Each folder next to SERVER is automatically published as a project.</p>"
        '<div class="grid">' + "".join(cards) + "</div>"
    )
    return page("Python projects", body)


@app.route("/<slug>", methods=["GET", "POST"])
def project_page(slug: str):
    project = get_project(slug)
    output = ""
    success = True
    if request.method == "POST":
        output, success = run_project(project, request.form.get("input", ""))
    files = "".join(f"<li>{html.escape(relative_file(project, file))}</li>" for file in project.files)
    run_panel = ""
    if project.runnable:
        run_panel = f"""
        <form method="post" class="panel">
          <label for="input">Input (one answer per line)</label>
          <textarea id="input" name="input" placeholder="Optional input for the project"></textarea>
          <p><button type="submit">Run project</button></p>
        </form>
        """
    else:
        run_panel = f'<div class="panel"><p class="muted">{html.escape(project.unavailable_reason or "")}</p></div>'
    result = ""
    if output:
        result = f'<h2>Output</h2><pre class="{"success" if success else "failure"}">{html.escape(output)}</pre>'
    body = (
        f'<p><a href="{url_for("index")}">&larr; All projects</a></p>'
        f"<h1>{html.escape(project.name)}</h1>"
        f"<p class=\"muted\">Entry point: {html.escape(relative_file(project, project.entrypoint)) if project.entrypoint else 'none'}</p>"
        f"{run_panel}{result}<h2>Files</h2><ul>{files or '<li>No Python files</li>'}</ul>"
    )
    return page(project.name, body)


if __name__ == "__main__":
    app.run(debug=True)
