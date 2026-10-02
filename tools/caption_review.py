#!/usr/bin/env python3
"""Write a short spot-check sheet from an existing captions.srt.

Not ASR, not an upload, and not an approval. Does not regenerate timings.
Does not check human boxes. A missing srt refuses.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MAX_LINE = 42
SLOW_S = 6.0
FAST_S = 0.45
WORD_RATE_LO = 1.2
WORD_RATE_HI = 4.8

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
        start = _seconds(match.group(2))
        end = _seconds(match.group(3))
        words = sum(len(line.split()) for line in lines)
        cues.append(
            {
                "index": int(match.group(1)),
                "start": match.group(2),
                "end": match.group(3),
                "start_s": start,
                "dur": end - start,
                "lines": lines,
                "words": words,
                "max_line": max((len(line) for line in lines), default=0),
            }
        )
    return cues


def flags_for(cue: dict) -> list[str]:
    flags = []
    if cue["max_line"] > MAX_LINE:
        flags.append(f"line>{MAX_LINE}")
    if cue["dur"] < FAST_S:
        flags.append(f"dur<{FAST_S}")
    if cue["dur"] > SLOW_S:
        flags.append(f"dur>{SLOW_S}")
    if cue["dur"] > 0 and cue["words"]:
        rate = cue["words"] / cue["dur"]
        if rate < WORD_RATE_LO or rate > WORD_RATE_HI:
            flags.append(f"rate={rate:.1f}w/s")
    return flags


def checkpoints(cues: list[dict]) -> list[dict]:
    if not cues:
        return []
    picks = []
    seen = set()
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        idx = min(len(cues) - 1, int(round(frac * (len(cues) - 1))))
        cue = cues[idx]
        if cue["index"] in seen:
            continue
        seen.add(cue["index"])
        picks.append(cue)
    return picks


def render(packet: Path, cues: list[dict]) -> str:
    flagged = [(cue, flags_for(cue)) for cue in cues]
    flagged = [(cue, flags) for cue, flags in flagged if flags]
    lines = [
        "# Caption spot-check",
        "",
        "Status: draft sheet, not an approval.",
        "Method: silence-proportional captions.srt already on disk. Not ASR. Not uploaded.",
        "This file does not check Description edited, First comment approved, or the captions spot-check box.",
        "",
        f"Packet: `{packet.name}`",
        f"Cues: {len(cues)}",
        f"Flagged cues: {len(flagged)}",
        "",
        "Human work: listen to the five checkpoints and any flagged cue. If the spoken words match, leave the spot-check box open until you have heard them. An agent must not check it.",
        "",
        "## Checkpoints",
        "",
    ]
    for cue in checkpoints(cues):
        text = " / ".join(cue["lines"])
        lines.append(f"- cue {cue['index']} {cue['start']} ({cue['dur']:.2f}s) — {text}")
    lines.extend(["", "## Flagged", ""])
    if not flagged:
        lines.append("- none under the current line-length, duration, and rate rules")
    else:
        for cue, flags in flagged:
            text = " / ".join(cue["lines"])
            lines.append(
                f"- cue {cue['index']} {cue['start']} ({cue['dur']:.2f}s) [{', '.join(flags)}] — {text}"
            )
    lines.extend(
        [
            "",
            "## Do not",
            "",
            "- Do not treat this sheet as uploaded captions.",
            "- Do not regenerate captions.srt unless the Selected VO checksum changes.",
            "- Do not check publish.md boxes from an agent run.",
            "",
        ]
    )
    return "\n".join(lines)


def build(packet: Path) -> tuple[str, dict]:
    srt = packet / "captions.srt"
    if not srt.is_file():
        raise FileNotFoundError(f"REFUSE: missing {srt}; do not invent captions")
    cues = parse_cues(srt.read_text(encoding="utf-8"))
    if not cues:
        raise ValueError(f"REFUSE: {srt} has no cues")
    text = render(packet, cues)
    if "- [x]" in text:
        raise ValueError("REFUSE: review sheet must not check a box")
    info = {
        "cues": len(cues),
        "flagged": sum(1 for cue in cues if flags_for(cue)),
        "method": "spot-check-sheet",
        "approval": False,
    }
    return text, info


def main() -> int:
    parser = argparse.ArgumentParser(description="Write captions_review.md from captions.srt")
    parser.add_argument("packet", type=Path)
    parser.add_argument("--write", action="store_true", help="write captions_review.md")
    args = parser.parse_args()
    packet = args.packet
    try:
        text, info = build(packet)
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if args.write:
        dest = packet / "captions_review.md"
        dest.write_text(text, encoding="utf-8")
        print(f"wrote {dest}")
    else:
        print(text)
    print(
        f"cues={info['cues']} flagged={info['flagged']} approval={info['approval']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
