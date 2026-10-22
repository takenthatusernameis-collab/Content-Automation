#!/usr/bin/env python3
"""Generate a complete mechanism-aligned draft skeleton from idea.md.

Combines the logic of the individual *suggest.py tools into one output.
Prints a structured starter for draft.md covering Hook, Payoff promise,
Body beat starters, Failure mode, CTA, and VISUAL directions.
Does not write any files. Suggestions are starting points only.
Run quality_scan.py / claim_scan.py after expanding into a full draft.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from phrase_utils import shorten

ROOT = Path(__file__).resolve().parents[1]

MECH_RE = re.compile(r"mechanism[^\n]*:\s*(.+)", re.I)
PROBLEM_RE = re.compile(r"problem:\s*(.+)", re.I)
TOPIC_RE = re.compile(r"topic:\s*(.+)", re.I)

WEAK = (
    "unlock your potential", "in today's fast-paced", "let's dive in",
    "the key is", "in this video", "you will learn", "work smarter",
    "in fact", "of course", "obviously", "to sum up", "stock footage",
)

def extract(idea_text: str) -> tuple[str, str, str]:
    mech = ""
    problem = ""
    topic = ""
    for line in idea_text.splitlines():
        m = MECH_RE.search(line)
        if m:
            mech = m.group(1).strip().rstrip(".")
        p = PROBLEM_RE.search(line)
        if p:
            problem = p.group(1).strip().rstrip(".")
        t = TOPIC_RE.search(line)
        if t:
            topic = t.group(1).strip().rstrip(".")
    return mech, problem, topic

def suggest_hooks(mech: str, problem: str) -> list[str]:
    base = (mech or "written next-action default").lower()
    stall = (problem or "the stall").lower()
    candidates = [
        f"You already know what to work on. The stall is still there when it is time to start. Write the {shorten(base, 40)} where the decision happens.",
        f"The list is ready. The next action is not. Put the {shorten(base, 35)} on disk before you open the first tab.",
        f"Same decision, same delay. Name the stall in one sentence and install the {shorten(base, 30)} as the default.",
    ]
    return [c for c in candidates if not any(w in c.lower() for w in WEAK)][:3]

def suggest_payoff(mech: str) -> str:
    base = (mech or "the written next-action default").lower()
    short = shorten(base, 40)
    return (
        f"After this, you can install the {short} as a concrete under-two-minute action. "
        f"Name the exact next step, write it where the stall starts, and finish the install before the next tab opens. "
        f"That is the whole outcome: one default on disk that ends the reopen."
    )

def suggest_bodies(mech: str, problem: str) -> list[str]:
    base = (mech or "written next-action default").lower()
    stall = (problem or "the list reopens").lower()
    candidates = [
        f"You open the file and the stall starts. The list is still the whole page. Write the exact next action from the {shorten(base, 40)} at the top of the document before you scroll. That single line is the difference between reopening the decision and starting the first two minutes.",
        f"The tab is open. The work is not. Put the {shorten(base, 35)} on a sticky note on the monitor edge where the cursor already lives. When the stall hits, the note is the only thing visible. No new list. No extra decision.",
        f"Same morning, same delay. The planned task has no cue. Name one physical object that already sits on the desk and write the {shorten(base, 30)} on it. The object becomes the start signal. Opening the list is no longer the first action.",
    ]
    return [c for c in candidates if not any(w in c.lower() for w in WEAK)][:3]

def suggest_failure(mech: str, problem: str) -> str:
    base = (mech or "written next-action default").lower()
    stall = (problem or "the list reopens").lower()
    short = shorten(base, 40)
    return (
        f"Without the {short}, the stall repeats. You reopen the list, the next action is still unnamed, and the same delay starts again. "
        f"The missing cue is the written default. No note, no object, no single verb stays open. The decision never finishes."
    )

def suggest_cta(mech: str) -> str:
    base = (mech or "the written next-action default").lower()
    short = shorten(base, 40)
    return (
        f"Write the exact words of the {short} on a sticky note or in a note on the device you use to open the list. "
        f"Put that note where the stall starts. Do that before you open the next tab. "
        f"That is the whole assignment. It takes less than two minutes and it installs the default the video named."
    )

def suggest_visuals(mech: str) -> list[str]:
    base = (mech or "written next-action default").lower()
    candidates = [
        f"Close on the open list. Cursor hovers. No note visible. Then a sticky note with the {shorten(base, 40)} appears at the top of the page.",
        f"Desk edge. Monitor shows the stalled task. Hand places a small card with the exact {shorten(base, 35)} next to the keyboard. List stays closed.",
        f"Tab is open. Nothing is written. Camera stays on the empty first line while the viewer writes the {shorten(base, 30)} and leaves it open.",
    ]
    return [c for c in candidates if not any(w in c.lower() for w in WEAK)][:3]

def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after the draft starter skeleton."""
    p = packet
    return [
        f"copy preferred: paste chosen Hook/Payoff/Body/Failure/CTA lines into {p}/draft.md",
        f"expand elements: python3 tools/draft_beat_expansion_starter.py {p} for per-beat concrete elements while expanding body to 140-220 words",
        f"coach progress: python3 tools/draft_expansion_coach.py {p} or python3 tools/draft_short_beat_coach.py {p}",
        f"pre-apply signals: python3 tools/draft_pre_apply_coach.py {p} for full quality gate before apply",
        f"scans: python3 tools/quality_scan.py {p} && python3 tools/claim_scan.py {p}",
        f"apply: python3 tools/apply_script.py {p} --from {p}/draft.md --write --refresh once signals clear",
    ]

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate mechanism-aligned draft skeleton.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)
    print("DRAFT STARTER (mechanism-aligned skeleton; expand into full WORDS)")
    print(f"mechanism: {mech or '(default)'}")
    if problem:
        print(f"problem: {problem}")
    if topic:
        print(f"topic: {topic}")
    print()
    print("## Hook (0:00\u20130:12)")
    print("WORDS:")
    for i, h in enumerate(suggest_hooks(mech, problem), 1):
        print(f"  {i}. {h}  ({len(h.split())} words)")
    print("VISUAL:")
    for v in suggest_visuals(mech)[:1]:
        print(f"  *{v}*")
    print()
    print("## Payoff promise")
    print("WORDS:")
    print(f"  {suggest_payoff(mech)}")
    print()
    print("## Beat 1 \u2014 (expand one of the body starters)")
    print("WORDS:")
    for i, b in enumerate(suggest_bodies(mech, problem), 1):
        print(f"  {i}. {b}  ({len(b.split())} words)")
    print("VISUAL:")
    for v in suggest_visuals(mech)[1:2]:
        print(f"  *{v}*")
    print()
    print("## Beat 2 \u2014 Failure mode (when the default is absent)")
    print("WORDS:")
    print(f"  {suggest_failure(mech, problem)}")
    print()
    print("## CTA")
    print("WORDS:")
    print(f"  {suggest_cta(mech)}")
    print("VISUAL:")
    for v in suggest_visuals(mech)[2:3]:
        print(f"  *{v}*")
    print()
    print("---")
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    print("Copy preferred lines into videos/<id>-<slug>/draft.md, expand body beats to 140-220 words each,")
    print("keep total spoken WORDS 900-1500, then run tools/quality_scan.py and tools/claim_scan.py.")
    print("Do not invent statistics or anecdotes. Preserve exact ## headings.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
