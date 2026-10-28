#!/usr/bin/env python3
"""Generate a paste-ready description install section from idea.md.

Extracts mechanism and problem, suggests 1-2 grounded placements from
keywords already in the text, builds 3-5 same-day operational steps,
and writes description_install_section.md with a short end-card version
and a longer description version.

Aligns with channel promise and voice. No invented mechanisms or claims.
Output stays local and gitignored. Reduces recurring human labor of
assembling the "install the default" block for the description or pinned
comment on every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract as idea_extract  # noqa: E402


def suggest_placements(problem: str, mech: str) -> list[str]:
    """Return 1-2 grounded placement suggestions from existing words only."""
    text = f"{problem} {mech}".lower()
    suggestions: list[str] = []

    if any(k in text for k in ("list", "lists", "todo", "to-do")):
        suggestions.append("On the list itself (or the note next to the list you already open).")
    if any(k in text for k in ("tab", "tabs", "browser", "extra tab")):
        suggestions.append("In the browser bar or on the tab that is still open.")
    if any(k in text for k in ("file", "document", "doc", "spreadsheet")):
        suggestions.append("In the file name, header, or first line of the work file.")
    if any(k in text for k in ("desk", "notebook", "paper", "calendar")):
        suggestions.append("On the desk or calendar page you already see when the stall starts.")
    if any(k in text for k in ("app", "application", "tool")):
        suggestions.append("Inside the app that absorbs the delay (sidebar, title, or first screen).")
    if any(k in text for k in ("morning", "start", "first")):
        suggestions.append("Where your eyes land in the first two minutes of the morning.")

    if not suggestions:
        suggestions.append("Where your cursor or eyes already land when the stall starts.")

    return suggestions[:2]


def build_steps(mech: str, problem: str) -> list[str]:
    """Return 3-5 operational steps grounded in the extracted fields."""
    steps: list[str] = []
    if problem:
        steps.append(f"Name the stall in one sentence: {problem}.")
    if mech:
        steps.append(f"Write the default on a note you already see: {mech}.")
        steps.append("Place the note where your cursor or eyes already land when the stall starts.")
        steps.append("Use that note as the only next action before reopening any list.")
    else:
        steps.append("Write one concrete next action before the next decision.")
    return steps[:5]


def main() -> int:
    p = argparse.ArgumentParser(description="Generate description install section from packet")
    p.add_argument("packet", type=Path, help="Path to packet directory")
    p.add_argument("--force", action="store_true", help="Overwrite existing description_install_section.md")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print("FAIL: idea.md missing", file=sys.stderr)
        return 2

    out_path = packet / "description_install_section.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    placements = suggest_placements(problem, mech)
    steps = build_steps(mech, problem)

    # Short end-card / spoken version
    short_parts = []
    if problem:
        short_parts.append(f"The stall is {problem}.")
    if mech:
        short_parts.append(f"The default is {mech}.")
    if placements:
        short_parts.append(f"It lives {placements[0].rstrip('.')}.")
    short_sentence = " ".join(short_parts) if short_parts else ""

    lines = [
        "# Description Install Section",
        "",
        "Generated locally from idea.md mechanism/problem only.",
        "Channel promise: one small default the viewer can install the same day.",
        "Not a rewrite. Review and paste into the video description or pinned comment.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "## Short version (end card / spoken)",
        "",
        short_sentence or "(insufficient fields)",
        "",
        "## Where it lives",
        "",
    ]
    for i, place in enumerate(placements, 1):
        lines.append(f"{i}. {place}")
    lines.append("")
    lines.append("## Same-day install steps")
    lines.append("")
    for i, step in enumerate(steps, 1):
        lines.append(f"{i}. {step}")
    lines.extend([
        "",
        "---",
        "Paste the short version or the steps. Do not invent additional defaults or locations.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"placements: {len(placements)}")
    print(f"steps: {len(steps)}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print("Description install section ready (local; estimated from packet fields only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
