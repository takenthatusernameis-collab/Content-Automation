#!/usr/bin/env python3
"""Generate a complete mechanism-aligned production starter from idea.md.

Combines draft_starter, metadata_starter, and visual_publish_starter into one command.
Prints the full text starting point for a packet: script skeleton, titles, description,
tags, chapters, first comment, thumbnail text, and end-screen / CTA.
Grounded in the packet mechanism, problem, and topic. Does not write any files.
Suggestions are starting points only. Run the individual scanners after adapting.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

def run_starter(script: str, packet: str) -> str:
    """Run one of the starter tools and return its stdout."""
    path = TOOLS / script
    if not path.is_file():
        return f"MISSING {script}"
    try:
        proc = subprocess.run(
            [sys.executable, str(path), packet],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            return f"ERROR from {script}: {proc.stderr.strip() or 'non-zero exit'}"
        return proc.stdout.strip()
    except Exception as e:
        return f"EXCEPTION running {script}: {e}"

def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after the full production starter."""
    p = packet
    return [
        f"write draft skeleton: python3 tools/draft_md_starter.py {p}  # then expand beats",
        f"or expand checklist: python3 tools/draft_beat_expansion_starter.py {p}",
        f"expansion coaches: python3 tools/draft_expansion_coach.py {p} and python3 tools/draft_short_beat_coach.py {p}",
        f"pre-apply gate: python3 tools/draft_pre_apply_coach.py {p}",
        f"quality scans: python3 tools/quality_scan.py {p} && python3 tools/claim_scan.py {p} && python3 tools/title_scan.py {p} && python3 tools/description_scan.py {p}",
        f"more scans: python3 tools/tags_scan.py {p} && python3 tools/first_comment_scan.py {p} && python3 tools/chapters_scan.py {p} && python3 tools/thumbnail_scan.py {p} && python3 tools/end_screen_scan.py {p}",
        f"apply script: python3 tools/apply_script.py {p} --from {p}/draft.md --write --refresh once signals clear",
        f"or research first if needed: python3 tools/research_package_starter.py {p}",
    ]

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate complete mechanism-aligned production starter (draft + metadata + visual publish)."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    packet = args.packet
    idea = Path(packet) / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {packet}")
        return 1

    print("FULL PRODUCTION STARTER (mechanism-aligned; draft + metadata + visual publish in one command)")
    print("Suggestions are starting points only. Adapt, then run the corresponding scanners.")
    print("=" * 72)
    print()

    sections = [
        ("DRAFT STARTER", "draft_starter.py"),
        ("METADATA STARTER", "metadata_starter.py"),
        ("VISUAL PUBLISH STARTER", "visual_publish_starter.py"),
    ]

    for title, script in sections:
        print(f"## {title}")
        print("-" * 40)
        output = run_starter(script, packet)
        # Skip the first header line of each if it duplicates, but print full for clarity
        print(output)
        print()
        print()

    print("=" * 72)
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(packet):
        print(f"- {rec}")
    print()
    print("Copy preferred sections into the packet files (draft.md, titles.md, publish.md, chapters.md, assets.md).")
    print("Expand body beats to word targets, keep total spoken WORDS 900-1500.")
    print("Then run the scanners listed above. Do not invent statistics or anecdotes. Keep language calm and operational.")
    print("Preferred unblocked path remains human OAuth (secrets + dispatch) before any live publish.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
