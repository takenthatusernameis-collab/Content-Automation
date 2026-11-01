#!/usr/bin/env python3
"""Write a local end_screen_options.md with grounded CTA candidates.

Extracts mechanism/problem/topic from idea.md (or prefers shortened primary from
assignment_source.md when present) and emits a structured end_screen_options.md
with 4 short operational end-screen / CTA candidates grounded only in those fields.
No invented claims, numbers, or engagement bait. Output stays local (gitignored).
Reduces recurring labor of manually drafting end-screen text for every future packet.
Aligns with channel voice (assignment, not reply prompt), end-screen rules (calm,
specific, concrete next action), and no-invent rule. Complements end_screen_suggest.py
and end_screen_scan.py. Not a final CTA; human or later scan selects one for
publish.md ## End screen or ## CTA.

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
        description="Write local end_screen_options.md from idea.md fields only"
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

    out_path = packet / "end_screen_options.md"
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
        base = shorten(primary_from_src, 40)
        source_note = "preferred from assignment_source.md"
    else:
        base = shorten(mech or "the written next-action default", 40)
        source_note = "from idea.md mechanism"
    stall = shorten(problem or "the stall reopens the list", 40)
    top = shorten(topic or "focused work", 30)

    candidates = [
        f"Write the {base} on disk today so {stall} stops.",
        f"Install the {base} before the next decision on {top}.",
        f"Name the {stall}. Install the {base}.",
        f"Same-day install: place the {base} where {stall} starts.",
    ]

    lines = [
        "# End Screen Options (local; grounded candidates)",
        "",
        "Generated locally from idea.md (preferring assignment_source.md primary when present).",
        "Four short operational end-screen / CTA candidates. No invented claims, numbers, or engagement bait.",
        f"Source preference: {source_note}.",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "Complements end_screen_suggest.py and end_screen_scan.py.",
        "Not a final CTA. Select one, run tools/end_screen_scan.py, then copy to publish.md ## End screen or ## CTA.",
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
        "- Prefer CTAs that name the concrete default and the stall.",
        "- Avoid weak/engagement-bait patterns (see tools/end_screen_scan.py / phrase_utils END_SCREEN_WEAK_PATTERNS).",
        "- Keep under ~15 words for the final version.",
        "- The CTA is the concrete next action from the mechanism, not a subscribe or reply prompt.",
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
    print("End-screen options ready (local; estimated from packet fields only; select next).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
