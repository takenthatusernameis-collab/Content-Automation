#!/usr/bin/env python3
"""Write a local expansion_checklist.md with per-beat expansion guidance.

Extracts mechanism/problem/topic from idea.md and emits a structured checklist
of concrete elements to add when expanding short starter WORDS (from
draft_skeleton.md) to the 140–220 spoken-word target per body beat.
Items are grounded only in those fields: worked example, distinction,
operational test, failure-mode scene. No invented spoken lines, statistics,
anecdotes, or claims. Output stays local (gitignored). Reduces recurring
human/agent labor of re-running printers or inventing structure while expanding
for every future packet. Aligns with channel voice (assignment, not reply prompt),
format word targets, and no-invent rule. Complements draft_skeleton_writer.py
and draft_beat_expansion_starter.py (printer). Not a final script.
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


def build_beats(mech: str, problem: str) -> list[tuple[str, list[str]]]:
    base = shorten(mech or "the written next-action default", 50)
    stall = problem or "the stall reopens the list"
    return [
        (
            "Beat 1 — Install the default",
            [
                f"One worked example of writing the {base} at the top of the open list before scrolling.",
                "A distinction between reopening the whole page vs. finishing the first two minutes.",
                "The exact file or note location the viewer already has.",
            ],
        ),
        (
            "Beat 2 — Place the cue",
            [
                f"Where the written {base} lives so the reopen ends (sticky, note app, top of document).",
                f"A short scene of the stall starting when the cue is missing ({stall}).",
                "One physical or file action the viewer can finish in under two minutes.",
            ],
        ),
        (
            "Beat 3 — One small test",
            [
                f"An operational check the viewer can run the same day using the {base}.",
                "What success looks like (the stall does not reopen).",
                "A failure signal if the test is skipped.",
            ],
        ),
        (
            "Beat 4 — Failure mode",
            [
                f"What repeats when the {base} is absent: the list stays the whole page, the next action stays unnamed.",
                "A concrete scene of the delay starting again.",
                "The missing cue that would have ended the reopen.",
            ],
        ),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write local expansion_checklist.md from idea.md fields only"
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

    out_path = packet / "expansion_checklist.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    beats = build_beats(mech, problem)

    lines = [
        "# Expansion Checklist (local; for draft skeleton WORDS)",
        "",
        "Generated locally from idea.md mechanism/problem/topic only.",
        "Per-beat checklist of concrete elements to add when expanding short starter",
        "WORDS (from draft_skeleton.md) to the 140–220 spoken-word target per body beat.",
        "Prefer observable scenes, decisions, and procedures over slogans.",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "No invented claims, statistics, or anecdotes. Expand using only these elements.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem / stall: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "For each body beat, add the following while expanding the starting WORDS.",
        "",
    ]
    for title, items in beats:
        lines.append(f"## {title}")
        for item in items:
            lines.append(f"- {item}")
        lines.append("<!-- Expand the starting WORDS to 140–220 spoken words using only the above elements. -->")
        lines.append("")

    lines.extend([
        "---",
        "After expanding into draft.md: run tools/draft_pre_apply_coach.py and",
        "tools/quality_scan.py before apply_script --write. Do not treat this file as script.md.",
        "Preferred unblocked path remains the human OAuth step for publish.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"beats: {len(beats)}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print(f"topic_found: {bool(topic)}")
    print("Expansion checklist ready (local; estimated from packet fields only; expand next).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
