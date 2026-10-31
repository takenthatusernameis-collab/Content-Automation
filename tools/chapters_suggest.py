#!/usr/bin/env python3
"""Suggest YouTube chapter timestamps from script sections.

Reads draft.md or script.md, extracts ## sections via shared helpers,
estimates cumulative spoken time using effective_rate (observed WPM preferred,
else 190/140), and prints ready-to-paste chapter lines starting at 0:00.
Flags short gaps (<10s) and low chapter count so the output is immediately
usable for description.md or chapters.md. Does not rewrite files or invent
titles. Reduces recurring manual timestamp arithmetic for chapters on every
future packet.

Uses shared phrase_utils.extract_sections, count_spoken_words, effective_rate.
Complements chapters_scan (quality of existing lines) with generation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import extract_sections, count_spoken_words, effective_rate  # noqa: E402


def format_stamp(seconds: float) -> str:
    """Format seconds as M:SS or H:MM:SS for YouTube chapters."""
    total = int(round(seconds))
    if total < 3600:
        m, s = divmod(total, 60)
        return f"{m}:{s:02d}"
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}"


def clean_title(title: str) -> str:
    """Shorten section title for a chapter label without inventing text."""
    # Prefer the first meaningful clause or up to ~40 chars, whole words
    t = title.strip()
    for sep in (" — ", " - ", ": ", " | "):
        if sep in t:
            t = t.split(sep)[0].strip()
            break
    if len(t) > 50:
        words = t.split()
        out = []
        for w in words:
            trial = " ".join(out + [w])
            if len(trial) > 48:
                break
            out.append(w)
        t = " ".join(out) if out else t[:48]
    return t or "Section"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest YouTube chapter lines from packet sections and estimated times. No file writes."
    )
    parser.add_argument("packet", type=Path, help="Packet folder under videos/")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if fewer than 3 chapters or any gap <10s")
    args = parser.parse_args()

    path = args.packet.resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    draft = path / "draft.md"
    script = path / "script.md"
    source = draft if draft.is_file() else script
    if not source.is_file():
        print(f"No draft.md or script.md in {path}")
        return 0

    text = source.read_text(encoding="utf-8")
    sections = extract_sections(text)
    if not sections:
        print("No ## sections extracted")
        return 0

    # Total words for rate selection (observed preferred)
    total_words = sum(count_spoken_words(sec["spoken"]) for sec in sections)
    rate, rate_label = effective_rate(path, total_words)

    print("CHAPTERS SUGGEST (estimated timestamps for YouTube description)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print(f"Clock: ~{rate} wpm ({rate_label})")
    print()
    print("Suggested lines (paste into description or chapters.md ## YouTube lines):")
    print()

    cumulative = 0.0
    issues = 0
    chapter_count = 0
    prev_stamp_sec = -999.0

    # Always start at 0:00 with the first section
    for i, sec in enumerate(sections):
        words = count_spoken_words(sec["spoken"])
        dur = (words / rate) * 60.0 if words and rate else 0.0
        stamp = format_stamp(cumulative)
        title = clean_title(sec["title"])
        print(f"{stamp} {title}")
        chapter_count += 1

        # Check gap from previous (YouTube requires >=10s)
        if i > 0 and (cumulative - prev_stamp_sec) < 10.0:
            print(f"  [GAP] only {cumulative - prev_stamp_sec:.1f}s from previous (YouTube wants >=10s)")
            issues += 1
        prev_stamp_sec = cumulative
        cumulative += dur

    print()
    print(f"Total estimated duration: {format_stamp(cumulative)} ({cumulative:.0f}s)")
    print(f"Chapters suggested: {chapter_count}")

    if chapter_count < 3:
        print("[COUNT] fewer than 3 chapters (YouTube chapters need at least 3)")
        issues += 1
    else:
        print("[OK] chapter count meets minimum")

    if issues == 0:
        print("Suggestions look usable. Confirm timestamps against a real Selected VO when available.")
    else:
        print("Review flagged gaps or count before pasting. Merge short sections if needed.")

    print()
    print("YouTube rules: first timestamp 0:00, at least 3 chapters, each gap >=10s.")
    print("This tool writes nothing. Complements chapters_scan for quality of the lines you keep.")
    return 1 if args.strict and issues else 0


if __name__ == "__main__":
    sys.exit(main())
