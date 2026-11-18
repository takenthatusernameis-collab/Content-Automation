#!/usr/bin/env python3
"""Generate a grounded research verification checklist for a packet.

Reads idea.md and research.md (if present). Prints a concrete checklist
of verification steps for any sources or claims. Does not invent sources,
URLs, numbers, or citations. Does not write files.

Reduces recurring human verification minutes by standardizing the process.
Use before claim_scan and before promoting research.md from stub.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

try:
    from idea_utils import extract as idea_extract
except ImportError:
    def idea_extract(text: str):
        return "", "", ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a research verification checklist grounded in the packet (no invented sources)."
    )
    parser.add_argument("packet", help="Packet folder")
    args = parser.parse_args()
    packet = Path(args.packet)
    idea_path = packet / "idea.md"
    research_path = packet / "research.md"

    if not idea_path.is_file():
        print(f"No idea.md in {packet}")
        return 1

    idea_text = idea_path.read_text(encoding="utf-8", errors="replace")
    mech, problem, topic = idea_extract(idea_text)
    mech = mech or "unspecified mechanism"
    problem = problem or "unspecified problem"
    topic = topic or "unspecified topic"

    has_research = research_path.is_file()
    research_status = "present" if has_research else "absent"

    print("RESEARCH VERIFICATION CHECKLIST")
    print(f"Packet: {packet}")
    print(f"Topic: {topic}")
    print(f"Mechanism: {mech}")
    print(f"Problem: {problem}")
    print(f"research.md: {research_status}")
    print("=" * 60)
    print()
    print("Standard verification steps (do not invent sources):")
    print("1. Confirm every number or percentage in spoken WORDS (script.md / draft.md) has a matching source line in research.md or sources.md.")
    print("2. For each source URL or citation, open it and confirm it supports the exact claim (not just related).")
    print("3. Prefer primary sources or operational claims the viewer can test this week over secondary summaries.")
    print("4. Remove or qualitative-ize any unsourced statistic before apply_script --write.")
    print("5. Run after updates:")
    print(f"   python3 tools/claim_scan.py {packet}")
    print(f"   python3 tools/research_brief.py {packet}")
    print("6. Tick 'No unsourced statistics' in qa.md only after human read of the sources.")
    print()
    print("Packet-specific notes:")
    print(f"- Mechanism '{mech}' should be demonstrated with concrete scenes, not studies, unless a source is already present.")
    print(f"- Problem '{problem}' is the stall to show; keep claims operational.")
    if has_research:
        print("- research.md exists; review its Sources and Facts sections against the checklist above.")
    else:
        print("- No research.md yet. Use python3 tools/research_sources_starter.py to generate a template, then fill and verify.")
    print()
    print("This checklist standardizes verification so future packets spend fewer human minutes on source checking.")
    print("Do not treat this output as verified sources. Human confirmation is still required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
