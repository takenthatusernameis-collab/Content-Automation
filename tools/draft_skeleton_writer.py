#!/usr/bin/env python3
"""Write a local draft_skeleton.md with structure and short spoken lines.

Extracts mechanism/problem/topic from idea.md and emits a structured skeleton
with ## Hook, ## Payoff promise, ## Beat 1–4, ## CTA and short operational
WORDS lines grounded only in those fields. Ready for expansion to word targets.
No invented content. Output stays local (gitignored). Reduces recurring human
labor of setting up the draft.md structure and pasting starter lines for every
future packet. Aligns with channel voice (assignment, not reply prompt),
format (hook 8-12s, payoff before middle, 4 beats, CTA as assignment), and
script_writer.md constraints. Complements draft_starter.py (printer) and
spoken_structure_lines.py. Not a final script.
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


def build_hook(mech: str, problem: str) -> str:
    if problem and mech:
        return f"The stall is {problem}. Today you install one default: {mech}."
    if problem:
        return f"The stall is {problem}."
    if mech:
        return f"Today you install one default: {mech}."
    return "Name the stall and install one default."


def build_payoff(mech: str, problem: str) -> str:
    lines = ["By the end of this video you will know exactly where that default lives."]
    if mech or problem:
        lines.append("The outcome is simple: the next time the stall starts, the default is already there.")
    return " ".join(lines)


def build_beats(mech: str, problem: str, topic: str) -> list[str]:
    base = mech or "the written next-action default"
    stall = problem or "the list reopens"
    beats = [
        f"Name the stall out loud: {stall}. Then write the first verb from {base}.",
        f"Put the default where your eyes already land: {base}. No new list.",
        f"Do the first concrete action of that default in the next five minutes.",
        f"When the stall returns, point at the default instead of deciding again.",
    ]
    if topic:
        beats[0] = f"For {topic}: name the stall ({stall}) and write the first verb from {base}."
    return beats


def build_cta(mech: str, problem: str) -> str:
    lines = []
    if mech:
        lines.append(f"Install this default today: {mech}.")
    lines.append("Write it where your eyes already land when the stall starts.")
    lines.append("Do the first concrete action of that default in the next five minutes.")
    if problem:
        lines.append(f"The stall is {problem}. Point at the default instead of reopening the list.")
    return " ".join(lines[:3])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write local draft_skeleton.md from idea.md fields only"
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

    out_path = packet / "draft_skeleton.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    hook = build_hook(mech, problem)
    payoff = build_payoff(mech, problem)
    beats = build_beats(mech, problem, topic)
    cta = build_cta(mech, problem)

    lines = [
        "# Draft Skeleton (local; expand to targets)",
        "",
        "Generated locally from idea.md mechanism/problem/topic only.",
        "Structured skeleton with short operational WORDS lines for Hook, Payoff,",
        "four body Beats, and CTA. Expand each section to format word targets",
        "(Hook 20-35, Payoff 40-70, each Beat 140-220, CTA 40-80; total 900-1500).",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "Not a final script. Copy preferred lines into draft.md and expand.",
        "Do not invent claims, statistics, or anecdotes. Preserve ## headings.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "## Hook (0:00\u20130:12)",
        "WORDS:",
        hook,
        "",
        "VISUAL:",
        "*Short on-screen card naming the stall and the default.*",
        "",
        "## Payoff promise",
        "WORDS:",
        payoff,
        "",
        "VISUAL:",
        "*Card showing the outcome: default already in place.*",
        "",
    ]
    for i, beat in enumerate(beats, 1):
        lines.extend([
            f"## Beat {i} \u2014 operational step",
            "WORDS:",
            beat,
            "",
            "VISUAL:",
            "*Card or diagram of the concrete action.*",
            "",
        ])
    lines.extend([
        "## CTA",
        "WORDS:",
        cta,
        "",
        "VISUAL:",
        "*Assignment card: install the default today.*",
        "",
        "---",
        "Expand the WORDS lines to land in band. Run tools/draft_pre_apply_coach.py",
        "and tools/quality_scan.py after filling draft.md. Do not treat this file as script.md.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"hook_words: {len(hook.split())}")
    print(f"payoff_words: {len(payoff.split())}")
    print(f"beats: {len(beats)}")
    print(f"cta_words: {len(cta.split())}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print(f"topic_found: {bool(topic)}")
    print("Draft skeleton ready (local; estimated from packet fields only; expand next).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
