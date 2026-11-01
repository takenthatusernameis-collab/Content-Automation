#!/usr/bin/env python3
"""Write a local description_options.md with grounded description candidates.

Extracts mechanism/problem/topic from idea.md (or prefers shortened primary from
assignment_source.md when present) and emits a structured description_options.md
with 4 short operational description candidates grounded only in those fields.
No invented claims, numbers, or clickbait. Output stays local (gitignored).
Reduces recurring labor of manually drafting description options for every future
packet. Aligns with channel voice (assignment, not reply prompt), description
rules (calm, specific, operational), and no-invent rule. Complements
description_suggest.py and description_scan.py. Not a final description; human
or later scan selects one for publish.md.

Run 954: now prefers primary from assignment_source.md via shared assignment_utils.read_primary
when present, for tighter consistency with the canonical source.
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
from assignment_utils import read_primary  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write local description_options.md from idea.md fields only"
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

    out_path = packet / "description_options.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    primary_from_src = read_primary(packet)
    if primary_from_src:
        base = shorten(primary_from_src, 50)
        source_note = "preferred from assignment_source.md"
    else:
        base = shorten(mech or "the written next-action default", 50)
        source_note = "from idea.md mechanism"
    stall = shorten(problem or "the stall reopens the list", 50)
    top = shorten(topic or "focused work", 30)

    candidates = [
        f"Install a {base} so {stall} stops. Do it before the next tab.",
        f"Write the exact words of the {base} where {stall} starts. Under two minutes.",
        f"The {base} ends the {stall}. Place it on the work itself.",
        f"Name the {stall}. Install the {base} for {top}. Start from the cue.",
    ]

    lines = [
        "# Description Options (local; grounded candidates)",
        "",
        "Generated locally from idea.md (preferring assignment_source.md primary when present).",
        "Four short operational description candidates. No invented claims, numbers, or clickbait.",
        f"Source preference: {source_note}.",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "Complements description_suggest.py and description_scan.py.",
        "Not a final description. Select one, run tools/description_scan.py, then copy to publish.md.",
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
        "- Prefer descriptions that name the concrete default and the stall.",
        "- Avoid weak patterns and engagement bait (see tools/description_scan.py).",
        "- Keep under ~150 words for the final version.",
        "",
        "---",
        "Preferred unblocked path remains the human OAuth step for publish.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"source_preference: {source_note}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print(f"topic_found: {bool(topic)}")
    print(f"candidates: {len(candidates)}")
    print("Description options ready (local; estimated from packet fields only; select next).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
