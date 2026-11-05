#!/usr/bin/env python3
"""Minimal contract for full_packet_review.py.

Verifies the aggregator runs on a temp packet stub and surfaces both sections.
Does not invent media, poll secrets, or change hard gates.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "full_packet_review.py"


def main() -> int:
    if not TOOL.is_file():
        print("full_packet_review_contract: tool missing")
        return 1
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "test-packet"
        packet.mkdir()
        # Minimal stubs so quality and soft tools have something to read
        (packet / "script.md").write_text("# Test\n\nWORDS: this is a short test script for the aggregator.\n", encoding="utf-8")
        (packet / "publish.md").write_text("## Title to upload\nTest Title\n\n## Description\nTest desc.\n", encoding="utf-8")
        (packet / "idea.md").write_text("topic: test\nmechanism: test\n", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(packet)],
            capture_output=True,
            text=True,
            timeout=90,
        )
        out = proc.stdout + proc.stderr
        if "FULL PACKET REVIEW" not in out:
            failures.append("missing header")
        if "## QUALITY PREP BRIEF" not in out:
            failures.append("missing quality section")
        if "## SOFT PRE-UPLOAD REPORT" not in out:
            failures.append("missing soft section")
        if proc.returncode != 0:
            failures.append(f"non-zero exit {proc.returncode}")
    if failures:
        print("full_packet_review_contract FAIL:", "; ".join(failures))
        return 1
    print("full_packet_review_contract PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
