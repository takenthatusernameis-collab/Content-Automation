#!/usr/bin/env python3
"""Write a local first_comment_options.md with grounded pin candidates.

Extracts mechanism/problem/topic from idea.md and emits a structured
first_comment_options.md with 4 short operational first-comment / pin candidates
grounded only in those fields. No invented claims, numbers, or engagement bait.
Output stays local (gitignored). Reduces recurring labor of manually drafting
the pinned first comment for every future packet. Aligns with channel voice
(assignment, not reply prompt), first-comment rules (calm, specific, concrete
next action), and no-invent rule. Complements first_comment_scan.py.
Not a final pin; human or later scan selects one for publish.md ## First comment.

Uses shared phrase_utils.shorten so short phrases prefer natural clause/word
breaks, matching title_options_writer, description_options_writer,
tags_options_writer, chapters_options_writer, and end_screen_options_writer.
Improves textual consistency of the channel promise across every future packet
automatically when generating first-comment options.
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
from phrase_utils import shorten  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write local first_comment_options.md from idea.md fields only"
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

    out_path = packet / "first_comment_options.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    base = shorten(mech or "the written next-action default", 40)
    stall = shorten(problem or "the stall", 30)
    top = shorten(topic or "focused work", 25)

    candidates = [
        f"Write the {base} on disk today so {stall} stops reopening the list.",
        f"Install the {base} before the next decision on {top}.",
        f"Name the {stall}. Place the {base} where your eyes land.",
        f"Same-day install: the {base} is the default when {stall} returns.",
    ]

    lines = [
        "# First Comment Options (local; grounded candidates)",
        "",
        "Generated locally from idea.md mechanism/problem/topic only.",
        "Four short operational first-comment / pin candidates. No invented claims, numbers, or engagement bait.",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "Complements first_comment_scan.py.",
        "Not a final pin. Select one, run tools/first_comment_scan.py, then copy to publish.md ## First comment.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem / stall: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "## Candidates",
        "",
    ]
    for i, cand in enumerate(candidates, 1):
        lines.append(f"{i}. {cand}")
    lines.extend([
        "",
        "## Notes",
        "- Prefer pins that name the concrete default and the stall.",
        "- Avoid weak/engagement-bait patterns (see tools/first_comment_scan.py / phrase_utils FIRST_COMMENT_BAIT_PATTERNS).",
        "- The pin is the assignment from the mechanism, not a reply prompt or subscribe call.",
        "- Keep under ~25 words for the final version.",
        "",
        "---",
        "Preferred unblocked path remains the human OAuth step for publish.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print(f"topic_found: {bool(topic)}")
    print(f"candidates: {len(candidates)}")
    print("First-comment options ready (local; estimated from packet fields only; select next).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
