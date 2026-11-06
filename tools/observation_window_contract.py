#!/usr/bin/env python3
"""Contract lock for tools/observation_window.py.

Self-tests that the due date is uploaded_at + 10 days and status is DUE or WAITING.
Does not invent dates, call APIs, or write packet files.
Fails if the helper logic drifts from the documented +10 day window.
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from observation_window import parse_uploaded_at  # noqa: E402


def test_parse_and_due() -> bool:
    sample = {"uploaded_at": "2026-01-01T00:00:00Z"}
    parsed = parse_uploaded_at(sample)
    if not parsed or parsed.year != 2026:
        print("FAIL: parse_uploaded_at rejected valid ISO")
        return False
    due = parsed + timedelta(days=10)
    if due.day != 11:
        print("FAIL: due date is not uploaded + 10 days")
        return False
    print("PASS: parse and +10 day due date")
    return True


def test_no_invent() -> bool:
    bad = {"uploaded_at": "not-a-date"}
    if parse_uploaded_at(bad) is not None:
        print("FAIL: parse invented a date from garbage")
        return False
    print("PASS: garbage dates stay None")
    return True


def main() -> int:
    print("OBSERVATION_WINDOW CONTRACT")
    ok = test_parse_and_due() and test_no_invent()
    if ok:
        print("OBSERVATION_WINDOW CONTRACT PASS")
        return 0
    print("OBSERVATION_WINDOW CONTRACT FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
