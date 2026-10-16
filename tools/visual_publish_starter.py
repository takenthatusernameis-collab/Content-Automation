#!/usr/bin/env python3
"""Generate mechanism-aligned thumbnail and end-screen starters from idea.md.

Combines thumbnail_suggest and end_screen_suggest logic into one command.
Prints short thumbnail text candidates and concrete end-screen / CTA candidates.
Grounded in the packet mechanism, problem, and topic. Does not write any files.
Suggestions are starting points only. Run thumbnail_scan.py and end_screen_scan.py after adapting.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MECH_RE = re.compile(r"mechanism[^\n]*:\s*(.+)", re.I)
PROBLEM_RE = re.compile(r"problem:\s*(.+)", re.I)
TOPIC_RE = re.compile(r"topic:\s*(.+)", re.I)

WEAK_THUMB = (
    "you won't believe", "must watch", "shocking", "secret hack",
    "this changes everything", "one weird trick", "will shock you",
    "don't miss", "watch till the end",
)
WEAK_CTA = (
    "smash the like", "don't forget to", "don’t forget to", "leave a comment",
    "subscribe for more", "hit the subscribe", "like and subscribe",
    "comment below", "what do you think", "let me know",
    "turn on notifications", "ring the bell",
)

def extract(idea_text: str) -> tuple[str, str, str]:
    mech = ""
    problem = ""
    topic = ""
    for line in idea_text.splitlines():
        m = MECH_RE.search(line)
        if m:
            mech = m.group(1).strip().rstrip(".")
        p = PROBLEM_RE.search(line)
        if p:
            problem = p.group(1).strip().rstrip(".")
        t = TOPIC_RE.search(line)
        if t:
            topic = t.group(1).strip().rstrip(".")
    return mech, problem, topic

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
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
