#!/usr/bin/env python3
"""Write a local chapters.md with estimated YouTube chapter lines.

Extracts mechanism/problem/topic from idea.md and emits a structured
chapters.md with ## YouTube lines using format.md segment targets at 150 wpm
for rough timestamps (Hook ~10s, Payoff ~22s, each Beat ~72s, CTA ~22s).
Chapter titles are short operational phrases grounded only in those fields.
No invented spoken lines or claims. Output stays local (gitignored).
Reduces recurring labor of manually estimating and writing chapter markers
for every future packet. Aligns with channel voice (assignment, not reply prompt),
format timing, and no-invent rule. Complements word_budget_writer.py and
draft_skeleton_writer.py. Not a final chapters file; human or later tool may refine
from real VO timestamps.
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


def shorten(s: str, n: int) -> str:
    s = (s or "").strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def fmt_time(secs: int) -> str:
    m = secs // 60
    s = secs % 60
    return f"{m}:{s:02d}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write local chapters.md from idea.md fields only"
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"FAIL: not a directory: {packet}", file=sys.stderr)
        return 1

    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print("FAIL: idea.md missing", file=sys.stderr)
        return 2

    out_path = packet / "chapters.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    base = shorten(mech or "the written next-action default", 40)
    stall = shorten(problem or "the stall reopens the list", 40)

    # Rough cumulative seconds from format.md targets at 150 wpm (~2.5 words/sec).
    # Hook 25w ~10s, Payoff 55w ~22s, Beat 180w ~72s each, CTA 55w ~22s.
    times = [0, 10, 32, 104, 176, 248, 320]
    labels = [
        f"Hook: Name the stall ({stall}) and install {base}",
        f"Payoff: Where {base} lives",
        f"Beat 1: Name stall + first verb from {base}",
        f"Beat 2: Place {base} where eyes land",
        f"Beat 3: First concrete action in five minutes",
        f"Beat 4: Point at {base} when stall returns",
        f"CTA: Install {base} today",
    ]

    lines = [
        "# Chapters (local; estimated from format targets)",
        "",
        "Generated locally from idea.md mechanism/problem/topic only.",
        "Estimated YouTube chapter lines using docs/format.md spoken-word targets",
        "at 150 wpm. Refine timestamps from real selected VO when available.",
        "Titles are short operational phrases. No invented claims or statistics.",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "Complements word_budget_writer.py and draft_skeleton_writer.py.",
        "Not a final chapters file. Copy preferred lines into publish.md Description",
        "or keep this file for chapters_scan.py.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem / stall: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "## YouTube lines",
        "",
    ]
    for t, lab in zip(times, labels):
        lines.append(f"{fmt_time(t)} {lab}")
    lines.extend([
        "",
        "## Notes",
        "- First chapter must be 0:00.",
        "- Minimum 10s gap between chapters (YouTube rule).",
        "- Aim for 3–12 chapters.",
        "- Run tools/chapters_scan.py after filling real times.",
        "",
        "---",
        "Preferred unblocked path remains the human OAuth step for publish.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print(f"topic_found: {bool(topic)}")
    print(f"chapters: {len(times)}")
    print("Chapters ready (local; estimated from packet fields only; refine with VO).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
