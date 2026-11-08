#!/usr/bin/env python3
"""Print a compact overview of all topics in docs/topic_queue.md.

No packet required. No writes. No invent. Useful for choosing which queued id to run
queued_full_starter.py (or individual starters) on while STALL_OAUTH_IDLE persists.
Reduces rediscovery of the queue board.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from queue_lib import parse_queue  # type: ignore


def main() -> int:
    queue_path = ROOT / "docs" / "topic_queue.md"
    if not queue_path.is_file():
        print(f"Missing queue: {queue_path}", file=sys.stderr)
        return 1

    rows = parse_queue(queue_path.read_text(encoding="utf-8"))
    if not rows:
        print("No rows in topic queue.")
        return 0

    print("# Topic queue overview (read-only)")
    print("# Use with: python3 tools/queued_full_starter.py --id QN")
    print("# Or individual starters. Do not scaffold while STALL_OAUTH_IDLE.")
    print()
    print(f"{'id':<4} {'status':<8} {'working_title':<48} {'one_line (truncated)':<50}")
    print("-" * 120)
    for r in rows:
        ol = (r["one_line"] or "")[:48]
        title = (r["working_title"] or "")[:46]
        print(f"{r['id']:<4} {r['status']:<8} {title:<48} {ol:<50}")
    print()
    queued = [r for r in rows if r["status"] == "queued"]
    print(f"Queued count: {len(queued)}")
    if queued:
        print("Suggested next for prep: first queued (currently " + queued[0]["id"] + ")")
        print(f"Command: python3 tools/queued_full_starter.py --id {queued[0]['id']}")
    print()
    print("Preferred human next remains OAuth (python3 tools/oauth_complete_guide.py).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
