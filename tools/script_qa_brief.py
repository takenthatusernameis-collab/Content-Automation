#!/usr/bin/env python3
"""Aggregate script QA briefs into one early structural overview.

Runs the recent no-write tools (speaking_time_estimate, script_pacing_brief,
visual_cues_brief, script_structure_brief) and prints a unified script QA brief.
Reduces recurring labor of sequential calls for duration, pacing, visual cues,
and format-target checks before recording, card planning, or apply on every future packet.
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
    ("SPEAKING TIME", "speaking_time_estimate.py"),
    ("PACING", "script_pacing_brief.py"),
    ("VISUAL CUES", "visual_cues_brief.py"),
    ("STRUCTURE / TARGET", "script_structure_brief.py"),
]


def run_tool(script: str, packet: str) -> tuple[int, str]:
    """Run one QA brief and return (returncode, output)."""
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
        description="Unified script QA brief from recent no-write tools. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("SCRIPT QA BRIEF (unified early structural / pacing / visual / target check)")
    print("Aggregates recent no-write tools. Signals only; verify with real take and individual tools for detail.")
    print("Use before recording, card planning, or apply_script. Do not invent content.")
    print("=" * 72)
    print()

    any_ok = False
    overall_warn = False
    for title, script in SECTIONS:
        print(f"## {title}")
        print("-" * 40)
        rc, output = run_tool(script, str(path))
        if output and "MISSING" not in output and "No script.md" not in output:
            any_ok = True
            # Keep full short outputs; truncate only if very long.
            lines = output.splitlines()
            if len(lines) > 35:
                print("\n".join(lines[:25]))
                print("\n... (truncated; run individual tool for full) ...\n")
                print("\n".join(lines[-6:]))
            else:
                print(output)
            if rc == 2 or "WARN" in output:
                overall_warn = True
        else:
            print(output or f"(no useful output from {script})")
        print()
        print()

    print("=" * 72)
    if overall_warn:
        print("Overall: WARN — review flags above before recording or asset steps.")
    else:
        print("Overall: PASS — duration, visuals, and structure appear within targets (verify with take).")
    print("Next: address WARNs, then re-run this brief or individual tools.")
    print("Reserve last ~20s for end-screen once duration is confirmed.")
    print("This tool writes nothing. Preferred unblocked path remains human OAuth for publish.")
    if not any_ok:
        print("No section produced useful output. Ensure script.md or draft.md exists.")
        return 1
    return 2 if overall_warn else 0


if __name__ == "__main__":
    sys.exit(main())
