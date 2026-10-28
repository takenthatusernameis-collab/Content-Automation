#!/usr/bin/env python3
"""Generate short spoken lines for the install-the-default segment.

Extracts mechanism/problem/topic from idea.md and emits 3-5 calm, operational
spoken lines the narrator can use near the end of the video. No invented
content. Output stays local (gitignored). Reduces recurring human labor of
writing the same-day install CTA for every future packet while staying
aligned with channel voice (assignment, not reply prompt).
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
    """Return 3-5 operational spoken lines grounded in extracted fields only."""
    lines: list[str] = []
    if problem:
        lines.append(f"The stall is {problem}.")
    if mech:
        lines.append(f"Install this default today: {mech}.")
    lines.append("Write it where your eyes already land when the stall starts.")
    lines.append("Do the first concrete action of that default in the next five minutes.")
    if mech or problem:
        lines.append("When the stall returns, point at the default instead of deciding again.")
    # Keep under 5, prefer concrete
    return lines[:5]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local install_spoken_lines.md from idea.md")
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

    out_path = packet / "install_spoken_lines.md"
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
        "# Install Spoken Lines (local)",
        "",
        "Generated locally from idea.md mechanism/problem only.",
        "Short operational lines for the same-day install segment of the video.",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "Not a rewrite. Review and use or adapt the lines that match the actual install.",
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
        "Use only the lines that match the actual default. Do not invent additional locations or engagement prompts.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"lines: {len(spoken)}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print("Install spoken lines ready (local; estimated from packet fields only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
