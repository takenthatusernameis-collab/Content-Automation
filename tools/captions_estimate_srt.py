#!/usr/bin/env python3
"""Generate a local estimated captions.srt from script.md spoken WORDS.

Extracts ## sections and WORDS blocks, splits long spoken text into readable
cues (~10-15 words or by sentence), estimates timings at 150 wpm, and writes
a standard SRT file (captions_estimate.srt).

No invented content. Output stays local and gitignored. Not a real alignment
to audio. Reduces recurring human labor of manually drafting initial caption
cues and timings for review or player preview on every future packet before
a Selected VO take exists.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WPM = 150
MAX_WORDS_PER_CUE = 12


def extract_spoken_blocks(text: str) -> list[tuple[str, str]]:
    """Return list of (header, spoken_text) in order. Only WORDS content."""
    sections: list[tuple[str, str]] = []
    # Find all ## headers and their following content until next ##
    pattern = re.compile(r"^##\s+(.+?)\s*$", re.M)
    matches = list(pattern.finditer(text))
    for i, m in enumerate(matches):
        header = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        # Extract WORDS: ... until VISUAL or end
        wm = re.search(r"WORDS:\s*(.*?)(?:\nVISUAL:|\n##|\Z)", block, re.S | re.I)
        if wm:
            spoken = wm.group(1).strip()
            # Clean extra whitespace
            spoken = re.sub(r"\s+", " ", spoken)
            if spoken:
                sections.append((header, spoken))
    return sections


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
    blocks = extract_spoken_blocks(text)
    if not blocks:
        print("FAIL: no spoken WORDS found in script.md", file=sys.stderr)
        return 2

    cues: list[str] = []
    for header, spoken in blocks:
        for cue in split_into_cues(spoken):
            cues.append(cue)

    if not cues:
        print("FAIL: no cues extracted", file=sys.stderr)
        return 2

    # Assign times
    srt_lines: list[str] = []
    cumulative = 0.0
    for idx, cue in enumerate(cues, 1):
        word_count = len(cue.split())
        duration = (word_count / WPM) * 60.0
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
    print(f"est_total_s: {total_sec}")
    print("Estimated SRT ready (local; not aligned to real VO).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
