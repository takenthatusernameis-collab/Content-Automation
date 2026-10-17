#!/usr/bin/env python3
"""Coach expansion of SHORT body beats in draft.md.

Parses draft.md (or script.md), counts spoken words per ## section against
targets, and for every SHORT body beat prints the matching checklist items
from the packet mechanism plus the exact word deficit. Does not invent spoken
lines, statistics, or anecdotes. Complements draft_word_progress.py and
draft_beat_expansion_starter.py by turning the progress table into actionable
per-beat guidance only for the beats that still need work, further reducing
free-form padding for every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WORD_RE = re.compile(r"WORDS:\s*(.*?)(?:\nVISUAL:|\n## |\Z)", re.S | re.I)
SECTION_RE = re.compile(r"^##\s+(.+?)$", re.M)
MECH_RE = re.compile(r"mechanism[^\n]*:\s*(.+)", re.I)
PROBLEM_RE = re.compile(r"problem:\s*(.+)", re.I)

TARGETS = {
    "hook": (20, 45),
    "payoff": (40, 90),
    "beat": (140, 220),
    "cta": (40, 90),
}


def count_words(text: str) -> int:
    cleaned = re.sub(r"[^\w\s'-]", " ", text)
    return len([w for w in cleaned.split() if w.strip()])


def classify(heading: str) -> str:
    h = heading.lower()
    if "hook" in h:
        return "hook"
    if "payoff" in h:
        return "payoff"
    if "cta" in h or "end" in h:
        return "cta"
    if "beat" in h:
        return "beat"
    return "other"


def extract_mech(idea_text: str) -> tuple[str, str]:
    mech = problem = ""
    for line in idea_text.splitlines():
        m = MECH_RE.search(line)
        if m:
            mech = m.group(1).strip().rstrip(".")
        p = PROBLEM_RE.search(line)
        if p:
            problem = p.group(1).strip().rstrip(".")
    return mech or "the written default", problem or "the stall"


def checklist_for(heading: str, mech: str) -> list[str]:
    base = mech[:50]
    h = heading.lower()
    if "install" in h or "beat 1" in h:
        return [
            f"One worked example of writing the {base} at the top of the open list before scrolling.",
            "A distinction between reopening the whole page vs. finishing the first two minutes.",
            "The exact file or note location the viewer already has.",
        ]
    if "place" in h or "cue" in h or "beat 2" in h:
        return [
            f"Where the written {base} lives so the reopen ends (sticky, note app, top of document).",
            "A short scene of the stall starting when the cue is missing.",
            "One physical or file action the viewer can finish in under two minutes.",
        ]
    if "test" in h or "beat 3" in h:
        return [
            f"An operational check the viewer can run the same day using the {base}.",
            "What success looks like (the stall does not reopen).",
            "A failure signal if the test is skipped.",
        ]
    if "failure" in h or "beat 4" in h:
        return [
            f"What repeats when the {base} is absent: the list stays the whole page, the next action stays unnamed.",
            "A concrete scene of the delay starting again.",
            "The missing cue that would have ended the reopen.",
        ]
    if "keep" in h or "beat 5" in h:
        return [
            f"How the constraint of the {base} stays after the first install (not pep).",
            "One way the cue remains visible on the device or in the file the viewer already uses.",
            "What changes if the default is removed.",
        ]
    return [
        f"One concrete worked example of the {base} on this packet's stall.",
        "A distinction or operational test the viewer can run the same day.",
        "A short failure-mode scene when the mechanism is absent.",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Coach SHORT body beats in draft.md. No invented spoken lines."
    )
    parser.add_argument("packet", help="Packet folder containing draft.md and idea.md")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    draft = path / "draft.md"
    source = draft if draft.is_file() else path / "script.md"
    idea = path / "idea.md"
    if not source.is_file():
        print(f"No draft.md or script.md in {args.packet}", file=sys.stderr)
        return 1
    if not idea.is_file():
        print(f"No idea.md in {args.packet}", file=sys.stderr)
        return 1

    text = source.read_text(encoding="utf-8").replace("\r\n", "\n")
    idea_text = idea.read_text(encoding="utf-8")
    mech, problem = extract_mech(idea_text)
    sections = SECTION_RE.findall(text)
    words_blocks = WORD_RE.findall(text)

    print("DRAFT SHORT BEAT COACH (targeted guidance for SHORT body beats only; no invented lines/stats)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print(f"Mechanism: {mech}")
    print()

    block_idx = 0
    short_count = 0
    for heading in sections:
        kind = classify(heading)
        count = 0
        if block_idx < len(words_blocks):
            count = count_words(words_blocks[block_idx])
            block_idx += 1
        if kind != "beat":
            continue
        lo, hi = TARGETS["beat"]
        if count >= lo:
            continue
        short_count += 1
        deficit = lo - count
        print(f"## {heading.strip()}  ({count} words, SHORT by {deficit})")
        print("Add these concrete elements while expanding (do not invent sources, numbers, or anecdotes):")
        for item in checklist_for(heading, mech):
            print(f"- {item}")
        print(f"<!-- Grow by ~{deficit} spoken words using only the above. Aim for {lo}-{hi}. -->")
        print()

    if short_count == 0:
        print("No SHORT body beats. Run draft_word_progress.py for the full table.")
    else:
        print(f"---\n{short_count} SHORT body beat(s). Expand using the items above, then re-run this tool.")
    print()
    print("Next (do not invent sources, numbers, or anecdotes):")
    print("- Prefer concrete mechanism language; avoid anti-slop phrases in docs/content_quality.md.")
    print("- Run python3 tools/quality_scan.py and python3 tools/claim_scan.py before apply_script.py --write.")
    print("This tool writes nothing. Preferred unblocked path remains human OAuth for publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
