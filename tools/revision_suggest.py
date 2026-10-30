#!/usr/bin/env python3
"""Targeted revision suggestions from common signals.

Reads idea.md and script.md (or draft). For long VISUAL cues, repeated
phrases, missing metadata sections, and bait comments, prints short
packet-grounded candidates or stubs. Does not write files, invent full
scripts, or poll secrets. A suggestion is a starting point for human or
agent edit, not an automatic rewrite.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from idea_utils import extract
from phrase_utils import shorten as _shorten

ROOT = Path(__file__).resolve().parents[1]
MAX_VIS_WORDS = 6
MAX_VIS_CHARS = 50


def extract_visuals(text: str) -> list[dict[str, str]]:
    visuals = []
    parts = re.split(r"^##[ \t]+", text, flags=re.M)
    for part in parts[1:]:
        lines = part.splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:])
        vis_m = re.search(r"VISUAL:\s*(.*?)(?:WORDS:|ON SCREEN:|^##|\Z)", body, re.S | re.I)
        if vis_m:
            need = re.sub(r"\s+", " ", vis_m.group(1)).strip()
            if need:
                visuals.append({"title": title, "need": need})
    return visuals


def shorten_visual(need: str, mech: str) -> list[str]:
    """Propose 2 shorter stage directions grounded in mechanism."""
    base = _shorten(mech.lower(), 25) if mech else "next-action default"
    clean = re.sub(r"[*]{1,2}", "", need).strip()
    if len(clean.split()) <= MAX_VIS_WORDS and len(clean) <= MAX_VIS_CHARS:
        return []
    candidates = [
        f"Card with {base}. List closed.",
        f"Sticky: {base}. No list.",
        f"Desk edge: {base} visible.",
        f"One sentence on card. Planner shut.",
    ]
    out = []
    for c in candidates:
        if len(c.split()) <= MAX_VIS_WORDS and len(c) <= MAX_VIS_CHARS:
            out.append(c)
    return out[:2] or [f"Short: {base}."]


def top_repeats(text: str, n: int = 3) -> list[str]:
    """Simple bigram counter for revision hint."""
    words = re.findall(r"\b[a-z]{3,}\b", text.lower())
    bigrams = {}
    for i in range(len(words) - 1):
        bg = f"{words[i]} {words[i+1]}"
        bigrams[bg] = bigrams.get(bg, 0) + 1
    ranked = sorted(bigrams.items(), key=lambda x: -x[1])
    return [bg for bg, cnt in ranked if cnt >= 3][:n]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print targeted revision suggestions for common signals. No writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    idea_path = path / "idea.md"
    idea_text = idea_path.read_text(encoding="utf-8") if idea_path.is_file() else ""
    mech, problem, topic = extract(idea_text)
    if not mech:
        mech = "written next-action default"

    script_path = path / "script.md"
    draft_path = path / "draft.md"
    source = script_path if script_path.is_file() else draft_path
    if not source.is_file():
        print("No script.md or draft.md", file=sys.stderr)
        return 1
    script_text = source.read_text(encoding="utf-8")

    print("REVISION SUGGESTIONS (packet-grounded candidates; no invent, no write)")
    print(f"packet: {path.name}")
    print(f"mechanism: {mech}")
    print()

    # Visual long cues
    visuals = extract_visuals(script_text)
    long_vis = []
    for v in visuals:
        words = len(v["need"].split())
        chars = len(v["need"])
        if words > MAX_VIS_WORDS or chars > MAX_VIS_CHARS:
            long_vis.append(v)
    if long_vis:
        print("## Long VISUAL cues (shorten for card readability)")
        for v in long_vis:
            print(f"- {v['title']}: {v['need'][:80]}...")
            suggs = shorten_visual(v["need"], mech)
            for s in suggs:
                print(f"  suggest: *{s}*")
        print()

    # Cadence / repeats
    repeats = top_repeats(script_text)
    if repeats:
        print("## Repeated phrases (vary or cut for cadence)")
        for r in repeats:
            print(f"- '{r}' appears often; prefer mechanism-specific wording or shorter sentence.")
        print(f"  hint: replace one occurrence of the top phrase with a direct verb from the {mech}.")
        print()

    # Missing sections stubs
    thumb_path = path / "thumbnail.md"
    if not thumb_path.is_file() or "thumbnail" not in thumb_path.read_text(encoding="utf-8").lower():
        print("## Missing thumbnail section")
        print("Stub to paste into thumbnail.md:")
        print("---")
        print("## Thumbnail")
        print(f"Text: {topic or 'Stop deciding what to work on'}")
        print("Visual: simple card with the mechanism sentence, high contrast, no list open.")
        print("---")
        print()

    # First comment non-bait
    print("## First comment (avoid bait / reply prompts)")
    print("Suggested non-bait:")
    print(f"- The default is one written next-action sentence: verb, object, place. Put it where morning-you sees it first.")
    print(f"- Night write, morning start. The stop rule stays on the same surface.")
    print()

    print("These are starting points only. Revise the packet files, then re-run revision_signals.py or the prep suites.")
    print("Does not write files. Does not invent full content. Prefer human OAuth for publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
