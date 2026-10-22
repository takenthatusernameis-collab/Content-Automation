#!/usr/bin/env python3
"""Generate mechanism-aligned thumbnail and end-screen starters from idea.md.

Combines thumbnail_suggest and end_screen_suggest logic into one command.
Prints short thumbnail text candidates and concrete end-screen / CTA candidates.
Grounded in the packet mechanism, problem, and topic. Does not write any files.
Suggestions are starting points only. Run thumbnail_scan.py and end_screen_scan.py after adapting.
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from idea_utils import extract



def suggest_thumbnails(mech: str, problem: str, topic: str) -> list[str]:
    if not mech:
        mech = "written next-action default"
    base = mech.lower()
    candidates = [
        f"Write the {base[:25]}",
        "Name the stall",
        f"Install: {base[:20]}",
        "One default on disk",
        f"Stop deciding. {base[:15]}",
        "Same-day install",
    ]
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower()
        if any(w in low for w in WEAK_THUMB):
            continue
        words = c.split()
        if len(words) > 8:
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())
    return cleaned[:5]

def suggest_end_screens(mech: str, problem: str, topic: str) -> list[str]:
    if not mech:
        mech = "written next-action default"
    base = mech.lower()
    candidates = [
        f"Write the {base[:30]} on disk today.",
        f"Install the {base[:25]} before the next decision.",
        "Name the stall in one sentence and write the default.",
        f"Same-day install: {base[:20]}",
        "One concrete default beats another open decision.",
    ]
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower()
        if any(w in low for w in WEAK_CTA):
            continue
        words = c.split()
        if len(words) > 15 or len(words) < 4:
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())
    return cleaned[:4]

def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after the visual publish starter."""
    p = packet
    return [
        f"adapt thumbnails: paste preferred into publish.md ## Thumbnail or assets.md then python3 tools/thumbnail_scan.py {p}",
        f"adapt end-screen/CTA: paste into publish.md ## End screen or ## CTA then python3 tools/end_screen_scan.py {p}",
        f"metadata starter if needed: python3 tools/metadata_starter.py {p}",
        f"full production view: python3 tools/full_production_starter.py {p}",
        f"quality scans: python3 tools/quality_scan.py {p} && python3 tools/claim_scan.py {p}",
    ]

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate mechanism-aligned thumbnail and end-screen starters.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    print("VISUAL PUBLISH STARTER (thumbnail text + end-screen / CTA; mechanism-aligned)")
    print(f"mechanism: {mech or '(default)'}")
    if problem:
        print(f"problem: {problem}")
    if topic:
        print(f"topic: {topic}")
    print()
    print("## Thumbnail text (prefer <=6 words; paste into publish.md ## Thumbnail or assets.md)")
    for i, t in enumerate(suggest_thumbnails(mech, problem, topic), 1):
        wc = len(t.split())
        print(f"  {i}. {t}  ({wc} words)")
    print()
    print("## End screen / final CTA (concrete action; paste into publish.md ## End screen or ## CTA)")
    for i, t in enumerate(suggest_end_screens(mech, problem, topic), 1):
        wc = len(t.split())
        print(f"  {i}. {t}  ({wc} words)")
    print()
    print("Keep thumbnail text large and high-contrast. Pair with a simple visual of the default or stall.")
    print("The CTA is the concrete next action from the mechanism, not a subscribe or reply prompt.")
    print("After adapting, run tools/thumbnail_scan.py and tools/end_screen_scan.py.")
    print("Do not invent statistics. Keep language calm and operational.")
    print()
    print("=" * 72)
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    print("Preferred unblocked path remains human OAuth (secrets + dispatch) before any live publish.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
