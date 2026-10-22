#!/usr/bin/env python3
"""Print a ready-to-copy draft.md skeleton grounded in idea.md.

Emits a complete Markdown structure matching script.md / draft.md format
(## headings, WORDS:, VISUAL:) with the first mechanism-aligned candidates
from the same logic as draft_starter.py inserted as starting WORDS.
Includes expansion notes and word-target reminders so agents can copy the
output straight into videos/<id>-<slug>/draft.md and expand the body beats.
Does not invent statistics, anecdotes, or unverifiable claims.
Does not write any files. Does not call APIs.
Complements draft_starter.py (which prints candidates) and expand_starter.py
by assembling them into the exact file shape needed before apply_script.py.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from phrase_utils import shorten as _shorten

MECH_RE = re.compile(r"mechanism[^\n]*:\s*(.+)", re.I)
PROBLEM_RE = re.compile(r"problem:\s*(.+)", re.I)
TOPIC_RE = re.compile(r"topic:\s*(.+)", re.I)

WEAK = (
    "unlock your potential", "in today's fast-paced", "let's dive in",
    "the key is", "in this video", "you will learn", "work smarter",
    "in fact", "of course", "obviously", "to sum up", "stock footage",
)

def extract(idea_text: str) -> tuple[str, str, str]:
    mech = problem = topic = ""
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
    return mech or "written next-action default", problem or "the stall", topic or ""

def suggest_hook(mech: str, problem: str) -> str:
    base = _shorten(mech.lower(), 40)
    stall = problem.lower()
    return (
        f"You already know what to work on. The stall is still there when it is time to start. "
        f"Write the {base} where the decision happens."
    )

def suggest_payoff(mech: str) -> str:
    base = _shorten(mech.lower(), 40)
    return (
        f"After this, you can install the {base} as a concrete under-two-minute action. "
        f"Name the exact next step, write it where the stall starts, and finish the install before the next tab opens. "
        f"That is the whole outcome: one default on disk that ends the reopen."
    )

def suggest_body(mech: str, problem: str) -> str:
    base = _shorten(mech.lower(), 40)
    return (
        f"You open the file and the stall starts. The list is still the whole page. "
        f"Write the exact next action from the {base} at the top of the document before you scroll. "
        f"That single line is the difference between reopening the decision and starting the first two minutes."
    )

def suggest_failure(mech: str, problem: str) -> str:
    base = _shorten(mech.lower(), 40)
    return (
        f"Without the {base}, the stall repeats. You reopen the list, the next action is still unnamed, "
        f"and the same delay starts again. The missing cue is the written default. "
        f"No note, no object, no single verb stays open. The decision never finishes."
    )

def suggest_cta(mech: str) -> str:
    base = _shorten(mech.lower(), 40)
    return (
        f"Write the exact words of the {base} on a sticky note or in a note on the device you use to open the list. "
        f"Put that note where the stall starts. Do that before you open the next tab. "
        f"That is the whole assignment. It takes less than two minutes and it installs the default the video named."
    )

def suggest_visual(mech: str) -> str:
    base = _shorten(mech.lower(), 35)
    return f"Close on the open list. Cursor hovers. No note visible. Then a sticky note with the {base} appears at the top of the page."

def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after using the draft.md skeleton starter."""
    p = packet
    return [
        f"paste: copy the entire skeleton output into {p}/draft.md then expand body beats using checklist elements",
        f"checklist: python3 tools/draft_beat_expansion_starter.py {p} for per-beat concrete elements to add while expanding",
        f"progress: after pasting and expanding, run python3 tools/draft_expansion_coach.py {p} or python3 tools/draft_short_beat_coach.py {p}",
        f"quality gate: python3 tools/draft_pre_apply_coach.py {p} for full signals + copy-paste next before apply",
        f"apply: once signals clear, python3 tools/apply_script.py {p} --from {p}/draft.md --write --refresh",
    ]

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a ready-to-copy draft.md skeleton with mechanism-aligned starting WORDS. No invented content."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {args.packet}", file=sys.stderr)
        return 1

    text = idea.read_text(encoding="utf-8")
    mech, problem, topic = extract(text)

    print("DRAFT.MD STARTER (ready-to-copy skeleton; expand body beats to targets; no invented statistics or anecdotes)")
    print(f"# Draft skeleton for {path.name}")
    print("<!-- spoken_words: TBD  hook: TBD  beats: 5  target: 900-1500 -->")
    print("Spoken words only under each beat. Visual notes in italics.")
    print()
    print("## Hook (0:00\u20130:12)")
    print("WORDS:")
    print(suggest_hook(mech, problem))
    print()
    print("VISUAL:")
    print(f"*{suggest_visual(mech)}*")
    print()
    print("## Payoff promise")
    print("WORDS:")
    print(suggest_payoff(mech))
    print()
    print("## Beat 1 \u2014 Install the default")
    print("WORDS:")
    print(suggest_body(mech, problem))
    print("<!-- Expand this beat to 140\u2013220 spoken words with a concrete worked example of the mechanism on this packet's stall. -->")
    print()
    print("VISUAL:")
    print(f"*{suggest_visual(mech)}*")
    print()
    print("## Beat 2 \u2014 Place the cue")
    print("WORDS:")
    print(suggest_body(mech, problem))
    print("<!-- Expand to 140\u2013220 words: show where the written default lives so the reopen ends. -->")
    print()
    print("## Beat 3 \u2014 One small test")
    print("WORDS:")
    print(suggest_body(mech, problem))
    print("<!-- Expand to 140\u2013220 words: one operational check the viewer can run the same day. -->")
    print()
    print("## Beat 4 \u2014 Failure mode")
    print("WORDS:")
    print(suggest_failure(mech, problem))
    print("<!-- Expand to 140\u2013220 words: what repeats when the mechanism is absent. -->")
    print()
    print("## Beat 5 \u2014 Keep the default")
    print("WORDS:")
    print(suggest_body(mech, problem))
    print("<!-- Expand to 140\u2013220 words: how the constraint stays after the first install. -->")
    print()
    print("## CTA")
    print("WORDS:")
    print(suggest_cta(mech))
    print()
    print("VISUAL:")
    print(f"*{suggest_visual(mech)}*")
    print()
    print("---")
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    print("Next (do not invent sources, numbers, or anecdotes):")
    print("1. Copy this output into videos/<id>-<slug>/draft.md")
    print("2. Expand each body beat to 140\u2013220 spoken words so total lands ~1200 (band 900\u20131500).")
    print("3. Replace TBD in the HTML comment with actual counts after expansion.")
    print("4. Run python3 tools/quality_scan.py and python3 tools/claim_scan.py before apply_script.py --write.")
    print("5. Prefer concrete mechanism language; avoid anti-slop phrases listed in docs/content_quality.md.")
    print("This starter writes nothing. Preferred unblocked path remains human OAuth for publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
