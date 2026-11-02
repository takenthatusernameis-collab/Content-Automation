#!/usr/bin/env python3
"""Generate estimated YouTube chapter lines from script sections.

Extracts ## sections via phrase_utils.extract_sections, estimates timestamps
from spoken word counts using effective_rate (observed VO or policy WPM),
and emits a chapters.md skeleton with first-line 0:00 and >=10s gaps.

Uses shared shorten and normalize so titles stay operational and avoid
weak patterns. Does not invent content beyond existing section titles
and first spoken sentences. Does not write unless --write. Output is
local. Compounds script structure into a ready chapter draft that
reduces manual timing labor for every future packet.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from phrase_utils import (
    extract_sections,
    count_spoken_words,
    effective_rate,
    shorten,
    normalize,
)


def format_stamp(seconds: float) -> str:
    """Format seconds as M:SS or H:MM:SS."""
    s = int(round(seconds))
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    if h:
        return f"{h}:{m:02d}:{sec:02d}"
    return f"{m}:{sec:02d}"


def generate_chapters(packet: Path) -> str:
    script = packet / "script.md"
    if not script.is_file():
        return "# Chapters\n\nNo script.md found. Run after apply_script.\n"

    text = script.read_text(encoding="utf-8")
    sections = extract_sections(text)
    if not sections:
        return "# Chapters\n\nNo ## sections extracted.\n"

    # Prefer spoken word count for rate; fall back to total
    total_words = sum(count_spoken_words(s["spoken"]) for s in sections)
    wpm, rate_label = effective_rate(packet, total_words)

    lines = [
        "# Chapters",
        "",
        f"Estimated from script.md sections using {wpm} WPM ({rate_label}).",
        "First line is 0:00. Gaps enforced at >=10s where possible.",
        "Titles shortened from section headings or first spoken sentence.",
        "Review and adjust before pasting into publish.md Description or chapters.md.",
        "Does not invent claims. Hits against chapters_scan are revision signals.",
        "",
        "## YouTube lines",
        "",
    ]

    t = 0.0
    for i, sec in enumerate(sections):
        spoken_wc = count_spoken_words(sec["spoken"])
        duration = (spoken_wc / wpm) * 60.0 if wpm else 10.0
        # Enforce minimum 10s gap after the first
        if i > 0 and (t - prev_t) < 10.0:
            t = prev_t + 10.0
        stamp = format_stamp(t)
        # Prefer shortened section title; fall back to first spoken clause
        title = sec["title"]
        # Strip common prefixes
        title = re_sub_title(title)
        short_title = shorten(title, max_len=40)
        if not short_title or len(short_title.split()) < 2:
            first = sec["spoken"].split(".")[0].strip() if sec["spoken"] else title
            short_title = shorten(first, max_len=40) or title[:40]
        short_title = normalize(short_title).strip(" .")
        lines.append(f"{stamp} {short_title}")
        prev_t = t
        t += max(duration, 10.0)

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append(f"Total estimated duration: {format_stamp(t)} at {wpm} WPM.")
    lines.append("Run python3 tools/chapters_scan.py <packet> after review.")
    lines.append("")
    return "\n".join(lines) + "\n"


def re_sub_title(title: str) -> str:
    """Clean common section title prefixes for chapter use."""
    import re
    title = re.sub(r"^Hook\s*\([^)]+\)", "Hook", title, flags=re.I)
    title = re.sub(r"^Beat\s+\d+\s*[\u2014\-]\s*", "", title, flags=re.I)
    title = re.sub(r"^Payoff promise", "Payoff", title, flags=re.I)
    title = re.sub(r"^CTA", "Next action", title, flags=re.I)
    return title.strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate estimated chapters.md from script sections."
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--write", action="store_true", help="Write chapters.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"Not a directory: {packet}", file=sys.stderr)
        return 1

    out = packet / "chapters.md"
    content = generate_chapters(packet)

    if args.write:
        if out.exists() and not args.force:
            print(f"SKIP: {out} exists (use --force)")
            return 0
        out.write_text(content, encoding="utf-8")
        print(f"WROTE: {out}")
    else:
        print(content)
        print("(dry-run; use --write to save)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
