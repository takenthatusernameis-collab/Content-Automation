#!/usr/bin/env python3
"""Packet prep brief: one-command early structure checks.

Runs the recent no-write format, card-hold, and visual-readability checkers
and prints a combined summary. Reduces the number of separate CLI invocations
before expanding, recording, or planning cards on every future packet.
Does not invent content, rewrite files, or call external services.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = [
    ("format_segment_check.py", "Format segments"),
    ("card_hold_check.py", "Card holds"),
    ("visual_readability_check.py", "Visual readability"),
]


def run_tool(script: str, packet: str) -> tuple[int, str]:
    cmd = [sys.executable, str(ROOT / "tools" / script), packet]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        out = (result.stdout or "") + (result.stderr or "")
        return result.returncode, out.strip()
    except Exception as exc:
        return 1, f"Failed to run {script}: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Combined early prep checks for a packet (format, holds, readability). No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("PACKET PREP BRIEF")
    print(f"Packet: {path.name}")
    print("Aggregates format_segment_check, card_hold_check, visual_readability_check.")
    print("=" * 72)
    print()

    overall = "PASS"
    summaries: list[str] = []
    for script, label in TOOLS:
        code, output = run_tool(script, str(path))
        status = "PASS" if code == 0 else ("WARN" if code == 2 else "FAIL")
        if code != 0:
            overall = "WARN" if code == 2 else "FAIL"
        # Extract the Overall line if present
        overall_line = next((ln for ln in output.splitlines() if ln.startswith("Overall:")), f"exit {code}")
        summaries.append(f"- {label}: {status} ({overall_line})")
        print(f"### {label}")
        print(output)
        print()

    print("=" * 72)
    print(f"Combined overall: {overall}")
    for s in summaries:
        print(s)
    print()
    print("Next: fix any WARN/FAIL items, then expand_brief.py / validate_packet.py / card_generator.py.")
    print("This tool writes nothing.")
    return 0 if overall == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
