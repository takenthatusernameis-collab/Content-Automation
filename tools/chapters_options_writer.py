#!/usr/bin/env python3
"""Write a local chapters_options.md with grounded chapter title candidates.

Prefers script.md (or draft.md) sections via shared extract_sections when present,
computes cumulative timestamps with count_spoken_words + effective_rate,
and emits short operational title candidates per section using phrase_utils.shorten.
Falls back to idea.md fields with format-target timing when no script exists.
No invented spoken lines, claims, or numbers. Output stays local (gitignored).
Reduces recurring labor of manually drafting concise chapter titles and rough
timestamps for every future packet. Aligns with channel voice, format timing,
chapters_scan rules, and no-invent rule. Complements chapters_writer.py and
chapters_scan.py. Not a final chapters file; human or later scan selects lines
for chapters.md or publish.md Description.

Uses shared phrase_utils.shorten so short titles prefer natural clause/word
breaks, matching title_options_writer, description_options_writer,
thumbnail_generator, card_generator, end_screen_options_writer, and
tags_options_writer. Improves textual consistency of the channel promise
across every future packet automatically when generating chapter options.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract as idea_extract  # noqa: E402
from phrase_utils import (  # noqa: E402
    shorten,
    extract_sections,
    count_spoken_words,
    effective_rate,
)


def fmt_time(secs: float) -> str:
    total = max(0, int(round(secs)))
    m = total // 60
    s = total % 60
    return f"{m}:{s:02d}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write local chapters_options.md from script sections or idea.md"
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"FAIL: not a directory: {packet}", file=sys.stderr)
        return 1

    out_path = packet / "chapters_options.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    # Prefer real script structure when available
    script_path = packet / "script.md"
    draft_path = packet / "draft.md"
    source_path = None
    source_label = ""
    if script_path.is_file():
        source_path = script_path
        source_label = "script.md"
    elif draft_path.is_file():
        source_path = draft_path
        source_label = "draft.md"

    idea_path = packet / "idea.md"
    mech, problem, topic = ("", "", "")
    if idea_path.is_file():
        idea_text = idea_path.read_text(encoding="utf-8")
        mech, problem, topic = idea_extract(idea_text)

    sections: list[dict] = []
    if source_path:
        text = source_path.read_text(encoding="utf-8")
        sections = extract_sections(text)

    lines = [
        "# Chapters Options (local; grounded candidates)",
        "",
        "Generated locally from packet structure only. No invented claims or statistics.",
        "Short operational chapter title candidates. Channel voice: calm, specific, operational.",
        "Complements chapters_writer.py and chapters_scan.py.",
        "Not a final chapters file. Select preferred titles, run tools/chapters_scan.py,",
        "then copy timestamped lines into chapters.md or publish.md Description.",
        "",
    ]

    if source_path and sections:
        # Accurate timing from actual spoken words
        total_words = sum(count_spoken_words(sec.get("spoken", "")) for sec in sections)
        wpm, rate_label = effective_rate(packet, total_words)
        lines.extend([
            f"Source: {source_label} ({len(sections)} sections)",
            f"Timing: cumulative from spoken words at {wpm} wpm ({rate_label})",
            f"- Topic: {topic or '(none)'}",
            f"- Problem / stall: {problem or '(none)'}",
            f"- Mechanism / default: {mech or '(none)'}",
            "",
            "## Candidates by section",
            "",
        ])
        cumulative = 0.0
        for i, sec in enumerate(sections):
            title = sec.get("title", f"Section {i+1}").strip()
            spoken = sec.get("spoken", "")
            words = count_spoken_words(spoken)
            duration = (words / wpm * 60.0) if wpm > 0 else 0.0
            stamp = fmt_time(cumulative)
            # Generate 2 short candidates from title or first clause of spoken
            base_title = shorten(title, 40) or shorten(spoken, 40)
            cand1 = shorten(f"{base_title}", 45)
            cand2 = shorten(f"{base_title}: {shorten(spoken, 25)}", 50) if spoken else cand1
            lines.append(f"### {stamp} — {title}")
            lines.append(f"1. {cand1}")
            lines.append(f"2. {cand2}")
            lines.append("")
            cumulative += duration
        lines.append(f"Estimated total: {fmt_time(cumulative)}")
    else:
        # Fallback to idea-based fixed targets (matches chapters_writer style)
        if not mech and not problem:
            print("FAIL: no script/draft sections and no mechanism or problem in idea.md", file=sys.stderr)
            return 2
        base = shorten(mech or "written next-action default", 35)
        stall = shorten(problem or "the stall", 30)
        lines.extend([
            "Source: idea.md only (no script.md or draft.md sections)",
            "Timing: rough format.md targets at 150 wpm",
            f"- Topic: {topic or '(none)'}",
            f"- Problem / stall: {problem or '(none)'}",
            f"- Mechanism / default: {mech or '(none)'}",
            "",
            "## Candidates",
            "",
        ])
        times = [0, 10, 32, 104, 176, 248, 320]
        labels = [
            f"Name the stall ({stall}) and install {base}",
            f"Where {base} lives",
            f"Name stall + first verb from {base}",
            f"Place {base} where eyes land",
            f"First concrete action in five minutes",
            f"Point at {base} when stall returns",
            f"Install {base} today",
        ]
        for t, lab in zip(times, labels):
            lines.append(f"{fmt_time(t)} {lab}")
            lines.append("")

    lines.extend([
        "## Notes",
        "- First chapter must be 0:00.",
        "- Minimum 10s gap between chapters (YouTube rule).",
        "- Aim for 3–12 chapters.",
        "- Prefer titles that name the concrete default, the stall, or the install action.",
        "- Avoid weak/engagement-bait patterns (see tools/chapters_scan.py).",
        "- Refine timestamps from real selected VO when available.",
        "",
        "---",
        "Preferred unblocked path remains the human OAuth step for publish.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"source: {source_label or 'idea.md'}")
    print(f"sections: {len(sections)}")
    print("Chapter options ready (local; estimated from packet fields only; select next).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
