#!/usr/bin/env python3
"""Soft suggestor for feeding observed feedback back into the topic queue.

Grounded in channel niche (systems for focused work; install one small default
the same day). Prints guidance on turning operational comment signals or
measured weak points into queue candidates without inventing topics or results.
Uses idea_utils when a packet is given. Complements experiment tools.
Does not write files, poll, invent data, or scaffold. Exit 0.
Also surfaces ready one_line, problem, and full queue_row snippets so the human can start the next queue row faster without inventing phrasing.
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
    print("FEEDBACK TO TOPIC SUGGEST (soft; no invent, no scaffold)")
    print(f"packet (optional): {packet.name if idea_path.is_file() else 'none'}")
    print(f"channel niche: Systems for doing focused work. Promise: install one small default the same day.")
    if mech:
        print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    print()
    print("When real feedback arrives (comments or metrics after observation window):")
    print("  - Prefer operational signals: mentions of installing/trying/starting the named default.")
    print("  - Weak points (low early retention, repeated questions about 'how to start') point to clearer cue/constraint topics.")
    print("  - Strong install mentions on a mechanism support keeping similar defaults; do not invent new ones.")
    print()
    print("Suggested queue refinement pattern (adapt, do not invent):")
    print("  - one_line: Name one concrete installable default (cue, constraint, checklist) tied to a specific stall.")
    print("  - problem: The stall that reopens the list or prevents starting.")
    print("  - Prefer topics that can be observed the same day via comment language.")
    print()
    print("Ready one_line topic snippets (copy/edit as starting language; adapt to actual decision and mechanism):")
    topic_snippets = {
        "keep": "Install a written next-action default for a related morning stall so the list does not reopen before starting the focused block.",
        "discard": "Return to a simpler cue or constraint default that viewers can install the same day without the failed change that reduced install mentions.",
        "retest": "Retest the same installable default on a different but comparable stall to isolate whether the mechanism drives same-day start comments.",
    }
    for dec, snip in topic_snippets.items():
        print(f"  {dec}: {snip}")
    print()
    print("Ready problem snippets (copy/edit as starting language for the problem field; grounded in the stall the decision addresses):")
    problem_snippets = {
        "keep": "The list reopens before the focused block starts because there is no written next-action default tied to the morning stall; viewers mention starting the installable default the same day.",
        "discard": "Viewers struggled to install the tested change the same day or reported fewer start mentions; the simpler prior cue or constraint reduced the stall more reliably.",
        "retest": "The same installable default needs a second observation on a comparable stall to confirm whether the mechanism reliably produces same-day start comments.",
    }
    for dec, snip in problem_snippets.items():
        print(f"  {dec}: {snip}")
    print()
    print("Ready full queue_row snippets (copy/edit as a complete starter row for docs/topic_queue.md; adapt one_line and problem to the actual decision):")
    for dec in ("keep", "discard", "retest"):
        one = topic_snippets.get(dec, "")
        prob = problem_snippets.get(dec, "")
        print(f"  {dec}:")
        print(f"    one_line: {one}")
        print(f"    problem: {prob}")
        print()
    print("How to use with existing tools:")
    print("  1. After experiment_decision.json records keep/discard/retest with documented source.")
    print("  2. Use a ready full queue_row snippet above (or edit the separate one_line/problem) as the starting row.")
    print("  3. Manually add one queued row in docs/topic_queue.md following the pattern.")
    print("  4. python3 tools/topic_queue_mechanism_check.py  # soft alignment")
    print("  5. python3 tools/next_topic.py  # confirm next scaffold candidate")
    print("  6. Only scaffold with explicit human instruction via new_packet.py")
    print()
    print("Do not invent topics, metrics, or decisions. Human OAuth remains the blocker for first publish.")
    print("FEEDBACK TO TOPIC SUGGEST complete.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
