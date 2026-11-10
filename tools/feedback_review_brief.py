#!/usr/bin/env python3
"""Single-command review brief from collected feedback_state.json.

Combines the classification counts from comment_class_suggest.py logic,
hypothesis candidates from feedback_hypothesis_suggest.py, and metric
suggestions aligned to candidate changes (from experiment_metric_suggest.py map).
Prints one reviewable brief. Does not invent comments, metrics, baselines,
or decisions. Does not write files or call APIs. Fail-closed if no real
collected comments exist.
Reduces recurring labor of running multiple suggest tools after every future collect.
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

# Same keyword rules as comment_class_suggest.py / feedback_hypothesis_suggest.py
RULES = [
    ("question", re.compile(r"\?|what|how|why|when|where|can you|does it|is there", re.I)),
    ("objection", re.compile(r"\bbut\b|wrong|disagree|actually|not true|however|instead", re.I)),
    ("praise", re.compile(r"great|awesome|helpful|thanks|thank you|love|excellent|useful", re.I)),
    ("confusion", re.compile(r"confus|unclear|don't understand|what do you mean|lost|hard to follow", re.I)),
    ("request", re.compile(r"please|can you make|next video|would like|suggestion|request", re.I)),
    ("spam/noise", re.compile(r"subscribe|follow me|check out|http|www\.|click here|free", re.I)),
]

# Metric map from experiment_metric_suggest.py (subset for candidate changes)
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

def suggest_hypotheses(counts: dict[str, int]) -> list[str]:
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

def extract_candidate_changes(hyps: list[str]) -> list[str]:
    """Pull mentioned allowed changes from hypothesis text. Signals only."""
    found = set()
    for h in hyps:
        low = h.lower()
        for ch in ALLOWED_CHANGES:
            if ch.replace("_", " ") in low or ch in low:
                found.add(ch)
    return sorted(found) if found else ["mechanism_framing"]

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Single review brief from collected feedback comments. No invent."
    )
    parser.add_argument("packet", help="Packet folder containing feedback_state.json")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    state_path = path / "feedback_state.json"

    print("FEEDBACK REVIEW BRIEF (signals only; from collected comments)")
    print(f"packet: {path.name}")
    print(f"allowed_changes: {', '.join(ALLOWED_CHANGES)}")

    if not state_path.is_file():
        print("feedback_state.json: ABSENT")
        print("HOLD: collect feedback first (after observation window).")
        print("See tools/post_publish_sequence.py")
        print("FEEDBACK REVIEW BRIEF HOLD (no feedback state)")
        return 0

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"feedback_state.json: INVALID ({e})")
        print("FEEDBACK REVIEW BRIEF FAIL")
        return 1

    if state.get("gate") != "COLLECTED" or not state.get("attempted_fetch"):
        print("feedback_state.json: not a collected fetch")
        print("HOLD: only real collected comments generate review signals. Do not invent.")
        print("FEEDBACK REVIEW BRIEF HOLD (not collected)")
        return 0

    comments = state.get("comments") or []
    if not isinstance(comments, list) or not comments:
        print("No comments in collected state.")
        print("FEEDBACK REVIEW BRIEF HOLD (empty comments)")
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
    print("## Hypothesis candidates (review before recording)")
    for h in hyps:
        print(f"- {h}")
    print()

    candidates = extract_candidate_changes(hyps)
    print("## Metric suggestions for candidate changes")
    for ch in candidates:
        metrics = METRIC_MAP.get(ch, METRIC_MAP["mechanism_framing"])
        print(f"- {ch}: {', '.join(metrics)}")
    print()
    print("Choose one change + one primary_metric, then document a real numeric baseline + source.")
    print("Next: python3 tools/experiment_baseline_starter.py", path)
    print("Then: python3 tools/experiment_template_validator.py", path / "experiment_baseline.json")
    print("Do not invent metrics or decisions. See docs/feedback_loop.md and docs/experiments.md.")
    print("FEEDBACK REVIEW BRIEF PASS (signals only)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
