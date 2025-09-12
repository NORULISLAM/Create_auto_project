# agent/tools.py
from __future__ import annotations
from pathlib import Path
from typing import List

from langchain_core.tools import tool

# All generated files live here (served at /preview)
PROJECT_ROOT = Path.cwd() / "generated_site"


def _ensure_root() -> None:
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)


def init_project_root() -> None:
    """Create/clear the output directory used to write generated files."""
    _ensure_root()


def _safe_join(path: str) -> Path:
    """
    Resolve a user-supplied relative path safely under PROJECT_ROOT.
    Prevents path traversal.
    """
    _ensure_root()
    p = (PROJECT_ROOT / path).resolve()
    if PROJECT_ROOT not in p.parents and p != PROJECT_ROOT:
        raise ValueError("Invalid path: must be inside project root")
    return p


@tool("write_file")
def write_file(path: str, content: str) -> str:
    """
    Write a UTF-8 text file at `path` (relative to the project root) with `content`.
    Creates parent folders as needed and overwrites if the file exists.
    Returns the absolute file path string on success.
    """
    p = _safe_join(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return str(p)


@tool("read_file")
def read_file(path: str) -> str:
    """
    Read and return the UTF-8 text content of the file at `path`
    (relative to the project root). Returns an empty string if missing.
    """
    p = _safe_join(path)
    if not p.exists():
        return ""
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # If the model tries to read a binary file, return a hint instead of crashing.
        return "[[binary file]]"


@tool("list_files")
def list_files() -> str:
    """
    Return a newline-separated list of all files (relative paths) in the project root.
    """
    _ensure_root()
    files: List[str] = []
    for fp in PROJECT_ROOT.rglob("*"):
        if fp.is_file():
            files.append(str(fp.relative_to(PROJECT_ROOT)))
    return "\n".join(sorted(files))


@tool("get_current_directory")
def get_current_directory() -> str:
    """
    Return the absolute path to the project root where files are written.
    """
    _ensure_root()
    return str(PROJECT_ROOT)
