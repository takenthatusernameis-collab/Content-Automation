#!/usr/bin/env python3
"""Print structured chapter candidates from script beats with estimated times.

Parses script.md (or draft.md) for ## beat headings with WORDS blocks.
Estimates cumulative start times at 150 wpm (same band as format.md).
Suggests short chapter titles from the first sentence of each beat (via shared shorten).
Flags weak patterns from CHAPTER_WEAK_PATTERNS. Enforces rough 10s minimum gap by skipping close estimates.
Does not invent content, write files, poll secrets, or call external services.
Exit 0 always (informational).
Useful for pre-VO chapter planning before captions.srt exists. Complements chapter_draft.py (requires srt) and chapters_scan.py.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import (  # type: ignore
    spoken_words,
    normalize,
    shorten,
    CHAPTER_WEAK_PATTERNS,
    compile_word_boundary_patterns,
)

WPM = 150.0
MIN_GAP_S = 10.0
HEADING_RE = re.compile(r"^##\s+(.+)$", re.M)


def _words(text: str) -> int:
    return len(re.findall(r"[a-z0-9']+", text.lower()))


def parse_beats(script: str) -> list[dict]:
    beats = []
    parts = HEADING_RE.split(script)
    if len(parts) < 3:
        return beats
    for heading, body in zip(parts[1::2], parts[2::2]):
        if "WORDS:" not in body:
            continue
        spoken = body.split("WORDS:", 1)[1]
        spoken = spoken.split("VISUAL:", 1)[0]
        tokens = _words(spoken)
        if tokens < 5:
            continue
        label = heading.strip()
        label = re.sub(r"\s*\([^)]*\)\s*", " ", label).strip(" -—")
        sentence = re.split(r"[.!?]", spoken.strip(), maxsplit=1)[0].strip()
        beats.append({
            "heading": heading.strip(),
            "label": label,
            "spoken": spoken.strip(),
            "sentence": sentence,
            "words": tokens,
        })
    return beats


def estimate_chapters(beats: list[dict]) -> list[dict]:
    chapters = []
    cum_words = 0
    prev_s = -MIN_GAP_S
    for beat in beats:
        start_s = (cum_words / WPM) * 60.0
        if start_s - prev_s >= MIN_GAP_S or not chapters:
            title = shorten(beat["sentence"] or beat["label"], max_len=42)
            if not title:
                title = beat["label"][:42] or "Chapter"
            chapters.append({
                "start_s": start_s,
                "title": title,
                "spoken_preview": beat["sentence"][:80],
                "words": beat["words"],
            })
            prev_s = start_s
        cum_words += beat["words"]
    # Force first to 0 if we have any
    if chapters:
        chapters[0]["start_s"] = 0.0
    return chapters


def _clock(seconds: float) -> str:
    total = max(0, int(seconds))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def hits_weak(text: str, patterns, compiled) -> list[str]:
    found = []
    for phrase, cre in zip(patterns, compiled):
        if cre.search(text):
            found.append(phrase)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print script-derived chapter candidates with estimated times. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    parser.add_argument(
        "--prefer",
        choices=("script", "draft", "auto"),
        default="auto",
        help="Which file to prefer for spoken WORDS (default: auto)",
    )
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("SCRIPT-TO-CHAPTER CANDIDATES (informational only; no writes)")
    print(f"Packet: {path.name}")
    print(f"Estimate: {WPM:.0f} wpm, min gap ~{MIN_GAP_S:.0f}s. Not ASR. Not final times.")
    print()

    script_path = path / "script.md"
    draft_path = path / "draft.md"
    chosen = None
    if args.prefer == "script" and script_path.is_file():
        chosen = script_path
    elif args.prefer == "draft" and draft_path.is_file():
        chosen = draft_path
    else:
        if script_path.is_file():
            chosen = script_path
        elif draft_path.is_file():
            chosen = draft_path

    if not chosen:
        print("No script.md or draft.md found.")
        print("This tool writes nothing.")
        return 0

    text = chosen.read_text(encoding="utf-8")
    beats = parse_beats(text)
    chapters = estimate_chapters(beats)

    weak_compiled = compile_word_boundary_patterns(CHAPTER_WEAK_PATTERNS)

    print("Suggested chapter candidates section (copy into chapters.md or publish.md Description; fill only with deliberate choices):")
    print("---")
    print("## Script-derived chapter candidates (baseline only; human decides final titles and times)")
    print()
    print("Chapters should name the concrete beat mechanism or next action. Prefer specific operational language. Times are estimates only until real VO + captions exist.")
    print()
    if chapters:
        for i, ch in enumerate(chapters, 1):
            preview = ch["spoken_preview"].replace("\n", " ")
            if len(preview) > 70:
                preview = preview[:70] + "..."
            title = ch["title"]
            weak_hits = hits_weak(title, CHAPTER_WEAK_PATTERNS, weak_compiled)
            print(f"{i}. Estimated: {_clock(ch['start_s'])}")
            print(f"   Spoken signal: {preview}")
            print(f"   Suggested title: {title}")
            if weak_hits:
                print(f"   - weak_chapter_patterns: {', '.join(weak_hits)} (rewrite to name the concrete mechanism)")
            else:
                print("   - weak_chapter_patterns: none")
            print("   - final_choice: (select or rewrite; leave blank until decided)")
            print()
    else:
        print("(none extracted; review script beats manually)")
        print()
    print("### Reminder")
    print("- Prefer calm, specific titles matching docs/channel.md voice.")
    print("- Avoid generic weak titles (see chapters_scan.py).")
    print("- YouTube requires first chapter at 0:00 and >=10s gaps.")
    print("- These are starters only; confirm against real take timing later.")
    print("- Run tools/chapter_draft.py after captions.srt exists, then tools/chapters_scan.py.")
    print("- Do not invent claims or commit secrets.")
    print("---")
    print()
    print("This skeleton does not invent content or write files.")
    print("Useful before VO for chapter planning to reduce blank-page work on every packet.")
    print("Complements tools/chapter_draft.py (srt-based) and tools/chapters_scan.py.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
