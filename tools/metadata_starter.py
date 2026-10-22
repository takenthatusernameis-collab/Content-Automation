#!/usr/bin/env python3
"""Generate a complete mechanism-aligned metadata skeleton from idea.md.

Combines the logic of the individual *suggest.py tools for the publish phase.
Prints structured starters for titles.md, publish.md (Description, Tags, First comment),
chapters.md, and related fields. Grounded in the packet mechanism, problem, and topic.
Does not write any files. Suggestions are starting points only.
Run the corresponding *_scan.py tools after adapting into the packet files.
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from idea_utils import extract



def suggest_titles(mech: str, problem: str, topic: str) -> list[str]:
    if not mech:
        mech = "the written next-action default"
    base = mech.lower()
    candidates = [
        f"Write the {base} before you open the next tab",
        f"Install one default: {base[:40]}",
        f"The stall is naming what to work on. The default is {base[:30]}",
        f"Stop deciding. Write the {base}",
        f"{base[:45]} on a sticky note",
        f"One note that installs the {base[:35]}",
    ]
    short = f"Write the {base[:35]}"
    if len(short) >= 50:
        short = short[:49]
    candidates.insert(0, short)
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower()
        if any(w in low for w in WEAK_TITLE):
            continue
        words = re.findall(r"[A-Za-z]+", c)
        if any(w.isupper() and len(w) >= 5 for w in words):
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())
    return cleaned[:6]

def suggest_description(mech: str, problem: str, topic: str) -> str:
    if not mech:
        mech = "the written next-action default"
    base = mech.lower()
    problem_part = f" The stall is {problem.lower()}." if problem else ""
    desc = (
        f"Write the exact words of the {base} on a sticky note or device note "
        f"and put it where the stall starts. Do that before you open the next tab."
        f"{problem_part} "
        f"That installs the default in under two minutes."
    )
    return desc.strip()

def suggest_tags(mech: str, problem: str, topic: str) -> list[str]:
    if not mech:
        mech = "written next-action default"
    base = mech.lower()
    candidates = [
        base[:40],
        f"install {base[:30]}",
        "sticky note default",
        "before next tab",
        "under two minutes",
        "written next action",
        "name the stall",
        "one concrete default",
    ]
    if problem:
        short_prob = problem.lower()[:35]
        candidates.append(f"stall: {short_prob}")
    if topic:
        candidates.append(topic.lower()[:40])
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower().strip()
        if not low or len(low) < 3 or len(low) > 40:
            continue
        if any(w in low for w in WEAK_TAG):
            continue
        if low not in seen:
            seen.add(low)
            cleaned.append(c.strip())
    extras = ["operational default", "mechanism install", "no decision stall"]
    for e in extras:
        if len(cleaned) >= 8:
            break
        if e not in seen and len(e) <= 40:
            cleaned.append(e)
            seen.add(e)
    return cleaned[:8]

def suggest_chapters(mech: str, problem: str, topic: str) -> list[str]:
    if not mech:
        mech = "the written next-action default"
    base = mech.lower()
    lines = [
        "0:00 Name the stall",
        "0:45 The concrete default",
        f"1:30 Write the {base[:40]}",
        "2:45 Where it lives on disk",
        "4:00 One under-two-minute install",
        "5:30 Common failure: deciding instead of writing",
        "6:45 The same-day test",
        "7:30 Close with the default still installed",
    ]
    cleaned = []
    for line in lines:
        title = line.split(None, 1)[1] if " " in line else line
        low = title.lower()
        if any(w in low for w in WEAK_CHAPTER):
            continue
        cleaned.append(line)
    if not cleaned or not cleaned[0].startswith("0:00"):
        cleaned.insert(0, "0:00 Name the stall")
    return cleaned[:8]

def suggest_first_comment(mech: str, problem: str) -> str:
    if not mech:
        mech = "the written next-action default"
    assignment = (
        f"Assignment: write the exact words of the {mech.lower()} "
        f"on a sticky note or device note and put it where the stall starts. "
        f"Do that before you open the next tab. That is the whole install."
    )
    return assignment


def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after the metadata starter."""
    p = packet
    return [
        f"adapt titles: paste Primary + alts into titles.md then python3 tools/title_scan.py {p}",
        f"adapt description/tags/first comment: paste into publish.md ## sections then python3 tools/description_scan.py {p} && python3 tools/tags_scan.py {p} && python3 tools/first_comment_scan.py {p}",
        f"adapt chapters: paste lines into chapters.md then python3 tools/chapters_scan.py {p}",
        f"metadata QA report: python3 tools/metadata_qa_report.py {p}",
        f"visual publish next: python3 tools/visual_publish_starter.py {p}",
        f"or full production view: python3 tools/full_production_starter.py {p}",
    ]

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate mechanism-aligned metadata skeleton.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    print("METADATA STARTER (mechanism-aligned skeleton for titles, description, tags, chapters, first comment)")
    print(f"mechanism: {mech or '(default)'}")
    if problem:
        print(f"problem: {problem}")
    if topic:
        print(f"topic: {topic}")
    print()
    print("## Titles (paste Primary + alts into titles.md)")
    for i, t in enumerate(suggest_titles(mech, problem, topic), 1):
        print(f"  {i}. {t}  ({len(t)} chars)")
    print()
    print("## Description (paste into publish.md ## Description)")
    print(suggest_description(mech, problem, topic))
    print()
    print("## Tags (paste bullet list into publish.md ## Tags)")
    for t in suggest_tags(mech, problem, topic):
        print(f"- {t}")
    print()
    print("## Chapters (paste into chapters.md; adjust times after VO)")
    for line in suggest_chapters(mech, problem, topic):
        print(line)
    print()
    print("## First comment (paste into publish.md ## First comment)")
    print(suggest_first_comment(mech, problem))
    print()
    print("Adapt preferred lines into the packet files, then run the corresponding *_scan.py tools.")
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
