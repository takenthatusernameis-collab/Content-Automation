#!/usr/bin/env python3
"""Contract check for tools/queued_field_check.py field integrity.

Locks the HARD/SOFT classification so later runs cannot silently weaken the queue gate.
Uses in-memory rows; never writes the live queue. Exit 0 on PASS.
"""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from queued_field_check import check_rows  # type: ignore


def fail(failures: list[str], cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


def main() -> int:
    failures: list[str] = []

    # Clean row
    clean = [{
        "id": "Q9",
        "status": "queued",
        "working_title": "A sufficiently long working title for testing",
        "one_line": "This one_line is longer than twenty characters easily.",
        "problem": "This problem description is also long enough for the soft threshold."
    }]
    issues = check_rows(clean)
    fail(failures, len(issues) == 0, f"clean row produced issues: {issues}")

    # Missing id
    bad_id = [{"id": "", "status": "queued", "working_title": "Title", "one_line": "One line here long enough", "problem": "Problem text long enough here"}]
    issues = check_rows(bad_id)
    fail(failures, any(sev == "HARD" and "missing id" in msg for sev, _, msg in issues), f"missing id: {issues}")

    # Invalid status
    bad_status = [{"id": "Q1", "status": "mystery", "working_title": "Title long enough", "one_line": "One line here long enough", "problem": "Problem text long enough here"}]
    issues = check_rows(bad_status)
    fail(failures, any("Invalid status" in msg for _, _, msg in issues), f"bad status: {issues}")

    # Empty title
    empty_title = [{"id": "Q1", "status": "queued", "working_title": "", "one_line": "One line here long enough", "problem": "Problem text long enough here"}]
    issues = check_rows(empty_title)
    fail(failures, any("Empty working_title" in msg for _, _, msg in issues), f"empty title: {issues}")

    # Duplicate id
    dup_id = [
        {"id": "Q1", "status": "queued", "working_title": "Title one long", "one_line": "One line here long enough", "problem": "Problem text long enough here"},
        {"id": "Q1", "status": "queued", "working_title": "Title two long", "one_line": "Another line here long enough", "problem": "Another problem long enough"}
    ]
    issues = check_rows(dup_id)
    fail(failures, any("Duplicate id" in msg for _, _, msg in issues), f"dup id: {issues}")

    # Short one_line (SOFT)
    short_ol = [{"id": "Q1", "status": "queued", "working_title": "Title long enough", "one_line": "short", "problem": "Problem text long enough here"}]
    issues = check_rows(short_ol)
    fail(failures, any(sev == "SOFT" and "one_line very short" in msg for sev, _, msg in issues), f"short one_line: {issues}")
    fail(failures, not any(sev == "HARD" for sev, _, _ in issues), "short one_line must be soft only")

    # Empty problem on queued (SOFT)
    empty_prob = [{"id": "Q1", "status": "queued", "working_title": "Title long enough", "one_line": "One line here long enough", "problem": ""}]
    issues = check_rows(empty_prob)
    fail(failures, any("empty problem" in msg.lower() for _, _, msg in issues), f"empty problem: {issues}")

    print("Queued field check contract")
    if failures:
        print("QUEUED_FIELD_CHECK CONTRACT FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("QUEUED_FIELD_CHECK CONTRACT PASS")
    print("This command writes nothing in the repo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
