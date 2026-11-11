#!/usr/bin/env python3
"""Suggest potential splits for the fastest caption cues.

Read-only. Identifies cues above a CPS threshold and proposes a simple
mid-text split suggestion to help human editors reduce reading speed.
Does not rewrite captions.srt, does not call YouTube, does not invent media.
Exit 0 always when parseable (informational). Exit 2 if captions absent.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FAST_CPS = 21.0
TOP_N = 8
CUE_RE = re.compile(
    r"(\d+)\s*\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s*\n(.*?)(?=\n\n|\Z)",
    re.S,
)


def _seconds(stamp: str) -> float:
    h, m, rest = stamp.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def suggest_split(lines: list[str]) -> str:
    full = " ".join(lines).strip()
    if len(full) < 40:
        return "(too short to split usefully)"
    # Prefer split after a natural break near the middle
    words = full.split()
    mid = len(words) // 2
    # Look for a period or comma near mid
    best = mid
    for i in range(max(1, mid - 4), min(len(words), mid + 5)):
        if words[i - 1].endswith((".", ",", "!", "?")):
            best = i
            break
    part1 = " ".join(words[:best])
    part2 = " ".join(words[best:])
    return f"suggest: '{part1}' || '{part2}'"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest splits for fastest caption cues (read-only)."
    )
    parser.add_argument("packet", type=Path)
    parser.add_argument("--threshold", type=float, default=FAST_CPS, help="CPS threshold")
    parser.add_argument("--top", type=int, default=TOP_N, help="Max suggestions")
    args = parser.parse_args()
    packet = args.packet.resolve()
    path = packet / "captions.srt"
    if not path.is_file():
        print(f"CAPTION_SPLIT_SUGGEST: captions.srt absent at {path}")
        return 2

    text = path.read_text(encoding="utf-8")
    fast = []
    for match in CUE_RE.finditer(text.strip() + "\n"):
        body = match.group(4).strip("\n")
        lines = [line.strip() for line in body.splitlines() if line.strip()]
        chars = sum(len(line) for line in lines)
        start = _seconds(match.group(2))
        end = _seconds(match.group(3))
        dur = max(0.001, end - start)
        cps = chars / dur
        if cps >= args.threshold:
            fast.append(
                {
                    "index": int(match.group(1)),
                    "cps": round(cps, 1),
                    "dur": round(dur, 2),
                    "lines": lines,
                    "suggest": suggest_split(lines),
                }
            )
    fast.sort(key=lambda x: -x["cps"])
    fast = fast[: args.top]

    print("CAPTION SPLIT SUGGEST (soft; for human editor; does not rewrite)")
    print(f"Packet: {packet.name}")
    print(f"Threshold: {args.threshold} cps  |  showing top {len(fast)}")
    print()
    if not fast:
        print("No cues above threshold. Nothing to suggest.")
    else:
        for f in fast:
            preview = " | ".join(f["lines"])[:70]
            print(f"cue {f['index']}: {f['cps']}cps  dur={f['dur']}s")
            print(f"  text: {preview}")
            print(f"  {f['suggest']}")
            print()
    print("Human: review suggestions, adjust timings if needed after listening.")
    print("Does not rewrite captions.srt, does not upload, does not invent media.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
