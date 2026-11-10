#!/usr/bin/env python3
"""Suggest candidate topic queue rows from request-class comments in collected feedback.

Reads feedback_state.json (via the same gates as other feedback tools).
Uses the same keyword classification rules. When request signals exist, prints the source comments and simple candidate working_title / one_line rows suitable for human review before adding to docs/topic_queue.md.
Does not invent topics, problems, write the queue file, or call APIs. Fail-closed if no real collected comments.
Reduces recurring labor of manually scanning request comments for next-video ideas after every future collect.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from youtube_feedback import COMMENT_CLASSES  # noqa: E402

RULES = [
    ("question", re.compile(r"\?|what|how|why|when|where|can you|does it|is there", re.I)),
    ("objection", re.compile(r"\bbut\b|wrong|disagree|actually|not true|however|instead", re.I)),
    ("praise", re.compile(r"great|awesome|helpful|thanks|thank you|love|excellent|useful", re.I)),
    ("confusion", re.compile(r"confus|unclear|don't understand|what do you mean|lost|hard to follow", re.I)),
    ("request", re.compile(r"please|can you make|next video|would like|suggestion|request", re.I)),
    ("spam/noise", re.compile(r"subscribe|follow me|check out|http|www\.|click here|free", re.I)),
]

def classify(text: str) -> str:
    if not text or not text.strip():
        return "unclassified"
    for cls, pat in RULES:
        if pat.search(text):
            return cls
    return "unclassified"

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print candidate topic queue rows from request comments in collected feedback. No writes, no invent."
    )
    parser.add_argument("packet", help="Packet folder")
    args = parser.parse_args()
    packet = Path(args.packet).resolve()
    if not packet.is_dir():
        print(f"not a directory: {packet}", file=sys.stderr)
        return 1

    state_path = packet / "feedback_state.json"
    if not state_path.is_file():
        print("HOLD: no feedback_state.json (collect first; do not invent)")
        print("Run: python3 tools/youtube_feedback.py <packet> or the post_publish_sequence collect step")
        return 2

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("HOLD: feedback_state.json is not valid JSON")
        return 2

    if state.get("gate") != "COLLECTED" or not state.get("attempted_fetch"):
        print("HOLD: feedback_state.json is not a collected fetch")
        print("Fail-closed. Do not invent comments or topics.")
        return 2

    comments = state.get("comments") or []
    if not isinstance(comments, list) or len(comments) == 0:
        print("HOLD: feedback_state.json has no collected comments list (or empty)")
        print("Fail-closed. Do not invent comments or topics.")
        return 2

    request_texts = []
    for c in comments:
        text = (c.get("text") or "") if isinstance(c, dict) else str(c)
        text = text.strip()
        if text and classify(text) == "request":
            request_texts.append(text)

    if not request_texts:
        print("NO_REQUEST_SIGNALS: no comments classified as request. No topic candidates suggested.")
        print("Review the full brief with: python3 tools/feedback_review_brief.py", packet)
        print("Manual topic ideas still required. Do not invent.")
        return 0

    print("CANDIDATE TOPIC ROWS (print only; review before adding to docs/topic_queue.md)")
    print(f"Found {len(request_texts)} request comment(s). Suggestions are signals only.")
    print()
    for i, text in enumerate(request_texts[:5], 1):
        short = text.split(".")[0][:70].strip() or text[:70].strip()
        print(f"Candidate {i}:")
        print(f"  working_title: {short}")
        print(f"  one_line: Audience requested coverage of: {short}")
        print(f"  problem: (human: extract the underlying stall or need from the comment)")
        print(f"  source_comment: {text[:180]}")
        print()
    print("Next human steps:")
    print("1. Review signals with python3 tools/feedback_review_brief.py", packet)
    print("2. Align candidates to the niche in docs/channel.md and the table format in docs/topic_queue.md")
    print("3. Add via tools/mark_topic.py or direct edit only after review. Do not auto-write the queue.")
    print("Do not invent topics, problems, or mechanisms.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
