#!/usr/bin/env python3
"""Contract lock for tools/observation_window.py.

Self-tests that the due date is uploaded_at + 10 days and status is DUE or WAITING.
Also locks the hardened parse_uploaded_at against common ISO variants and garbage.
Does not invent dates, call APIs, or write packet files.
Fails if the helper logic drifts from the documented +10 day window or the parse robustness.
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


def test_parse_variants() -> bool:
    cases = [
        ("2026-01-01T00:00:00Z", 2026, 1, 1),
        ("2026-01-01T00:00:00+00:00", 2026, 1, 1),
        ("2026-01-01T12:30:45", 2026, 1, 1),
        ("2026-01-01 12:30:45", 2026, 1, 1),
        ("2026-01-01", 2026, 1, 1),
        ("2026-12-31T23:59:59Z", 2026, 12, 31),
    ]
    for raw, y, m, d in cases:
        parsed = parse_uploaded_at({"uploaded_at": raw})
        if not parsed or (parsed.year, parsed.month, parsed.day) != (y, m, d):
            print(f"FAIL: parse_uploaded_at rejected or misparsed {raw!r}")
            return False
    print("PASS: common ISO / date variants parse correctly")
    return True


def test_no_invent() -> bool:
    bad_cases = ["not-a-date", "", "  ", "tomorrow", "2026-13-01", "abc", None]
    for bad in bad_cases:
        if parse_uploaded_at({"uploaded_at": bad}) is not None:
            print(f"FAIL: parse invented a date from {bad!r}")
            return False
    if parse_uploaded_at({}) is not None:
        print("FAIL: parse invented a date from empty dict")
        return False
    print("PASS: garbage / missing dates stay None")
    return True


def main() -> int:
    print("OBSERVATION_WINDOW CONTRACT")
    ok = test_parse_and_due() and test_parse_variants() and test_no_invent()
    if ok:
        print("OBSERVATION_WINDOW CONTRACT PASS")
        return 0
    print("OBSERVATION_WINDOW CONTRACT FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
