#!/usr/bin/env python3
"""Generate a single consolidated install full pack from idea.md.

Combines spoken lines for the install segment, same-day verification checks,
short assignment, grounded placements, and operational steps into one
install_full.md. Uses the same extraction and suggestion logic as the
individual generators (install_spoken_lines, install_verifier, install_package).
No invented content. Output stays local (gitignored). Reduces recurring human
or agent labor of running three separate tools and reconciling multiple
markdown files on every future packet while staying aligned with channel
voice (assignment, not reply prompt) and promise (install and verify same day).
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


def build_spoken_lines(mech: str, problem: str) -> list[str]:
    """Return 3-5 calm operational spoken lines for the install segment."""
    lines: list[str] = []
    if problem:
        lines.append(f"The stall is {problem}.")
    if mech:
        lines.append(f"Install this default today: {mech}.")
    lines.append("Write it where your eyes already land when the stall starts.")
    lines.append("Do the first concrete action of that default in the next five minutes.")
    if mech or problem:
        lines.append("When the stall returns, point at the default instead of deciding again.")
    return lines[:5]


def build_checks(mech: str, problem: str) -> list[str]:
    """Return 3-4 operational verification checks."""
    checks: list[str] = []
    if mech:
        checks.append(f"The written default is visible where the stall starts: {mech}.")
    if problem:
        checks.append(f"The stall named in the idea ({problem}) no longer requires reopening the whole list.")
    checks.append("The first concrete action of the default was completed in the same session.")
    if mech or problem:
        checks.append("When the stall returns, the default is pointed at instead of a new decision.")
    return checks[:4]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate consolidated install_full.md from idea.md")
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

    out_path = packet / "install_full.md"
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
    spoken = build_spoken_lines(mech, problem)
    checks = build_checks(mech, problem)

    assignment_parts = []
    if mech:
        assignment_parts.append(f"Install this default today: {mech}.")
    if problem:
        assignment_parts.append(f"The stall is {problem}.")
    if placements:
        assignment_parts.append(f"It lives {placements[0].rstrip('.')}.")
    assignment = " ".join(assignment_parts) if assignment_parts else "(insufficient fields)"

    lines = [
        "# Install Full Pack (consolidated)",
        "",
        "Generated locally from idea.md mechanism/problem only.",
        "One file combining spoken lines, verification checks, assignment, placements, and steps.",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "Channel promise: one small default the viewer can install and verify the same day.",
        "Not a rewrite. Review and use or adapt the sections that match the actual install.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "## Short assignment",
        "",
        assignment,
        "",
        "## Spoken lines (install segment)",
        "",
    ]
    for i, line in enumerate(spoken, 1):
        lines.append(f"{i}. {line}")
    lines.extend([
        "",
        "## Grounded placements (1-2)",
        "",
    ])
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
        "## Verification checks",
        "",
    ])
    for i, check in enumerate(checks, 1):
        lines.append(f"{i}. {check}")
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
        "Use only the lines that match the actual default. Do not invent additional locations, defaults, or engagement prompts.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"spoken_lines: {len(spoken)}")
    print(f"checks: {len(checks)}")
    print(f"placements: {len(placements)}")
    print(f"steps: {len(steps)}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print("Install full pack ready (local; estimated from packet fields only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
