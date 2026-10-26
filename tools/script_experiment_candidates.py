#!/usr/bin/env python3
"""Print potential single-variable experiment candidates extracted from the script.

Extracts anticipated questions/objections and long sentences (retention risks) from spoken WORDS.
Maps each to a suggested ALLOWED_CHANGES type with blank slots for hypothesis, metric, and notes.
Prepares the next-video experiment selection so agents or humans start from concrete script-derived candidates
instead of a blank page. Does not invent hypotheses, metrics, baselines, or decisions.
Does not write files, poll secrets, or call external services. Exit 0 always.
Complements feedback_to_experiment_bridge.py (post-comment) and experiment_hypothesis_suggest.py.
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
from experiment_loop import ALLOWED_CHANGES  # type: ignore


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


def word_count(sent: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", sent))


def suggest_change_for_question(q: str) -> str:
    low = q.lower()
    if any(w in low for w in ("how", "why", "what")):
        return "mechanism_framing"
    if "example" in low or "for instance" in low:
        return "example_density"
    return "hook"


def suggest_change_for_long(sent: str) -> str:
    return "pacing"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print script-derived experiment candidate skeletons. No file writes."
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

    print("SCRIPT-TO-EXPERIMENT CANDIDATES (informational only; no writes)")
    print(f"Packet: {path.name}")
    print(f"Allowed changes: {', '.join(ALLOWED_CHANGES)}")
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

    candidates: list[tuple[str, str, str]] = []  # (kind, preview, suggested_change)
    if chosen:
        text = chosen.read_text(encoding="utf-8")
        spoken = spoken_words(text)
        if spoken.strip():
            sents = sentences(spoken)
            questions = [s for s in sents if is_potential_question(s)][:3]
            longs = [s for s in sents if word_count(s) > 30][:2]
            for q in questions:
                preview = q[:80].replace("\n", " ")
                if len(q) > 80:
                    preview += "..."
                candidates.append(("question", preview, suggest_change_for_question(q)))
            for L in longs:
                preview = L[:80].replace("\n", " ")
                if len(L) > 80:
                    preview += "..."
                candidates.append(("long_sentence", preview, suggest_change_for_long(L)))

    print("Suggested candidates section (copy into experiments.md or idea.md for the next packet; fill only with observed or deliberate data):")
    print("---")
    print("## Script-derived experiment candidates (baseline only; one variable each; do not invent results)")
    print()
    if candidates:
        for i, (kind, preview, change) in enumerate(candidates, 1):
            print(f"{i}. Kind: {kind}")
            print(f"   Signal: {preview}")
            print(f"   Suggested change: {change}")
            print("   - hypothesis: (one sentence naming the mechanism and predicted effect; edit if needed)")
            print("   - primary_metric: (predeclare one Analytics field; do not invent numbers)")
            print("   - notes: (why this signal might matter; leave blank until real evidence)")
            print()
    else:
        print("(none extracted; add manually from script review if useful)")
        print()
    print("### Reminder")
    print("- Prefer one change per experiment.")
    print("- These are candidates only; confirm against real feedback later.")
    print("- Use tools/experiment_hypothesis_suggest.py after choosing one.")
    print("- Do not invent metrics, baselines, or decisions.")
    print("---")
    print()
    print("This skeleton does not invent comments, changes, or results.")
    print("Useful before or after the observation window to reduce blank-page selection of the next single variable.")
    print("Complements tools/feedback_to_experiment_bridge.py, tools/cadence_repetition_scan.py, and tools/experiment_package_starter.py.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
