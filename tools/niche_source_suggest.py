#!/usr/bin/env python3
"""Niche source suggester for research starters.

Prints a short, curated list of common, high-quality, publicly available sources
relevant to the channel niche (systems for focused work / process design).
These are starting points only; the human or agent must verify relevance and
extract only supported claims for a specific packet's research.md.
Does not invent packet-specific citations, numbers, or URLs that are not well-known.
Does not write files. Does not call APIs.
Reduces blank-page research friction for every future packet in this niche.
"""

from __future__ import annotations

import sys

SOURCES = [
    {
        "title": "Getting Things Done (David Allen)",
        "type": "book",
        "covers": "next-action systems, capture, clarify, organize, reflect, engage",
        "note": "Classic implementation-intention style workflow; widely available summaries exist.",
    },
    {
        "title": "Atomic Habits (James Clear)",
        "type": "book",
        "covers": "cue-craving-response-reward loops, environment design, identity",
        "note": "Practical habit installation; pair with specific packet mechanism.",
    },
    {
        "title": "Deep Work (Cal Newport)",
        "type": "book",
        "covers": "scheduled focus blocks, attention residue, shutdown rituals",
        "note": "Useful for stall-at-start and context-switch costs.",
    },
    {
        "title": "The Power of Full Engagement (Loehr & Schwartz)",
        "type": "book",
        "covers": "energy management over time management, recovery cycles",
        "note": "Relevant when the stall is depletion rather than list reopening.",
    },
    {
        "title": "Implementation intentions research (Gollwitzer et al.)",
        "type": "academic",
        "covers": "if-then plans that link cues to actions",
        "note": "Search for primary papers on 'implementation intentions'; do not invent effect sizes.",
    },
    {
        "title": "Attention residue (Leroy 2009)",
        "type": "academic",
        "covers": "cognitive cost of unfinished tasks and task switching",
        "note": "Supports arguments about closing open loops before starting.",
    },
    {
        "title": "Public-domain / open summaries",
        "type": "web",
        "covers": "Wikipedia pages, author blogs, or free chapters for the above",
        "note": "Prefer primary or author-controlled sources when possible; cite what you actually read.",
    },
]


def main() -> int:
    print("NICHE SOURCE SUGGESTER (systems for focused work)")
    print("These are common starting points only. Verify each source and extract only claims")
    print("that actually appear in it before placing anything in research.md or sources.md.")
    print("Do not invent numbers, study details, or URLs.")
    print("=" * 72)
    print()
    print("| Title | Type | Covers | Note |")
    print("|-------|------|--------|------|")
    for s in SOURCES:
        print(f"| {s['title']} | {s['type']} | {s['covers']} | {s['note']} |")
    print()
    print("=" * 72)
    print(f"Suggested sources: {len(SOURCES)}")
    print("Next: pick 1-3 relevant ones, read or summarize them, then fill the")
    print("Source column in a claim-to-source table or research.md skeleton.")
    print("Tools: python3 tools/claim_source_table.py PATH  or  research_package_starter.py PATH")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
