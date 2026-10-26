#!/usr/bin/env python3
"""Print structured hook candidates from the opening of script spoken WORDS.

Extracts the first beat or early sentences (preferring a ## Hook section) and
prints a Markdown candidates section mapping each signal to a suggested short
high-retention hook phrase (via shared shorten, capped ~60 chars for spoken
openers) with weak-pattern flags and blank final_choice slots.
Reduces recurring labor of manually drafting strong opening hooks from the
script for every future packet while the stall continues.
Does not invent content, write files, poll secrets, or call external services.
Exit 0 always (informational).
Useful before script promotion or titles/thumbnail planning to reduce blank-page
hook drafting on every packet.
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

# Weak opener patterns (subset; expand later if needed). Prefer concrete mechanism over generic.
HOOK_WEAK_PATTERNS = (
    "in this video",
    "today we",
    "let's talk about",
    "have you ever",
    "did you know",
    "welcome back",
    "hey guys",
    "what's up",
)

WEAK_RE = re.compile(
    r"\b(" + "|".join(re.escape(p) for p in HOOK_WEAK_PATTERNS) + r")\b",
    re.IGNORECASE,
)


def extract_opening(text: str) -> list[str]:
    """Return list of candidate opening sentences or first-beat spoken text."""
    text = normalize(text)
    # Prefer ## Hook section
    hook_m = re.search(r"##\s*Hook[^\n]*\n(.*?)(?=\n##|\Z)", text, re.S | re.I)
    if hook_m:
        body = hook_m.group(1)
        spoken = spoken_words("WORDS: " + body)
    else:
        # Fallback: first WORDS block or first 150 words
        spoken = spoken_words(text)
        if not spoken:
            return []

    sentences = re.split(r"(?<=[.!?])\s+", spoken.strip())
    # Take first 3 non-empty sentences as signals
    candidates = [s.strip() for s in sentences if s.strip()][:3]
    if not candidates and spoken:
        candidates = [spoken[:200]]
    return candidates


def flag_weak(phrase: str) -> str:
    if WEAK_RE.search(phrase):
        return " [WEAK_OPENER]"
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print script hook candidates. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("SCRIPT HOOK CANDIDATES (informational only; no writes)")
    print(f"Packet: {path.name}")
    print("Prefer early concrete mechanism over generic openers. final_choice slots are blank for human selection.")
    print()

    script_path = path / "script.md"
    draft_path = path / "draft.md"
    chosen = script_path if script_path.is_file() else draft_path
    if not chosen.is_file():
        print("No script.md or draft.md found.")
        print("This tool writes nothing.")
        return 0

    text = chosen.read_text(encoding="utf-8")
    openings = extract_opening(text)

    if not openings:
        print("No spoken WORDS found for hook extraction.")
        print("This tool writes nothing.")
        return 0

    print("### Candidates (from opening spoken text)")
    for i, signal in enumerate(openings, 1):
        short = shorten(signal, max_len=60)
        weak = flag_weak(short)
        print(f"{i}. Signal: {signal[:120]}{'...' if len(signal) > 120 else ''}")
        print(f"   Suggested hook: {short}{weak}")
        print(f"   final_choice: ")
        print()

    print("### Reminder")
    print("- Strong hooks name the concrete stall or mechanism in the first 5-12 seconds.")
    print("- Avoid generic 'in this video' or 'have you ever' openers.")
    print("- These are starters only; rewrite for voice and specificity.")
    print("- Do not invent content or commit secrets.")
    print()
    print("This brief does not invent content or write files.")
    print("Useful before titles, thumbnails, or promotion to reduce blank-page hook drafting on every packet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
