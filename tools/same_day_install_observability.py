#!/usr/bin/env python3
"""Soft suggestor for making the channel promise more observable in comments.

Grounded in niche: systems for focused work; promise is install one small default
the same day. Suggests concrete phrasing or cue-naming so that real viewer
comments can more reliably surface operational signals (tried it today, installed
the cue) without inventing topics or results.
Uses idea_utils when a packet is given. Complements feedback_to_topic_suggest
and niche_metric_bridge. Does not write files, poll, invent data, or scaffold.
Exit 0.
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
    print("SAME-DAY INSTALL OBSERVABILITY (soft; no invent, no scaffold)")
    print(f"packet (optional): {packet.name if idea_path.is_file() else 'none'}")
    print("channel promise: viewer installs one small default (cue, constraint, or checklist) the same day.")
    if mech:
        print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    print()
    print("To make operational signals easier to observe in future comments:")
    print("  - Name the exact default in the CTA and description (e.g., 'write the next verb on the file itself').")
    print("  - Use a short, reportable phrase the viewer can echo: 'I put the start cue on the work.'")
    print("  - Prefer cues that are visible or file-based so a comment can describe the physical change.")
    print("  - Avoid abstract mechanisms that leave no concrete action to report the same day.")
    if mech:
        print(f"  - For this mechanism, consider a reportable phrase around: {mech[:80]}")
    print()
    print("Queue refinement pattern (when feedback shows low install mentions):")
    print("  - one_line: Name one concrete, same-day-installable default with an explicit reportable cue.")
    print("  - problem: The stall that has no visible or named starting point.")
    print()
    print("How to use with existing tools:")
    print("  1. python3 tools/niche_metric_bridge.py <packet>  # signals to watch")
    print("  2. python3 tools/feedback_to_topic_suggest.py <packet>  # after real comments")
    print("  3. Manually refine docs/topic_queue.md one_line/problem for higher observability.")
    print("  4. python3 tools/topic_queue_mechanism_check.py")
    print()
    print("Do not invent topics or comment counts. Human OAuth remains the blocker for first publish.")
    print("SAME-DAY INSTALL OBSERVABILITY complete.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
