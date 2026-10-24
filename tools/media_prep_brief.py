#!/usr/bin/env python3
"""Aggregate media and assembly preparation tools into one brief.

Runs existing no-write (or dry-run) timeline, media_qa, assemble (default dry-run),
and export_probe and prints a unified media prep brief.
Reduces the recurring labor of invoking multiple separate tools and
collecting their outputs before checking assembly readiness or locking a master.
Does not invent media, run ffmpeg, rewrite packets, or call external services.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

SECTIONS = [
    ("TIMELINE PLAN (dry-run)", "timeline.py", ["--dry-run"]),
    ("MEDIA QA (no-write)", "media_qa.py", []),
    ("ASSEMBLY PLANNER (dry-run)", "assemble.py", []),
    ("EXPORT PROBE (no-write)", "export_probe.py", []),
]


def run_tool(script: str, packet: str, extra: list[str]) -> tuple[int, str]:
    """Run one tool and return (returncode, output)."""
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path), packet] + extra
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out.strip()
    except Exception as e:
        return 1, f"EXCEPTION running {script}: {e}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a unified media prep brief from existing tools. No file writes."
    )
    parser.add_argument("packet", help="Packet folder containing script.md (and optionally VO/cards/export)")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("MEDIA PREP BRIEF (unified media and assembly signals; readiness signals only)")
    print("Aggregates existing no-write / dry-run media tools. Hits are signals for human action or media placement, not automatic encoding.")
    print("Run individual tools with --write or --execute only after review. Do not invent media or rematerialize if present.")
    print("=" * 72)
    print()

    any_ok = False
    for title, script, extra in SECTIONS:
        print(f"## {title}")
        print("-" * 40)
        rc, output = run_tool(script, str(path), extra)
        if output and "MISSING" not in output and "REFUSE" not in output.upper()[:20]:
            any_ok = True
            print(output)
        else:
            print(output or f"(no useful output from {script})")
        print()
        print()

    print("=" * 72)
    print("Next: place packet-relative Selected VO and 1920x1080 cards if missing, then re-run this brief or the individual tools.")
    print("Encode only after media_qa PASS and ready_to_assemble=yes (assemble.py --execute). See docs/editor.md and media tools.")
    if not any_ok:
        print("No section produced useful output. Ensure script.md exists; VO and cards may be needed for full signals.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
