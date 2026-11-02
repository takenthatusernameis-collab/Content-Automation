#!/usr/bin/env python3
"""Generate a reviewable tags.md skeleton from idea.md mechanism and problem.

Extracts mechanism, problem, and topic via idea_utils, shortens operational phrases
using shared shorten/normalize, and emits tags.md with 5-8 specific tags that name
the stall, the default, or the install action. Avoids weak/generic/spam patterns.
Dry-run default; --write optional. No packet content edits beyond the skeleton.
Compounds idea into a ready tags draft that reduces manual tag labor for every
future packet.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract
from phrase_utils import shorten, normalize

WEAK = (
    "video", "youtube", "tutorial", "how to", "subscribe", "free", "best",
    "amazing", "viral", "secret", "hack", "tips", "tricks",
)


def generate_tags(packet: Path) -> str:
    idea = packet / "idea.md"
    if not idea.is_file():
        return "# Tags\n\nNo idea.md found. Run after apply_idea.\n"

    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    if not mech:
        mech = "written next-action default"

    # Build operational candidates
    base = shorten(normalize(mech), max_len=35)
    candidates = [
        base,
        f"install {base[:25]}",
        "sticky note default",
        "before next tab",
        "under two minutes",
        "written next action",
        "name the stall",
        "one concrete default",
    ]
    if problem:
        short_prob = shorten(normalize(problem), max_len=30)
        candidates.append(f"stall: {short_prob}")
    if topic:
        candidates.append(shorten(normalize(topic), max_len=35))

    # Filter
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower().strip()
        if not low or len(low) < 3 or len(low) > 40:
            continue
        if any(w in low for w in WEAK):
            continue
        if low not in seen:
            seen.add(low)
            cleaned.append(c.strip())
    # Pad to at least 5
    extras = ["operational default", "mechanism install", "no decision stall"]
    for e in extras:
        if len(cleaned) >= 6:
            break
        if e.lower() not in seen:
            cleaned.append(e)
            seen.add(e.lower())
    cleaned = cleaned[:8]

    lines = [
        "# Tags",
        "",
        "Estimated operational tags from idea.md mechanism and problem.",
        "Review and adjust before pasting into publish.md ## Tags as a bullet list.",
        "Does not invent claims. Hits against tags_scan are revision signals.",
        "",
        "## Suggested tags",
        "",
    ]
    for tag in cleaned:
        lines.append(f"- {tag}")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("Keep 5-10 tags. Name the stall, the default, or the under-two-minute install.")
    lines.append("Avoid generic/spam terms. Run python3 tools/tags_scan.py <packet> after review.")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate estimated tags.md from idea.md."
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--write", action="store_true", help="Write tags.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"Not a directory: {packet}", file=sys.stderr)
        return 1

    out = packet / "tags.md"
    content = generate_tags(packet)

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
