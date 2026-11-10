#!/usr/bin/env python3
"""Lock the feedback review brief tool.

Verifies fail-closed behavior on missing/invalid collected state,
presence of classification counts, hypothesis candidates, metric suggestions,
and that the tool writes nothing. Soft only. No invent of comments or decisions.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "feedback_review_brief.py"


def fail(msg: str) -> int:
    print("FEEDBACK REVIEW BRIEF CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("feedback_review_brief.py missing")

    # Case 1: no feedback_state.json -> HOLD
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "no-state"
        packet.mkdir()
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(packet)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=15,
        )
        if proc.returncode != 0:
            return fail(f"no-state CLI exited {proc.returncode}")
        out = proc.stdout
        if "HOLD" not in out or "no feedback state" not in out.lower():
            return fail("missing HOLD language for absent feedback_state.json")

    # Case 2: collected state with comments -> PASS with signals
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "with-comments"
        packet.mkdir()
        state = {
            "gate": "COLLECTED",
            "attempted_fetch": True,
            "comments": [
                {"text": "What does that mean? I don't understand."},
                {"text": "How does this work exactly?"},
                {"text": "Please make a follow-up on this."},
            ],
        }
        state_path = packet / "feedback_state.json"
        state_path.write_text(json.dumps(state), encoding="utf-8")
        before = state_path.stat().st_mtime

        proc = subprocess.run(
            [sys.executable, str(TOOL), str(packet)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=15,
        )
        if proc.returncode != 0:
            return fail(f"with-comments CLI exited {proc.returncode}: {proc.stderr}")
        out = proc.stdout
        required = [
            "FEEDBACK REVIEW BRIEF",
            "Classified",
            "Hypothesis candidates",
            "Metric suggestions",
            "PASS",
            "Do not invent",
        ]
        for phrase in required:
            if phrase not in out:
                return fail(f"output missing required phrase: {phrase!r}")

        # No writes
        if state_path.stat().st_mtime != before:
            return fail("feedback_review_brief.py modified feedback_state.json")

        # No invented metrics or decisions
        low = out.lower()
        weak = ["baseline is ", "we decided", "increase by", "ctr of"]
        for w in weak:
            if w in low:
                return fail(f"invented pattern leaked: {w}")

    print("FEEDBACK REVIEW BRIEF CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
