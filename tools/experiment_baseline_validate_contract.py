#!/usr/bin/env python3
"""Minimal contract for experiment_baseline_validate.py.

Verifies it rejects a missing baseline and accepts a valid numeric one on a temp packet.
Does not invent real metrics, poll secrets, or change hard gates.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "experiment_baseline_validate.py"


def main() -> int:
    if not TOOL.is_file():
        print("experiment_baseline_validate_contract: tool missing")
        return 1
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "test-packet"
        packet.mkdir()
        # Missing file should fail
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(packet)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if proc.returncode == 0 or "FAIL" not in (proc.stdout + proc.stderr):
            failures.append("missing file should fail")
        # Valid file should pass
        valid = {
            "hypothesis": "A stronger hook raises average view duration",
            "change": "hook",
            "primary_metric": "average_view_duration_seconds",
            "baseline": 45.0,
            "source": "YouTube Studio analytics for prior video on 2026-01-15",
        }
        (packet / "experiment_baseline.json").write_text(json.dumps(valid) + "\n", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(packet)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        out = proc.stdout + proc.stderr
        if proc.returncode != 0 or "PASS" not in out:
            failures.append(f"valid baseline should pass (exit {proc.returncode})")
        # Null baseline should fail
        invalid = valid.copy()
        invalid["baseline"] = None
        (packet / "experiment_baseline.json").write_text(json.dumps(invalid) + "\n", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(packet)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if proc.returncode == 0 or "FAIL" not in (proc.stdout + proc.stderr):
            failures.append("null baseline should fail")
    if failures:
        print("experiment_baseline_validate_contract FAIL:", "; ".join(failures))
        return 1
    print("experiment_baseline_validate_contract PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
