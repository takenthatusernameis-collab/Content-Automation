#!/usr/bin/env python3
"""Suggest additional operational topics for the queue grounded in channel.md.

Prints candidate rows in markdown table format that can be pasted into
docs/topic_queue.md. Does not invent sources, numbers, or specific claims.
Does not write the queue file. Does not scaffold packets. Does not poll secrets.
Useful for expanding the idea inventory while the publish path is blocked.

Candidates load from tools/topic_candidates.json so future expansions are data-only
(no Python edits). Idea skeletons for the top candidates are emitted via
idea_brief.paste_block so the format matches apply_idea / idea_brief --queue exactly.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from queue_lib import parse_queue  # noqa: E402
from idea_brief import paste_block  # noqa: E402

CHANNEL = ROOT / "docs" / "channel.md"
QUEUE = ROOT / "docs" / "topic_queue.md"
CANDIDATES = TOOLS / "topic_candidates.json"


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


def next_qid(queue_text: str) -> int:
    """Return the next Q number after the highest existing QN in the queue."""
    rows = parse_queue(queue_text)
    highest = 0
    for row in rows:
        m = re.match(r"Q(\d+)", row.get("id", ""))
        if m:
            highest = max(highest, int(m.group(1)))
    return highest + 1


def load_candidates() -> list[tuple[str, str, str]]:
    """Load (working_title, one_line, problem) from tools/topic_candidates.json."""
    if not CANDIDATES.is_file():
        print(f"Missing candidates: {CANDIDATES}", file=sys.stderr)
        return []
    try:
        data = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {CANDIDATES}: {e}", file=sys.stderr)
        return []
    out = []
    for item in data:
        title = item.get("working_title", "").strip()
        one = item.get("one_line", "").strip()
        prob = item.get("problem", "").strip()
        if title and one and prob:
            out.append((title, one, prob))
    return out


def suggestions(niche: str, promise: str, existing: set[str]) -> list[tuple[str, str, str]]:
    """Return (working_title, one_line, problem) tuples that fit the niche."""
    candidates = load_candidates()
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
    start_id = 6
    if QUEUE.is_file():
        queue_text = QUEUE.read_text(encoding="utf-8")
        existing = existing_titles(queue_text)
        start_id = next_qid(queue_text)

    rows = suggestions(niche, promise, existing)[: args.count]

    print("TOPIC SUGGEST (operational defaults only; no invented sources or numbers)")
    print(f"Niche: {niche}")
    print(f"Promise: {promise}")
    print(f"Existing titles skipped: {len(existing)}")
    print(f"Next id starts at: Q{start_id}")
    print()
    print("Candidate rows (paste into docs/topic_queue.md):")
    print("| id | status | working_title | one_line | problem |")
    print("|----|--------|---------------|----------|---------|")
    for i, (title, one, prob) in enumerate(rows):
        qid = start_id + i
        print(f"| Q{qid} | queued | {title} | {one} | {prob} |")
    print()
    print("These are suggestions only. Review, edit, and mark status before use.")
    print("Do not scaffold until Q1 ships. Do not invent a packet from this output.")
    print("After adding the row(s), run: python3 tools/next_topic.py")
    print(f"Or get paste-ready idea.md (after row is in queue): python3 tools/idea_brief.py --queue Q{start_id}")
    print()
    # Canonical idea.md skeletons via idea_brief.paste_block (same path as apply_idea)
    print("Ready idea.md skeletons (canonical paste_block format; grounded, no invented claims):")
    print("=" * 60)
    for i, (title, one, prob) in enumerate(rows[:2]):
        qid = start_id + i
        print(f"# For Q{qid} — {title}")
        # Pass explicit problem/mechanism so paste_block does not depend on a queue row yet
        block = paste_block(title, problem=prob, mechanism=one, topic=title)
        print(block, end="")
        print("# After the packet folder exists, use apply_idea.py or paste the above.")
        print("# This print writes nothing.")
        print("-" * 40)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
