"""S1 — validate: checks registry.yaml for shape errors and dangling references.

Runnable standalone: python py/step_validate.py [--strict]
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import architecture_utils as au  # noqa: E402

REQUIRED_FIELDS = ("id", "kind", "role", "status", "status_level")
VALID_KINDS = ("repo", "external-system")
VALID_STATUS_LEVELS = ("done", "in-progress", "error")


def run(strict: bool = False) -> int:
    data = au.load_registry()
    repos = data["repos"]

    errors: list[str] = []
    warnings: list[str] = []

    ids = [r.get("id") for r in repos]
    seen: set[str] = set()
    for repo_id in ids:
        if not repo_id:
            errors.append("entry without an 'id'")
            continue
        if repo_id in seen:
            errors.append(f"duplicate id: {repo_id}")
        seen.add(repo_id)

    for repo in repos:
        repo_id = repo.get("id", "<missing id>")
        for field in REQUIRED_FIELDS:
            if not repo.get(field):
                errors.append(f"{repo_id}: missing required field '{field}'")
        if repo.get("kind") not in VALID_KINDS:
            errors.append(f"{repo_id}: kind must be one of {VALID_KINDS}, got {repo.get('kind')!r}")
        if repo.get("status_level") not in VALID_STATUS_LEVELS:
            errors.append(
                f"{repo_id}: status_level must be one of {VALID_STATUS_LEVELS}, "
                f"got {repo.get('status_level')!r}"
            )
        if repo.get("kind") == "repo" and not repo.get("url"):
            warnings.append(f"{repo_id}: kind is 'repo' but 'url' is not set")

        for consumed in repo.get("consumes") or []:
            source = consumed.get("from")
            if source is not None and source not in seen and source not in ids:
                errors.append(
                    f"{repo_id}: consumes.from references unknown id '{source}'"
                )
            if not consumed.get("artifact"):
                warnings.append(f"{repo_id}: a consumes entry has no 'artifact'")

    print(f"registry.yaml: {len(repos)} entries, {len(errors)} errors, {len(warnings)} warnings")
    for w in warnings:
        print(f"  warning: {w}")
    for e in errors:
        print(f"  error: {e}")

    if errors:
        return 1
    if strict and warnings:
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate registry.yaml")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args()
    sys.exit(run(strict=args.strict))
