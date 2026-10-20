#!/usr/bin/env python3
"""Lock the unsourced-claim scan. Does not touch the live Q1 packet."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "claim_scan.py"


def fail(msg: str) -> int:
    print("CLAIM SCAN CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("claim_scan.py missing")
    sys.path.insert(0, str(ROOT / "tools"))
    from claim_scan import scan_path
    from set_status import check

    q1 = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
    before = (q1 / "script.md").read_bytes()
    research_before = (q1 / "research.md").read_bytes()
    q1_hits = scan_path(q1)
    if q1_hits:
        return fail(f"Q1 was not clear: {q1_hits}")
    if (q1 / "script.md").read_bytes() != before or (q1 / "research.md").read_bytes() != research_before:
        return fail("scanner rewrote Q1")

    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "videos" / "009-contract"
        packet.mkdir(parents=True)
        (packet / "packet.md").write_text(
            "- id: contract\n- working_title: contract\n- status: draft\n",
            encoding="utf-8",
        )
        script = packet / "script.md"
        script.write_text(
            "# Script\n\n## Hook\nWORDS:\n"
            "Most people waste 40% of the morning reopening the list.\n",
            encoding="utf-8",
        )
        (packet / "research.md").write_text(
            "# Research\n\n## Sources\n- (add URL + the single claim it supports)\n",
            encoding="utf-8",
        )
        blocked = check(packet, "ready_for_vo")
        if not any("claim_scan hits" in item and "40%" in item and "most people" in item for item in blocked):
            return fail(f"set_status did not refuse unsourced claims: {blocked}")
        (packet / "research.md").write_text(
            "# Research\n\n## Sources\n"
            "- https://example.com/morning Most people waste 40% of the morning.\n",
            encoding="utf-8",
        )
        if scan_path(packet):
            return fail(f"cited source did not clear hits: {scan_path(packet)}")
        allowed = check(packet, "ready_for_vo")
        if any("claim_scan hits" in item for item in allowed):
            return fail(f"cited packet still refused: {allowed}")
        # Table Source column path
        (packet / "research.md").write_text(
            "# Research\n\n| Claim | Source |\n| --- | --- |\n"
            "| Most people waste 40% of the morning | https://example.com/morning-table |\n",
            encoding="utf-8",
        )
        if scan_path(packet):
            return fail(f"table Source column did not clear hits: {scan_path(packet)}")
        script_after = script.read_text(encoding="utf-8")
        if "40%" not in script_after or "Write the next action" in script_after:
            return fail("contract rewrote the spoken line")

    proc = subprocess.run(
        [sys.executable, str(TOOL), str(q1)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0 or "clear" not in proc.stdout:
        return fail(proc.stdout + proc.stderr)
    print("CLAIM SCAN CONTRACT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
