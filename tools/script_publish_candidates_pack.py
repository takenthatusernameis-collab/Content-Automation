#!/usr/bin/env python3
"""Print a unified publish candidates pack from existing script-derived candidates tools.

Aggregates the no-write script_title_candidates, script_description_candidates,
script_tags_candidates, script_chapter_candidates, script_end_screen_candidates,
script_first_comment_candidates, script_thumbnail_candidates, script_hook_candidates,
script_visual_plan, script_duration_brief, script_objection_candidates, and
script_mechanism_candidates into one overview.
Reduces the recurring labor of invoking multiple separate candidates printers
and collating their structured Markdown sections before drafting titles.md,
publish.md, chapters, end-screens, hooks, or assets for every future packet.
Does not invent content, write files, poll secrets, or call external services.
Exit 0 always (informational).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

SECTIONS = [
    ("HOOK CANDIDATES", "script_hook_candidates.py"),
    ("TITLE CANDIDATES", "script_title_candidates.py"),
    ("DESCRIPTION CANDIDATES", "script_description_candidates.py"),
    ("TAGS CANDIDATES", "script_tags_candidates.py"),
    ("CHAPTER CANDIDATES", "script_chapter_candidates.py"),
    ("END-SCREEN / CTA CANDIDATES", "script_end_screen_candidates.py"),
    ("FIRST COMMENT CANDIDATES", "script_first_comment_candidates.py"),
    ("THUMBNAIL TEXT CANDIDATES", "script_thumbnail_candidates.py"),
    ("OBJECTION / CLARIFICATION CANDIDATES", "script_objection_candidates.py"),
    ("MECHANISM / INSTALLABLE-DEFAULT CANDIDATES", "script_mechanism_candidates.py"),
    ("VISUAL PLAN", "script_visual_plan.py"),
    ("DURATION / PACING BRIEF", "script_duration_brief.py"),
]


def run_tool(script: str, packet: str) -> tuple[int, str]:
    """Run one candidates tool and return (returncode, output)."""
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
        description="Print a unified script-derived publish candidates pack. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("SCRIPT PUBLISH CANDIDATES PACK (unified overview of script-derived starters)")
    print("Aggregates existing no-write candidates tools. Hits and suggestions are starters for human choice, not automatic writes.")
    print("Use individual tools for deeper detail. Do not invent content or commit secrets.")
    print("=" * 72)
    print()

    any_ok = False
    for title, script in SECTIONS:
        print(f"## {title}")
        print("-" * 40)
        rc, output = run_tool(script, str(path))
        if output and "MISSING" not in output and "No script.md" not in output:
            any_ok = True
            # Truncate very long outputs to keep pack readable; full detail is in individual tools.
            lines = output.splitlines()
            if len(lines) > 50:
                print("\n".join(lines[:35]))
                print("\n... (truncated; run the individual tool for full output) ...\n")
                print("\n".join(lines[-8:]))
            else:
                print(output)
        else:
            print(output or f"(no useful output from {script})")
        print()
        print()

    print("=" * 72)
    print("Next: select or rewrite final_choice slots in the relevant files (titles.md, publish.md, chapters, assets.md, or opening script beats).")
    print("Then run the matching scanners (title_scan.py, description_scan.py, etc.) for weak-pattern confirmation.")
    print("This pack does not invent content or write files.")
    print("Useful before publish-stage drafting to reduce multi-command collation on every packet.")
    if not any_ok:
        print("No section produced useful output. Ensure packet has script.md or draft.md.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
