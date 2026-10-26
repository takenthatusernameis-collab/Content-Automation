#!/usr/bin/env python3
"""Print structured mechanism / installable-default candidates from script spoken WORDS.

Extracts sentences that name a concrete system, cue, constraint, or next action
(preferring CTA or later beats) and prints a Markdown candidates section mapping
each signal to a suggested short installable default phrase (via shared shorten,
capped ~70 chars) with weak-pattern flags and blank final_choice slots.
Reduces recurring labor of manually scanning for the channel promise (one small
default the viewer can install the same day) and drafting specific operational
language for every future packet while the stall continues.
Does not invent content, write files, poll secrets, or call external services.
Exit 0 always (informational).
Useful before publish-stage drafting, CTA refinement, or description planning
to reduce blank-page mechanism extraction on every packet.
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

# Patterns that often signal a concrete mechanism or installable default.
MECHANISM_HINTS = (
    "default",
    "cue",
    "constraint",
    "checklist",
    "next action",
    "start cue",
    "install",
    "put the",
    "keep the",
    "close the",
    "name one",
)

HINT_RE = re.compile(
    r"\b(" + "|".join(re.escape(p) for p in MECHANISM_HINTS) + r")\b",
    re.IGNORECASE,
)

WEAK_PATTERNS = (
    "just start",
    "be motivated",
    "find your why",
    "you got this",
    "stay consistent",
)

WEAK_RE = re.compile(
    r"\b(" + "|".join(re.escape(p) for p in WEAK_PATTERNS) + r")\b",
    re.IGNORECASE,
)


def extract_mechanism_signals(text: str) -> list[str]:
    """Return list of candidate sentences that may name an installable default."""
    text = normalize(text)
    spoken = spoken_words(text)
    if not spoken:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", spoken.strip())
    signals = []
    # Prefer later sentences (CTA / payoff area)
    candidates = sentences[-6:] if len(sentences) > 6 else sentences
    for s in candidates:
        s = s.strip()
        if not s:
            continue
        if HINT_RE.search(s) or any(w in s.lower() for w in ("default", "cue", "constraint", "checklist", "start")):
            signals.append(s)
        if len(signals) >= 4:
            break
    # Fallback: last few sentences if nothing matched
    if not signals and sentences:
        signals = [s.strip() for s in sentences[-3:] if s.strip()]
    return signals[:3]


def flag_weak(phrase: str) -> str:
    if WEAK_RE.search(phrase):
        return " [WEAK_MECHANISM]"
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print script mechanism / installable-default candidates. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("SCRIPT MECHANISM / INSTALLABLE-DEFAULT CANDIDATES (informational only; no writes)")
    print(f"Packet: {path.name}")
    print("Prefer concrete, same-day installable defaults over motivation. final_choice slots are blank for human selection.")
    print("Channel promise: after the video the viewer can install one small default.")
    print()

    script_path = path / "script.md"
    draft_path = path / "draft.md"
    chosen = script_path if script_path.is_file() else draft_path
    if not chosen.is_file():
        print("No script.md or draft.md found.")
        print("This tool writes nothing.")
        return 0

    text = chosen.read_text(encoding="utf-8")
    signals = extract_mechanism_signals(text)

    if not signals:
        print("No spoken WORDS found for mechanism extraction.")
        print("This tool writes nothing.")
        return 0

    print("### Candidates (from potential mechanism / default signals)")
    for i, signal in enumerate(signals, 1):
        short = shorten(signal, max_len=70)
        weak = flag_weak(short)
        print(f"{i}. Signal: {signal[:140]}{'...' if len(signal) > 140 else ''}")
        print(f"   Suggested installable default: {short}{weak}")
        print(f"   final_choice: ")
        print()

    print("### Reminder")
    print("- Strong defaults name a concrete cue, constraint, or checklist the viewer can place today.")
    print("- Avoid generic motivation language.")
    print("- These are starters only; rewrite for voice and specificity.")
    print("- Do not invent content or commit secrets.")
    print()
    print("This brief does not invent content or write files.")
    print("Useful before CTA, description, or end-screen drafting on every packet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
