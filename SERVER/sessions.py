"""Persistent subprocess sessions for terminal-style project interaction."""

import os
import queue
import re
import subprocess
import sys
import threading
import time

try:
    from .config import MAX_OUTPUT_CHARACTERS, RUN_TIMEOUT_SECONDS
    from .models import Project
except ImportError:
    from config import MAX_OUTPUT_CHARACTERS, RUN_TIMEOUT_SECONDS
    from models import Project


class ProjectSession:
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
            if pattern and re.search(pattern, self.output):
                break
        if self.process.poll() is not None:
            ended = True
        if time.monotonic() >= deadline and not ended:
            self.process.kill()
            self.output += f"\n\nThe project exceeded the {RUN_TIMEOUT_SECONDS}-second limit."
            ended = True
        if ended and self.project.name == "Day 24":
            self.output += "\n\nGenerated letters:\n" + "\n".join(
                file.name for file in sorted(
                    (self.project.path / "Output" / "ReadyToSend").glob("letter_for_*.txt")
                )
            )
        display_output = re.sub(r"\n[ \t]+", "\n", self.output)
        if len(display_output) > MAX_OUTPUT_CHARACTERS:
            display_output = display_output[:MAX_OUTPUT_CHARACTERS] + "\n\n[Output truncated]"
        return display_output, not ended

    def close(self):
        if self.process.poll() is None:
            self.process.kill()
