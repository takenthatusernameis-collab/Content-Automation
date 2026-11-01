#!/usr/bin/env python3
"""Write a local assignment_source.md as the canonical short assignment source.

Extracts mechanism/problem/topic from idea.md and writes a single-source
assignment_source.md with shortened natural phrases and one recommended
primary assignment statement. Uses shared phrase_utils.shorten for natural
breaks. No invented claims. Output stays local (gitignored).
Provides a reusable source of truth that future option writers, scanners,
or human edits can reference for tighter channel-promise consistency
across titles, descriptions, chapters, first comments, and CTAs.
Reduces drift between independently generated options. Aligns with
no-invent rule and mechanism alignment goals.
Not a candidates list; it is the grounded core statement.
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
        description="Write local assignment_source.md from idea.md fields only"
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

    out_path = packet / "assignment_source.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    short_mech = shorten(mech or "the written next-action default", 42)
    short_problem = shorten(problem or "the stall", 32)
    short_topic = shorten(topic or "focused work", 28)

    primary = f"Install the {short_mech} so {short_problem} stops reopening the list."

    lines = [
        "# Assignment Source (local; canonical grounded core)",
        "",
        "Generated locally from idea.md mechanism/problem/topic only.",
        "Single source of truth for the short operational assignment.",
        "Uses shared phrase_utils.shorten for natural clause/word breaks.",
        "No invented claims, numbers, or engagement bait.",
        "Channel voice: calm, specific, operational. Name the stall. Name the default.",
        "Future option writers and scanners may prefer this file when present for tighter consistency.",
        "Not a final publish field. Copy or adapt into publish.md / cards as needed.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem / stall (short): {short_problem}",
        f"- Mechanism / default (short): {short_mech}",
        "",
        "## Primary assignment statement",
        "",
        primary,
        "",
        "## Usage notes",
        "- Prefer this shortened mechanism in titles, descriptions, chapters, first comments, and CTA cards.",
        "- Aligns with mechanism_align_scan and the channel promise (install one small default the same day).",
        "- Keep final spoken or on-screen versions under the length limits of their respective gates.",
        "",
        "---",
        "Preferred unblocked path remains the human OAuth step for publish.",
    ]

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"short_mech: {short_mech}")
    print(f"short_problem: {short_problem}")
    print(f"primary: {primary}")
    print("Assignment source ready (local; estimated from packet fields only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
