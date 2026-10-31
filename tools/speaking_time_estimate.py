#!/usr/bin/env python3
"""Estimate narration duration from spoken word count.

Extracts spoken WORDS from draft.md or script.md using shared helpers,
counts words with the canonical counter, and estimates speaking time at a
typical clear-narration rate (140 wpm for human; higher for generated).
When a packet-relative Selected VO exists, also reports observed duration
and words-per-minute so future estimates can be calibrated.
Prints minutes:seconds and a short note for timeline/planning use.
Reduces recurring manual calculation of expected VO length before recording or assembly
for every future packet. Does not invent content, rewrite files, or call external services.
"""

from __future__ import annotations

import argparse
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import spoken_words, count_spoken_words
from render_brief import selected_vo_drop  # noqa: E402

HUMAN_WPM = 140  # typical clear explanatory narration rate
GENERATED_WPM = 190  # observed on Q1 generated take; use when origin is generated


def estimate_seconds(word_count: int, wpm: int) -> int:
    if word_count <= 0 or wpm <= 0:
        return 0
    return int(round(word_count / wpm * 60))


def format_duration(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    return f"{m}:{s:02d}"


def observed_duration(vo_path: Path) -> float | None:
    if not vo_path.is_file():
        return None
    try:
        with wave.open(str(vo_path), "rb") as w:
            return w.getnframes() / float(w.getframerate())
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Estimate speaking time from packet spoken words. Reports observed WPM when Selected VO exists. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    draft = path / "draft.md"
    script = path / "script.md"
    source = draft if draft.is_file() else script
    if not source.is_file():
        print(f"No draft.md or script.md in {path}", file=sys.stderr)
        return 1

    text = source.read_text(encoding="utf-8")
    words_text = spoken_words(text)
    count = count_spoken_words(words_text)

    # Prefer generated rate if vo_origin marks generated
    origin_path = path / "vo_origin.md"
    is_generated = False
    if origin_path.is_file():
        origin_text = origin_path.read_text(encoding="utf-8").lower()
        is_generated = "kind: generated" in origin_text or "kind=generated" in origin_text
    rate = GENERATED_WPM if is_generated else HUMAN_WPM

    seconds = estimate_seconds(count, rate)
    duration = format_duration(seconds)

    print("SPEAKING TIME ESTIMATE (approximate; verify with real take)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print(f"Spoken words: {count}")
    print(f"Estimated rate: {rate} wpm ({'generated' if is_generated else 'human'} default)")
    print(f"Estimated duration: {duration} ({seconds} seconds)")

    vo_rel = selected_vo_drop(path)
    vo_path = ROOT / vo_rel if vo_rel.startswith("videos/") else path / vo_rel
    obs = observed_duration(vo_path)
    if obs is not None and count > 0:
        obs_wpm = int(round(count / (obs / 60.0)))
        print()
        print(f"Observed Selected VO: {obs:.1f}s ({format_duration(int(obs))})")
        print(f"Observed rate: {obs_wpm} wpm")
        print("Use observed rate for future packets of the same origin type.")
    else:
        print()
        print("No Selected VO on disk; estimate only.")

    print()
    print("Use for timeline planning and end-screen reservation (last 20s).")
    print("Actual take length may differ; run media_qa after a selected VO exists.")
    print("Word count uses shared phrase_utils.count_spoken_words.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
