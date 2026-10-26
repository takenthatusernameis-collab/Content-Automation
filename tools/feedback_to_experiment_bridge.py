#!/usr/bin/env python3
"""Print a bridge skeleton from anticipated viewer questions to possible experiments.

Extracts potential questions/objections from spoken WORDS and emits a structured
Markdown section that maps each baseline question to blank slots for a possible
content change, hypothesized effect, and metric. Prepares the improvement loop
so later real-comment analysis can be turned into explicit tests without starting
from a blank page. Does not invent questions, changes, metrics, or decisions.
Does not write files, poll secrets, or call external services. Exit 0 always.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import spoken_words, normalize  # type: ignore


def sentences(text: str) -> list[str]:
    text = normalize(text)
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 15]


def is_potential_question(sent: str) -> bool:
    low = sent.lower()
    if "?" in sent:
        return True
    starters = (
        "why ",
        "how ",
        "what if",
        "what about",
        "but ",
        "however ",
        "the problem is",
        "the issue is",
        "people might",
        "viewers might",
        "you might think",
        "common objection",
        "some will say",
    )
    return any(low.startswith(s) or f" {s}" in low for s in starters)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a questions-to-experiment bridge skeleton. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    parser.add_argument(
        "--prefer",
        choices=("script", "draft", "auto"),
        default="auto",
        help="Which file to prefer for spoken WORDS (default: auto)",
    )
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("FEEDBACK-TO-EXPERIMENT BRIDGE (informational only; no writes)")
    print(f"Packet: {path.name}")
    print()

    script_path = path / "script.md"
    draft_path = path / "draft.md"
    chosen = None
    if args.prefer == "script" and script_path.is_file():
        chosen = script_path
    elif args.prefer == "draft" and draft_path.is_file():
        chosen = draft_path
    else:
        if script_path.is_file():
            chosen = script_path
        elif draft_path.is_file():
            chosen = draft_path

    questions: list[str] = []
    if chosen:
        text = chosen.read_text(encoding="utf-8")
        spoken = spoken_words(text)
        if spoken.strip():
            sents = sentences(spoken)
            questions = [s for s in sents if is_potential_question(s)][:5]

    print("Suggested bridge section (copy into experiments.md or feedback.md after real comments exist; fill only with observed data):")
    print("---")
    print("## Questions-to-experiment bridge (baseline only; do not invent matches or results)")
    print()
    if questions:
        for i, q in enumerate(questions, 1):
            preview = q[:90].replace("\n", " ")
            if len(q) > 90:
                preview += "..."
            print(f"{i}. Anticipated: {preview}")
            print("   - real_comment_match: (paste quote or count after window; leave blank if none)")
            print("   - possible_change: (one material variable: hook / mechanism_framing / example_density / title_promise / visual_explanation / pacing / cta / topic_selection)")
            print("   - hypothesized_effect: (qualitative only until baseline exists)")
            print("   - target_metric: (predeclare; do not invent numbers)")
            print("   - next_test_idea: (one sentence; do not decide keep/discard here)")
            print()
    else:
        print("(none extracted; add manually if useful after real comments arrive)")
        print()
    print("### Reminder")
    print("- Prefer one change per experiment.")
    print("- Record observation separately from interpretation.")
    print("- Use tools/experiment_hypothesis_suggest.py after choosing a change.")
    print("- Do not invent metrics, baselines, or decisions.")
    print("---")
    print()
    print("This skeleton does not invent comments, changes, or results.")
    print("Fill only after a real provider_video_id, uploaded_at, and observation window exist.")
    print("Complements tools/viewer_questions_extract.py, tools/feedback_review_starter.py, and tools/comment_mapping_starter.py.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
