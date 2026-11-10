#!/usr/bin/env python3
"""Suggest comment classifications from a collected feedback_state.json.

Reads comments already fetched into feedback_state.json (COLLECTED only).
Applies simple keyword rules to suggest one of the COMMENT_CLASSES from youtube_feedback.py.
Prints a reviewable list of suggestions. Does not invent comments, rewrite the state,
or call APIs. Fail-closed if no collected comments exist.
Reduces recurring labor of manually scanning raw comments for every future video.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from youtube_feedback import COMMENT_CLASSES  # noqa: E402

# Simple keyword rules (case-insensitive). First match wins. Not exhaustive; signals only.
RULES = [
    ("question", re.compile(r"\?|what|how|why|when|where|can you|does it|is there", re.I)),
    ("objection", re.compile(r"\bbut\b|wrong|disagree|actually|not true|however|instead", re.I)),
    ("praise", re.compile(r"great|awesome|helpful|thanks|thank you|love|excellent|useful", re.I)),
    ("confusion", re.compile(r"confus|unclear|don't understand|what do you mean|lost|hard to follow", re.I)),
    ("request", re.compile(r"please|can you make|next video|would like|suggestion|request", re.I)),
    ("spam/noise", re.compile(r"subscribe|follow me|check out|http|www\.|click here|free", re.I)),
]

def classify(text: str) -> str:
    """Return first matching class or 'unclassified'."""
    if not text or not text.strip():
        return "unclassified"
    for cls, pat in RULES:
        if pat.search(text):
            return cls
    return "unclassified"

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest classifications for comments in a collected feedback_state.json. No invent."
    )
    parser.add_argument("packet", help="Packet folder containing feedback_state.json")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    state_path = path / "feedback_state.json"

    print("COMMENT CLASS SUGGEST (signals only; from collected comments)")
    print(f"packet: {path.name}")

    if not state_path.is_file():
        print("feedback_state.json: ABSENT")
        print("HOLD: collect feedback first (after observation window).")
        print("See tools/youtube_feedback.py and tools/post_publish_sequence.py")
        print("COMMENT CLASS SUGGEST HOLD (no feedback state)")
        return 0

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"feedback_state.json: INVALID ({e})")
        print("COMMENT CLASS SUGGEST FAIL")
        return 1

    if state.get("gate") != "COLLECTED" or not state.get("attempted_fetch"):
        print("feedback_state.json: not a collected fetch")
        print("HOLD: only real collected comments are classified. Do not invent.")
        print("COMMENT CLASS SUGGEST HOLD (not collected)")
        return 0

    comments = state.get("comments") or []
    if not isinstance(comments, list) or not comments:
        print("No comments in collected state.")
        print("COMMENT CLASS SUGGEST HOLD (empty comments)")
        return 0

    print(f"Found {len(comments)} collected comment(s). Suggestions (first matching rule):")
    print()
    counts = {c: 0 for c in COMMENT_CLASSES}
    counts["unclassified"] = 0
    for i, c in enumerate(comments, 1):
        text = str(c.get("text") or "").strip()
        if not text:
            continue
        cls = classify(text)
        counts[cls] = counts.get(cls, 0) + 1
        short = text[:80] + ("..." if len(text) > 80 else "")
        print(f"{i}. [{cls}] {short}")

    print()
    print("## Counts")
    for cls, n in counts.items():
        if n:
            print(f"- {cls}: {n}")
    print()
    print("Review the suggestions. Map repeated specific needs into experiment hypotheses.")
    print("Do not treat one-off comments as strategy. See docs/feedback_loop.md.")
    print("COMMENT CLASS SUGGEST PASS (signals only)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
