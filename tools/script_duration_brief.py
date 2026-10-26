#!/usr/bin/env python3
"""Print a structured duration and pacing brief from script spoken WORDS.

Counts total spoken words, estimates runtime at 150 wpm, checks against the
900–1500 word band from docs/content_quality.md, and optionally breaks down
by ## beat headings when present. Flags if the script is outside the target
band so humans can expand or cut before promotion without manual counting.
Does not invent content, write files, poll secrets, or call external services.
Exit 0 always (informational).
Useful before script promotion or VO planning to reduce recurring word-count
and timing estimation labor on every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import spoken_words, normalize  # type: ignore

TARGET_MIN = 900
TARGET_MAX = 1500
WPM = 150


def estimate_seconds(word_count: int) -> int:
    return int(round(word_count / WPM * 60))


def format_time(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    return f"{m}:{s:02d}"


def beat_breakdown(text: str) -> list[tuple[str, int]]:
    """Return list of (beat_title, word_count) for ## sections containing WORDS."""
    text = normalize(text)
    # Rough split on ## headings
    parts = re.split(r"\n##\s+", text)
    results = []
    for part in parts[1:]:  # skip before first ##
        lines = part.splitlines()
        if not lines:
            continue
        title = lines[0].strip()[:60]
        body = "\n".join(lines[1:])
        spoken = spoken_words("WORDS: " + body)  # fake prefix so extractor works
        wc = len(spoken.split()) if spoken.strip() else 0
        if wc > 0:
            results.append((title, wc))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print script duration and pacing brief. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    parser.add_argument(
        "--prefer",
        choices=("script", "draft", "auto"),
        default="auto",
        help="Which file to prefer for spoken WORDS (default: auto)",
    )
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("SCRIPT DURATION / PACING BRIEF (informational only; no writes)")
    print(f"Packet: {path.name}")
    print()

    script_path = path / "script.md"
    draft_path = path / "draft.md"
    chosen = None
    if args.prefer == "script" and script_path.is_file():
        chosen = script_path
    elif args.prefer == "draft" and draft_path.is_file():
        chosen = draft_path
    else:
        if script_path.is_file():
            chosen = script_path
        elif draft_path.is_file():
            chosen = draft_path

    if not chosen:
        print("No script.md or draft.md found.")
        print("This tool writes nothing.")
        return 0

    text = chosen.read_text(encoding="utf-8")
    spoken = spoken_words(text)
    words = spoken.split()
    wc = len(words)
    est_sec = estimate_seconds(wc)
    est_str = format_time(est_sec)

    print(f"Spoken words: {wc}")
    print(f"Estimated duration at {WPM} wpm: {est_str} ({est_sec}s)")
    print(f"Target band (docs/content_quality.md): {TARGET_MIN}–{TARGET_MAX} words")

    if wc < TARGET_MIN:
        print(f"FLAG: below band (needs expansion of ~{TARGET_MIN - wc} words)")
    elif wc > TARGET_MAX:
        print(f"FLAG: above band (consider cutting ~{wc - TARGET_MAX} words)")
    else:
        print("FLAG: within target band")

    print()
    beats = beat_breakdown(text)
    if beats:
        print("Beat breakdown (approximate word counts from ## sections):")
        cum = 0
        for title, bwc in beats:
            cum += bwc
            print(f"  - {title}: {bwc} words (~{format_time(estimate_seconds(bwc))})")
        print(f"  Total from beats: {cum} (may differ slightly from full spoken extract)")
    else:
        print("No ## beat headings detected; full-script estimate only.")

    print()
    print("### Reminder")
    print("- 150 wpm is a conservative spoken rate for clear narration.")
    print("- Land in the 900–1500 spoken-word band before promoting to ready_for_vo.")
    print("- These estimates are for planning only; actual VO timing may vary.")
    print("- Do not invent content or commit secrets.")
    print()
    print("This brief does not invent content or write files.")
    print("Useful before script promotion or VO planning to reduce manual word-count and timing estimation on every packet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
