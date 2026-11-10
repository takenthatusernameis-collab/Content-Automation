#!/usr/bin/env python3
"""Suggest experiment hypothesis candidates from classified comments in a collected feedback_state.json.

Reads comments already present in a COLLECTED feedback_state.json.
Applies the same keyword rules as comment_class_suggest.py to count classes.
If repeated question, confusion, or request signals exist (count >= 2), prints grounded hypothesis candidates tied to ALLOWED_CHANGES from experiment_loop.py.
Suggestions are revision signals only for the experiment loop. Does not invent comments, metrics, or decisions. Does not write files or call APIs.
Fail-closed if no real collected comments exist.
Reduces recurring labor of manually forming hypotheses after every future collect + classify.
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

from experiment_loop import ALLOWED_CHANGES  # noqa: E402
from youtube_feedback import COMMENT_CLASSES  # noqa: E402

# Same keyword rules as tools/comment_class_suggest.py (first match wins). Signals only.
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

def suggest_hypotheses(counts: dict[str, int]) -> list[str]:
    """Return grounded hypothesis candidates based on repeated signal classes. Signals only."""
    suggestions = []
    if counts.get("confusion", 0) >= 2:
        suggestions.append(
            "Repeated confusion signals: a clearer mechanism_framing or higher example_density may reduce viewer lost points. "
            "Candidate change: mechanism_framing or example_density."
        )
    if counts.get("question", 0) >= 2:
        suggestions.append(
            "Repeated question signals: viewers are asking for specifics that the current framing may not deliver. "
            "Candidate change: mechanism_framing, example_density, or visual_explanation."
        )
    if counts.get("request", 0) >= 2:
        suggestions.append(
            "Repeated request signals: audience is naming desired next topics or deeper coverage. "
            "Candidate change: topic_selection (for a follow-up packet) or cta."
        )
    if counts.get("objection", 0) >= 2:
        suggestions.append(
            "Repeated objection signals: a claim or framing is meeting pushback. "
            "Candidate change: mechanism_framing or example_density (add counter-examples or tighter evidence)."
        )
    if not suggestions and any(counts.get(c, 0) >= 1 for c in ("question", "confusion", "request", "objection")):
        suggestions.append(
            "Isolated signals present but below the repeated-threshold (count >= 2). "
            "Review individual comments manually before forming a hypothesis. Prefer repeated specific needs."
        )
    if not suggestions:
        suggestions.append(
            "No strong repeated question/confusion/request/objection signals in the collected comments. "
            "No hypothesis candidate suggested. Praise or spam do not automatically drive experiments."
        )
    return suggestions

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest experiment hypothesis candidates from classified comments in collected feedback_state.json. No invent."
    )
    parser.add_argument("packet", help="Packet folder containing feedback_state.json")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    state_path = path / "feedback_state.json"

    print("FEEDBACK HYPOTHESIS SUGGEST (signals only; from collected comments)")
    print(f"packet: {path.name}")
    print(f"allowed_changes: {', '.join(ALLOWED_CHANGES)}")

    if not state_path.is_file():
        print("feedback_state.json: ABSENT")
        print("HOLD: collect feedback first (after observation window).")
        print("See tools/youtube_feedback.py, tools/comment_class_suggest.py, and tools/post_publish_sequence.py")
        print("FEEDBACK HYPOTHESIS SUGGEST HOLD (no feedback state)")
        return 0

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"feedback_state.json: INVALID ({e})")
        print("FEEDBACK HYPOTHESIS SUGGEST FAIL")
        return 1

    if state.get("gate") != "COLLECTED" or not state.get("attempted_fetch"):
        print("feedback_state.json: not a collected fetch")
        print("HOLD: only real collected comments generate hypothesis signals. Do not invent.")
        print("FEEDBACK HYPOTHESIS SUGGEST HOLD (not collected)")
        return 0

    comments = state.get("comments") or []
    if not isinstance(comments, list) or not comments:
        print("No comments in collected state.")
        print("FEEDBACK HYPOTHESIS SUGGEST HOLD (empty comments)")
        return 0

    counts = {c: 0 for c in COMMENT_CLASSES}
    counts["unclassified"] = 0
    for c in comments:
        text = str(c.get("text") or "").strip()
        if not text:
            continue
        cls = classify(text)
        counts[cls] = counts.get(cls, 0) + 1

    print(f"Classified {sum(counts.values())} comment(s). Counts:")
    for cls, n in counts.items():
        if n:
            print(f"- {cls}: {n}")
    print()

    hyps = suggest_hypotheses(counts)
    print("## Hypothesis candidates (review before recording in experiments.md or experiment_baseline.json)")
    for h in hyps:
        print(f"- {h}")
    print()
    print("These are grounded signals only. Do not invent a numeric baseline. "
          "Use tools/experiment_baseline_starter.py after choosing one change. "
          "See docs/feedback_loop.md and docs/experiments.md.")
    print("FEEDBACK HYPOTHESIS SUGGEST PASS (signals only)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
