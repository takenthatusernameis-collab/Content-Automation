#!/usr/bin/env python3
"""Approximate YouTube chapter timestamps from script beats at 140 wpm.

Extracts ## beat titles and spoken WORDS, estimates cumulative start times,
and prints suggested chapter lines. Useful for early description planning
before captions.srt or a real take exist.
Reduces recurring manual beat-to-timestamp arithmetic before every publish prep.
Does not invent content, rewrite files, or call external services.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

try:
    from phrase_utils import spoken_words  # type: ignore
except Exception:
    spoken_words = None  # type: ignore

WPM = 140


def extract_beats(text: str) -> list[dict[str, str]]:
    """Split on ## headings; capture title and spoken body."""
    beats: list[dict[str, str]] = []
    parts = re.split(r"^##[ \t]+", text, flags=re.M)
    for part in parts[1:]:
        lines = part.splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:])
        words_m = re.search(r"^WORDS:\s*\n(.*?)(?=^VISUAL:|^##|\Z)", body, re.M | re.S)
        spoken = (words_m.group(1).strip() if words_m else body)
        spoken = re.sub(r"\s+", " ", spoken).strip()
        beats.append({"title": title, "spoken": spoken})
    return beats


def count_words(text: str) -> int:
    if spoken_words is not None:
        cleaned = spoken_words(text)
        return len(cleaned.split()) if cleaned else 0
    cleaned = re.sub(r"[^\w\s'-]", " ", text)
    return len([w for w in cleaned.split() if w.strip()])


def estimate_seconds(word_count: int) -> int:
    if word_count <= 0:
        return 0
    return int(round(word_count / WPM * 60))


def format_ts(seconds: int) -> str:
    m, s = divmod(max(0, seconds), 60)
    return f"{m}:{s:02d}"


def short_title(title: str, max_len: int = 40) -> str:
    cleaned = re.sub(r"\s*\([^)]*\)\s*", " ", title).strip(" -—")
    return cleaned[:max_len]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Approximate chapter timestamps from script beats at 140 wpm. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    source = path / "script.md"
    if not source.is_file():
        source = path / "draft.md"
    if not source.is_file():
        print(f"No script.md or draft.md in {path}", file=sys.stderr)
        return 1

    text = source.read_text(encoding="utf-8")
    beats = extract_beats(text)
    if not beats:
        print("No ## beats found.")
        return 1

    print("CHAPTER TIMING BRIEF (approximate; verify with real take or captions.srt)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print(f"Rate: {WPM} wpm")
    print()
    print("Suggested YouTube chapter lines (first at 0:00):")
    print()

    cumulative = 0
    for i, beat in enumerate(beats):
        wc = count_words(beat["spoken"])
        sec = estimate_seconds(wc)
        title = short_title(beat["title"])
        if i == 0:
            print(f"0:00 {title}")
        else:
            print(f"{format_ts(cumulative)} {title}")
        cumulative += sec

    print()
    print(f"Estimated total: {format_ts(cumulative)}")
    print()
    print("Notes:")
    print("- These are planning estimates only. Prefer chapter_draft.py once captions.srt exists.")
    print("- Enforce YouTube's minimum ~10s gap when finalizing.")
    print("- Last ~20s reserved for end-screen; do not start a new chapter too late.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
