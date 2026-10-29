#!/usr/bin/env python3
"""Write a local title_options.md with grounded title candidates.

Extracts mechanism/problem/topic from idea.md and emits a structured
title_options.md with 6 short operational title candidates grounded only
in those fields. No invented claims, numbers, or clickbait. Output stays
local (gitignored). Reduces recurring labor of manually drafting title
options for every future packet. Aligns with channel voice (assignment,
not reply prompt), title rules (calm, specific), and no-invent rule.
Complements title_suggest.py and chapters_writer.py. Not a final title;
human or later scan selects one for publish.md.
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write local title_options.md from idea.md fields only"
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

    out_path = packet / "title_options.md"
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
    top = shorten(topic or "focused work", 30)

    candidates = [
        f"Install a {base} so {stall} stops",
        f"Stop {stall} with one {base}",
        f"The {base} that ends the {stall}",
        f"Name the {stall}. Install the {base}.",
        f"Where the {base} lives for {top}",
        f"A written {base} for the morning {stall}",
    ]

    lines = [
        "# Title Options (local; grounded candidates)",
        "",
        "Generated locally from idea.md mechanism/problem/topic only.",
        "Six short operational title candidates. No invented claims, numbers, or clickbait.",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "Complements title_suggest.py and title_scan.py.",
        "Not a final title. Select one, run tools/title_scan.py, then copy to publish.md.",
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
        "- Prefer titles under 60 characters when possible.",
        "- Avoid weak patterns (see tools/title_scan.py / phrase_utils TITLE_WEAK_PATTERNS).",
        "- Keep the mechanism and stall concrete.",
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
    print("Title options ready (local; estimated from packet fields only; select next).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
