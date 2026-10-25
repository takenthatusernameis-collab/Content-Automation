#!/usr/bin/env python3
"""Card placement brief from script pacing and visual cues.

Combines per-beat spoken-word timing (140 wpm) with VISUAL / card needs
to print approximate start timestamps for each card. Reduces recurring
manual mapping of script structure to timeline positions before assembly
or editor sessions. Does not invent content, rewrite files, or call
external services. Builds on script_pacing_brief and visual_cues_brief
helpers when available.
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

try:
    from asset_brief import script_cards  # type: ignore
except Exception:
    script_cards = None  # type: ignore

WPM = 140
END_SCREEN_SEC = 20


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
        # Spoken words
        words_m = re.search(r"^WORDS:\s*\n(.*?)(?=^VISUAL:|^##|\Z)", body, re.M | re.S)
        spoken = (words_m.group(1).strip() if words_m else body)
        spoken = re.sub(r"\s+", " ", spoken).strip()
        # Visual need
        vis_m = re.search(r"VISUAL:\s*(.*?)(?:WORDS:|ON SCREEN:|\Z)", body, re.S | re.I)
        need = re.sub(r"\s+", " ", vis_m.group(1)).strip() if vis_m else ""
        beats.append({"title": title, "spoken": spoken, "need": need})
    if not beats:
        beats.append({"title": "(whole)", "spoken": text, "need": ""})
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
    if seconds < 0:
        seconds = 0
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Approximate card placement timestamps from script beats. No file writes."
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

    # Prefer asset_brief cards if available for consistency
    cards_from_asset = []
    if script_cards is not None:
        try:
            cards_from_asset = script_cards(text)
        except Exception:
            cards_from_asset = []

    print("CARD PLACEMENT BRIEF (approximate; verify with real take and timeline.py)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print(f"Rate: {WPM} wpm")
    print()

    total_sec = 0
    placements = []
    for beat in beats:
        wc = count_words(beat["spoken"])
        sec = estimate_seconds(wc)
        start = total_sec
        total_sec += sec
        if beat["need"]:
            placements.append(
                {
                    "beat": beat["title"],
                    "start": start,
                    "need": beat["need"],
                    "duration_sec": sec,
                }
            )

    if not placements and cards_from_asset:
        # Fallback to asset list without timing if extraction missed needs
        print("Visual needs found via asset_brief but no per-beat timing; showing list only.")
        for c in cards_from_asset:
            print(f"- {c.get('beat', '')}: {c.get('need', '')}")
        print()
        print("This tool writes nothing.")
        return 0

    if not placements:
        print("No VISUAL cues found in beats. Add VISUAL: lines under headings.")
        print("This tool writes nothing.")
        return 0

    print("| Beat | Approx start | Duration | Visual need |")
    print("|------|--------------|----------|-------------|")
    for p in placements:
        beat = p["beat"][:32]
        need = p["need"][:60].replace("|", "/")
        print(
            f"| {beat} | {format_ts(p['start'])} | {format_ts(p['duration_sec'])} | {need} |"
        )

    print()
    print(f"Total estimated duration: {format_ts(total_sec)} ({total_sec}s)")
    end_start = max(0, total_sec - END_SCREEN_SEC)
    print(f"End-screen window starts ~{format_ts(end_start)} (reserve final {END_SCREEN_SEC}s).")
    print()
    print("Notes:")
    print("- Timestamps are estimates from spoken words; actual VO may differ.")
    print("- Use with timeline.py once a selected take exists.")
    print("- Cards should not crowd the final end-screen window.")
    print("- This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
