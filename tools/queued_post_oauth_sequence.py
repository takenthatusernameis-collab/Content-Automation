#!/usr/bin/env python3
"""Print the post-OAuth production sequence for a queued topic.

No packet required. No writes. No invent. No secrets. No dispatch.
Grounded in docs/topic_queue.md + existing tools.

Useful after STALL_OAUTH_IDLE ends (or while preparing for it): one command
shows the exact next commands to scaffold and fill a queued topic once
credentials exist and a video id is visible. Reduces rediscovery of the
standard packet path for every subsequent video.

Does not scaffold. Does not mark used. Does not call APIs.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from queue_lib import parse_queue, slugify, next_id  # type: ignore


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print post-OAuth sequence for a queued topic id (or first queued). No writes."
    )
    parser.add_argument("--id", default="", help="Topic id (e.g. Q2). Default: first queued row.")
    args = parser.parse_args()

    queue_path = ROOT / "docs" / "topic_queue.md"
    if not queue_path.is_file():
        print(f"Missing queue: {queue_path}", file=sys.stderr)
        return 1

    rows = parse_queue(queue_path.read_text(encoding="utf-8"))
    if not rows:
        print("No rows in topic queue.")
        return 0

    if args.id:
        row = next((r for r in rows if r["id"].upper() == args.id.upper()), None)
        if not row:
            print(f"No row for id {args.id}.", file=sys.stderr)
            return 1
    else:
        queued = [r for r in rows if r["status"] == "queued"]
        if not queued:
            print("No queued topics.")
            return 0
        row = queued[0]

    title = row["working_title"]
    one_line = row["one_line"]
    tid = row["id"]
    slug = slugify(title)
    # Predict next folder number (read-only; does not create)
    videos_dir = ROOT / "videos"
    nid = next_id(videos_dir)
    predicted = f"videos/{nid}-{slug}"

    print(f"# Post-OAuth sequence for {tid}: {title}")
    print("# (read-only; grounded in queue; does not scaffold or invent)")
    print("# Run only after a private video id exists from the first dispatch.")
    print("# Preferred human step remains OAuth until then: python3 tools/oauth_complete_guide.py")
    print()
    print(f"Predicted folder: {predicted}")
    print(f"Mechanism: {one_line}")
    print()
    print("=== 1. Confirm stall ended ===")
    print("python3 tools/human_success_check.py")
    print("python3 tools/post_publish_sequence.py   # after id visible")
    print()
    print("=== 2. Scaffold the packet (human or explicit agent instruction only) ===")
    print(f"python3 tools/new_packet.py \"{title}\"")
    print("# Then mark used only after folder exists:")
    print(f"# python3 tools/mark_topic.py --id {tid} --write")
    print()
    print("=== 3. Fill idea from queue (dry-run first) ===")
    print(f"python3 tools/apply_idea.py {predicted}")
    print(f"python3 tools/apply_idea.py {predicted} --write   # only if blank template")
    print(f"python3 tools/idea_brief.py {predicted} --check")
    print()
    print("=== 4. One-command grounded starters (no packet needed, or after) ===")
    print(f"python3 tools/queued_full_starter.py --id {tid}")
    print("# Copy preferred idea / research / outline / titles / thumbnail / description sections")
    print()
    print("=== 5. Draft and quality path ===")
    print(f"python3 tools/draft_starter.py {predicted}")
    print("# Paste into draft.md, expand body beats to targets")
    print(f"python3 tools/draft_pre_apply_coach.py {predicted}")
    print(f"python3 tools/words.py {predicted}")
    print(f"python3 tools/apply_script.py {predicted} --from {predicted}/draft.md")
    print(f"python3 tools/apply_script.py {predicted} --from {predicted}/draft.md --write --refresh")
    print(f"python3 tools/set_status.py {predicted} --to ready_for_vo   # dry-run first; --write after band + clear signals")
    print()
    print("=== 6. Remaining human / media ===")
    print("# Record or materialize Selected VO to the named path")
    print("# Run media_qa / assemble / complete only after evidence")
    print("# Do not invent VO, cards, or master")
    print()
    print("Do not scaffold while STALL_OAUTH_IDLE. Do not poll secrets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
