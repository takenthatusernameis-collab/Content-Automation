#!/usr/bin/env python3
"""Generate a local visual sequence plan from idea.md.

Extracts mechanism/problem/topic and emits a short visual_sequence_plan.md
with suggested on-screen text and card types for Hook, Payoff, body Beats,
and CTA. Grounded only in those fields. No invented content. Output stays
local (gitignored). Reduces recurring human labor of planning the visual
sequence and on-screen phrases for every future packet while staying
aligned with channel voice and format (text-card first, short on-screen).
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


def build_visuals(mech: str, problem: str, topic: str) -> list[dict[str, str]]:
    """Return list of dicts with segment, on_screen, type."""
    base = mech or "written next-action default"
    stall = problem or "the stall"
    visuals = [
        {
            "segment": "Hook",
            "on_screen": f"Stall: {stall[:40]}",
            "type": "text-card",
            "note": "Same promise as hook spoken line. Card on from first word."
        },
        {
            "segment": "Payoff",
            "on_screen": "Default installed",
            "type": "text-card",
            "note": "Viewer can state the outcome before the middle."
        },
        {
            "segment": "Beat 1",
            "on_screen": f"Name the stall: {stall[:30]}",
            "type": "text-card",
            "note": "Show the stall then the first verb."
        },
        {
            "segment": "Beat 2",
            "on_screen": f"Place: {base[:30]}",
            "type": "diagram" if "place" in base.lower() or "note" in base.lower() else "text-card",
            "note": "Where eyes already land."
        },
        {
            "segment": "Beat 3",
            "on_screen": "First action (5 min)",
            "type": "text-card",
            "note": "Concrete under-two-minute step."
        },
        {
            "segment": "Beat 4",
            "on_screen": "Point at the default",
            "type": "text-card",
            "note": "When stall returns."
        },
        {
            "segment": "CTA",
            "on_screen": f"Install: {base[:35]}",
            "type": "text-card",
            "note": "Assignment, not subscribe. Stays through end-screen reserve."
        },
    ]
    if topic:
        visuals[0]["on_screen"] = f"{topic[:20]}: {stall[:25]}"
    return visuals


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate local visual_sequence_plan.md from idea.md"
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

    out_path = packet / "visual_sequence_plan.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    visuals = build_visuals(mech, problem, topic)

    lines = [
        "# Visual Sequence Plan (local)",
        "",
        "Generated locally from idea.md mechanism/problem/topic only.",
        "Suggested on-screen text and card types for Hook, Payoff, body Beats, and CTA.",
        "Text-card first. On-screen phrases short (<=5-7 words preferred).",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "Not a rewrite of assets.md. Review and adapt before card generation.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "## Sequence",
        "",
        "| Segment | On-screen (suggested) | Type | Note |",
        "|---------|-----------------------|------|------|",
    ]
    for v in visuals:
        on = v["on_screen"].replace("|", "/")
        note = v["note"].replace("|", "/")
        lines.append(f"| {v['segment']} | {on} | {v['type']} | {note} |")
    lines.extend([
        "",
        "---",
        "Use only phrases that match the actual default and outcome. Do not invent locations, claims, or stock. Prefer tools/card_text_suggest.py after script VISUAL exists.",
        "Run tools/asset_brief.py after script.md is filled to produce the official assets.md intake stub.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"segments: {len(visuals)}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print(f"topic_found: {bool(topic)}")
    print("Visual sequence plan ready (local; estimated from packet fields only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
