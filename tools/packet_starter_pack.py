#!/usr/bin/env python3
"""Generate a single consolidated packet starter pack from idea.md.

Combines spoken structure lines (Hook/Payoff/Beats/CTA), visual sequence plan
(on-screen text and card types), and install full pack into one
packet_starter.md. Uses extraction from idea_utils and reuses builder logic
patterns from the individual generators. No invented content. Output stays
local (gitignored). Reduces recurring human or agent labor of running three
separate tools and reconciling multiple markdown files on every future packet
while staying aligned with channel voice (assignment, not reply prompt),
format (text-card first, short on-screen, structure rules), and promise
(install and verify same day).
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

# Reuse builders by importing where possible; fall back to inline for stability.
try:
    from spoken_structure_lines import (
        build_hook_lines,
        build_payoff_lines,
        build_beat_lines,
        build_cta_lines,
    )
except ImportError:
    # Minimal fallbacks if import fails (should not happen).
    def build_hook_lines(mech, problem, topic):
        lines = []
        if problem:
            lines.append(f"The stall is {problem}.")
        if mech:
            lines.append(f"Today you install one default: {mech}.")
        return lines[:2]

    def build_payoff_lines(mech, problem):
        return [
            "By the end of this video you will know exactly where that default lives.",
            "The outcome is simple: the next time the stall starts, the default is already there.",
        ][:2]

    def build_beat_lines(mech, problem, topic):
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

    def build_cta_lines(mech, problem):
        lines = []
        if mech:
            lines.append(f"Install this default today: {mech}.")
        lines.append("Write it where your eyes already land when the stall starts.")
        lines.append("Do the first concrete action of that default in the next five minutes.")
        return lines[:3]

try:
    from visual_sequence_plan import build_visuals
except ImportError:
    def build_visuals(mech, problem, topic):
        base = mech or "written next-action default"
        stall = problem or "the stall"
        return [
            {"segment": "Hook", "on_screen": f"Stall: {stall[:40]}", "type": "text-card", "note": "Same promise as hook spoken line."},
            {"segment": "Payoff", "on_screen": "Default installed", "type": "text-card", "note": "Viewer can state the outcome before the middle."},
            {"segment": "Beat 1", "on_screen": f"Name the stall: {stall[:30]}", "type": "text-card", "note": "Show the stall then the first verb."},
            {"segment": "Beat 2", "on_screen": f"Place: {base[:30]}", "type": "text-card", "note": "Where eyes already land."},
            {"segment": "Beat 3", "on_screen": "First action (5 min)", "type": "text-card", "note": "Concrete under-two-minute step."},
            {"segment": "Beat 4", "on_screen": "Point at the default", "type": "text-card", "note": "When stall returns."},
            {"segment": "CTA", "on_screen": f"Install: {base[:35]}", "type": "text-card", "note": "Assignment, not subscribe."},
        ]

try:
    from install_full_pack import (
        suggest_placements,
        build_steps,
        build_spoken_lines as build_install_spoken,
        build_checks,
    )
except ImportError:
    def suggest_placements(problem, mech):
        return ["Where your cursor or eyes already land when the stall starts."]

    def build_steps(mech, problem):
        steps = []
        if problem:
            steps.append(f"Name the stall out loud: {problem}.")
        if mech:
            steps.append(f"Write the default where you will see it: {mech}.")
        steps.append("Do the first concrete action of that default in the next five minutes.")
        return steps[:5]

    def build_install_spoken(mech, problem):
        return build_cta_lines(mech, problem)

    def build_checks(mech, problem):
        return ["The first concrete action of the default was completed in the same session."]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate local packet_starter.md consolidating structure, visuals, and install from idea.md"
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

    out_path = packet / "packet_starter.md"
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
    visuals = build_visuals(mech, problem, topic)
    placements = suggest_placements(problem, mech)
    steps = build_steps(mech, problem)
    install_spoken = build_install_spoken(mech, problem)
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
        "# Packet Starter Pack (consolidated)",
        "",
        "Generated locally from idea.md mechanism/problem/topic only.",
        "One file combining spoken structure lines, visual sequence plan, and install full pack.",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "Format: text-card first, short on-screen; hook 8-12 s; payoff before middle; 4-7 beats; CTA as assignment.",
        "Channel promise: one small default the viewer can install and verify same day.",
        "Not a rewrite of script.md or assets.md. Review and adapt before drafting or card generation.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "## Spoken Structure",
        "",
        "### Hook",
        "",
    ]
    for i, line in enumerate(hook, 1):
        lines.append(f"{i}. {line}")
    lines.extend([
        "",
        "### Payoff",
        "",
    ])
    for i, line in enumerate(payoff, 1):
        lines.append(f"{i}. {line}")
    lines.extend([
        "",
        "### Body Beats",
        "",
    ])
    for i, line in enumerate(beats, 1):
        lines.append(f"Beat {i}: {line}")
    lines.extend([
        "",
        "### CTA",
        "",
    ])
    for i, line in enumerate(cta, 1):
        lines.append(f"{i}. {line}")
    lines.extend([
        "",
        "## Visual Sequence",
        "",
        "| Segment | On-screen (suggested) | Type | Note |",
        "|---------|-----------------------|------|------|",
    ])
    for v in visuals:
        on = v["on_screen"].replace("|", "/")
        note = v.get("note", "").replace("|", "/")
        lines.append(f"| {v['segment']} | {on} | {v['type']} | {note} |")
    lines.extend([
        "",
        "## Install Pack",
        "",
        "### Short assignment",
        "",
        assignment,
        "",
        "### Spoken lines (install segment)",
        "",
    ])
    for i, line in enumerate(install_spoken, 1):
        lines.append(f"{i}. {line}")
    lines.extend([
        "",
        "### Grounded placements",
        "",
    ])
    for p in placements:
        lines.append(f"- {p}")
    lines.extend([
        "",
        "### Same-day steps",
        "",
    ])
    for i, step in enumerate(steps, 1):
        lines.append(f"{i}. {step}")
    lines.extend([
        "",
        "### Verification checks",
        "",
    ])
    for i, check in enumerate(checks, 1):
        lines.append(f"{i}. {check}")
    lines.extend([
        "",
        "### First comment / Description install candidate",
        "",
        assignment,
        "",
        "---",
        "Use only phrases that match the actual default and outcome. Do not invent locations, claims, stock, or engagement prompts.",
        "Prefer individual tools (spoken_structure_lines.py, visual_sequence_plan.py, install_full_pack.py) if you need only one section.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"hook: {len(hook)}")
    print(f"payoff: {len(payoff)}")
    print(f"beats: {len(beats)}")
    print(f"visuals: {len(visuals)}")
    print(f"install_spoken: {len(install_spoken)}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print(f"topic_found: {bool(topic)}")
    print("Packet starter pack ready (local; estimated from packet fields only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
