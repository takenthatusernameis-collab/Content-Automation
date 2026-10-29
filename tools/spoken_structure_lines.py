#!/usr/bin/env python3
"""Generate short spoken lines for the full video structure.

Extracts mechanism/problem/topic from idea.md and emits calm, operational
spoken lines for Hook, Payoff, 4 body Beats, and CTA. Grounded only in
those fields. No invented content. Output stays local (gitignored).
Reduces recurring human labor of drafting the initial spoken skeleton
for every future packet while staying aligned with channel voice
(assignment, not reply prompt) and format (hook 8-12s, payoff before
middle, 4-7 beats, CTA as assignment).
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


def build_hook_lines(mech: str, problem: str, topic: str) -> list[str]:
    lines: list[str] = []
    if problem:
        lines.append(f"The stall is {problem}.")
    if mech:
        lines.append(f"Today you install one default: {mech}.")
    return lines[:2]


def build_payoff_lines(mech: str, problem: str) -> list[str]:
    lines: list[str] = []
    lines.append("By the end of this video you will know exactly where that default lives.")
    if mech or problem:
        lines.append("The outcome is simple: the next time the stall starts, the default is already there.")
    return lines[:2]


def build_beat_lines(mech: str, problem: str, topic: str) -> list[str]:
    """Four short operational beat starters."""
    base = mech or "the written next-action default"
    stall = problem or "the list reopens"
    lines = [
        f"Name the stall out loud: {stall}. Then write the first verb from {base}.",
        f"Put the default where your eyes already land: {base}. No new list.",
        f"Do the first concrete action of that default in the next five minutes.",
        f"When the stall returns, point at the default instead of deciding again.",
    ]
    if topic:
        lines[0] = f"For {topic}: name the stall ({stall}) and write the first verb from {base}."
    return lines[:4]


def build_cta_lines(mech: str, problem: str) -> list[str]:
    lines: list[str] = []
    if mech:
        lines.append(f"Install this default today: {mech}.")
    lines.append("Write it where your eyes already land when the stall starts.")
    lines.append("Do the first concrete action of that default in the next five minutes.")
    if problem:
        lines.append(f"The stall is {problem}. Point at the default instead of reopening the list.")
    return lines[:3]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate local spoken_structure_lines.md from idea.md"
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

    out_path = packet / "spoken_structure_lines.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    hook = build_hook_lines(mech, problem, topic)
    payoff = build_payoff_lines(mech, problem)
    beats = build_beat_lines(mech, problem, topic)
    cta = build_cta_lines(mech, problem)

    lines = [
        "# Spoken Structure Lines (local)",
        "",
        "Generated locally from idea.md mechanism/problem/topic only.",
        "Short operational lines for Hook, Payoff, four body Beats, and CTA.",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "Format: hook 8-12 s; payoff before the middle; 4-7 beats; CTA as assignment.",
        "Not a rewrite. Review and use or adapt the lines that match the actual promise.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "## Hook",
        "",
    ]
    for i, line in enumerate(hook, 1):
        lines.append(f"{i}. {line}")
    lines.extend([
        "",
        "## Payoff",
        "",
    ])
    for i, line in enumerate(payoff, 1):
        lines.append(f"{i}. {line}")
    lines.extend([
        "",
        "## Body beats",
        "",
    ])
    for i, line in enumerate(beats, 1):
        lines.append(f"Beat {i}: {line}")
    lines.extend([
        "",
        "## CTA",
        "",
    ])
    for i, line in enumerate(cta, 1):
        lines.append(f"{i}. {line}")
    lines.extend([
        "",
        "---",
        "Use only the lines that match the actual default and outcome. Do not invent additional claims, locations, or engagement prompts.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"hook: {len(hook)}")
    print(f"payoff: {len(payoff)}")
    print(f"beats: {len(beats)}")
    print(f"cta: {len(cta)}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print(f"topic_found: {bool(topic)}")
    print("Spoken structure lines ready (local; estimated from packet fields only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
