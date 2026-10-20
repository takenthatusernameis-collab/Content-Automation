#!/usr/bin/env python3
"""Suggest additional operational topics for the queue grounded in channel.md.

Prints candidate rows in markdown table format that can be pasted into
docs/topic_queue.md. Does not invent sources, numbers, or specific claims.
Does not write the queue file. Does not scaffold packets. Does not poll secrets.
Useful for expanding the idea inventory while the publish path is blocked.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANNEL = ROOT / "docs" / "channel.md"
QUEUE = ROOT / "docs" / "topic_queue.md"


def extract_niche_promise(channel_text: str) -> tuple[str, str]:
    niche = "systems for focused work"
    promise = "install one small default the same day"
    lines = channel_text.splitlines()
    for i, line in enumerate(lines):
        low = line.lower().strip()
        if low.startswith("## niche") and i + 1 < len(lines):
            niche = lines[i + 1].strip()
        if low.startswith("## promise") and i + 1 < len(lines):
            promise = lines[i + 1].strip()
    return niche, promise


def existing_titles(queue_text: str) -> set[str]:
    titles = set()
    for line in queue_text.splitlines():
        if line.startswith("| Q") and "|" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) > 3:
                titles.add(parts[3].lower())
    return titles


def suggestions(niche: str, promise: str, existing: set[str]) -> list[tuple[str, str, str]]:
    """Return (working_title, one_line, problem) tuples that fit the niche."""
    candidates = [
        (
            "Put the timer on the task file itself",
            "Attach the start timer to the file or note that holds the work so opening the work starts the clock.",
            "the timer lives in a separate app, so starting the work means switching away first",
        ),
        (
            "One visible next verb",
            "Write the single next verb on the edge of the open file so the stall has a concrete target.",
            "the next action is still in the head, so the morning reopens the choice",
        ),
        (
            "Close the review tab before the work tab",
            "A shutdown order that removes the review surface before the work surface is available.",
            "the review tab is still open, so the work session begins with checking",
        ),
        (
            "Put the constraint in the filename",
            "Encode the constraint in the filename of the working file so the stall sees it on open.",
            "the constraint is in a separate note, so the open file has nothing to hit",
        ),
        (
            "One list for the first two minutes",
            "A short list that only contains the first two minutes of the planned task.",
            "the full list is visible, so the first action is still a choice among many",
        ),
        (
            "Name the stall surface",
            "Identify the exact surface (tab, app, desk edge) where the delay happens and put the cue there.",
            "the stall surface is unnamed, so the default has no place to live",
        ),
        (
            "The cue is the open file",
            "Make the open working file itself the cue that the first two minutes have begun.",
            "the cue is elsewhere, so opening the file does not start the work",
        ),
        (
            "Remove the second list before the first",
            "A close-default that eliminates the competing list before the primary list is used.",
            "two lists are open, so neither has a clear next action",
        ),
    ]
    out = []
    for title, one, prob in candidates:
        if title.lower() not in existing:
            out.append((title, one, prob))
        if len(out) >= 6:
            break
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print candidate topic rows for docs/topic_queue.md. No writes. No invented claims."
    )
    parser.add_argument("--count", type=int, default=6, help="Max suggestions (default 6)")
    args = parser.parse_args()

    if not CHANNEL.is_file():
        print(f"Missing channel: {CHANNEL}", file=sys.stderr)
        return 1
    channel_text = CHANNEL.read_text(encoding="utf-8")
    niche, promise = extract_niche_promise(channel_text)

    existing: set[str] = set()
    if QUEUE.is_file():
        existing = existing_titles(QUEUE.read_text(encoding="utf-8"))

    rows = suggestions(niche, promise, existing)[: args.count]

    print("TOPIC SUGGEST (operational defaults only; no invented sources or numbers)")
    print(f"Niche: {niche}")
    print(f"Promise: {promise}")
    print(f"Existing titles skipped: {len(existing)}")
    print()
    print("Candidate rows (paste into docs/topic_queue.md; next id after highest QN):")
    print("| id | status | working_title | one_line | problem |")
    print("|----|--------|---------------|----------|---------|")
    for i, (title, one, prob) in enumerate(rows, start=6):
        print(f"| Q{i} | queued | {title} | {one} | {prob} |")
    print()
    print("These are suggestions only. Review, edit, and mark status before use.")
    print("Do not scaffold until Q1 ships. Do not invent a packet from this output.")
    print("After adding, run: python3 tools/next_topic.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
