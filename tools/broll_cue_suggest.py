#!/usr/bin/env python3
"""Suggest sparse B-roll texture cues for the editor.

Reads assets.md or script.md for beat structure and emits simple, non-invented
cue suggestions for optional abstract texture under cards on the BROLL track.
Does not generate footage, write files, or call external services.

Reduces the recurring labor of deciding where to place optional B-roll
texture on the BROLL track for every future video.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))


def parse_beats(text: str) -> list[str]:
    """Extract beat names from assets.md table or simple headers."""
    beats = []
    in_table = False
    for line in text.splitlines():
        if "| Beat |" in line:
            in_table = True
            continue
        if in_table and line.startswith("|") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells and cells[0]:
                beats.append(cells[0])
        elif in_table and not line.startswith("|"):
            break
    if not beats:
        for line in text.splitlines():
            if line.lower().startswith(("## beat", "### beat", "hook", "payoff", "cta")):
                beats.append(line.strip("# ").strip())
    return beats[:8]


def suggest_cues(beats: list[str]) -> list[str]:
    """Return a short list of operational B-roll cue suggestions. No invented footage."""
    if not beats:
        return ["No beats found. Run asset_brief.py first."]
    cues = [
        "BROLL: none required. Cards and VO carry the video.",
        "BROLL: optional subtle texture under body beats only (never under hook or CTA).",
        "BROLL: keep opacity low; never cover card text or fight the spoken words.",
    ]
    if any("payoff" in b.lower() for b in beats):
        cues.append("BROLL: optional slight lift or change of texture at payoff (still under cards).")
    if any("cta" in b.lower() or "end" in b.lower() for b in beats):
        cues.append("BROLL: fade out before the final CTA and end-screen reserve (last 20s clear).")
    cues.append("Rule: B-roll is optional texture. Prefer no B-roll over distracting footage. Human decides final placement.")
    return cues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest sparse B-roll texture cues from beat structure. No file writes."
    )
    parser.add_argument("packet", help="Packet folder containing assets.md or script.md")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    source = "assets.md"
    assets = path / "assets.md"
    text = ""
    if assets.is_file():
        text = assets.read_text(encoding="utf-8")
    else:
        script = path / "script.md"
        if script.is_file():
            text = script.read_text(encoding="utf-8")
            source = "script.md"
        else:
            print("No assets.md or script.md found.")
            return 1

    beats = parse_beats(text)
    cues = suggest_cues(beats)

    print("BROLL TEXTURE CUE SUGGESTIONS (sparse; optional; no invented footage)")
    print(f"Source: {source}")
    print(f"Beats detected: {', '.join(beats) if beats else 'none'}")
    print("Use these as starting points for the optional BROLL track in the editor.")
    print("=" * 72)
    print()
    for i, c in enumerate(cues, 1):
        print(f"{i}. {c}")
    print()
    print("=" * 72)
    print("Next: place optional texture in the NLE or leave the track empty. Cards carry the message.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
