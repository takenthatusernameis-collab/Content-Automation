#!/usr/bin/env python3
"""Check whether the packet mechanism from idea.md appears in spoken WORDS.

Extracts significant terms from the mechanism line and reports which ones
appear in the WORDS of draft.md or script.md. Uses shared phrase_utils.spoken_words (includes normalize). Helps keep scripts grounded
in the operational default rather than drifting into generic advice.
Does not rewrite files. Default exit 0; --strict exits 1 if key terms missing.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract as idea_extract  # noqa: E402
from phrase_utils import spoken_words as shared_spoken_words  # noqa: E402
STOP = {
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "so", "that",
    "this", "it", "is", "as", "with", "by", "from", "on", "at", "be", "are",
    "was", "were", "will", "can", "not", "but", "if", "when", "then", "than",
    "into", "over", "after", "before", "does", "do", "did", "have", "has",
    "had", "their", "they", "them", "its", "his", "her", "our", "your",
}

def extract_mechanism(text: str) -> str:
    mech, _problem, _topic = idea_extract(text)
    return mech

def significant_terms(mech: str) -> list[str]:
    words = re.findall(r"[a-zA-Z]{4,}", mech.lower())
    return [w for w in words if w not in STOP]

def spoken_words(path: Path) -> str:
    for name in ("script.md", "draft.md"):
        f = path / name
        if f.is_file():
            text = f.read_text(encoding="utf-8")
            return shared_spoken_words(text).lower()
    return ""

def main() -> int:
    parser = argparse.ArgumentParser(description="Scan for mechanism term alignment in WORDS.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any significant term is missing.")
    args = parser.parse_args()
    packet = Path(args.packet)
    idea = packet / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {packet}")
        return 1
    mech = extract_mechanism(idea.read_text(encoding="utf-8"))
    terms = significant_terms(mech)
    body = spoken_words(packet)
    print("MECHANISM ALIGN SCAN (presence of idea.md mechanism terms in WORDS)")
    print(f"mechanism: {mech or '(none)'}")
    if not terms:
        print("No significant terms extracted.")
        return 0
    present = []
    missing = []
    for t in terms:
        if t in body:
            present.append(t)
        else:
            missing.append(t)
    print(f"terms_checked: {len(terms)}")
    print(f"present: {', '.join(present) or 'none'}")
    print(f"missing: {', '.join(missing) or 'none'}")
    if missing:
        print("revision_signal: consider weaving the missing mechanism terms into spoken WORDS")
    else:
        print("status: aligned")
    if args.strict and missing:
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
