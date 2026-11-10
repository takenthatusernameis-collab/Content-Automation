#!/usr/bin/env python3
"""Lock the next-from-decision tool.

Verifies fail-closed behavior on missing file (exit 1, FAIL),
invalid/missing decision or reason/source (exit 0, HOLD),
and presence of direction skeleton on a filled keep decision.
Soft only. No invent of topics or decisions.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "next_from_decision.py"


def fail(msg: str) -> int:
    print("NEXT FROM DECISION CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("next_from_decision.py missing")

    # Case 1: missing file -> FAIL, exit 1
    with tempfile.TemporaryDirectory() as tmp:
        missing = Path(tmp) / "no-such.json"
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(missing)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=15,
        )
        if proc.returncode != 1:
            return fail(f"missing-file CLI exited {proc.returncode} (expected 1)")
        out = (proc.stdout or "") + (proc.stderr or "")
        if "FAIL" not in out or "not found" not in out.lower():
            return fail("missing FAIL language for absent file")

    # Case 2: invalid decision -> HOLD, exit 0
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / "bad.json"
        bad.write_text(json.dumps({"decision": "maybe", "reason": "x", "source": "y"}), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(bad)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=15,
        )
        if proc.returncode != 0:
            return fail(f"invalid-decision CLI exited {proc.returncode} (expected 0)")
        out = proc.stdout
        if "HOLD" not in out or "not in" not in out:
            return fail("missing HOLD language for invalid decision")

    # Case 3: missing reason -> HOLD, exit 0
    with tempfile.TemporaryDirectory() as tmp:
        incomplete = Path(tmp) / "incomplete.json"
        incomplete.write_text(json.dumps({"decision": "keep", "reason": "", "source": "documented"}), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(incomplete)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=15,
        )
        if proc.returncode != 0:
            return fail(f"incomplete CLI exited {proc.returncode} (expected 0)")
        out = proc.stdout
        if "HOLD" not in out or "reason or source missing" not in out:
            return fail("missing HOLD language for incomplete decision")

    # Case 4: valid keep -> PASS phrases, exit 0
    with tempfile.TemporaryDirectory() as tmp:
        good = Path(tmp) / "good.json"
        good.write_text(
            json.dumps({
                "decision": "keep",
                "reason": "The change improved average view duration as measured.",
                "source": "YouTube Analytics after observation window",
                "primary_metric": "average_view_duration"
            }),
            encoding="utf-8",
        )
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(good)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=15,
        )
        if proc.returncode != 0:
            return fail(f"valid-keep CLI exited {proc.returncode} (expected 0)")
        out = proc.stdout
        required = (
            "NEXT FROM DECISION",
            "decision: keep",
            "Keep the tested change",
            "Next commands",
            "Do not invent metrics",
        )
        missing_phrases = [p for p in required if p not in out]
        if missing_phrases:
            return fail(f"missing required phrases on valid keep: {missing_phrases}")

    print("NEXT FROM DECISION CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
