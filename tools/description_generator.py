#!/usr/bin/env python3
"""Generate a reviewable description.md skeleton from idea.md mechanism and problem.

Extracts mechanism, problem, and topic via idea_utils, shortens operational phrases
using shared shorten/normalize, and emits description.md with a calm, mechanism-aligned
description suitable for the ## Description section of publish.md.
Avoids filler and engagement bait patterns. Dry-run default; --write optional.
No packet content edits beyond the skeleton. Compounds idea into a ready description
draft that reduces manual description labor for every future packet.
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


def generate_description(packet: Path) -> str:
    idea = packet / "idea.md"
    if not idea.is_file():
        return "# Description\n\nNo idea.md found. Run after apply_idea.\n"

    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    if not mech:
        mech = "the written next-action default"

    core = shorten(normalize(mech), max_len=55)
    base = core.lower()
    problem_part = f" The stall is {shorten(normalize(problem), max_len=40).lower()}." if problem else ""
    suggested = (
        f"Write the exact words of the {base} on a sticky note or device note "
        f"and put it where the stall starts. Do that before you open the next tab."
        f"{problem_part} "
        f"That installs the default in under two minutes."
    ).strip()

    lines = [
        "# Description",
        "",
        "Estimated operational description from idea.md mechanism and problem.",
        "Review and adjust before pasting into publish.md ## Description.",
        "Does not invent claims. Hits against description_scan are revision signals.",
        "",
        "## Suggested text",
        "",
        suggested,
        "",
        "## Notes",
        "",
        "Keep calm and operational. Name the concrete default, the stall, and the under-two-minute install.",
        "Avoid filler, engagement bait, and anti-slop phrases.",
        "Run python3 tools/description_scan.py <packet> after review.",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate estimated description.md from idea.md."
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--write", action="store_true", help="Write description.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"Not a directory: {packet}", file=sys.stderr)
        return 1

    out = packet / "description.md"
    content = generate_description(packet)

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
