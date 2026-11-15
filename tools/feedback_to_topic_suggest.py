#!/usr/bin/env python3
"""Soft suggestor for feeding observed feedback back into the topic queue.

Grounded in channel niche (systems for focused work; install one small default
the same day). Prints guidance on turning operational comment signals or
measured weak points into queue candidates without inventing topics or results.
Uses idea_utils when a packet is given. Complements experiment tools.
Does not write files, poll, invent data, or scaffold. Exit 0.
Also surfaces ready working_title, one_line, problem, full queue_row, and idea.md paste snippets (dynamically adapted to the packet's mechanism/problem when present) so the human can start the next queue row and idea.md faster without inventing phrasing.
The idea.md section now emits a complete copy-paste-ready markdown block.
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
    print("  - working_title: Short operational title naming the installable default or stall.")
    print("  - one_line: Name one concrete installable default (cue, constraint, checklist) tied to a specific stall.")
    print("  - problem: The stall that reopens the list or prevents starting.")
    print("  - Prefer topics that can be observed the same day via comment language.")
    print()
        # Dynamic snippets when packet idea is present; fall back to generic. Keep language natural.
    short_mech = (mech.split(" so ")[0] if mech and " so " in mech else (mech or "the installable default")).strip()
    if short_mech.lower().startswith("install "):
        short_mech = short_mech[8:].strip() or short_mech
    short_prob = (problem or "the morning stall that reopens the list").strip()
    print("Ready working_title snippets (copy/edit as starting language; adapted to packet mechanism when present):")
    title_snippets = {
        "keep": f"Install {short_mech.lower()} for related stalls" if mech else "Install a written next-action default for related morning stalls",
        "discard": "Return to the simpler prior default that increased same-day installs",
        "retest": f"Retest {short_mech.lower()} on a comparable stall" if mech else "Retest the same installable default on a comparable stall",
    }
    for dec, snip in title_snippets.items():
        print(f"  {dec}: {snip}")
    print()
    print("Ready one_line topic snippets (copy/edit as starting language; adapted to packet when present):")
    topic_snippets = {
        "keep": f"Install {short_mech} for a related stall so the list does not reopen before starting the focused block." if mech else "Install a written next-action default for a related morning stall so the list does not reopen before starting the focused block.",
        "discard": "Return to a simpler cue or constraint default that viewers can install the same day without the failed change that reduced install mentions.",
        "retest": f"Retest {short_mech} on a different but comparable stall to isolate whether the mechanism drives same-day start comments." if mech else "Retest the same installable default on a different but comparable stall to isolate whether the mechanism reliably produces same-day start comments.",
    }
    for dec, snip in topic_snippets.items():
        print(f"  {dec}: {snip}")
    print()
    print("Ready problem snippets (copy/edit as starting language for the problem field; adapted to packet stall when present):")
    problem_snippets = {
        "keep": f"{short_prob.capitalize()} because there is no written next-action default tied to it; viewers mention starting the installable default the same day." if problem else "The list reopens before the focused block starts because there is no written next-action default tied to the morning stall; viewers mention starting the installable default the same day.",
        "discard": "Viewers struggled to install the tested change the same day or reported fewer start mentions; the simpler prior cue or constraint reduced the stall more reliably.",
        "retest": f"The same {short_mech.lower()} needs a second observation on a comparable stall to confirm whether the mechanism reliably produces same-day start comments." if mech else "The same installable default needs a second observation on a comparable stall to confirm whether the mechanism reliably produces same-day start comments.",
    }
    for dec, snip in problem_snippets.items():
        print(f"  {dec}: {snip}")
    print()
    print("Ready full queue_row snippets (copy/edit as a complete starter row for docs/topic_queue.md; adapt working_title, one_line, and problem to the actual decision):")
    for dec in ("keep", "discard", "retest"):
        title = title_snippets.get(dec, "")
        one = topic_snippets.get(dec, "")
        prob = problem_snippets.get(dec, "")
        print(f"  {dec}:")
        print(f"    working_title: {title}")
        print(f"    one_line: {one}")
        print(f"    problem: {prob}")
        print()
    print("Ready idea.md paste snippets (complete copy-paste-ready markdown blocks; adapt to actual decision):")
    idea_why_now = {
        "keep": "The winning mechanism produced same-day install mentions; the related stall is still present for many viewers.",
        "discard": "The tested change reduced install mentions; the simpler prior default is the more reliable same-day install.",
        "retest": "One observation window is not enough to confirm the mechanism; a second comparable stall will isolate the variable.",
    }
    for dec in ("keep", "discard", "retest"):
        title = title_snippets.get(dec, "")
        one = topic_snippets.get(dec, "")
        prob = problem_snippets.get(dec, "")
        why = idea_why_now.get(dec, "")
        print(f"  {dec}:")
        print("```markdown")
        print("# Idea")
        print()
        print(f"- topic: {title}")
        print(f"- viewer: People who already plan their week, then stall when it is time to start.")
        print(f"- problem: {prob}")
        print(f"- mechanism (the system, not the pep talk): {one}")
        print(f"- why now: {why}")
        print("- related videos to avoid repeating: none published yet")
        print("```")
        print()
    print("How to use with existing tools:")
    print("  1. After experiment_decision.json records keep/discard/retest with documented source.")
    print("  2. Use a ready full queue_row snippet above (or edit the separate working_title/one_line/problem) as the starting row.")
    print("  3. Manually add one queued row in docs/topic_queue.md following the pattern.")
    print("  4. Use a ready idea.md paste snippet above when filling idea.md (or python3 tools/apply_idea.py PACKET --write).")
    print("  5. python3 tools/topic_queue_mechanism_check.py  # soft alignment")
    print("  6. python3 tools/next_topic.py  # confirm next scaffold candidate")
    print("  7. Only scaffold with explicit human instruction via new_packet.py")
    print()
    print("Do not invent topics, metrics, or decisions. Human OAuth remains the blocker for first publish.")
    print("FEEDBACK TO TOPIC SUGGEST complete.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
