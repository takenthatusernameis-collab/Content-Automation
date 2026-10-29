#!/usr/bin/env python3
"""Write a local word_budget.md with per-segment spoken-word targets.

Extracts mechanism/problem/topic from idea.md and emits a structured
word_budget.md that maps format.md targets (Hook 20-35, Payoff 40-70,
each of 4 Beats 140-220, CTA 40-80, total 900-1500) to the packet fields.
No invented spoken lines or claims. Output stays local (gitignored).
Reduces recurring labor of manually calculating and tracking word budgets
while expanding draft_skeleton.md for every future packet. Aligns with
channel voice (assignment, not reply prompt), format word band, and no-invent
rule. Complements draft_skeleton_writer.py and expansion_checklist_writer.py.
Not a final script.
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


def shorten(s: str, n: int) -> str:
    s = (s or "").strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write local word_budget.md from idea.md fields only"
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

    out_path = packet / "word_budget.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    base = shorten(mech or "the written next-action default", 50)
    stall = problem or "the stall reopens the list"

    lines = [
        "# Word Budget (local; expansion tracker)",
        "",
        "Generated locally from idea.md mechanism/problem/topic only.",
        "Per-segment spoken-word targets from docs/format.md for expanding",
        "draft_skeleton.md short lines to the 900–1500 total band (aim ~1200).",
        "Track progress here while expanding. No invented claims or statistics.",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "Complements draft_skeleton_writer.py and expansion_checklist_writer.py.",
        "Not a final script. Copy expanded WORDS into draft.md.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem / stall: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "## Targets (spoken words)",
        "",
        "| Segment | Min | Target | Max | Notes |",
        "|---------|-----|--------|-----|-------|",
        "| Hook | 20 | 25 | 35 | Name stall + install default. Card on from first word. |",
        "| Payoff | 40 | 55 | 70 | Viewer can state the outcome before middle. |",
        "| Beat 1 | 140 | 180 | 220 | Name stall + first verb from default. |",
        "| Beat 2 | 140 | 180 | 220 | Place the default where eyes already land. |",
        "| Beat 3 | 140 | 180 | 220 | First concrete action in next five minutes. |",
        "| Beat 4 | 140 | 180 | 220 | Point at default when stall returns. |",
        "| CTA | 40 | 55 | 80 | Assignment to install today. Not subscribe. |",
        "| **Total** | **900** | **~1200** | **1500** | Stay in band. Use quality_scan after. |",
        "",
        "## Grounding notes (from idea.md only)",
        f"- Default to expand around: {base}",
        f"- Stall scene to keep concrete: {stall}",
        "- Prefer observable actions and decisions over slogans.",
        "- Do not add numbers, percentages, or anecdotes without a source in research_notes.md.",
        "",
        "## Tracking",
        "After each expansion pass, note approximate word counts here:",
        "- Hook: ",
        "- Payoff: ",
        "- Beat 1: ",
        "- Beat 2: ",
        "- Beat 3: ",
        "- Beat 4: ",
        "- CTA: ",
        "- Total: ",
        "",
        "---",
        "Run tools/draft_skeleton_writer.py first if missing, then this, then",
        "tools/expansion_checklist_writer.py. Expand into draft.md. Run",
        "tools/draft_pre_apply_coach.py and tools/quality_scan.py before apply.",
        "Preferred unblocked path remains the human OAuth step for publish.",
    ]

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print(f"topic_found: {bool(topic)}")
    print("Word budget ready (local; estimated from packet fields only; expand next).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
