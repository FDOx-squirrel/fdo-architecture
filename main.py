"""fdo-architecture orchestrator — the only entry point.

    python main.py                     all steps, in order
    python main.py --list              print steps and exit
    python main.py --only render       one step
    python main.py --from render       this step and everything after
    python main.py --skip validate     everything but this
    python main.py --dry-run           print the plan, run nothing
    python main.py --strict            warnings become errors (this is what CI runs)

There is no fetch step: registry.yaml is hand-maintained, not harvested, so
the whole pipeline runs offline against it.
"""

from __future__ import annotations

import argparse
import importlib
import io
import os
import pathlib
import sys
import time
from contextlib import redirect_stdout

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "py"))

ROOT = pathlib.Path(__file__).resolve().parent

# (id, module name, entry function, one-line description)
STEPS = [
    ("validate", "step_validate", "run", "Check registry.yaml for shape errors and dangling references"),
    ("render", "step_render", "run", "Build dist/architecture.mmd and docs/index.html from registry.yaml"),
]

STEP_IDS = [s[0] for s in STEPS]


def select_steps(only: str | None, frm: str | None, skip: str | None) -> list[tuple]:
    steps = STEPS
    if only:
        if only not in STEP_IDS:
            sys.exit(f"error: unknown step '{only}' (choices: {', '.join(STEP_IDS)})")
        return [s for s in steps if s[0] == only]
    if frm:
        if frm not in STEP_IDS:
            sys.exit(f"error: unknown step '{frm}' (choices: {', '.join(STEP_IDS)})")
        idx = STEP_IDS.index(frm)
        steps = steps[idx:]
    if skip:
        if skip not in STEP_IDS:
            sys.exit(f"error: unknown step '{skip}' (choices: {', '.join(STEP_IDS)})")
        steps = [s for s in steps if s[0] != skip]
    return steps


def run_step(step_id: str, module_name: str, func_name: str, strict: bool) -> tuple[int, str, float]:
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    buf = io.StringIO()
    start = time.perf_counter()
    try:
        with redirect_stdout(buf):
            try:
                exit_code = func(strict=strict)
            except TypeError:
                exit_code = func()
    except SystemExit as exc:
        exit_code = exc.code if isinstance(exc.code, int) else 1
    elapsed = time.perf_counter() - start
    return (exit_code or 0), buf.getvalue(), elapsed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--list", action="store_true", help="print steps and exit")
    parser.add_argument("--only", metavar="STEP", help="run exactly one step")
    parser.add_argument("--from", dest="frm", metavar="STEP", help="run this step and everything after")
    parser.add_argument("--skip", metavar="STEP", help="run everything but this step")
    parser.add_argument("--dry-run", action="store_true", help="print the plan, run nothing")
    parser.add_argument("--strict", action="store_true", help="warnings become errors")
    args = parser.parse_args()

    if args.list:
        for step_id, _, _, desc in STEPS:
            print(f"{step_id:10s} {desc}")
        return 0

    steps = select_steps(args.only, args.frm, args.skip)

    if args.dry_run:
        print("plan:")
        for step_id, _, _, desc in steps:
            print(f"  {step_id:10s} {desc}")
        return 0

    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

    report_lines: list[str] = []
    timings: list[tuple[str, float]] = []
    overall_ok = True

    for step_id, module_name, func_name, desc in steps:
        print(f"== {step_id} — {desc} ==")
        exit_code, output, elapsed = run_step(step_id, module_name, func_name, args.strict)
        for line in output.rstrip("\n").splitlines():
            print(f"  {line}")
        report_lines.append(f"== {step_id} ({elapsed:.2f}s, exit {exit_code}) ==")
        report_lines.append(output.rstrip("\n"))
        timings.append((step_id, elapsed))
        if exit_code != 0:
            overall_ok = False
            print(f"step '{step_id}' failed with exit code {exit_code}")
            break

    total = sum(t for _, t in timings)
    report_lines.append("")
    report_lines.append("timing:")
    for step_id, elapsed in timings:
        share = (elapsed / total * 100) if total else 0
        report_lines.append(f"  {step_id:10s} {elapsed:6.2f}s  ({share:5.1f}%)")
        print(f"  {step_id:10s} {elapsed:6.2f}s  ({share:5.1f}%)")

    dist_dir = ROOT / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)
    (dist_dir / "pipeline_report.txt").write_text(
        "\n".join(report_lines).rstrip("\n") + "\n", encoding="utf-8", newline="\n"
    )

    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
