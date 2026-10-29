#!/usr/bin/env python3
"""Generate short spoken lines for the hook and payoff segments.

Extracts mechanism/problem/topic from idea.md and emits 3-6 calm, operational
spoken lines the narrator can use in the opening of the video (hook + early payoff).
No invented content. Output stays local (gitignored). Reduces recurring human labor
of drafting the opening promise and outcome for every future packet while staying
aligned with channel voice (assignment, not reply prompt) and format (hook 8-12s,
payoff before beat 2).
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


def build_lines(mech: str, problem: str, topic: str) -> list[str]:
    """Return 3-6 operational spoken lines grounded in extracted fields only."""
    lines: list[str] = []
    if problem:
        lines.append(f"The stall is {problem}.")
    if mech:
        lines.append(f"Today you install one default: {mech}.")
    lines.append("By the end of this video you will know exactly where that default lives.")
    if mech or problem:
        lines.append(f"The outcome is simple: the next time the stall starts, the default is already there.")
    lines.append("No new system. One visible cue or constraint you can put in place today.")
    if topic:
        lines.append(f"This is how {topic} becomes one written next action instead of another reopen.")
    return lines[:6]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local hook_payoff_lines.md from idea.md")
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

    out_path = packet / "hook_payoff_lines.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    spoken = build_lines(mech, problem, topic)

    lines = [
        "# Hook and Payoff Spoken Lines (local)",
        "",
        "Generated locally from idea.md mechanism/problem/topic only.",
        "Short operational lines for the hook (8-12 s) and early payoff segments.",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "Format: viewer can state the outcome before the middle of the video.",
        "Not a rewrite. Review and use or adapt the lines that match the actual promise.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "## Spoken lines",
        "",
    ]
    for i, line in enumerate(spoken, 1):
        lines.append(f"{i}. {line}")
    lines.extend([
        "",
        "---",
        "Use only the lines that match the actual default and outcome. Do not invent additional claims, locations, or engagement prompts.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"lines: {len(spoken)}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print(f"topic_found: {bool(topic)}")
    print("Hook and payoff spoken lines ready (local; estimated from packet fields only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
