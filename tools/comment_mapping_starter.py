#!/usr/bin/env python3
"""Print a structured comment-mapping skeleton for post-observation analysis.

Extracts potential viewer questions/objections from spoken WORDS (same logic as
viewer_questions_extract) and emits a ready-to-copy Markdown section that maps
real comments to those baselines plus free-form classification counts.
Reduces recurring labor of manually setting up the classification and mapping
structure after the observation window on every future packet. Does not invent
comments, metrics, or sources; does not write files, poll secrets, or call
external services. Exit 0 always; informational only.
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
        description="Print a comment mapping starter for feedback analysis. No file writes."
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

    print("COMMENT MAPPING STARTER (informational only; no writes)")
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
            questions = [s for s in sents if is_potential_question(s)][:6]

    print("Suggested comment mapping section (copy into feedback.md after real comments exist; fill only with observed data):")
    print("---")
    print("## Comment mapping (baseline from script; do not invent matches)")
    print()
    print("### Anticipated questions / objections")
    if questions:
        for i, q in enumerate(questions, 1):
            preview = q[:100].replace("\n", " ")
            if len(q) > 100:
                preview += "..."
            print(f"{i}. {preview}")
            print("   - matching_comments: (paste short quotes or count; leave blank if none)")
            print("   - classification: question / objection / confusion / request / other")
            print("   - strength: repeated / single / none")
    else:
        print("(none extracted; add manually if useful)")
    print()
    print("### Free classification counts (from real comments only)")
    print("- question: ")
    print("- objection: ")
    print("- praise: ")
    print("- confusion: ")
    print("- request: ")
    print("- spam/noise: ")
    print()
    print("### Signal hierarchy reminder (from docs/feedback_loop.md)")
    print("1. Repeated specific questions or confusion (highest signal)")
    print("2. Consistent retention patterns across comparable videos")
    print("3. Repeated comments that map to a concrete content choice")
    print("4. One-off comments")
    print("5. Raw vanity counts without context")
    print()
    print("### One diagnosis note (interpretation only after mapping)")
    print("- observed pattern: ")
    print("- possible content mechanism: ")
    print("- next test idea (do not decide keep/discard here): ")
    print("---")
    print()
    print("This skeleton does not invent comments, counts, or decisions.")
    print("Fill only after a real provider_video_id, uploaded_at, and observation window exist.")
    print("Use with tools/viewer_questions_extract.py and tools/feedback_review_starter.py.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
