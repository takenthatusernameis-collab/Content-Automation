#!/usr/bin/env python3
"""Suggest a candidate experiment_baseline.json skeleton from collected feedback.

Reads feedback_state.json (via the same gates as other feedback tools).
Uses the same keyword classification and hypothesis rules as feedback_hypothesis_suggest.py
and feedback_review_brief.py. Picks the strongest repeated signal (confusion/question/request/objection
with count >= 2) and emits a printable JSON stub with hypothesis and change filled,
primary_metric suggested from the map, baseline null, and source marked pending human documentation.
Does not invent numeric baselines, metrics, or decisions. Does not write files or call APIs.
Fail-closed if no real collected comments. Reduces labor of manually translating review signals
into the baseline template fields after every future collect.
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

# Reuse the same rules and map as feedback_review_brief.py
RULES = [
    ("question", re.compile(r"\?|what|how|why|when|where|can you|does it|is there", re.I)),
    ("objection", re.compile(r"\bbut\b|wrong|disagree|actually|not true|however|instead", re.I)),
    ("praise", re.compile(r"great|awesome|helpful|thanks|thank you|love|excellent|useful", re.I)),
    ("confusion", re.compile(r"confus|unclear|don't understand|what do you mean|lost|hard to follow", re.I)),
    ("request", re.compile(r"please|can you make|next video|would like|suggestion|request", re.I)),
    ("spam/noise", re.compile(r"subscribe|follow me|check out|http|www\.|click here|free", re.I)),
]

METRIC_MAP = {
    "hook": ["average_view_duration_seconds", "average_percentage_viewed", "views"],
    "mechanism_framing": ["average_view_duration_seconds", "average_percentage_viewed", "likes"],
    "example_density": ["average_view_duration_seconds", "average_percentage_viewed", "comments"],
    "title_promise": ["impressions_click_through_rate", "views", "average_view_duration_seconds"],
    "visual_explanation": ["average_view_duration_seconds", "average_percentage_viewed", "likes"],
    "pacing": ["average_view_duration_seconds", "average_percentage_viewed", "views"],
    "cta": ["end_screen_element_click_rate", "subscribers_gained", "average_view_duration_seconds"],
    "topic_selection": ["views", "average_view_duration_seconds", "impressions"],
}


def classify(text: str) -> str:
    if not text or not text.strip():
        return "unclassified"
    for cls, pat in RULES:
        if pat.search(text):
            return cls
    return "unclassified"


def suggest_hypotheses(counts: dict[str, int]) -> list[tuple[str, str]]:
    """Return (hypothesis_text, preferred_change) pairs for strong signals."""
    suggestions = []
    if counts.get("confusion", 0) >= 2:
        suggestions.append((
            "Repeated confusion signals indicate viewers are lost on the core mechanism; clearer mechanism_framing or higher example_density may reduce drop-off.",
            "mechanism_framing"
        ))
    if counts.get("question", 0) >= 2:
        suggestions.append((
            "Repeated question signals show viewers asking for specifics the current framing does not deliver; mechanism_framing, example_density, or visual_explanation are candidate changes.",
            "mechanism_framing"
        ))
    if counts.get("request", 0) >= 2:
        suggestions.append((
            "Repeated request signals name desired next topics or deeper coverage; topic_selection for a follow-up or stronger cta are candidates.",
            "topic_selection"
        ))
    if counts.get("objection", 0) >= 2:
        suggestions.append((
            "Repeated objection signals indicate a claim or framing is meeting pushback; tighter mechanism_framing or added counter-examples (example_density) may address it.",
            "mechanism_framing"
        ))
    return suggestions


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a candidate experiment_baseline.json skeleton from collected feedback. No writes, no invent."
    )
    parser.add_argument("packet", help="Packet folder")
    args = parser.parse_args()
    packet = Path(args.packet).resolve()
    if not packet.is_dir():
        print(f"not a directory: {packet}", file=sys.stderr)
        return 1

    # Reuse the same fail-closed gate as other feedback tools
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

    comments = state.get("comments") or []
    if not isinstance(comments, list) or len(comments) == 0:
        print("HOLD: feedback_state.json has no collected comments list (or empty)")
        print("Fail-closed. Do not invent comments or baselines.")
        return 2

    counts: dict[str, int] = {cls: 0 for cls in COMMENT_CLASSES}
    for c in comments:
        text = (c.get("text") or "") if isinstance(c, dict) else str(c)
        cls = classify(text)
        if cls in counts:
            counts[cls] += 1

    hypotheses = suggest_hypotheses(counts)
    if not hypotheses:
        print("NO_STRONG_SIGNAL: no class reached count >= 2. No candidate baseline suggested.")
        print("Review the full brief with: python3 tools/feedback_review_brief.py", packet)
        print("Manual baseline still required. Do not invent.")
        return 0

    # Pick the first (strongest in the order we check)
    hyp_text, preferred_change = hypotheses[0]
    if preferred_change not in ALLOWED_CHANGES:
        preferred_change = "mechanism_framing"

    suggested_metric = METRIC_MAP.get(preferred_change, ["average_view_duration_seconds"])[0]

    stub = {
        "_suggested_from_feedback": True,
        "_comment": "SUGGESTION ONLY. Copy to experiment_baseline.json, replace baseline with a real numeric value from documented analytics, replace source with a real documented observation, then validate. Do not invent numbers.",
        "hypothesis": hyp_text,
        "change": preferred_change,
        "primary_metric": suggested_metric,
        "baseline": None,
        "source": "PENDING: replace with documented source from human review of analytics or Studio after the observation window",
        "notes": f"Auto-suggested from collected comments (counts: {counts}). Preferred change {preferred_change}. Fill baseline (numeric) and source before using with experiment_loop.py. Other candidates exist; see feedback_review_brief.py."
    }

    print("CANDIDATE BASELINE STUB (print only; do not auto-write)")
    print(json.dumps(stub, indent=2))
    print()
    print("Next human steps:")
    print("1. Review with python3 tools/feedback_review_brief.py", packet)
    print("2. Copy the stub above into", packet / "experiment_baseline.json")
    print("3. Fill the real numeric baseline and documented source.")
    print("4. python3 tools/experiment_baseline_validate.py", packet)
    print("5. python3 tools/experiment_loop.py", packet)
    print("Do not invent metrics or decisions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
