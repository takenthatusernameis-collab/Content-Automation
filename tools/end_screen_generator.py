#!/usr/bin/env python3
"""Generate a reviewable end-screen skeleton from script CTA or channel promise.

Extracts the last section or CTA via phrase_utils, shortens an operational phrase
using shared shorten/normalize, and emits end_screen.md with last-20s notes.
Avoids weak patterns. Dry-run default; --write optional. No packet content edits
beyond the skeleton. Compounds script into a ready end-screen draft that reduces
manual end-screen text labor for every future packet.
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
    END_SCREEN_WEAK_PATTERNS,
)


def generate_end_screen(packet: Path) -> str:
    script = packet / "script.md"
    if not script.is_file():
        return "# End screen\n\nNo script.md found. Run after apply_script.\n"

    text = script.read_text(encoding="utf-8")
    sections = extract_sections(text)
    if not sections:
        return "# End screen\n\nNo ## sections extracted.\n"

    # Prefer last section for CTA
    last = sections[-1]
    title = last["title"]
    spoken = last["spoken"]
    # Clean and shorten an operational phrase
    phrase = title
    phrase = re_sub_title(phrase)
    short = shorten(phrase, max_len=30)
    if not short or len(short.split()) < 2:
        first = spoken.split(".")[0].strip() if spoken else title
        short = shorten(first, max_len=30) or title[:30]
    short = normalize(short).strip(" .")

    # Channel promise fallback note
    channel_note = "Aligned to channel promise: one small default the same day."

    lines = [
        "# End screen",
        "",
        "Estimated operational phrase from last script section.",
        "Last 20s of export reserved for YouTube end screen (see docs/editor.md).",
        "CTA card should show the assignment, not a subscribe ask.",
        "Review and adjust before using in assets or publish.md.",
        "Does not invent claims. Hits against end-screen weak patterns are revision signals.",
        "",
        "## Suggested text",
        "",
        short,
        "",
        "## Notes",
        "",
        channel_note,
        "Hold CTA card at least 1.5s. Keep readable in last 20s.",
        "Run python3 tools/chapters_scan.py or relevant scanners after review if needed.",
        "",
    ]
    # Simple weak pattern check note
    weak_hits = [p for p in END_SCREEN_WEAK_PATTERNS if p in short.lower()]
    if weak_hits:
        lines.append(f"WARNING: possible weak patterns: {', '.join(weak_hits)}")
        lines.append("")

    return "\n".join(lines) + "\n"


def re_sub_title(title: str) -> str:
    """Clean common section title prefixes for end-screen use."""
    import re
    title = re.sub(r"^Hook\s*\([^)]+\)", "Hook", title, flags=re.I)
    title = re.sub(r"^Beat\s+\d+\s*[\u2014\-]\s*", "", title, flags=re.I)
    title = re.sub(r"^Payoff promise", "Payoff", title, flags=re.I)
    title = re.sub(r"^CTA", "Next action", title, flags=re.I)
    title = re.sub(r"^Tomorrow's sentence", "Write the sentence", title, flags=re.I)
    return title.strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate estimated end_screen.md from script last section."
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--write", action="store_true", help="Write end_screen.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"Not a directory: {packet}", file=sys.stderr)
        return 1

    out = packet / "end_screen.md"
    content = generate_end_screen(packet)

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
