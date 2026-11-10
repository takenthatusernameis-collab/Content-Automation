#!/usr/bin/env python3
"""Lock the feedback topic suggest tool.

Verifies fail-closed behavior on missing state (exit 2, HOLD),
presence of candidate topic rows when request comments exist,
NO_REQUEST_SIGNALS when none, and that the tool writes nothing.
Soft only. No invent of comments or topics.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "feedback_topic_suggest.py"


def fail(msg: str) -> int:
    print("FEEDBACK TOPIC SUGGEST CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("feedback_topic_suggest.py missing")

    # Case 1: no feedback_state.json -> HOLD, exit 2
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
        if proc.returncode != 2:
            return fail(f"no-state CLI exited {proc.returncode} (expected 2)")
        out = proc.stdout
        if "HOLD" not in out or "no feedback_state.json" not in out:
            return fail("missing HOLD language for absent feedback_state.json")

    # Case 2: collected with request comments -> candidates, exit 0
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "with-request"
        packet.mkdir()
        state = {
            "gate": "COLLECTED",
            "attempted_fetch": True,
            "comments": [
                {"text": "Please make a video on automating the morning start."},
                {"text": "Can you make a follow-up on the edge cases."},
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
            return fail(f"with-request CLI exited {proc.returncode}: {proc.stderr}")
        out = proc.stdout
        required = [
            "CANDIDATE TOPIC ROWS",
            "working_title",
            "one_line",
            "source_comment",
            "Do not invent",
        ]
        for phrase in required:
            if phrase not in out:
                return fail(f"output missing required phrase: {phrase!r}")

        if state_path.stat().st_mtime != before:
            return fail("feedback_topic_suggest.py modified feedback_state.json")

    # Case 3: collected but no request class -> NO_REQUEST_SIGNALS, exit 0
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "no-request"
        packet.mkdir()
        state = {
            "gate": "COLLECTED",
            "attempted_fetch": True,
            "comments": [
                {"text": "Great video, thanks!"},
                {"text": "This was helpful."},
            ],
        }
        (packet / "feedback_state.json").write_text(json.dumps(state), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(packet)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=15,
        )
        if proc.returncode != 0:
            return fail(f"no-request CLI exited {proc.returncode}")
        if "NO_REQUEST_SIGNALS" not in proc.stdout:
            return fail("missing NO_REQUEST_SIGNALS for non-request comments")

    print("FEEDBACK TOPIC SUGGEST CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
