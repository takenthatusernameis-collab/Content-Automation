#!/usr/bin/env python3
"""Visual cue readability check for planned cards.

Extracts VISUAL: lines from script.md or draft.md and flags any cue that is
too long for comfortable on-screen text (more than 6 words or 50 characters).
Prints a table with status. Reduces recurring labor of manual length checks
before card generation or timeline planning on every future packet.
Does not invent content, rewrite files, or call external services.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MAX_WORDS = 6
MAX_CHARS = 50


def extract_visuals(text: str) -> list[dict[str, str]]:
    """Extract VISUAL cues paired with their beat titles."""
    visuals: list[dict[str, str]] = []
    parts = re.split(r"^##[ \t]+", text, flags=re.M)
    for part in parts[1:]:
        lines = part.splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:])
        vis_m = re.search(r"VISUAL:\s*(.*?)(?:WORDS:|ON SCREEN:|^##|\Z)", body, re.S | re.I)
        if vis_m:
            need = re.sub(r"\s+", " ", vis_m.group(1)).strip()
            if need:
                visuals.append({"title": title, "need": need})
    return visuals


def assess(need: str) -> tuple[str, str]:
    words = len(need.split())
    chars = len(need)
    issues = []
    if words > MAX_WORDS:
        issues.append(f"{words} words > {MAX_WORDS}")
    if chars > MAX_CHARS:
        issues.append(f"{chars} chars > {MAX_CHARS}")
    if issues:
        return "LONG", "; ".join(issues)
    return "OK", "fits card readability"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check VISUAL cue length for on-screen card readability. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    script = path / "script.md"
    draft = path / "draft.md"
    source = script if script.is_file() else draft
    if not source.is_file():
        print(f"No script.md or draft.md in {path}", file=sys.stderr)
        return 1

    text = source.read_text(encoding="utf-8")
    visuals = extract_visuals(text)

    print("VISUAL READABILITY CHECK (length vs card-friendly limits)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print(f"Limits: <= {MAX_WORDS} words, <= {MAX_CHARS} characters")
    print()

    if not visuals:
        print("No VISUAL cues found. Add VISUAL: lines under headings.")
        print("This tool writes nothing.")
        return 0

    print("| Beat | Words | Chars | Status | Note |")
    print("|------|------:|------:|--------|------|")

    overall = "PASS"
    for v in visuals:
        st, note = assess(v["need"])
        if st == "LONG":
            overall = "WARN"
        title_short = v["title"][:32]
        wc = len(v["need"].split())
        cc = len(v["need"])
        print(f"| {title_short} | {wc} | {cc} | {st} | {note} |")

    print()
    print(f"Overall: {overall}")
    if overall == "WARN":
        print("- Shorten LONG cues before generating cards or building the timeline.")
        print("- Prefer the shortest readable version that still names the action or object.")
    else:
        print("- All VISUAL cues fit card readability limits.")

    print()
    print("Rule of thumb: on-screen card text should stay short enough to read at a glance.")
    print("This tool writes nothing. Pair with card_text_suggest.py or card_generator.py.")
    return 0 if overall == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
