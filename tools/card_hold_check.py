#!/usr/bin/env python3
"""Card minimum-hold check from script spoken estimates.

For each beat with a VISUAL cue, estimates spoken duration at the channel
rate and flags any beat shorter than the 1.5 s card minimum from
docs/format.md. Prints a compact table with recommended hold notes.
Reduces recurring manual verification that every card can stay on screen
long enough before timeline or assembly on every future packet.
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

# docs/format.md: otherwise script WORDS at ~150 wpm. Recent tools used 140;
# prefer the documented rate for consistency.
WPM = 150
MIN_HOLD_SEC = 1.5


def extract_beats(text: str) -> list[dict[str, str]]:
    """Split on ## headings; capture title, spoken, and visual need."""
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
        vis_m = re.search(r"VISUAL:\s*(.*?)(?:WORDS:|ON SCREEN:|\Z)", body, re.S | re.I)
        need = re.sub(r"\s+", " ", vis_m.group(1)).strip() if vis_m else ""
        beats.append({"title": title, "spoken": spoken, "need": need})
    return beats


def count_words(text: str) -> int:
    if spoken_words is not None:
        cleaned = spoken_words(text)
        return len(cleaned.split()) if cleaned else 0
    cleaned = re.sub(r"[^\w\s'-]", " ", text)
    return len([w for w in cleaned.split() if w.strip()])


def estimate_seconds(word_count: int) -> float:
    if word_count <= 0:
        return 0.0
    return word_count / WPM * 60.0


def format_sec(sec: float) -> str:
    return f"{sec:.1f}s"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check estimated spoken duration vs 1.5s card minimum. No file writes."
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
    beats = extract_beats(text)

    print("CARD HOLD CHECK (estimated spoken vs docs/format.md 1.5s minimum)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print(f"Rate: {WPM} wpm (documented default)")
    print(f"Minimum card hold: {MIN_HOLD_SEC}s")
    print()

    visual_beats = [b for b in beats if b["need"]]
    if not visual_beats:
        print("No VISUAL cues found. Add VISUAL: lines under headings.")
        print("This tool writes nothing.")
        return 0

    print("| Beat | Words | Est. spoken | Status | Note |")
    print("|------|------:|------------:|--------|------|")

    overall = "PASS"
    notes: list[str] = []
    for beat in visual_beats:
        wc = count_words(beat["spoken"])
        sec = estimate_seconds(wc)
        if sec < MIN_HOLD_SEC:
            st = "SHORT"
            overall = "WARN"
            note = f"extend hold or add silence to reach {MIN_HOLD_SEC}s"
            notes.append(f"{beat['title'][:40]}: {format_sec(sec)} < {MIN_HOLD_SEC}s")
        elif sec < MIN_HOLD_SEC + 0.5:
            st = "TIGHT"
            note = "close to minimum; verify with real take"
        else:
            st = "OK"
            note = "sufficient for minimum hold"
        title_short = beat["title"][:36]
        print(f"| {title_short} | {wc} | {format_sec(sec)} | {st} | {note} |")

    print()
    print(f"Overall: {overall}")
    if notes:
        for n in notes:
            print(f"- {n}")
    else:
        print("- All visual beats meet or exceed estimated minimum hold.")

    print()
    print("Rule from docs/format.md: Hold each card \u2265 1.5 s even if the sentence is shorter.")
    print("Estimates use spoken WORDS only. Actual VO and editor holds may differ.")
    print("This tool writes nothing. Use with card_placement_brief.py or timeline.py once a take exists.")
    return 0 if overall == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
