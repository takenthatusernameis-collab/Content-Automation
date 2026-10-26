#!/usr/bin/env python3
"""Print structured objection / clarification candidates from script spoken WORDS.

Extracts sentences that may surface viewer objections, stalls, or "what if" points
(preferring failure-mode language or middle beats) and prints a Markdown candidates
section mapping each signal to a suggested short clarification or reply phrase
(via shared shorten, capped ~80 chars) with weak-pattern flags and blank final_choice slots.
Reduces recurring labor of manually scanning for objection points and drafting
handling text for first comments, descriptions, or script clarifications on every
future packet while the stall continues.
Does not invent content, write files, poll secrets, or call external services.
Exit 0 always (informational).
Useful before publish-stage drafting or first-comment planning to reduce blank-page
objection handling on every packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import spoken_words, normalize, shorten  # type: ignore

# Patterns that often signal a potential objection or stall the viewer might raise.
OBJECTION_HINTS = (
    "but what if",
    "what if",
    "however",
    "the problem is",
    "you might think",
    "it might seem",
    "common mistake",
    "failure mode",
    "when this fails",
    "if you skip",
)

HINT_RE = re.compile(
    r"\b(" + "|".join(re.escape(p) for p in OBJECTION_HINTS) + r")\b",
    re.IGNORECASE,
)

WEAK_PATTERNS = (
    "just do it",
    "it's easy",
    "simply",
    "obviously",
    "everyone knows",
)

WEAK_RE = re.compile(
    r"\b(" + "|".join(re.escape(p) for p in WEAK_PATTERNS) + r")\b",
    re.IGNORECASE,
)


def extract_objection_signals(text: str) -> list[str]:
    """Return list of candidate sentences that may contain objection or stall signals."""
    text = normalize(text)
    spoken = spoken_words(text)
    if not spoken:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", spoken.strip())
    signals = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if HINT_RE.search(s) or any(w in s.lower() for w in ("fail", "problem", "skip", "miss", "wrong")):
            signals.append(s)
        if len(signals) >= 5:
            break
    # Fallback: a few middle sentences if nothing matched
    if not signals and len(sentences) > 3:
        signals = [sentences[i].strip() for i in range(1, min(4, len(sentences))) if sentences[i].strip()]
    return signals[:4]


def flag_weak(phrase: str) -> str:
    if WEAK_RE.search(phrase):
        return " [WEAK_CLARIFICATION]"
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print script objection / clarification candidates. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("SCRIPT OBJECTION / CLARIFICATION CANDIDATES (informational only; no writes)")
    print(f"Packet: {path.name}")
    print("Prefer concrete mechanism-based clarifications over generic reassurance. final_choice slots are blank for human selection.")
    print()

    script_path = path / "script.md"
    draft_path = path / "draft.md"
    chosen = script_path if script_path.is_file() else draft_path
    if not chosen.is_file():
        print("No script.md or draft.md found.")
        print("This tool writes nothing.")
        return 0

    text = chosen.read_text(encoding="utf-8")
    signals = extract_objection_signals(text)

    if not signals:
        print("No spoken WORDS found for objection extraction.")
        print("This tool writes nothing.")
        return 0

    print("### Candidates (from potential stall / objection signals)")
    for i, signal in enumerate(signals, 1):
        short = shorten(signal, max_len=80)
        weak = flag_weak(short)
        print(f"{i}. Signal: {signal[:140]}{'...' if len(signal) > 140 else ''}")
        print(f"   Suggested clarification: {short}{weak}")
        print(f"   final_choice: ")
        print()

    print("### Reminder")
    print("- Strong clarifications name the concrete mechanism or the exact next action.")
    print("- Avoid generic 'just do it' or 'it's easy' responses.")
    print("- These are starters only; rewrite for voice and specificity.")
    print("- Do not invent content or commit secrets.")
    print()
    print("This brief does not invent content or write files.")
    print("Useful before first-comment, description, or mid-script clarification drafting on every packet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
