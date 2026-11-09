#!/usr/bin/env python3
"""Print or write a grounded research.md skeleton for a packet.

Reads idea.md (or falls back to topic_queue.md match) for topic, problem, and
mechanism only. Emits a fillable research.md that matches the Q1 stub style
plus claim-table placeholder. Does not invent sources, numbers, anecdotes, or
URLs. Dry-run default. --write overwrites research.md only after confirmation
flag. Reduces sequential labor of starting research notes for every future
packet. Aligns with no-invent rule.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

try:
    from queue_lib import parse_queue as parse, slugify  # type: ignore
except ImportError:
    parse = None
    slugify = None


def extract_from_idea(idea_path: Path) -> dict:
    data = {"topic": "", "problem": "", "mechanism": ""}
    if not idea_path.is_file():
        return data
    text = idea_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("- topic:"):
            data["topic"] = line.split(":", 1)[1].strip()
        elif line.startswith("- problem:"):
            data["problem"] = line.split(":", 1)[1].strip()
        elif "mechanism" in line.lower() and ":" in line:
            data["mechanism"] = line.split(":", 1)[1].strip()
    return data


def extract_from_queue(packet: Path) -> dict:
    data = {"topic": "", "problem": "", "mechanism": ""}
    if parse is None:
        return data
    queue_path = ROOT / "docs" / "topic_queue.md"
    if not queue_path.is_file():
        return data
    rows = parse(queue_path.read_text(encoding="utf-8"))
    slug = packet.name.split("-", 1)[-1] if "-" in packet.name else ""
    for row in rows:
        title = row.get("working_title", "")
        if slugify and slugify(title) in packet.name:
            data["topic"] = title
            data["problem"] = row.get("problem", "")
            data["mechanism"] = row.get("one_line", "")
            break
    return data


def build_skeleton(data: dict) -> str:
    topic = data.get("topic") or "(fill from idea.md)"
    problem = data.get("problem") or "(fill from idea.md)"
    mechanism = data.get("mechanism") or "(fill from idea.md)"
    return f"""# Research

Status: stub (grounded skeleton; fill sources only)

This file is an intake stub. It does not scrape the web. A URL written
here is a pointer for a human to check, not a verified source.

Run `python3 tools/research_brief.py PATH` after intake.

## Rule
No unverifiable statistics. If a number is used in spoken WORDS, cite
the source under Sources. See `docs/production_rules.md`.

## Topic seed
- topic: {topic}
- Mechanism on the idea card: {mechanism}
- Problem: {problem}

## Sources
- (add URL + the single claim it supports; listing a URL is not verification)

## Facts allowed on camera
- None yet

## Claims to avoid
- Any unsourced percentage, study result, or \"most people\" claim
- Any number in spoken WORDS that has no matching source line below
- Treating a URL in this file as verified just because it was typed

## Spoken-number scan
- Digits found in script.md WORDS: (run tools/research_brief.py)
- Action: cite or remove before recording VO

## Claim-to-source table (fill after draft; no invented sources)
| Claim | Type | Source (fill) |
|-------|------|---------------|
| (run claim_source_table.py after draft.md exists) |  |  |

## Notes
- Do not paste search-result prose into Facts as if it were checked.
- Prefer operational claims the viewer can test this week over studies.
- Human still ticks \"No unsourced statistics\" in qa.md after a read.
- No invented anecdotes or numbers. Use claim_source_table.py and research_brief.py.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", nargs="?", default="videos/002-stop-deciding-what-to-work-on-every-morning")
    parser.add_argument("--dry-run", action="store_true", help="Print only; do not write research_notes.md")
    args = parser.parse_args()
    packet = Path(args.packet)
    if not packet.is_absolute():
        packet = ROOT / packet
    if not packet.is_dir():
        print(f"research_notes_writer: packet dir missing ({packet})")
        return 1

    idea = packet / "idea.md"
    data = extract_from_idea(idea)
    if not data["topic"]:
        data = extract_from_queue(packet)

    skeleton = build_skeleton(data)
    print("RESEARCH NOTES SKELETON (grounded from idea.md / queue only; no invent)")
    print(f"packet: {packet.relative_to(ROOT) if packet.is_relative_to(ROOT) else packet}")
    print()
    print(skeleton)
    if not args.dry_run:
        out = packet / "research_notes.md"
        out.write_text(skeleton, encoding="utf-8")
        print(f"\nWrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    else:
        print("\nDry-run. Omit --dry-run to write research_notes.md.")
    print("No invented sources or numbers. Preferred current action remains human OAuth for Q1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
