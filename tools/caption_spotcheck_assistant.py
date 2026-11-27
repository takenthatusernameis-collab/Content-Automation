#!/usr/bin/env python3
"""Print a structured human-friendly captions spot-check list.

Parses an existing captions.srt (does not rewrite or invent content).
Prints each cue with timing, duration, line lengths, and soft flags
(near max line length, long/short cue, large gap) so a human can scan
faster than reading the raw SRT. Hard failures remain in caption_gate.py.
Reduces recurring captions spot-check minutes across future videos.
Does not call YouTube, does not encode, does not write files.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MAX_LINE = 42
NEAR_MAX = 38
LONG_CUE_S = 4.0
SHORT_CUE_S = 0.8
LARGE_GAP_S = 1.5

CUE_RE = re.compile(
    r"(\d+)\s*\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s*\n(.*?)(?=\n\n|\Z)",
    re.S,
)


def _seconds(stamp: str) -> float:
    h, m, rest = stamp.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def parse_cues(text: str) -> list[dict]:
    cues = []
    for match in CUE_RE.finditer(text.strip() + "\n"):
        body = match.group(4).strip("\n")
        lines = [line.strip() for line in body.splitlines() if line.strip()]
        cues.append(
            {
                "index": int(match.group(1)),
                "start": _seconds(match.group(2)),
                "end": _seconds(match.group(3)),
                "lines": lines,
            }
        )
    return cues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print structured captions spot-check list (no invent, no write)."
    )
    parser.add_argument("packet", type=Path, help="Packet folder containing captions.srt")
    args = parser.parse_args()
    packet = args.packet
    path = packet / "captions.srt"
    if not path.is_file():
        print(f"No captions.srt in {packet}")
        print("Hard gate: python3 tools/caption_gate.py PATH (exits 2 if absent)")
        return 1

    text = path.read_text(encoding="utf-8", errors="replace")
    cues = parse_cues(text)
    if not cues:
        print("CAPTIONS_UNPARSEABLE (no cues extracted)")
        return 1

    print("CAPTION SPOTCHECK ASSISTANT (structured review list; no invent, no write)")
    print(f"Packet: {packet}")
    print(f"Cues: {len(cues)}")
    print("Hard gate remains: python3 tools/caption_gate.py PATH")
    print("=" * 70)
    print()

    flag_counts = {"near_max": 0, "long": 0, "short": 0, "gap": 0}
    prev_end = 0.0
    for cue in cues:
        start = cue["start"]
        end = cue["end"]
        dur = end - start
        lines = cue["lines"]
        line_info = " | ".join(f"{len(ln)}c" for ln in lines)
        flags = []
        if any(len(ln) >= NEAR_MAX for ln in lines):
            flags.append("near_max")
            flag_counts["near_max"] += 1
        if dur > LONG_CUE_S:
            flags.append("long")
            flag_counts["long"] += 1
        if dur < SHORT_CUE_S and dur > 0:
            flags.append("short")
            flag_counts["short"] += 1
        gap = start - prev_end
        if gap > LARGE_GAP_S and prev_end > 0:
            flags.append(f"gap={gap:.1f}s")
            flag_counts["gap"] += 1
        flag_str = " [" + ", ".join(flags) + "]" if flags else ""
        print(
            f"{cue['index']:3d}. {start:6.2f}s -> {end:6.2f}s ({dur:4.2f}s) {line_info}{flag_str}"
        )
        for ln in lines:
            print(f"     {ln}")
        print()
        prev_end = end

    print("Soft flag summary (human still verifies):")
    print(f"  near_max (>= {NEAR_MAX} chars): {flag_counts['near_max']}")
    print(f"  long (>{LONG_CUE_S}s): {flag_counts['long']}")
    print(f"  short (<{SHORT_CUE_S}s): {flag_counts['short']}")
    print(f"  large_gap (>{LARGE_GAP_S}s): {flag_counts['gap']}")
    print()
    print("These flags are soft hints only. Run caption_gate.py for hard failures.")
    print("Spot-check time is reduced by scanning this list instead of raw SRT.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
