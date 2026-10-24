#!/usr/bin/env python3
"""Script structure brief: early structural QA for channel format.

Combines beat extraction, word-count timing (140 wpm), and VISUAL presence check.
Flags if estimated duration is outside the 6-10 minute target from docs/channel.md,
or if any beat lacks a VISUAL cue.
Prints a compact pass/warn report. Reduces recurring manual structural review
before recording or card planning on every future packet.
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
TARGET_MIN_SEC = 6 * 60  # 360
TARGET_MAX_SEC = 10 * 60  # 600
TARGET_IDEAL_SEC = 8 * 60  # 480


def extract_beats(text: str) -> list[dict[str, str]]:
    """Split on ## headings; capture title, spoken body, and whether VISUAL is present."""
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
        has_visual = bool(re.search(r"^VISUAL:\s*\S", body, re.M | re.I))
        beats.append({"title": title, "spoken": spoken, "has_visual": has_visual})
    if not beats:
        beats.append({"title": "(whole)", "spoken": text, "has_visual": False})
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
        description="Structural QA brief for script vs channel format. No file writes."
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

    total_words = 0
    total_sec = 0
    missing_visual = []
    for b in beats:
        wc = count_words(b["spoken"])
        sec = estimate_seconds(wc)
        total_words += wc
        total_sec += sec
        if not b["has_visual"]:
            missing_visual.append(b["title"])

    print("SCRIPT STRUCTURE BRIEF (early QA; verify with real take)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print(f"Beats found: {len(beats)}")
    print(f"Total spoken words: {total_words}")
    print(f"Estimated duration: {format_duration(total_sec)} ({total_sec}s) at {WPM} wpm")
    print(f"Channel target: 6-10 min (ideal ~8 min / {TARGET_IDEAL_SEC}s)")
    print()

    status = "PASS"
    notes = []
    if total_sec < TARGET_MIN_SEC:
        status = "WARN"
        notes.append(f"Short: under 6 min target ({format_duration(total_sec)}). Consider expanding beats.")
    elif total_sec > TARGET_MAX_SEC:
        status = "WARN"
        notes.append(f"Long: over 10 min target ({format_duration(total_sec)}). Consider tightening or splitting.")
    else:
        notes.append(f"Duration in target range.")

    if missing_visual:
        status = "WARN"
        notes.append(f"Missing VISUAL cue on {len(missing_visual)} beat(s): {', '.join(missing_visual[:3])}{'...' if len(missing_visual) > 3 else ''}")
    else:
        notes.append("VISUAL cue present on every beat.")

    if len(beats) < 4:
        status = "WARN"
        notes.append(f"Few beats ({len(beats)}). Typical explainers use 5-8 sections.")

    print(f"Overall: {status}")
    for n in notes:
        print(f"- {n}")

    print()
    print("Reserve last ~20s for end-screen once duration is confirmed.")
    print("This tool writes nothing. Use with script_pacing_brief.py or visual_cues_brief.py for detail.")
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
