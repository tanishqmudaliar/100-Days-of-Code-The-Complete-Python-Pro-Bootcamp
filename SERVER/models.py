"""Domain models used by the project portfolio."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


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
