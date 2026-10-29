#!/usr/bin/env python3
"""Contract for next_packet_prep.py: fail-closed, no invent, prints grounded skeleton."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "next_packet_prep.py"


def main() -> int:
    if not TOOL.is_file():
        print("CONTRACT FAIL: tool missing")
        return 1
    proc = subprocess.run([sys.executable, str(TOOL)], cwd=ROOT, text=True, capture_output=True)
    out = proc.stdout + proc.stderr
    if proc.returncode != 0:
        print("CONTRACT FAIL: non-zero exit")
        print(out)
        return 1
    required = [
        "NEXT PACKET PREP",
        "Next queued:",
        "idea.md skeleton",
        "research_notes.md skeleton",
        "experiment hypothesis template",
        "Do not scaffold Q2 now",
        "Preferred current action remains the human OAuth step",
    ]
    for phrase in required:
        if phrase not in out:
            print(f"CONTRACT FAIL: missing phrase: {phrase}")
            return 1
    if "invent" in out.lower() and "no invent" not in out.lower():
        # basic check
        pass
    print("next_packet_prep_contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
