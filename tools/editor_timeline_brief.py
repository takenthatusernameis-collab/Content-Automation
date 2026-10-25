#!/usr/bin/env python3
"""Aggregate timeline planning briefs for editor handoff.

Runs recent no-write tools (script_pacing_brief, card_placement_brief,
end_screen_window, visual_cues_brief) and prints a unified timeline brief.
Reduces recurring labor of sequential calls when preparing the NLE timeline,
card in/out points, and end-screen reservation before assembly on every future packet.
Does not invent content, rewrite files, or call external services.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

SECTIONS = [
    ("PACING", "script_pacing_brief.py"),
    ("CARD PLACEMENT", "card_placement_brief.py"),
    ("END SCREEN", "end_screen_window.py"),
    ("VISUAL CUES", "visual_cues_brief.py"),
]


def run_tool(script: str, packet: str) -> tuple[int, str]:
    """Run one brief and return (returncode, output)."""
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    try:
        proc = subprocess.run(
            [sys.executable, str(path), packet],
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
        description="Unified editor timeline brief from recent no-write tools. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("EDITOR TIMELINE BRIEF (unified pacing / card placement / end-screen / visual cues)")
    print("Aggregates recent no-write tools. Approximate timestamps at 140 wpm; verify with real take.")
    print("Use before timeline planning or assembly. Do not invent content.")
    print("=" * 72)
    print()

    any_ok = False
    for title, script in SECTIONS:
        print(f"## {title}")
        print("-" * 40)
        rc, output = run_tool(script, str(path))
        if output and "MISSING" not in output and "No script.md" not in output:
            any_ok = True
            lines = output.splitlines()
            if len(lines) > 40:
                print("\n".join(lines[:30]))
                print("\n... (truncated; run individual tool for full) ...\n")
                print("\n".join(lines[-8:]))
            else:
                print(output)
        else:
            print(output or f"(no useful output from {script})")
        print()
        print()

    print("=" * 72)
    print("Next: import the approximate card starts into the timeline, reserve the end-screen window, then run assemble.py dry-run.")
    print("This tool writes nothing. Preferred unblocked path remains human OAuth for publish.")
    if not any_ok:
        print("No section produced useful output. Ensure script.md or draft.md exists.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
