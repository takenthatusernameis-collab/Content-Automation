#!/usr/bin/env python3
"""Print a structured feedback.md starter template for a packet.

Extracts potential viewer questions/objections from spoken WORDS (same logic as
viewer_questions_extract) and emits a ready-to-copy Markdown skeleton with
sections for mapping real comments to those baselines, plus slots for analytics
metrics, classification counts, and one diagnosis note. Reduces recurring labor
of manually setting up the feedback record structure after the observation window
on every future packet. Does not invent comments, metrics, or sources; does not
write files, poll secrets, or call external services. Exit 0 always; informational only.
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
        description="Print a feedback review starter template. No file writes."
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

    print("FEEDBACK REVIEW STARTER (informational only; no writes)")
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
            questions = [s for s in sents if is_potential_question(s)][:8]

    print("Suggested feedback.md skeleton (copy into the packet after observation window; fill with real data only):")
    print("---")
    print(f"# Feedback — {path.name}")
    print()
    print("## Observation window")
    print("- video_id: (from provider after upload)")
    print("- uploaded_at: (ISO timestamp)")
    print("- window_start: (uploaded_at date)")
    print("- window_end: (uploaded_at + 10 days = 7 calendar + 3 Analytics lag)")
    print("- retrieved_at: (when metrics/comments were fetched)")
    print()
    print("## Analytics (do not invent)")
    print("- views: ")
    print("- average_view_duration_percent: ")
    print("- estimated_minutes_watched: ")
    print("- likes: ")
    print("- (other primary metric from experiment plan)")
    print()
    print("## Anticipated questions / objections (from script; baseline only)")
    if questions:
        for i, q in enumerate(questions, 1):
            preview = q[:120].replace("\n", " ")
            if len(q) > 120:
                preview += "..."
            print(f"{i}. {preview}")
            print("   - real_comments_matching: (paste or count)")
            print("   - classification: question / objection / confusion / request / other")
            print("   - notes: ")
    else:
        print("(none extracted; add manually if useful)")
    print()
    print("## Other comment samples")
    print("- classification counts: question=, objection=, praise=, confusion=, request=, spam=")
    print("- representative quotes (max 5):")
    print("  - ")
    print()
    print("## Diagnosis (one plausible mechanism)")
    print("- observed pattern: ")
    print("- possible content cause: ")
    print("- not a decision yet; see experiment_loop.py")
    print()
    print("## Links")
    print("- feedback_state.json: (path or artifact)")
    print("- experiment id: ")
    print("---")
    print()
    print("This template does not invent comments, metrics, or keep/discard decisions.")
    print("Fill only after a real provider_video_id, uploaded_at, and observation window exist.")
    print("Use with tools/viewer_questions_extract.py and tools/experiment_prep.py.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
