#!/usr/bin/env python3
"""Check key production tools for truncation / placeholder risk.

Prints OK or FAIL for expected minimum line counts and basic syntax.
Does not invent data. Useful after any file update via GitHub tools
that have been observed to silently truncate large Python files.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Expected minimum lines (as of Run 538 era). Update if tools grow.
EXPECTED = {
    "status_report.py": 250,
    "reusable_commands_index.py": 20,
    "stall_pattern_detector.py": 30,
    "run_history_summary.py": 20,
    "post_upload_confirm.py": 20,
    "observation_window.py": 20,
    "materialize_q1_release.py": 40,
    "media_qa.py": 40,
    "next_action.py": 30,
    "record_run.py": 80,
    "operator_card.py": 20,
    "media_fingerprint.py": 20,
}

def check_file(name: str, min_lines: int) -> tuple[bool, str]:
    path = ROOT / "tools" / name
    if not path.is_file():
        return False, f"MISSING {name}"
    text = path.read_text(encoding="utf-8")
    lines = len(text.splitlines())
    if lines < min_lines:
        return False, f"SHORT {name}: {lines} < {min_lines} (possible truncation)"
    if "PLACEHOLDER" in text and lines < 10:
        return False, f"PLACEHOLDER {name}"
    try:
        ast.parse(text)
    except SyntaxError as e:
        return False, f"SYNTAX {name}: {e}"
    return True, f"OK {name}: {lines} lines"

def main() -> int:
    fails = []
    print("TOOL INTEGRITY CHECK (truncation / syntax; do not invent)")
    for name, min_lines in EXPECTED.items():
        ok, msg = check_file(name, min_lines)
        print(msg)
        if not ok:
            fails.append(name)
    if fails:
        print(f"FAIL: {len(fails)} tools need attention ({', '.join(fails)})")
        return 1
    print("PASS: all checked tools meet minimum size and syntax")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
