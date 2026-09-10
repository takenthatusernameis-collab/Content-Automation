#!/usr/bin/env python3
"""Contract check for the operator Q1 pin.

Read-only versus videos/. Does not write idea.md, the queue, or packets.
Locks, while Q1 is still queued:
- docs/human_session.md contains the Q1 working_title from topic_queue.md
- predicted folder videos/002-<slugify(title)>
- queue one_line (mechanism reprint)
- fill-idea before expand
- new_packet does not write idea.md
- mark_topic --id Q1 dry-run is shown

Unmapped in which_contract. Not a reconstruct wave.
"""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from queue_lib import parse_queue, slugify  # noqa: E402


def fail(failures: list[str], cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


def first_queued(rows: list[dict[str, str]]) -> dict[str, str] | None:
    for row in rows:
        if row.get("status") == "queued":
            return row
    return None


def main() -> int:
    failures: list[str] = []
    queue_path = ROOT / "docs" / "topic_queue.md"
    human_path = ROOT / "docs" / "human_session.md"
    fail(failures, queue_path.is_file(), "missing docs/topic_queue.md")
    fail(failures, human_path.is_file(), "missing docs/human_session.md")
    if failures:
        print("OPERATOR PIN CONTRACT FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1

    rows = parse_queue(queue_path.read_text(encoding="utf-8"))
    fail(failures, bool(rows), "topic_queue parsed zero rows")
    q1 = next((r for r in rows if r["id"] == "Q1"), None)
    fail(failures, q1 is not None, "Q1 row missing from topic_queue")
    first = first_queued(rows)
    human = human_path.read_text(encoding="utf-8")

    if q1 and q1["status"] == "queued":
        title = q1["working_title"]
        mechanism = q1["one_line"]
        slug = slugify(title)
        folder = f"videos/002-{slug}"
        fail(failures, title in human, f"human_session missing Q1 title {title!r}")
        fail(failures, folder in human, f"human_session missing predicted folder {folder}")
        fail(
            failures,
            mechanism in human,
            f"human_session missing Q1 one_line {mechanism!r}",
        )
        fail(failures, "fill-idea" in human, "human_session missing fill-idea")
        fail(
            failures,
            "does not write idea.md" in human,
            "human_session missing new_packet no-write-idea note",
        )
        fail(
            failures,
            "mark_topic.py --id Q1" in human,
            "human_session missing mark_topic --id Q1",
        )
        fail(
            failures,
            f'new_packet.py "{title}"' in human or f"new_packet.py '{title}'" in human,
            "human_session missing exact new_packet Q1 command",
        )
        fail(
            failures,
            "expand_prompt.py" in human and folder in human,
            "human_session missing expand_prompt on the pinned folder",
        )
        if first is not None:
            fail(
                failures,
                first["id"] == "Q1",
                f"first queued row is {first['id']}, human_session still pins Q1",
            )
    elif q1 and q1["status"] != "queued":
        print(f"Q1 status is {q1['status']}; title pin not required")

    print("Operator pin contract")
    print("Q1 title / 002-slug / one_line / fill-idea stay on human_session while queued")
    if failures:
        print("OPERATOR PIN CONTRACT FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("OPERATOR PIN CONTRACT PASS")
    print("This command writes nothing in videos/ and does not write idea.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
