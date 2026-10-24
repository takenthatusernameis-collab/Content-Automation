#!/usr/bin/env python3
"""Aggregate research preparation tools into one brief.

Runs existing no-write research_brief_starter (print only), research_source_extract_check,
claim_source_table, and claim_scan and prints a unified research prep brief.
Reduces the recurring labor of invoking multiple separate tools and
collecting their outputs before filling research.md / sources.md or drafting a script.
Does not invent sources, numbers, citations, rewrite packets, or call external services.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

SECTIONS = [
    ("RESEARCH BRIEF STARTER (print only)", "research_brief_starter.py", []),
    ("SOURCE EXTRACT CHECK (preview for claim_scan)", "research_source_extract_check.py", []),
    ("CLAIM SOURCE TABLE (fillable, no invented sources)", "claim_source_table.py", []),
    ("CLAIM SCAN (unsourced digits/hedges)", "claim_scan.py", []),
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
        description="Print a unified research prep brief from existing tools. No file writes."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md (and optionally draft.md / script.md / research.md)")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("RESEARCH PREP BRIEF (unified research and claim signals; readiness signals only)")
    print("Aggregates existing no-write research tools. Hits are signals for human source filling or qualitative rewrite, not automatic content.")
    print("Run individual tools with --write only after review. Do not invent sources, numbers, or citations.")
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
    print("Next: fill Source columns in the table or research.md, then re-run this brief or claim_scan before drafting spoken WORDS.")
    print("See docs/content_quality.md and research tools. No invented claims.")
    if not any_ok:
        print("No section produced useful output. Ensure idea.md exists; draft or script helps for claim table/scan.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
