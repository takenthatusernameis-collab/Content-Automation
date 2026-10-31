#!/usr/bin/env python3
"""Minimum timeline estimate including forced card holds.

Extracts ## sections from script.md or draft.md, estimates spoken duration
at the documented ~150 wpm, and applies the docs/format.md 1.5 s minimum
hold for every visual card. Sums the adjusted holds to produce a minimum
total duration that accounts for short-beat padding.

Prints a compact summary versus the 6–10 minute target. Reduces recurring
manual arithmetic of “spoken time + forced holds” before timeline or
assembly planning on every future packet. Does not invent content, rewrite
files, or call external services.

Uses shared phrase_utils.extract_sections and count_spoken_words so section
boundaries and word counts stay identical to end-screen and other tools.
Previous local count_words re-applied spoken_words to already-extracted
section text and reported 0 words.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import extract_sections, count_spoken_words

WPM = 150
MIN_HOLD_SEC = 1.5
TARGET_MIN_SEC = 360  # 6 min
TARGET_MAX_SEC = 600  # 10 min
END_SCREEN_SEC = 20


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Estimate minimum total duration after applying 1.5s card holds. No file writes."
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
    sections = extract_sections(text)

    print("MINIMUM TIMELINE ESTIMATE (spoken + forced 1.5s card holds)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print(f"Clock: ~{WPM} wpm")
    print(f"Min card hold: {MIN_HOLD_SEC}s (docs/format.md)")
    print()

    if not sections:
        print("No ## sections found.")
        return 0

    total_spoken = 0.0
    total_adjusted = 0.0
    visual_count = 0
    short_count = 0

    print("| Section | Words | Spoken | Hold applied | Adjusted |")
    print("|---------|------:|-------:|-------------:|---------:|")

    for sec in sections:
        wc = count_spoken_words(sec["spoken"])
        spoken = (wc / WPM) * 60 if wc else 0.0
        total_spoken += spoken
        has_visual = bool(sec["need"])
        if has_visual:
            visual_count += 1
            adjusted = max(spoken, MIN_HOLD_SEC)
            if adjusted > spoken:
                short_count += 1
        else:
            adjusted = spoken
        total_adjusted += adjusted
        title_short = sec["title"][:28]
        print(
            f"| {title_short} | {wc} | {spoken:.1f}s | "
            f"{'yes' if has_visual and adjusted > spoken else '-'} | {adjusted:.1f}s |"
        )

    print()
    print(f"Visual cards: {visual_count} (short beats padded: {short_count})")
    print(f"Raw spoken total: {total_spoken:.0f}s")
    print(f"Minimum adjusted total (holds applied): {total_adjusted:.0f}s")
    print(f"End-screen reserve: {END_SCREEN_SEC}s (already included in final export length)")

    status = "OK"
    notes: list[str] = []
    if total_adjusted < TARGET_MIN_SEC:
        status = "SHORT"
        notes.append(f"Adjusted {total_adjusted:.0f}s < {TARGET_MIN_SEC}s floor")
    elif total_adjusted > TARGET_MAX_SEC:
        status = "LONG"
        notes.append(f"Adjusted {total_adjusted:.0f}s > {TARGET_MAX_SEC}s ceiling")
    else:
        notes.append("Adjusted duration sits inside the 6–10 minute band after holds.")

    print()
    print(f"Overall vs 6–10 min target: {status}")
    for n in notes:
        print(f"- {n}")

    print()
    print("This is a planning estimate only. Actual VO length and editor decisions differ.")
    print("CTA card must remain readable through the final 20 s end-screen reserve.")
    print("Section extraction and word counts use shared phrase_utils helpers.")
    print("This tool writes nothing.")
    return 0 if status == "OK" else 2


if __name__ == "__main__":
    sys.exit(main())
