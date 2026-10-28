#!/usr/bin/env python3
"""Generate a local end-screen preparation pack from script.md spoken WORDS.

Estimates total duration at 150 wpm, identifies spoken text that falls in the
final ~20 seconds (reserved for YouTube end-screen elements per format.md),
extracts the CTA section if present, and writes end_screen_prep.md with
placement notes and simple card text suggestions.

No invented content. Output stays local and gitignored. Reduces recurring
human labor of calculating end-screen window and extracting CTA for cards
on every future packet before a Selected VO take exists.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WPM = 150
END_SCREEN_SECONDS = 20


def extract_spoken_blocks(text: str) -> list[tuple[str, str]]:
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


def main() -> int:
    p = argparse.ArgumentParser(description="Generate end-screen prep from script.md")
    p.add_argument("packet", type=Path, help="Path to packet directory")
    p.add_argument("--force", action="store_true", help="Overwrite existing end_screen_prep.md")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    script_path = packet / "script.md"
    if not script_path.is_file():
        print("FAIL: script.md missing", file=sys.stderr)
        return 2

    out_path = packet / "end_screen_prep.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    text = script_path.read_text(encoding="utf-8")
    blocks = extract_spoken_blocks(text)
    if not blocks:
        print("FAIL: no spoken WORDS found in script.md", file=sys.stderr)
        return 2

    # Build cumulative timings
    cumulative = 0.0
    timed: list[tuple[str, str, float, float]] = []  # header, spoken, start, duration
    for header, spoken in blocks:
        wc = len(spoken.split())
        dur = (wc / WPM) * 60.0
        timed.append((header, spoken, cumulative, dur))
        cumulative += dur

    total_sec = cumulative
    end_window_start = max(0.0, total_sec - END_SCREEN_SECONDS)

    lines: list[str] = [
        "# End-Screen Prep",
        "",
        "Generated locally from script.md WORDS blocks. Estimated at 150 wpm.",
        "Format reserves the last ~20 seconds for YouTube end-screen elements.",
        "Not a rewrite. Review for placement and CTA card text.",
        "",
        f"Estimated total duration: {format_time(total_sec)} ({int(round(total_sec))}s)",
        f"End-screen window starts at: {format_time(end_window_start)}",
        "",
    ]

    # Text that falls in the end window
    end_text_parts: list[str] = []
    for header, spoken, start, dur in timed:
        section_end = start + dur
        if section_end > end_window_start:
            # overlap
            overlap_start = max(start, end_window_start)
            # rough word estimate for overlap
            overlap_dur = section_end - overlap_start
            if overlap_dur > 0.5:
                end_text_parts.append(f"**{header}** (from {format_time(overlap_start)}): {spoken}")

    lines.append("## Spoken text overlapping last 20s")
    lines.append("")
    if end_text_parts:
        lines.extend(end_text_parts)
    else:
        lines.append("(none — script shorter than 20s or no overlap)")
    lines.append("")

    # CTA extraction
    cta_spoken = None
    for header, spoken in blocks:
        if re.search(r"cta|call.to.action|end", header, re.I):
            cta_spoken = spoken
            break
    if not cta_spoken and blocks:
        # fallback to last section
        cta_spoken = blocks[-1][1]

    lines.append("## CTA section (for card text)")
    lines.append("")
    if cta_spoken:
        lines.append(cta_spoken)
        lines.append("")
        # simple first-sentence suggestion
        first_sent = re.split(r'(?<=[.!?])\s+', cta_spoken.strip())[0]
        lines.append(f"Suggested short card line: {first_sent[:80]}{'...' if len(first_sent) > 80 else ''}")
    else:
        lines.append("(no CTA-like section found)")
    lines.append("")

    lines.append("---")
    lines.append("Place end-screen cards/elements after the estimated window start. Do not invent timings from a real take.")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"est_total: {format_time(total_sec)}")
    print(f"end_window_start: {format_time(end_window_start)}")
    print("End-screen prep ready (local; estimated only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
