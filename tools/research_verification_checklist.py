#!/usr/bin/env python3
"""Generate a grounded research verification checklist for a packet.

Reads idea.md and research.md (if present). Prints a concrete checklist
of verification steps for any sources or claims. Extracts potential quantitative
items (digit tokens in non-heading content) from the files for targeted review.
Does not invent sources, URLs, numbers, or citations. Does not write files.

Reduces recurring human verification minutes by standardizing the process and
listing specific items that may need sourcing.
Use before claim_scan and before promoting research.md from stub.
"""

from __future__ import annotations

import argparse
import re
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


def extract_potential_claims(text: str, source_label: str) -> list[str]:
    """Return lines with digit tokens that are not obvious headings/timestamps."""
    claims = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        # Skip pure headings and common structural lines
        if stripped.startswith("#") or stripped.startswith("<!--") or re.match(r"^(Hook|Beat)\s+\d", stripped, re.I):
            continue
        if re.search(r"\(0:\d+–0:\d+\)", stripped) or re.search(r"Beat\s+\d+\s+—", stripped):
            continue
        if re.search(r"\b\d+(?:[.,]\d+)?%?", stripped):
            # Truncate
            display = stripped if len(stripped) <= 140 else stripped[:137] + "..."
            claims.append(f"({source_label}) {display}")
    return claims[:12]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a research verification checklist grounded in the packet (no invented sources)."
    )
    parser.add_argument("packet", help="Packet folder")
    args = parser.parse_args()
    packet = Path(args.packet)
    idea_path = packet / "idea.md"
    research_path = packet / "research.md"
    script_path = packet / "script.md"
    draft_path = packet / "draft.md"

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
    research_text = research_path.read_text(encoding="utf-8", errors="replace") if has_research else ""

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

    # Targeted extraction
    potential = []
    if has_research:
        potential.extend(extract_potential_claims(research_text, "research.md"))
    potential.extend(extract_potential_claims(idea_text, "idea.md"))
    for pth in (script_path, draft_path):
        if pth.is_file():
            txt = pth.read_text(encoding="utf-8", errors="replace")
            potential.extend(extract_potential_claims(txt, pth.name))

    if potential:
        print("Potential quantitative items found (verify each or qualitative-ize):")
        for i, item in enumerate(potential, 1):
            print(f"  {i}. {item}")
        print()
        print("These are non-heading lines containing digits. Confirm sources exist or remove the numbers.")
        print()
        print("Fillable claim-to-source table (paste into sources.md / research.md; fill only Source):")
        print("| Claim excerpt | Source (fill) | Notes |")
        print("|---------------|---------------|-------|")
        for item in potential[:8]:  # limit for readability
            excerpt = item.split(") ", 1)[-1] if ") " in item else item
            excerpt = excerpt[:80].replace("|", "/") + ("..." if len(excerpt) > 80 else "")
            print(f"| {excerpt} |  |  |")
        print()
        print("For spoken WORDS claims specifically, also run: python3 tools/claim_source_table.py PATH")
    else:
        print("No non-heading digit tokens found in idea.md / research.md / script.md / draft.md.")
        print("Keep it that way, or cite before adding any number to spoken WORDS.")
    print()
    print("This checklist standardizes verification so future packets spend fewer human minutes on source checking.")
    print("Do not treat this output as verified sources. Human confirmation is still required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
