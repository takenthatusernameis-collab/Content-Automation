#!/usr/bin/env python3
"""Aggregate caption preparation tools into one brief.

Runs existing no-write (or dry-run) caption_brief, caption_align, caption_review,
and caption_gate and prints a unified caption prep brief.
Reduces the recurring labor of invoking multiple separate tools and
collecting their outputs before locking captions.md or captions.srt.
Does not rewrite captions, invent timings, or call external services.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

SECTIONS = [
    ("SCRIPT-DERIVED CUES (dry-run)", "caption_brief.py", ["--dry-run"]),
    ("SILENCE-PROPORTIONAL SRT DRAFT (dry-run)", "caption_align.py", ["--dry-run"]),
    ("SPOT-CHECK REVIEW (no-write)", "caption_review.py", []),
    ("CAPTION GATE (no-write)", "caption_gate.py", []),
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
        description="Print a unified caption prep brief from existing tools. No file writes."
    )
    parser.add_argument("packet", help="Packet folder containing script.md (and optionally captions.srt / vo)")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("CAPTION PREP BRIEF (unified caption signals; revision signals only)")
    print("Aggregates existing no-write / dry-run caption tools. Hits are signals for human revision, not automatic rewrites.")
    print("Run individual tools with --write or --force only after review. Do not invent timings or upload estimated cues.")
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
    print("Next: revise cues in captions.md or generate/align captions.srt if signals remain, then re-run this brief or the individual tools.")
    print("Promote only after clear caption gate and human spot-check. See docs/narration.md and caption tools.")
    if not any_ok:
        print("No section produced useful output. Ensure script.md exists; VO may be needed for align/review.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
