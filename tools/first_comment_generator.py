#!/usr/bin/env python3
"""Generate a reviewable first-comment skeleton from script CTA or channel promise.

Extracts the last section or CTA via phrase_utils, shortens an operational phrase
using shared shorten/normalize, and emits first_comment.md with assignment notes.
Avoids bait patterns. Dry-run default; --write optional. No packet content edits
beyond the skeleton. Compounds script into a ready first-comment draft that reduces
manual pin text labor for every future packet.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from phrase_utils import (
    extract_sections,
    shorten,
    normalize,
    FIRST_COMMENT_BAIT_PATTERNS,
)


def generate_first_comment(packet: Path) -> str:
    script = packet / "script.md"
    if not script.is_file():
        return "# First comment\n\nNo script.md found. Run after apply_script.\n"

    text = script.read_text(encoding="utf-8")
    sections = extract_sections(text)
    if not sections:
        return "# First comment\n\nNo ## sections extracted.\n"

    # Prefer last section for CTA / assignment
    last = sections[-1]
    title = last["title"]
    spoken = last["spoken"]
    # Clean and shorten an operational phrase
    phrase = title
    phrase = re_sub_title(phrase)
    short = shorten(phrase, max_len=40)
    if not short or len(short.split()) < 2:
        first = spoken.split(".")[0].strip() if spoken else title
        short = shorten(first, max_len=40) or title[:40]
    short = normalize(short).strip(" .")

    # Channel promise alignment
    channel_note = "Aligned to channel promise: one small default the same day. Assignment, not a reply prompt."

    suggested = f"Assignment: {short}. Do that today before the next decision."

    lines = [
        "# First comment",
        "",
        "Estimated operational pin from last script section.",
        "Pin this as the first comment so viewers see the assignment immediately.",
        "Review and adjust before copying to publish.md ## First comment.",
        "Does not invent claims. Hits against first-comment bait patterns are revision signals.",
        "",
        "## Suggested text",
        "",
        suggested,
        "",
        "## Notes",
        "",
        channel_note,
        "Keep under ~25 words. Name the concrete default and the stall if possible.",
        "Run python3 tools/first_comment_scan.py <packet> after review.",
        "",
    ]
    # Simple bait pattern check note
    weak_hits = [p for p in FIRST_COMMENT_BAIT_PATTERNS if p in suggested.lower()]
    if weak_hits:
        lines.append(f"WARNING: possible bait patterns: {', '.join(weak_hits)}")
        lines.append("")

    return "\n".join(lines) + "\n"


def re_sub_title(title: str) -> str:
    """Clean common section title prefixes for first-comment use."""
    import re
    title = re.sub(r"^Hook\s*\([^)]+\)", "Hook", title, flags=re.I)
    title = re.sub(r"^Beat\s+\d+\s*[\u2014\-]\s*", "", title, flags=re.I)
    title = re.sub(r"^Payoff promise", "Payoff", title, flags=re.I)
    title = re.sub(r"^CTA", "Next action", title, flags=re.I)
    title = re.sub(r"^Tomorrow's sentence", "Write the sentence", title, flags=re.I)
    return title.strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate estimated first_comment.md from script last section."
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--write", action="store_true", help="Write first_comment.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"Not a directory: {packet}", file=sys.stderr)
        return 1

    out = packet / "first_comment.md"
    content = generate_first_comment(packet)

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
