#!/usr/bin/env python3
"""Read-only fixture contract check.

Runs against videos/sample-001-* only. Writes nothing.
Purpose: future runs can prove validate/doctor/hint/set_status/apply_script
contracts instead of leaving runtime unverified.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from apply_script import check as apply_check  # noqa: E402
from hint import commands_for  # noqa: E402
from next_action import recommend  # noqa: E402
from pipeline_status import inspect  # noqa: E402
from set_status import check as status_check, is_fixture  # noqa: E402
from validate_packet import packet_duration_warning, validate  # noqa: E402


def sample_packet() -> Path:
    videos = ROOT / "videos"
    hits = sorted(
        p
        for p in videos.iterdir()
        if p.is_dir() and p.name.startswith("sample-001")
    )
    if not hits:
        raise SystemExit("selftest: no videos/sample-001-* fixture")
    return hits[0]


def first_live_command(cmds: list[str]) -> str | None:
    for c in cmds:
        s = c.strip()
        if s and not s.startswith("#"):
            return s
    return None


def main() -> int:
    path = sample_packet()
    failures: list[str] = []

    if not is_fixture(path):
        failures.append(f"is_fixture({path.name}) is False")

    errors, incompletes = validate(path, draft=False)
    if errors:
        failures.append(f"publish gate should PASS, got FAIL: {errors}")
    if incompletes:
        failures.append(f"publish gate incompletes unexpected: {incompletes}")

    dur = packet_duration_warning(path)
    if not dur:
        failures.append("expected duration WARN on short fixture WORDS")
    elif "below" not in dur:
        failures.append(f"duration WARN should say below band, got: {dur}")

    errs_dur, _ = validate(path, draft=False, duration=True)
    if not errs_dur:
        failures.append("--duration should FAIL the short fixture")

    row = inspect(path)
    if row["gate"] != "PASS":
        failures.append(f"inspect gate expected PASS, got {row['gate']}")
    if row["status"] != "draft":
        failures.append(f"fixture status expected draft, got {row['status']}")
    if row["drift"]:
        failures.append(f"fixture should have no drift, got {row['drift']}")

    code, why = recommend(path, row)
    if code != "expand-script":
        failures.append(f"next-action code expected expand-script, got {code} ({why})")

    cmds = commands_for(path, row, code)
    live = first_live_command(cmds)
    if live is None:
        failures.append("hint produced no live command")
    elif "--write" in live:
        failures.append(f"first live command must not include --write: {live}")
    lock = any("fixture lock" in c.lower() for c in cmds)
    if not lock:
        failures.append("hint must print fixture lock on sample-001")

    blocked_status = status_check(path, "ready_for_vo")
    if not blocked_status:
        failures.append("set_status ready_for_vo must refuse the fixture")
    else:
        blob = " ".join(blocked_status).lower()
        if "fixture" not in blob and "sample-001" not in blob:
            failures.append(f"set_status refuse should mention fixture: {blocked_status}")

    fake_script = (
        "# Script\n\n"
        "## Hook (0:00–0:12)\n\n"
        "WORDS: This line is only here so apply_script has headings to parse.\n\n"
        "## Payoff promise\n\nWORDS: payoff\n\n"
        "## Beat 1\n\nWORDS: beat\n\n"
        "## Beat 2\n\nWORDS: beat\n\n"
        "## Beat 3\n\nWORDS: beat\n\n"
        "## Beat 4\n\nWORDS: beat\n\n"
        "## CTA\n\nWORDS: cta\n"
    )
    blocked_apply = apply_check(path, fake_script)
    if not blocked_apply:
        failures.append("apply_script must refuse the fixture")
    elif not any("fixture" in e.lower() or "sample-001" in e.lower() for e in blocked_apply):
        failures.append(f"apply_script refuse should mention fixture: {blocked_apply}")

    print(f"Fixture: {path.name}")
    print(f"Gate: {row['gate']}")
    print(f"Status: {row['status']}")
    print(f"Code: {code}")
    print(f"Duration WARN: {dur or '—'}")
    print(f"First live command: {live}")
    if failures:
        print("SELFTEST FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("SELFTEST PASS")
    print("This command writes nothing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
