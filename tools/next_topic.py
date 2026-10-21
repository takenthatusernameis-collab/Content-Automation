#!/usr/bin/env python3
"""Print the next queued topic and the scaffold commands. Read-only."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from queue_lib import already_used, existing_slugs, next_id, parse_queue, slugify  # noqa: E402
from topic_priority_scan import (
    CHANNEL_KEYWORDS,
    extract_keywords,
    load_text,
    score_topic,
)  # noqa: E402

QUEUE = ROOT / "docs" / "topic_queue.md"
VIDEOS = ROOT / "videos"

Q1_HOLD = (
    "# Q1 remaining labor is docs/gate_machine.md; do not scaffold Q2"
)
PARKED_LABEL = (
    "# Parked until Q1 ships (copy-paste only after Selected VO exists on the gate machine):"
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print the next queued topic (read-only; does not scaffold)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Print every queued row that is not already a packet",
    )
    args = parser.parse_args()

    if not QUEUE.is_file():
        print(f"Missing queue: {QUEUE}", file=sys.stderr)
        return 1

    rows = parse_queue(QUEUE.read_text(encoding="utf-8"))
    slugs = existing_slugs(VIDEOS)
    available = [
        r
        for r in rows
        if r["status"] == "queued" and not already_used(r["working_title"], slugs)
    ]

    # Rank by channel fit + mechanism continuity (same scoring as topic_priority_scan)
    channel_text = load_text(ROOT / "docs" / "channel.md")
    q1_text = load_text(ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning" / "idea.md")
    channel_kws = extract_keywords(channel_text)
    q1_kws = extract_keywords(q1_text)

    def _score(row):
        # Adapt row keys to what score_topic expects
        adapted = {
            "title": row["working_title"],
            "one_line": row["one_line"],
            "problem": row.get("problem", ""),
        }
        s, phrases = score_topic(adapted, channel_kws, q1_kws)
        return s, phrases

    if available:
        available.sort(key=lambda r: -_score(r)[0])

    print("This command writes nothing.")
    print("Queue file: docs/topic_queue.md")
    print(f"Queued unused: {len(available)} / {len(rows)}")
    print("Selection: highest mechanism-continuity score (from topic_priority_scan logic)")
    print(Q1_HOLD)
    if not available:
        print("No unused queued topic. Add a row to docs/topic_queue.md or reuse an existing packet.")
        return 0

    predicted_id = next_id(VIDEOS)
    show = available if args.all else available[:1]
    for i, row in enumerate(show):
        title = row["working_title"]
        slug = slugify(title)
        vid = f"{int(predicted_id) + i:03d}" if args.all else predicted_id
        dest = f"videos/{vid}-{slug}"
        score, phrases = _score(row)
        print(f"Next (parked until Q1 ships): {row['id']} — {title} (score {score})")
        print(f"One-line: {row['one_line']}")
        if phrases:
            print(f"Matched phrases: {', '.join(phrases)}")
        print(f"Predicted path: {dest}")
        print(PARKED_LABEL)
        print("Optional before scaffold (no folder required; writes nothing):")
        print(f"  python3 tools/idea_brief.py --queue {row['id']}")
        print("Scaffold (human / instructed agent only; not the fixture):")
        print(f'  python3 tools/new_packet.py "{title}"')
        print(f'  python3 tools/new_idea.py "{row["one_line"]}"')
        print(f"  python3 tools/doctor.py {dest}")
        print("After the folder exists (dry-run first; apply_idea does not scaffold):")
        print(f"  python3 tools/apply_idea.py {dest}")
        print(f"  # blank template only: python3 tools/apply_idea.py {dest} --write")
        print(f"  python3 tools/idea_brief.py {dest} --check")
        print(f"  python3 tools/mark_topic.py --id {row['id']}")
        print(f"  # python3 tools/mark_topic.py --id {row['id']} --write")
        print("Do not apply WORDS to sample-001. Do not invent a script here.")
        print(Q1_HOLD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
