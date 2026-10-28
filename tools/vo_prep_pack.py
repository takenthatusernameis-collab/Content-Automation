#!/usr/bin/env python3
"""Generate a local VO preparation pack from script.md spoken WORDS.

Extracts ## sections and WORDS blocks, computes word counts and estimated
durations at 150 wpm, and writes a paste-ready vo_prep.md with a clean
reading script, section markers, cumulative timings, and simple practice
notes (long sections or numbers).

No invented content. Output stays local and gitignored. Not a real VO
recording. Reduces recurring human labor of extracting clean spoken text,
estimating section lengths, and preparing recording markers on every future
packet before a Selected VO take exists.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WPM = 150


def extract_spoken_blocks(text: str) -> list[tuple[str, str]]:
    """Return list of (header, spoken_text) in order. Only WORDS content."""
    sections: list[tuple[str, str]] = []
    pattern = re.compile(r"^##\s+(.+?)\s*$", re.M)
    matches = list(pattern.finditer(text))
    for i, m in enumerate(matches):
        header = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        wm = re.search(r"WORDS:\s*(.*?)(?:\nVISUAL:|\n##|\Z)", block, re.S | re.I)
        if wm:
            spoken = wm.group(1).strip()
            spoken = re.sub(r"\s+", " ", spoken)
            if spoken:
                sections.append((header, spoken))
    return sections


def format_time(seconds: float) -> str:
    if seconds < 0:
        seconds = 0.0
    total = int(round(seconds))
    m, s = divmod(total, 60)
    return f"{m}:{s:02d}"


def find_numbers(text: str) -> list[str]:
    return re.findall(r"\b\d+(?:\.\d+)?%?\b", text)


def main() -> int:
    p = argparse.ArgumentParser(description="Generate VO preparation pack from script.md")
    p.add_argument("packet", type=Path, help="Path to packet directory")
    p.add_argument("--force", action="store_true", help="Overwrite existing vo_prep.md")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    script_path = packet / "script.md"
    if not script_path.is_file():
        print("FAIL: script.md missing", file=sys.stderr)
        return 2

    out_path = packet / "vo_prep.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    text = script_path.read_text(encoding="utf-8")
    blocks = extract_spoken_blocks(text)
    if not blocks:
        print("FAIL: no spoken WORDS found in script.md", file=sys.stderr)
        return 2

    lines: list[str] = [
        "# VO Preparation Pack",
        "",
        "Generated locally from script.md WORDS blocks. Estimated at 150 wpm.",
        "Not a real recording. Use for reading practice, section markers, and timing estimates.",
        "",
        "## Overview",
        "",
    ]

    total_words = 0
    cumulative = 0.0
    section_rows: list[str] = []
    practice_notes: list[str] = []
    reading_script: list[str] = []

    for idx, (header, spoken) in enumerate(blocks, 1):
        words = spoken.split()
        wc = len(words)
        total_words += wc
        duration = (wc / WPM) * 60.0
        start = cumulative
        cumulative += duration

        section_rows.append(
            f"| {idx} | {header} | {wc} | {format_time(start)} | {format_time(duration)} |"
        )

        if duration > 45:
            practice_notes.append(f"- Section {idx} ({header}) is ~{format_time(duration)} \u2014 consider a breath marker.")

        nums = find_numbers(spoken)
        if nums:
            practice_notes.append(f"- Section {idx} contains numbers: {', '.join(nums)}")

        reading_script.append(f"### {idx}. {header}  (~{format_time(start)})")
        reading_script.append("")
        reading_script.append(spoken)
        reading_script.append("")

    total_sec = int(round(cumulative))
    lines.append(f"- Total words: {total_words}")
    lines.append(f"- Estimated duration: {format_time(cumulative)} ({total_sec}s)")
    lines.append(f"- Sections: {len(blocks)}")
    lines.append("")
    lines.append("## Section Timings")
    lines.append("")
    lines.append("| # | Section | Words | Start | Duration |")
    lines.append("|---|---|---|---|---|")
    lines.extend(section_rows)
    lines.append("")

    if practice_notes:
        lines.append("## Practice Notes")
        lines.append("")
        lines.extend(practice_notes)
        lines.append("")

    lines.append("## Clean Reading Script")
    lines.append("")
    lines.extend(reading_script)
    lines.append("---")
    lines.append("End of spoken text. Record or review against these markers.")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"sections: {len(blocks)}")
    print(f"words: {total_words}")
    print(f"est_total: {format_time(cumulative)}")
    print("VO prep pack ready (local; estimated timings only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
