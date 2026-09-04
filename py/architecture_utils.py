"""Shared constants and helpers for fdo-architecture.

Holds the one place a date is allowed to appear in generated output
(RELEASE), the path constants, and the writer that keeps docs/index.html
and dist/architecture.mmd byte-identical across repeated runs.
"""

from __future__ import annotations

import pathlib
import sys

import yaml

# The only place a date may appear in generated output. Bump by hand when
# registry.yaml changes in a way worth dating; never call datetime.now().
RELEASE = "2026-09-04"

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGISTRY_YAML = ROOT / "registry.yaml"
DIST_DIR = ROOT / "dist"
DOCS_DIR = ROOT / "docs"
MERMAID_PATH = DIST_DIR / "architecture.mmd"
INDEX_HTML_PATH = DOCS_DIR / "index.html"


def ensure_dirs() -> None:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)


def load_registry() -> dict:
    if not REGISTRY_YAML.exists():
        print(f"error: {REGISTRY_YAML} not found", file=sys.stderr)
        sys.exit(1)
    with REGISTRY_YAML.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not data or "repos" not in data:
        print(f"error: {REGISTRY_YAML} has no top-level 'repos' list", file=sys.stderr)
        sys.exit(1)
    return data


def write_text(path: pathlib.Path, content: str) -> None:
    """Write text deterministically: UTF-8, LF line endings, one trailing newline."""
    normalised = content.replace("\r\n", "\n").rstrip("\n") + "\n"
    path.write_text(normalised, encoding="utf-8", newline="\n")
