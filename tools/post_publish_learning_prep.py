#!/usr/bin/env python3
"""One-command soft post-publish learning-loop readiness summary.

Aggregates grounded guidance from the recent soft suggestors (metric focus,
niche metric bridge, same-day install observability, feedback-to-topic,
experiment prep) into a single view for a packet.
Uses idea_utils when idea.md present. Does not invent numbers, topics,
baselines, or decisions. Does not write files, poll secrets, or scaffold.
Reduces sequential human/agent invocation of five tools across future packets.
Exit 0 always when packet optional or present.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
try:
    from idea_utils import extract
except ImportError:
    print("idea_utils not found; run from repo root", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    idea_path = packet / "idea.md"
    mech = problem = topic = ""
    if idea_path.is_file():
        idea_text = idea_path.read_text(encoding="utf-8")
        mech, problem, topic = extract(idea_text)

    print("POST-PUBLISH LEARNING PREP (soft one-command aggregator; no invent)")
    print(f"packet (optional): {packet.name if idea_path.is_file() else 'none'}")
    print("channel promise: viewer installs one small default (cue, constraint, or checklist) the same day.")
    if mech:
        print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    print()

    print("1. METRIC FOCUS (what to measure; operational, not pure AVD)")
    if mech:
        print(f"   Primary: start-completion or same-day install mentions for the default in '{mech[:70]}...'")
    else:
        print("   Primary: viewer-reported ability to start the planned work the same day.")
    print("   Guardrails: retention secondary; comment quality; avoid likes/subs as primary.")
    print()

    print("2. NICHE SIGNAL BRIDGE (how to observe the promise)")
    print("   Look for comments mentioning installing/trying/starting the named default the same day.")
    print("   Document qualitative rate as baseline source later; proxies are AVD/comments secondary.")
    if mech:
        print(f"   Cue language around: {mech[:60]}")
    print()

    print("3. SAME-DAY OBSERVABILITY (make it reportable in comments)")
    print("   Name the exact default in CTA/description. Use a short echoable phrase.")
    print("   Prefer visible/file-based cues so comments can describe the physical change.")
    if mech:
        print(f"   Reportable phrase idea: something concrete from '{mech[:50]}'")
    print()

    print("4. FEEDBACK → TOPIC (after real signals)")
    print("   Weak install mentions → clearer cue/constraint topics. Strong mentions → keep similar defaults.")
    print("   Queue pattern: one_line = concrete installable default; problem = the stall with no named start.")
    print()

    print("5. EXPERIMENT PREP POINTER")
    print("   After window + comparison: use tools/experiment_full_prep.py for hypothesis + JSON skeletons.")
    print("   Prefer single change (often hook) tied to the mechanism. No invented baselines.")
    print()

    print("Recommended sequence after first private id + observation window:")
    print("  - Collect feedback, count operational mentions.")
    print("  - Document baseline, then experiment_full_prep + validator.")
    print("  - Decision, then feedback_to_topic_suggest + topic_queue_mechanism_check.")
    print()
    print("Individual tools remain available for depth. This aggregator reduces sequential rediscovery.")
    print("Do not invent data. Human OAuth remains the blocker for first publish.")
    print("POST-PUBLISH LEARNING PREP complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
