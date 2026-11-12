#!/usr/bin/env python3
"""Suggest one grounded first experiment hypothesis for a packet.

Extracts mechanism/problem/topic from idea.md via idea_utils.
Selects the most relevant single-variable change from ALLOWED_CHANGES
(prefers hook for this productivity niche when mechanism is present).
Prints a ready-to-adapt hypothesis sentence and points to the baseline starter.
Does not invent metrics, baselines, sources, or decisions.
Does not write files, poll secrets, or call external services.
Reusable to reduce post-publish experiment-planning labor across future videos.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract as idea_extract  # noqa: E402

# Prefer hook for first experiment on this channel (names the stall early).
PREFERRED_FIRST_CHANGE = "hook"
ALLOWED = {
    "hook",
    "mechanism_framing",
    "example_density",
    "title_promise",
    "visual_explanation",
    "pacing",
    "cta",
    "topic_selection",
}


def suggest_change(mech: str, problem: str) -> str:
    """Choose the single highest-leverage first change."""
    if mech and ("stall" in mech.lower() or "start" in mech.lower() or "default" in mech.lower()):
        return PREFERRED_FIRST_CHANGE
    if problem and len(problem) > 20:
        return "mechanism_framing"
    return PREFERRED_FIRST_CHANGE


def build_hypothesis(mech: str, topic: str, change: str) -> str:
    base = (mech or topic or "the core mechanism").strip()
    if len(base) > 70:
        base = base[:67] + "..."
    if change == "hook":
        return (
            f"A hook that names the exact stall '{base}' in the first 15 seconds "
            "will raise average view duration on the first 30 seconds"
        )
    if change == "mechanism_framing":
        return (
            f"Framing the mechanism as '{base}' more operationally (one concrete default) "
            "will raise average view duration"
        )
    return (
        f"Improving {change.replace('_', ' ')} around '{base}' "
        "will raise the primary retention metric"
    )


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python3 tools/first_experiment_suggest.py <packet>", file=sys.stderr)
        return 1
    packet = Path(sys.argv[1]).resolve()
    idea = packet / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {packet}", file=sys.stderr)
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(text)
    change = suggest_change(mech, problem)
    if change not in ALLOWED:
        change = PREFERRED_FIRST_CHANGE
    hyp = build_hypothesis(mech, topic, change)
    print("FIRST EXPERIMENT SUGGEST (soft; no invented metrics or baselines)")
    print(f"packet: {packet.name}")
    print(f"mechanism: {mech or '(none)'}")
    print(f"problem: {problem or '(none)'}")
    print(f"suggested_change: {change}")
    print()
    print("Suggested hypothesis (adapt if needed):")
    print(f"  {hyp}")
    print()
    print("Next concrete steps (after a real private video id + observation window):")
    print(f"  python3 tools/experiment_baseline_starter.py {packet} --change {change}")
    print("  # edit the printed JSON: set numeric baseline + documented source")
    print(f"  python3 tools/experiment_template_validator.py {packet}/experiment_baseline.json")
    print("  python3 tools/experiment_loop.py {packet}")
    print()
    print("Do not invent baselines. Human OAuth remains the blocker for first publish.")
    print("FIRST EXPERIMENT SUGGEST complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
