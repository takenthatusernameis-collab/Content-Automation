#!/usr/bin/env python3
"""Aggregate all major prep briefs into one full packet overview.

Runs the existing no-write research_prep_brief, quality_prep_brief,
editor_prep_brief, caption_prep_brief, media_prep_brief, publish_prep_brief,
and metadata_prep_brief and prints a unified full packet preparation brief.
Reduces the recurring labor of invoking multiple separate briefs and
collecting their outputs before deciding readiness or locking any stage.
Does not rewrite files, invent content, or call external services.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

SECTIONS = [
    ("RESEARCH PREP", "research_prep_brief.py"),
    ("QUALITY PREP", "quality_prep_brief.py"),
    ("EDITOR PREP", "editor_prep_brief.py"),
    ("CAPTION PREP", "caption_prep_brief.py"),
    ("MEDIA PREP", "media_prep_brief.py"),
    ("PUBLISH PREP", "publish_prep_brief.py"),
    ("METADATA PREP", "metadata_prep_brief.py"),
]


def run_tool(script: str, packet: str) -> tuple[int, str]:
    """Run one prep brief and return (returncode, output)."""
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
        description="Print a unified full packet prep brief from existing stage briefs. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("FULL PACKET PREP BRIEF (unified overview of all stage prep signals)")
    print("Aggregates existing no-write prep briefs. Hits are signals for human revision, not automatic actions.")
    print("Use individual briefs or scanners for deeper detail or hard gates. Do not invent content.")
    print("=" * 72)
    print()

    any_ok = False
    for title, script in SECTIONS:
        print(f"## {title}")
        print("-" * 40)
        rc, output = run_tool(script, str(path))
        if output and "MISSING" not in output:
            any_ok = True
            # Truncate very long outputs to keep brief readable; full detail is in individual tools.
            lines = output.splitlines()
            if len(lines) > 40:
                print("\n".join(lines[:30]))
                print("\n... (truncated; run the individual brief for full output) ...\n")
                print("\n".join(lines[-5:]))
            else:
                print(output)
        else:
            print(output or f"(no useful output from {script})")
        print()
        print()

    print("=" * 72)
    print("Next: address any remaining hits in the relevant stage, then re-run this brief or individual tools.")
    print("Lock stages only after clear signals. See docs/content_quality.md and docs/production_rules.md.")
    if not any_ok:
        print("No section produced useful output. Ensure packet files exist.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
