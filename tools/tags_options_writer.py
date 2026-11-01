#!/usr/bin/env python3
"""Write a local tags_options.md with grounded tag candidates.

Extracts mechanism/problem/topic from idea.md (or prefers shortened primary from
assignment_source.md when present) and emits a structured tags_options.md with
6-8 short operational tag candidates grounded only in those fields. No invented
claims, numbers, or spammy patterns. Output stays local (gitignored). Reduces
recurring labor of manually drafting tags for every future packet. Aligns with
channel voice (assignment, not reply prompt), tag rules (specific, mechanism-aligned),
and no-invent rule. Complements tags_suggest.py and tags_scan.py. Not a final
tag list; human or later scan selects ones for publish.md ## Tags.

Run 956: now prefers primary from assignment_source.md via shared assignment_utils.read_primary
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
        description="Write local tags_options.md from idea.md fields only"
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

    out_path = packet / "tags_options.md"
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
        base = shorten(primary_from_src, 35)
        source_note = "preferred from assignment_source.md"
    else:
        base = shorten(mech or "written next-action default", 35)
        source_note = "from idea.md mechanism"
    stall = shorten(problem or "the stall", 30)
    top = shorten(topic or "focused work", 25)

    candidates = [
        base.lower(),
        f"install {base.lower()}",
        f"{stall.lower()} default",
        f"{top.lower()} system",
        "sticky note default",
        "before next tab",
        "written next action",
        "name the stall",
    ]

    # Deduplicate while preserving order and keep lengths reasonable
    seen = set()
    unique = []
    for c in candidates:
        low = c.strip().lower()
        if low and 3 <= len(low) <= 40 and low not in seen:
            seen.add(low)
            unique.append(c.strip())

    lines = [
        "# Tags Options (local; grounded candidates)",
        "",
        "Generated locally from idea.md (preferring assignment_source.md primary when present).",
        "Six to eight short operational tag candidates. No invented claims, numbers, or spam patterns.",
        f"Source preference: {source_note}.",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "Complements tags_suggest.py and tags_scan.py.",
        "Not a final tag list. Select a subset, run tools/tags_scan.py, then copy to publish.md ## Tags.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem / stall: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "## Candidates",
        "",
    ]
    for i, cand in enumerate(unique[:8], 1):
        lines.append(f"{i}. {cand}")
    lines.extend([
        "",
        "## Notes",
        "- Prefer tags that name the concrete default, the stall, or the install action.",
        "- Avoid weak/generic/spam patterns (see tools/tags_scan.py).",
        "- Keep each tag under 40 characters.",
        "- No duplicates.",
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
    print(f"candidates: {len(unique[:8])}")
    print("Tag options ready (local; estimated from packet fields only; select next).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
