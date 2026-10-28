#!/usr/bin/env python3
"""Generate a consolidated install package from idea.md for one-command paste.

Combines short assignment, grounded placements, same-day steps, first-comment
pin candidate, and description-section text into a single install_package.md.
Uses the same extraction and suggestion logic as the individual generators.
No invented content. Output stays local and gitignored. Reduces the labor of
running multiple tools and reconciling several markdown files on every future
packet.
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
        steps.append(f"Name the stall out loud: {problem}.")
    if mech:
        steps.append(f"Write the default where you will see it: {mech}.")
    steps.append("Do the first concrete action of that default in the next five minutes.")
    steps.append("Leave the default visible for the rest of the day.")
    if problem or mech:
        steps.append("When the stall returns, point at the default instead of deciding again.")
    return steps[:5]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate consolidated install_package.md")
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

    out_path = packet / "install_package.md"
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

    assignment_parts = []
    if mech:
        assignment_parts.append(f"Install this default today: {mech}.")
    if problem:
        assignment_parts.append(f"The stall is {problem}.")
    if placements:
        assignment_parts.append(f"It lives {placements[0].rstrip('.')}.")
    assignment = " ".join(assignment_parts) if assignment_parts else "(insufficient fields)"

    lines = [
        "# Install Package (consolidated)",
        "",
        "Generated locally from idea.md mechanism/problem only.",
        "One file for the assignment, placement, steps, pin comment, and description section.",
        "Channel promise: one small default the viewer can install the same day.",
        "Not a rewrite. Review and paste the relevant sections into publish.md or Studio.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "## Short assignment",
        "",
        assignment,
        "",
        "## Grounded placements (1-2)",
        "",
    ]
    for p in placements:
        lines.append(f"- {p}")
    lines.extend([
        "",
        "## Same-day steps",
        "",
    ])
    for i, step in enumerate(steps, 1):
        lines.append(f"{i}. {step}")
    lines.extend([
        "",
        "## First comment (pin candidate)",
        "",
        assignment,
        "",
        "## Description install section",
        "",
        assignment,
        "",
        "Steps:",
        "",
    ])
    for i, step in enumerate(steps, 1):
        lines.append(f"{i}. {step}")
    lines.extend([
        "",
        "---",
        "Paste only the parts you need. Do not invent additional defaults, locations, or engagement prompts.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"placements: {len(placements)}")
    print(f"steps: {len(steps)}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print("Install package ready (local; estimated from packet fields only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
