#!/usr/bin/env python3
"""Report spoken word progress against targets in draft.md.

Parses draft.md (or falls back to script.md) for ## sections, extracts WORDS:
blocks, counts spoken words, and compares to packet targets (Hook short,
body beats 140-220, total 900-1500). Prints a concise progress table so
agents know exactly which beats still need expansion or are over target.
Does not invent content, rewrite files, or call APIs.
Complements draft_md_starter.py and draft_beat_expansion_starter.py by
giving precise feedback during the expansion step, reducing free-form
padding and slop risk for every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WORD_RE = re.compile(r"WORDS:\s*(.*?)(?:\nVISUAL:|\n## |\Z)", re.S | re.I)
SECTION_RE = re.compile(r"^##\s+(.+?)$", re.M)

TARGETS = {
    "hook": (20, 45),
    "payoff": (40, 90),
    "beat": (140, 220),
    "cta": (40, 90),
    "total": (900, 1500),
}


def count_words(text: str) -> int:
    """Simple spoken-word count (split on whitespace; ignores pure punctuation)."""
    cleaned = re.sub(r"[^\w\s'-]", " ", text)
    return len([w for w in cleaned.split() if w.strip()])


def classify(heading: str) -> str:
    h = heading.lower()
    if "hook" in h:
        return "hook"
    if "payoff" in h:
        return "payoff"
    if "cta" in h or "end" in h:
        return "cta"
    if "beat" in h:
        return "beat"
    return "other"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report draft.md spoken word counts vs targets. No invented content."
    )
    parser.add_argument("packet", help="Packet folder containing draft.md")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    draft = path / "draft.md"
    source = draft if draft.is_file() else path / "script.md"
    if not source.is_file():
        print(f"No draft.md or script.md in {args.packet}", file=sys.stderr)
        return 1

    text = source.read_text(encoding="utf-8").replace("\r\n", "\n")
    sections = SECTION_RE.findall(text)
    words_blocks = WORD_RE.findall(text)

    print("DRAFT WORD PROGRESS (spoken words vs targets; expand or trim as needed)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print()

    total = 0
    rows = []
    # Pair headings with following WORDS blocks approximately
    # (robust enough for the starter format)
    block_idx = 0
    for heading in sections:
        kind = classify(heading)
        count = 0
        if block_idx < len(words_blocks):
            count = count_words(words_blocks[block_idx])
            block_idx += 1
        total += count
        lo, hi = TARGETS.get(kind, (0, 9999))
        if kind == "other":
            status = "OK"
            target_str = "-"
        elif count < lo:
            status = "SHORT"
            target_str = f"{lo}-{hi}"
        elif count > hi:
            status = "LONG"
            target_str = f"{lo}-{hi}"
        else:
            status = "OK"
            target_str = f"{lo}-{hi}"
        rows.append((heading.strip(), count, target_str, status))

    print(f"{'Section':<40} {'Words':>6} {'Target':>10} {'Status':>8}")
    print("-" * 70)
    for heading, count, target_str, status in rows:
        short_h = (heading[:37] + "...") if len(heading) > 40 else heading
        print(f"{short_h:<40} {count:>6} {target_str:>10} {status:>8}")

    lo, hi = TARGETS["total"]
    total_status = "SHORT" if total < lo else ("LONG" if total > hi else "OK")
    print("-" * 70)
    print(f"{'TOTAL':<40} {total:>6} {lo}-{hi:>6} {total_status:>8}")
    print()
    print("Next (do not invent sources, numbers, or anecdotes):")
    print("- Expand SHORT body beats using the checklist from draft_beat_expansion_starter.py.")
    print("- Trim LONG sections; prefer cutting filler over adding more.")
    print("- Aim for total 900-1500 spoken words (~1200).")
    print("- Run python3 tools/quality_scan.py and python3 tools/claim_scan.py before apply_script.py --write.")
    print("This tool writes nothing. Preferred unblocked path remains human OAuth for publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
