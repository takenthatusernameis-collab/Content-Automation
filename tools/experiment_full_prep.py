#!/usr/bin/env python3
"""Packet-specific full experiment prep: grounded hypothesis + ready-to-adapt JSON examples.

Extracts mechanism from idea.md (via idea_utils), suggests preferred first change (hook),
builds a ready hypothesis, and prints complete baseline + decision JSON examples with
the hypothesis filled in (baseline remains null; sources use valid phrasing).
Does not invent numeric baselines, decisions, video ids, or dates.
Does not write files, poll secrets, or call APIs.
Reduces sequential runs of first_experiment_suggest + experiment_json_examples for every future packet.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract as idea_extract  # noqa: E402

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

BASELINE_SOURCE = (
    "YouTube Studio analytics for the prior video titled '<exact title>' retrieved on YYYY-MM-DD"
)
DECISION_SOURCE = (
    "Human review of YouTube Studio analytics for video '<exact title>' (id <PROVIDER_VIDEO_ID>) "
    "on YYYY-MM-DD after the observation window"
)


def suggest_change(mech: str, problem: str) -> str:
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


def example_baseline(hypothesis: str, change: str) -> dict:
    return {
        "_example": "ready-to-adapt for this packet; replace angle-brackets and YYYY-MM-DD; set numeric baseline",
        "hypothesis": hypothesis,
        "change": change,
        "primary_metric": "average_view_duration_seconds",
        "baseline": None,  # MUST replace with real number from documented source
        "source": BASELINE_SOURCE,
        "notes": "change is the suggested single variable; baseline must be numeric before use; source phrasing passes rejected-words check",
    }


def example_decision(hypothesis: str) -> dict:
    return {
        "_example": "ready-to-adapt; replace placeholders; choose keep/discard/retest only after real numeric comparison",
        "decision": "keep",  # or discard / retest; do not invent
        "reason": f"Average view duration improved relative to the documented baseline for hypothesis: {hypothesis[:80]}...",
        "source": DECISION_SOURCE,
        "primary_metric": "average_view_duration_seconds",
        "notes": "source must be a documented review; do not use invented/assumed/placeholder/guess",
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python3 tools/experiment_full_prep.py <packet>", file=sys.stderr)
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

    print("EXPERIMENT FULL PREP (soft; packet-specific; no invented numbers or decisions)")
    print(f"packet: {packet.name}")
    print(f"mechanism: {mech or '(none)'}")
    print(f"suggested_change: {change}")
    print()
    print("Suggested hypothesis (already filled into examples below):")
    print(f"  {hyp}")
    print()
    print("--- ready-to-adapt experiment_baseline.json ---")
    print(json.dumps(example_baseline(hyp, change), indent=2))
    print()
    print("--- ready-to-adapt experiment_decision.json ---")
    print(json.dumps(example_decision(hyp), indent=2))
    print()
    print("Next concrete steps (after real private video id + observation window + comparison):")
    print(f"  # adapt the baseline JSON above (set numeric baseline + real source), write to {packet.name}/experiment_baseline.json")
    print(f"  python3 tools/experiment_template_validator.py {packet}/experiment_baseline.json")
    print("  # after comparison, adapt decision JSON and validate")
    print(f"  python3 tools/next_from_decision.py {packet}")
    print()
    print("Do not invent baselines or decisions. Human OAuth remains the blocker for first publish.")
    print("EXPERIMENT FULL PREP complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
