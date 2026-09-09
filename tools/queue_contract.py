#!/usr/bin/env python3
"""Read-only contract check for the topic-queue board.

Uses a temp tree only. Never writes docs/topic_queue.md or videos/.
Locks classify codes, PACKET column, --strict exits, next_id, and
mark_topic line rewrite so later runs cannot silently regress Run 031.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from mark_topic import rewrite_status  # noqa: E402
from queue_lib import next_id, parse_queue, slugify  # noqa: E402
from queue_status import classify, exit_code, packet_status, report  # noqa: E402


QUEUE_TEXT = """# Topic queue

| id | status | working_title | one_line |
|----|--------|---------------|----------|
| Q1 | queued | Stop deciding what to work on every morning | Install a written next-action default. |
| Q2 | queued | Put the start cue on the work itself | Name one physical cue. |
| Q3 | used | Close the extra tab before you open the work | Shutdown default. |
| Q4 | parked | Keep the checklist where the stall happens | Put the constraint on the desk. |
| Q5 | mystery | One list, one next action | Bad status on purpose. |
"""


def fail(failures: list[str], cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


def main() -> int:
    failures: list[str] = []

    rows = parse_queue(QUEUE_TEXT)
    fail(failures, [r["id"] for r in rows] == ["Q1", "Q2", "Q3", "Q4", "Q5"], f"parse ids: {[r['id'] for r in rows]}")

    q1 = next(r for r in rows if r["id"] == "Q1")
    q3 = next(r for r in rows if r["id"] == "Q3")
    q4 = next(r for r in rows if r["id"] == "Q4")
    q5 = next(r for r in rows if r["id"] == "Q5")

    slug_q1 = slugify(q1["working_title"])
    fail(failures, slug_q1 == "stop-deciding-what-to-work-on-every-morning", f"slug q1: {slug_q1}")

    code, _, folder = classify(q1, [])
    fail(failures, code == "ok-queued" and folder is None, f"queued no folder: {code} {folder}")

    folder_name = f"002-{slug_q1}"
    code, _, folder = classify(q1, [folder_name])
    fail(failures, code == "mark-needed" and folder == folder_name, f"mark-needed: {code} {folder}")

    code, _, folder = classify(q1, ["sample-001-" + slug_q1])
    fail(failures, code == "fixture-refuse", f"fixture-refuse: {code} {folder}")

    code, _, folder = classify(q3, [])
    fail(failures, code == "missing-folder" and folder is None, f"missing-folder: {code} {folder}")

    used_folder = "003-close-the-extra-tab-before-you-open-the-work"
    code, _, folder = classify(q3, [used_folder])
    fail(failures, code == "ok-used" and folder == used_folder, f"ok-used: {code} {folder}")

    code, _, _ = classify(q4, [])
    fail(failures, code == "parked", f"parked: {code}")

    code, _, _ = classify(q5, [])
    fail(failures, code == "unknown-status", f"unknown-status: {code}")

    fail(failures, exit_code({"missing-folder": 0, "mark-needed": 0, "unknown-status": 0}, False) == 0, "default clean")
    fail(failures, exit_code({"missing-folder": 1, "mark-needed": 0, "unknown-status": 0}, False) == 0, "default missing still 0")
    fail(failures, exit_code({"missing-folder": 1, "mark-needed": 0, "unknown-status": 0}, True) == 2, "strict missing=2")
    fail(failures, exit_code({"missing-folder": 0, "mark-needed": 1, "unknown-status": 0}, True) == 1, "strict mark=1")
    fail(failures, exit_code({"missing-folder": 0, "mark-needed": 0, "unknown-status": 1}, True) == 1, "strict unknown=1")
    fail(failures, exit_code({"missing-folder": 1, "mark-needed": 1, "unknown-status": 0}, True) == 2, "missing beats mark")
    fail(failures, exit_code({"missing-folder": 0, "mark-needed": 0, "unknown-status": 0}, True) == 0, "strict clean")

    raw = "| Q1 | queued | Stop deciding what to work on every morning | Install a written next-action default. |"
    rewritten = rewrite_status(raw, "used")
    fail(failures, "| used |" in rewritten and "queued" not in rewritten, f"rewrite: {rewritten}")

    with tempfile.TemporaryDirectory() as tmp:
        videos = Path(tmp) / "videos"
        sample = videos / "sample-001-why-systems-beat-motivation"
        sample.mkdir(parents=True)
        (sample / "packet.md").write_text("- status: draft\n", encoding="utf-8")
        live = videos / folder_name
        live.mkdir()
        (live / "packet.md").write_text("- status: draft\n- working_title: x\n", encoding="utf-8")
        empty = videos / "no-status-packet"
        empty.mkdir()
        (empty / "packet.md").write_text("- working_title: x\n", encoding="utf-8")

        # sample-001 + 002-slug => highest 2 => next 003
        fail(failures, next_id(videos) == "003", f"next_id expected 003, got {next_id(videos)}")

        fail(failures, packet_status(videos, None) == "-", "packet none")
        fail(failures, packet_status(videos, folder_name) == "draft", f"packet draft got {packet_status(videos, folder_name)}")
        fail(failures, packet_status(videos, "missing-dir") == "no-packet", "no-packet")
        fail(
            failures,
            packet_status(videos, "no-status-packet") == "no-status",
            f"no-status got {packet_status(videos, 'no-status-packet')}",
        )

        body, counts = report(
            QUEUE_TEXT,
            ["sample-001-why-systems-beat-motivation", folder_name],
            "003",
            videos,
        )
        fail(failures, counts["mark-needed"] == 1, f"counts mark-needed {counts}")
        fail(failures, counts["ok-queued"] == 1, f"counts ok-queued {counts}")
        fail(failures, counts["missing-folder"] == 1, f"counts missing-folder {counts}")
        fail(failures, counts["parked"] == 1, f"counts parked {counts}")
        fail(failures, counts["unknown-status"] == 1, f"counts unknown {counts}")
        fail(failures, "PACKET" in body.splitlines()[3], "header has PACKET")
        fail(failures, "python3 tools/mark_topic.py --id Q1" in body, "dry-run mark printed")
        fail(
            failures,
            "--write" in body and body.count("# python3 tools/mark_topic.py --id Q1 --write") >= 1,
            "write is commented",
        )
        fail(
            failures,
            "do not auto-scaffold" in body.lower() or "Do not treat this board" in body,
            "no-write banner",
        )

    print("Queue contract")
    print(f"Rows parsed: {len(rows)}")
    print("Strict missing-folder exit: 2")
    print("Strict mark-needed exit: 1")
    print("Default exit with drift: 0")
    if failures:
        print("QUEUE CONTRACT FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("QUEUE CONTRACT PASS")
    print("This command writes nothing in the repo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
