#!/usr/bin/env python3
"""Generate a YouTube-friendly chapters list from script.md section WORDS.

Extracts standard sections (Hook, Body, Payoff, CTA and any ## headers),
counts spoken words, estimates cumulative start times at 150 wpm,
and writes a simple chapters.txt (or prints) suitable for description or Studio.
Output stays local / can be gitignored. No invented content, no external services.
Reduces recurring human labor of manually timing chapters on every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from phrase_utils import spoken_words
except ImportError:
    def spoken_words(text: str) -> str:
        return text

WPM = 150


def extract_sections(text: str) -> list[tuple[str, str]]:
    """Return list of (header, words_text) preserving order."""
    sections: list[tuple[str, str]] = []
    current_header = None
    current_lines: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("##"):
            if current_header is not None:
                body = "\n".join(current_lines)
                sections.append((current_header, spoken_words(body)))
            current_header = stripped.lstrip("#").strip()
            current_lines = []
            continue
        if current_header is not None:
            if stripped.startswith("WORDS") or stripped.startswith("VISUAL") or not stripped:
                continue
            current_lines.append(line)

    if current_header is not None:
        body = "\n".join(current_lines)
        sections.append((current_header, spoken_words(body)))

    if not sections:
        # fallback whole body
        body = spoken_words(text)
        if body.strip():
            sections.append(("Full script", body))
    return sections


def format_time(seconds: int) -> str:
    m, s = divmod(max(0, seconds), 60)
    return f"{m}:{s:02d}"


def main() -> int:
    p = argparse.ArgumentParser(description="Generate chapters list from script.md")
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    p.add_argument("--out", type=Path, default=None, help="Optional output path (default: print + packet/chapters_estimate.txt)")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    script = packet / "script.md"
    if not script.is_file():
        print("ERROR: script.md missing", file=sys.stderr)
        return 1

    text = script.read_text(encoding="utf-8")
    sections = extract_sections(text)

    lines = ["# Estimated chapters (150 wpm from section WORDS)"]
    cumulative = 0
    for header, words in sections:
        count = len(words.split()) if words else 0
        start = format_time(cumulative)
        lines.append(f"{start} {header} ({count} words)")
        cumulative += round(count / WPM * 60)

    total_sec = cumulative
    lines.append("")
    lines.append(f"# Total estimated duration: {format_time(total_sec)} ({total_sec}s)")
    lines.append("# Estimates only — replace with real VO timings after narration exists.")

    out_text = "\n".join(lines) + "\n"
    out_path = args.out or (packet / "chapters_estimate.txt")
    out_path.write_text(out_text, encoding="utf-8")

    print(out_text)
    print(f"wrote: {out_path}")
    print(f"sections: {len(sections)}")
    print(f"est_total_s: {total_sec}")
    print("Chapters estimate ready (local; gitignore if desired).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
