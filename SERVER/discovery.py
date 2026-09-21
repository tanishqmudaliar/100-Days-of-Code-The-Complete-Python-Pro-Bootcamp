"""Discover and classify projects stored beside the server."""

import re
from pathlib import Path
from typing import Optional

try:
    from .config import EXCLUDED_FOLDERS, EXCLUDED_PROJECTS, PROJECT_GUIDES
    from .models import Project
except ImportError:
    from config import EXCLUDED_FOLDERS, EXCLUDED_PROJECTS, PROJECT_GUIDES
    from models import Project

SERVER_DIR = Path(__file__).resolve().parent
REPOSITORY_DIR = SERVER_DIR.parent
UNSUPPORTED_IMPORTS = {
    "pygame": "pygame windows are not available on PythonAnywhere",
    "tkinter": "desktop Tkinter windows are not available on PythonAnywhere",
    "turtle": "desktop turtle windows are not available on PythonAnywhere",
}


def slugify(name: str) -> str:
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
    source = entrypoint.read_text(encoding="utf-8", errors="replace").lower()
    for module, reason in UNSUPPORTED_IMPORTS.items():
        if re.search(rf"\b(?:from|import)\s+{re.escape(module)}\b", source):
            return reason
    return None


def discover_projects() -> list[Project]:
    projects = []
    used_slugs: set[str] = set()
    for folder in sorted(REPOSITORY_DIR.iterdir(), key=lambda item: item.name.lower()):
        if not folder.is_dir() or folder.name == SERVER_DIR.name or folder.name.startswith("."):
            continue
        if folder.name in EXCLUDED_FOLDERS or folder.name in EXCLUDED_PROJECTS:
            continue
        files = sorted(
            (file for file in folder.rglob("*.py") if file.is_file()),
            key=lambda item: str(item).lower(),
        )
        slug = slugify(folder.name)
        if slug in used_slugs:
            slug = f"{slug}-{len(used_slugs) + 1}"
        used_slugs.add(slug)
        entrypoint = _entrypoint(folder, files)
        unavailable_reason = _unsupported_reason(entrypoint)
        projects.append(Project(
            name=folder.name,
            slug=slug,
            path=folder,
            entrypoint=entrypoint,
            files=tuple(files),
            runnable=entrypoint is not None and unavailable_reason is None,
            unavailable_reason=unavailable_reason,
            guide=PROJECT_GUIDES.get(folder.name),
        ))
    return projects


def get_project(slug: str) -> Optional[Project]:
    return next((project for project in discover_projects() if project.slug == slug), None)
