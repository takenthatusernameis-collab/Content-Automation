#!/usr/bin/env python3
"""Generate a reviewable thumbnail.md skeleton from idea.md mechanism and problem.

Extracts mechanism, problem, and topic via idea_utils, shortens operational phrases
using shared shorten/normalize, and emits thumbnail.md with 3-5 short (<=6 word)
candidates suitable for the ## Thumbnail section of publish.md or assets.md.
Avoids weak/clickbait patterns. Prefer concrete mechanism or stall naming.
Dry-run default; --write optional. No packet content edits beyond the skeleton.
Compounds idea into a ready thumbnail-text draft that reduces manual thumbnail
labor for every future packet.
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
from phrase_utils import shorten, normalize, THUMBNAIL_WEAK_PATTERNS


def generate_thumbnail(packet: Path) -> str:
    idea = packet / "idea.md"
    if not idea.is_file():
        return "# Thumbnail\n\nNo idea.md found. Run after apply_idea.\n"

    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    if not mech:
        mech = "the written next-action default"

    # Prefer very short operational phrases
    core = topic.strip() if topic and len(topic.split()) <= 5 else shorten(normalize(mech), max_len=28)
    base = core.lower()

    candidates = [
        core if len(core.split()) <= 5 else shorten(normalize(mech), 22),
        f"Write the {shorten(normalize(mech), 18)}",
        f"Install the {shorten(normalize(mech), 20)}",
        f"{shorten(normalize(problem or mech), 24)}" if problem else f"Default: {shorten(normalize(mech), 20)}",
        f"One note. {shorten(normalize(mech), 18)}",
        shorten(normalize(mech), 20),
    ]

    cleaned = []
    seen = set()
    for c in candidates:
        c = c.strip()
        if not c or len(c.split()) > 6:
            c = shorten(c, 24)
        low = c.lower()
        if any(w in low for w in THUMBNAIL_WEAK_PATTERNS):
            continue
        # Prefer short
        if len(c.split()) > 6:
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c)

    if not cleaned:
        cleaned = [shorten(normalize(mech), 22)]

    # Ensure we have at least a few short ones
    cleaned = [c for c in cleaned if 2 <= len(c.split()) <= 6][:5]
    if not cleaned:
        cleaned = [shorten(normalize(mech), 20)]

    lines = [
        "# Thumbnail",
        "",
        "Estimated short operational thumbnail text from idea.md mechanism, problem, and topic.",
        "Review and adjust before pasting into publish.md ## Thumbnail or assets.md.",
        "Prefer 2-5 words. Does not invent claims. Hits against thumbnail_scan are revision signals.",
        "",
        "## Candidates",
        "",
    ]
    for cand in cleaned:
        lines.append(f"- {cand}")
    if not cleaned:
        lines.append("- (adapt from mechanism or re-run after idea update)")

    lines.extend([
        "",
        "## Notes",
        "",
        "Keep calm and operational. Name the concrete default or stall. Prefer under 5 words.",
        "Avoid clickbait, weak patterns, and long phrases.",
        "Run python3 tools/thumbnail_scan.py <packet> after review.",
        "",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate estimated thumbnail.md from idea.md."
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--write", action="store_true", help="Write thumbnail.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"Not a directory: {packet}", file=sys.stderr)
        return 1

    out = packet / "thumbnail.md"
    content = generate_thumbnail(packet)

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
