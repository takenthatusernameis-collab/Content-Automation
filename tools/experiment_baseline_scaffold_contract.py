#!/usr/bin/env python3
"""Reliability contract for experiment_baseline_scaffold.py.

Creates a temp packet, runs the scaffold, confirms the template file appears,
then confirms experiment_baseline_validate rejects it (as expected for a template),
and that a filled stub would pass. No secrets, no real packets, no APIs.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SCAFFOLD = TOOLS / "experiment_baseline_scaffold.py"
VALIDATE = TOOLS / "experiment_baseline_validate.py"


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "test-packet"
        packet.mkdir()
        # Scaffold
        result = subprocess.run(
            [sys.executable, str(SCAFFOLD), str(packet)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"scaffold failed: {result.stderr}")
            return 1
        dest = packet / "experiment_baseline.json"
        if not dest.is_file():
            print("scaffold did not write experiment_baseline.json")
            return 1
        data = json.loads(dest.read_text(encoding="utf-8"))
        if not data.get("_template"):
            print("written file is not the template")
            return 1
        print("scaffold wrote template OK")

        # Validate should fail on template
        val = subprocess.run(
            [sys.executable, str(VALIDATE), str(packet)],
            capture_output=True,
            text=True,
        )
        if val.returncode == 0:
            print("validate unexpectedly passed on template")
            return 1
        if "FAIL" not in val.stdout:
            print("validate did not report FAIL on template")
            return 1
        print("validate correctly rejects template OK")

        # Fill a minimal valid stub and confirm validate passes
        filled = {
            "hypothesis": "A stronger hook raises average view duration",
            "change": "hook",
            "primary_metric": "average_view_duration_seconds",
            "baseline": 45.0,
            "source": "YouTube Studio analytics for prior video on 2026-09-15",
        }
        dest.write_text(json.dumps(filled, indent=2) + "\n", encoding="utf-8")
        val2 = subprocess.run(
            [sys.executable, str(VALIDATE), str(packet)],
            capture_output=True,
            text=True,
        )
        if val2.returncode != 0 or "PASS" not in val2.stdout:
            print(f"validate failed on filled stub: {val2.stdout} {val2.stderr}")
            return 1
        print("validate accepts filled stub OK")

    print("experiment_baseline_scaffold_contract PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
