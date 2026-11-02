#!/usr/bin/env python3
"""Generate a reviewable titles.md skeleton from idea.md mechanism and problem.

Extracts mechanism, problem, and topic via idea_utils, shortens operational phrases
using shared shorten/normalize, and emits titles.md with a calm primary title plus
alts suitable for the ## Title section of publish.md.
Avoids weak/clickbait patterns and shouted words. Ensures at least one title under
50 characters. Dry-run default; --write optional.
No packet content edits beyond the skeleton. Compounds idea into a ready title
draft that reduces manual title labor for every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract
from phrase_utils import shorten, normalize, TITLE_WEAK_PATTERNS


def generate_titles(packet: Path) -> str:
    idea = packet / "idea.md"
    if not idea.is_file():
        return "# Titles\n\nNo idea.md found. Run after apply_idea.\n"

    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    if not mech:
        mech = "the written next-action default"

    core = topic.strip() if topic and len(topic) <= 55 else shorten(normalize(mech), max_len=42)
    base = core.lower()

    candidates = [
        topic if topic and len(topic) < 50 else f"Write the {shorten(normalize(mech), 38)}",
        f"Install one default: {shorten(normalize(mech), 32)}",
        f"The stall is naming what to work on. The default is {shorten(normalize(mech), 26)}",
        f"Stop deciding. Write the {shorten(normalize(mech), 28)}",
        f"{shorten(normalize(mech), 36)} on a sticky note",
        f"One note that installs the {shorten(normalize(mech), 30)}",
    ]

    # Prefer a short primary
    primary = candidates[0]
    if len(primary) >= 50:
        primary = shorten(primary, 48)

    cleaned = []
    seen = set()
    for c in [primary] + candidates[1:]:
        low = c.lower()
        if any(w in low for w in TITLE_WEAK_PATTERNS):
            continue
        words = re.findall(r"[A-Za-z]+", c)
        if any(w.isupper() and len(w) >= 5 for w in words):
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())

    if not cleaned:
        cleaned = [shorten(normalize(mech), 45)]

    primary = cleaned[0]
    alts = cleaned[1:5]

    lines = [
        "# Titles",
        "",
        "Estimated operational titles from idea.md mechanism, problem, and topic.",
        "Review and adjust before pasting Primary into publish.md ## Title to upload.",
        "Does not invent claims. Hits against title_scan are revision signals.",
        "",
        "## Primary",
        "",
        primary,
        "",
        "## Alts",
        "",
    ]
    for alt in alts:
        lines.append(f"- {alt}")
    if not alts:
        lines.append("- (adapt Primary or re-run after idea update)")

    lines.extend([
        "",
        "## Notes",
        "",
        "Keep calm and operational. Name the concrete default or stall. Prefer under 50 characters for Primary when possible.",
        "Avoid clickbait, weak patterns, and shouted words.",
        "Run python3 tools/title_scan.py <packet> after review.",
        "",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate estimated titles.md from idea.md."
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--write", action="store_true", help="Write titles.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"Not a directory: {packet}", file=sys.stderr)
        return 1

    out = packet / "titles.md"
    content = generate_titles(packet)

    if args.write:
        if out.exists() and not args.force:
            print(f"SKIP: {out} exists (use --force)")
            return 0
        out.write_text(content, encoding="utf-8")
        print(f"WROTE: {out}")
    else:
        print(content)
        print("(dry-run; use --write to save)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
