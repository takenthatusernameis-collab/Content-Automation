#!/usr/bin/env python3
"""Reliability contract for tools/experiment_loop.py.

Creates a temporary empty packet and asserts the fail-closed missing-provider_video_id
path (exit 2 + key phrases including gate: HOLD_UNPUBLISHED).
Soft only; does not invent metrics, baselines, decisions, or call APIs. Locks the
post-publish experiment ledger so the unpublished hold cannot silently regress
while the long OAuth stall continues.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "experiment_loop.py"

REQUIRED = [
    "gate: HOLD_UNPUBLISHED",
    "provider_video_id: none",
    "experiment_loop never invents results or calls Analytics",
    "missing provider_video_id is HOLD_UNPUBLISHED, not a learned experiment",
]


def main() -> int:
    if not TOOL.is_file():
        print("CONTRACT FAIL: experiment_loop.py missing")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "empty-packet"
        packet.mkdir()
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(packet)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        out = proc.stdout + proc.stderr
        missing = [p for p in REQUIRED if p not in out]
        if missing or proc.returncode != 2:
            print("EXPERIMENT LOOP CONTRACT FAIL")
            for m in missing:
                print(f"  missing: {m}")
            print(f"  exit {proc.returncode} (expected 2)")
            return 1
    print("EXPERIMENT LOOP CONTRACT PASS (HOLD_UNPUBLISHED path locked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
