#!/usr/bin/env python3
"""Compact every live log in one step, then refuse a file that is still over cap.

Run this in the same commit that prepends a STATE, NEXT, RUNS, PROGRESS, or
FAILURES section. A selftest that ran before that prepend does not keep the
Actions size check green. This tool does not poll OAuth, does not dispatch a
workflow, and does not write packets.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import log_compact  # noqa: E402
import next_compact  # noqa: E402
import runs_compact  # noqa: E402
import state_compact  # noqa: E402

TOOLS = (
    "state_compact.py",
    "next_compact.py",
    "runs_compact.py",
    "log_compact.py",
)


def counts() -> dict[str, int]:
    state = (ROOT / "STATE.md").read_text().count("## Run ")
    _pre, items = next_compact.split_items((ROOT / "NEXT.md").read_text())
    _pre_r, entries, _foot = runs_compact.split_runs((ROOT / "RUNS.md").read_text())
    _pre_p, progress = log_compact.split_sections((ROOT / "PROGRESS.md").read_text())
    _pre_f, failures = log_compact.split_sections((ROOT / "FAILURES.md").read_text())
    return {
        "STATE.md": state,
        "NEXT.md": len(items),
        "RUNS.md": len(entries),
        "PROGRESS.md": len(progress),
        "FAILURES.md": len(failures),
    }


def over_cap(found: dict[str, int]) -> list[str]:
    limits = {
        "STATE.md": state_compact.MAX_RUNS,
        "NEXT.md": next_compact.MAX_ITEMS,
        "RUNS.md": runs_compact.MAX_RUNS,
        "PROGRESS.md": log_compact.MAX_SECTIONS,
        "FAILURES.md": log_compact.MAX_SECTIONS,
    }
    return [
        f"{name} has {found[name]} sections, max {limits[name]}"
        for name in limits
        if found[name] > limits[name]
    ]


def main() -> int:
    check = "--check" in sys.argv
    if not check:
        for name in TOOLS:
            proc = subprocess.run(
                [sys.executable, str(ROOT / "tools" / name)],
                cwd=ROOT,
                text=True,
            )
            if proc.returncode != 0:
                print(f"COMPACT ALL FAIL tool={name}", file=sys.stderr)
                return proc.returncode
    found = counts()
    misses = over_cap(found)
    summary = " ".join(f"{name.split('.')[0]}={found[name]}" for name in found)
    if misses:
        print("COMPACT ALL FAIL " + "; ".join(misses), file=sys.stderr)
        print(summary, file=sys.stderr)
        return 1
    mode = "check" if check else "write"
    print(f"COMPACT ALL OK mode={mode} {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
