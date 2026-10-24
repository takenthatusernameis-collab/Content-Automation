#!/usr/bin/env python3
"""Compute the recommended YouTube end-screen window from estimated narration duration.

Uses speaking_time_estimate helpers (or a simple fallback) to get total spoken-word
duration at 140 wpm, then prints the start timestamp for the final 20 seconds that
must be reserved for end-screen elements. Reduces recurring manual subtraction
before timeline planning or assembly on every future packet.
Does not invent content, rewrite files, or call external services.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

try:
    from speaking_time_estimate import estimate_seconds, count_spoken_words  # type: ignore
except Exception:
    estimate_seconds = None  # type: ignore
    count_spoken_words = None  # type: ignore

END_SCREEN_SEC = 20
WPM = 140


def simple_count(text: str) -> int:
    """Fallback spoken-word count when shared helper is unavailable."""
    import re
    words = re.findall(r"\b[\w']+\b", text)
    return len(words)


def get_duration_seconds(packet: Path) -> tuple[int, int]:
    """Return (word_count, seconds) from script.md or draft.md."""
    for name in ("script.md", "draft.md"):
        p = packet / name
        if p.is_file():
            text = p.read_text(encoding="utf-8")
            if count_spoken_words is not None:
                wc = count_spoken_words(text)
            else:
                wc = simple_count(text)
            if estimate_seconds is not None:
                secs = estimate_seconds(wc)
            else:
                secs = int(wc * 60 / WPM) if wc else 0
            return wc, secs
    return 0, 0


def format_ts(seconds: int) -> str:
    if seconds < 0:
        seconds = 0
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print recommended end-screen start time from estimated narration duration. No writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    wc, total = get_duration_seconds(path)
    if total <= 0:
        print("No spoken words found in script.md or draft.md.")
        print("Run speaking_time_estimate.py or add WORDS blocks first.")
        return 1

    start = max(0, total - END_SCREEN_SEC)
    print("END-SCREEN WINDOW (from estimated narration)")
    print("=" * 48)
    print(f"Spoken words: {wc}")
    print(f"Estimated duration @ {WPM} wpm: {format_ts(total)} ({total}s)")
    print(f"Reserve final {END_SCREEN_SEC}s: start end-screen at {format_ts(start)}")
    print()
    print("Notes:")
    print("- Confirm with actual selected VO duration before encoding.")
    print("- Last ~20s must remain free of new spoken content and critical cards.")
    print("- See docs/editor.md for end-screen placement rules.")
    print("This tool writes nothing. Prefer human OAuth for publish once media is ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
