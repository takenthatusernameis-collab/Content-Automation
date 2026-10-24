#!/usr/bin/env python3
"""Per-beat pacing brief from script.md or draft.md.

Extracts section/beat titles and spoken words (via phrase_utils when available),
counts words per beat, and estimates duration at 140 wpm.
Prints a compact table for recording, timeline, and end-screen planning.
Reduces recurring manual parsing of script structure before every narration or assembly step.
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

WPM = 140  # consistent with speaking_time_estimate.py


def extract_beats(text: str) -> list[dict[str, str]]:
    """Split on ## headings; capture title and body."""
    beats: list[dict[str, str]] = []
    parts = re.split(r"^##[ \t]+", text, flags=re.M)
    for part in parts[1:]:
        lines = part.splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:])
        # Prefer WORDS: block if present (script.md style)
        words_m = re.search(r"^WORDS:\s*\n(.*?)(?=^VISUAL:|^##|\Z)", body, re.M | re.S)
        spoken = (words_m.group(1).strip() if words_m else body)
        spoken = re.sub(r"\s+", " ", spoken).strip()
        beats.append({"title": title, "spoken": spoken})
    if not beats:
        # Fallback: whole file as one beat
        beats.append({"title": "(whole)", "spoken": text})
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


def format_duration(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    return f"{m}:{s:02d}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Per-beat spoken-word pacing brief. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    draft = path / "draft.md"
    script = path / "script.md"
    source = script if script.is_file() else draft
    if not source.is_file():
        print(f"No script.md or draft.md in {path}", file=sys.stderr)
        return 1

    text = source.read_text(encoding="utf-8")
    beats = extract_beats(text)

    print("SCRIPT PACING BRIEF (approximate; verify with real take)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print(f"Rate: {WPM} wpm (clear narration)")
    print()
    print("| Beat | Words | Est. time | Cumulative |")
    print("|------|-------|-----------|------------|")

    total_words = 0
    total_sec = 0
    for beat in beats:
        wc = count_words(beat["spoken"])
        sec = estimate_seconds(wc)
        total_words += wc
        total_sec += sec
        print(
            f"| {beat['title'][:40]} | {wc} | {format_duration(sec)} | {format_duration(total_sec)} |"
        )

    print()
    print(f"Total spoken words: {total_words}")
    print(f"Total estimated duration: {format_duration(total_sec)} ({total_sec} seconds)")
    print()
    print("Reserve last ~20s for end-screen. Actual take may differ.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
