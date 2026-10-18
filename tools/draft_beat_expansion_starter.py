#!/usr/bin/env python3
"""Print a per-beat expansion checklist for draft.md body beats.

Grounded in idea.md mechanism/problem. For each body beat, lists concrete
elements the agent should add when expanding the short starting WORDS from
draft_md_starter.py to the 140–220 spoken-word target: worked example of the
mechanism on the packet stall, a distinction, an operational test the viewer
can run the same day, and a failure-mode scene when the mechanism is absent.
Does not invent spoken lines, statistics, anecdotes, or claims.
Does not write files. Complements draft_md_starter.py and expand_starter.py
by turning the expansion step into a structured checklist instead of free-form
writing, reducing padding and slop risk for every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MECH_RE = re.compile(r"mechanism[^\n]*:\s*(.+)", re.I)
PROBLEM_RE = re.compile(r"problem:\s*(.+)", re.I)


def extract(idea_text: str) -> tuple[str, str]:
    mech = problem = ""
    for line in idea_text.splitlines():
        m = MECH_RE.search(line)
        if m:
            mech = m.group(1).strip().rstrip(".")
        p = PROBLEM_RE.search(line)
        if p:
            problem = p.group(1).strip().rstrip(".")
    return mech or "the written default", problem or "the stall"


def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after the per-beat expansion checklist."""
    p = packet
    return [
        f"skeleton: python3 tools/draft_md_starter.py {p}  # ready-to-copy draft.md with starting WORDS",
        f"expand: paste skeleton, then expand each beat using the checklist items above to 140-220 words",
        f"coach: python3 tools/draft_expansion_coach.py {p} or python3 tools/draft_short_beat_coach.py {p} for progress + targeted guidance",
        f"quality: python3 tools/draft_pre_apply_coach.py {p} for full signals before apply",
        f"apply: python3 tools/apply_script.py {p} --from {p}/draft.md --write --refresh once signals clear",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print per-beat expansion checklist for draft.md. No invented spoken lines."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {args.packet}", file=sys.stderr)
        return 1

    text = idea.read_text(encoding="utf-8")
    mech, problem = extract(text)
    base = mech[:50]

    print("DRAFT BEAT EXPANSION STARTER (checklist only; expand starting WORDS to 140–220; no invented lines/stats)")
    print(f"Packet: {path.name}")
    print(f"Mechanism: {mech}")
    print(f"Problem/stall: {problem}")
    print()
    print("For each body beat in draft.md (from draft_md_starter.py), add the following concrete elements")
    print("while expanding to the word target. Prefer observable scenes, decisions, and procedures over slogans.")
    print()
    beats = [
        ("Beat 1 — Install the default", [
            f"One worked example of writing the {base} at the top of the open list before scrolling.",
            "A distinction between reopening the whole page vs. finishing the first two minutes.",
            "The exact file or note location the viewer already has.",
        ]),
        ("Beat 2 — Place the cue", [
            f"Where the written {base} lives so the reopen ends (sticky, note app, top of document).",
            "A short scene of the stall starting when the cue is missing.",
            "One physical or file action the viewer can finish in under two minutes.",
        ]),
        ("Beat 3 — One small test", [
            f"An operational check the viewer can run the same day using the {base}.",
            "What success looks like (the stall does not reopen).",
            "A failure signal if the test is skipped.",
        ]),
        ("Beat 4 — Failure mode", [
            f"What repeats when the {base} is absent: the list stays the whole page, the next action stays unnamed.",
            "A concrete scene of the delay starting again.",
            "The missing cue that would have ended the reopen.",
        ]),
        ("Beat 5 — Keep the default", [
            f"How the constraint of the {base} stays after the first install (not pep).",
            "One way the cue remains visible on the device or in the file the viewer already uses.",
            "What changes if the default is removed.",
        ]),
    ]
    for title, items in beats:
        print(f"## {title}")
        for item in items:
            print(f"- {item}")
        print("<!-- Expand the starting WORDS to 140–220 spoken words using only the above elements. -->")
        print()
    print("---")
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    print("Next (do not invent sources, numbers, or anecdotes):")
    print("1. Copy the draft.md skeleton from tools/draft_md_starter.py into the packet.")
    print("2. For each body beat, expand using the checklist items above.")
    print("3. Keep Hook/Payoff/CTA near their shorter targets; do not pad.")
    print("4. Run python3 tools/quality_scan.py and python3 tools/claim_scan.py before apply_script.py --write.")
    print("5. Prefer concrete mechanism language; avoid anti-slop phrases in docs/content_quality.md.")
    print("This starter writes nothing. Preferred unblocked path remains human OAuth for publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
