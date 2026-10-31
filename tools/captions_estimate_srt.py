#!/usr/bin/env python3
"""Generate a local estimated captions.srt from script.md spoken WORDS.

Extracts ## sections via shared helpers, splits long spoken text into readable
cues (~12 words or by sentence), estimates timings with effective_rate
(prefers observed WPM from Selected VO if present, else select_rate 190/140),
and writes a standard SRT file (captions_estimate.srt).

No invented content. Output stays local and gitignored. Not a real alignment
to audio. Reduces recurring human labor of manually drafting initial caption
cues and timings for review or player preview on every future packet before
a Selected VO take exists. Rate selection now matches speaking-time, end-screen,
timeline, and minimum-timeline tools.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import extract_sections, count_spoken_words, effective_rate  # noqa: E402

MAX_WORDS_PER_CUE = 12


def split_into_cues(text: str, max_words: int = MAX_WORDS_PER_CUE) -> list[str]:
    """Split spoken text into short cues, preferring sentence boundaries."""
    if not text:
        return []
    # Rough sentence split
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    cues: list[str] = []
    for sent in sentences:
        words = sent.split()
        if not words:
            continue
        if len(words) <= max_words:
            cues.append(sent.strip())
            continue
        # Chunk long sentence
        for i in range(0, len(words), max_words):
            chunk = " ".join(words[i : i + max_words])
            cues.append(chunk)
    return [c for c in cues if c]


def format_srt_time(seconds: float) -> str:
    if seconds < 0:
        seconds = 0.0
    ms = int(round(seconds * 1000))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> int:
    p = argparse.ArgumentParser(description="Generate estimated captions.srt from script.md")
    p.add_argument("packet", type=Path, help="Path to packet directory")
    p.add_argument("--force", action="store_true", help="Overwrite existing captions_estimate.srt")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    script_path = packet / "script.md"
    if not script_path.is_file():
        print("FAIL: script.md missing", file=sys.stderr)
        return 2

    out_path = packet / "captions_estimate.srt"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    text = script_path.read_text(encoding="utf-8")
    sections = extract_sections(text)
    if not sections:
        print("FAIL: no ## sections / spoken WORDS found in script.md", file=sys.stderr)
        return 2

    spoken_bodies = [s["spoken"] for s in sections if s.get("spoken")]
    total_words = sum(count_spoken_words(body) for body in spoken_bodies)
    rate, rate_label = effective_rate(packet, total_words)

    cues: list[str] = []
    for spoken in spoken_bodies:
        for cue in split_into_cues(spoken):
            cues.append(cue)

    if not cues:
        print("FAIL: no cues extracted", file=sys.stderr)
        return 2

    # Assign times using shared effective rate
    srt_lines: list[str] = []
    cumulative = 0.0
    for idx, cue in enumerate(cues, 1):
        word_count = count_spoken_words(cue)
        duration = (word_count / rate) * 60.0 if rate > 0 else 1.0
        start = cumulative
        end = cumulative + max(duration, 0.8)  # minimum display time
        cumulative = end

        srt_lines.append(str(idx))
        srt_lines.append(f"{format_srt_time(start)} --> {format_srt_time(end)}")
        srt_lines.append(cue)
        srt_lines.append("")

    out_path.write_text("\n".join(srt_lines) + "\n", encoding="utf-8")
    total_sec = int(round(cumulative))
    print(f"WROTE: {out_path}")
    print(f"cues: {len(cues)}")
    print(f"spoken_words: {total_words}")
    print(f"rate: {rate} wpm ({rate_label})")
    print(f"est_total_s: {total_sec}")
    print("Estimated SRT ready (local; not aligned to real VO). Rate uses shared effective_rate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
