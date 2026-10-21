#!/usr/bin/env python3
"""Lock the experiment hypothesis suggestion tool.

Verifies output shape, presence of operational hypothesis language (mechanism, change type, prediction without invented numbers),
avoidance of invented baselines/results/decisions, reasonable template count, and that the tool writes nothing.
Does not scaffold, poll secrets, or modify any live packets.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
TOOL = TOOLS / "experiment_hypothesis_suggest.py"


def fail(msg: str) -> int:
    print("EXPERIMENT HYPOTHESIS SUGGEST CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("experiment_hypothesis_suggest.py missing")

    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "test-packet"
        packet.mkdir()
        idea = packet / "idea.md"
        idea.write_text(
            "# Idea\n\n"
            "- topic: Close the extra tab before you open the work\n"
            "- problem: the extra tab is still open, so starting means checking one more thing\n"
            "- mechanism (the system, not the pep talk): close that tab before the work file\n"
            "- hook: name the stall immediately\n",
            encoding="utf-8",
        )
        before = idea.stat().st_mtime

        proc = subprocess.run(
            [sys.executable, str(TOOL), str(packet)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if proc.returncode != 0:
            return fail(f"CLI exited {proc.returncode}: {proc.stderr}")
        out = proc.stdout
        required = [
            "EXPERIMENT HYPOTHESIS SUGGEST",
            "detected_change:",
            "mechanism:",
            "Recommended hypothesis templates",
            "Do not invent a numeric baseline",
            "RECOMMENDED NEXT",
        ]
        for phrase in required:
            if phrase not in out:
                return fail(f"output missing required phrase: {phrase!r}")

        # Confirm operational hypothesis language
        low = out.lower()
        operational = ["mechanism", "change", "retention", "duration", "compared", "improve", "raise"]
        if not any(op in low for op in operational):
            return fail("missing expected operational hypothesis language")

        # Confirm no invented numbers or decisions leaked
        weak = [
            "baseline is 42",
            "result was",
            "we decided to keep",
            "increase by 15%",
            "ctr of 3.2",
        ]
        body = out.split("Recommended hypothesis templates", 1)[-1] if "Recommended hypothesis templates" in out else out
        body_low = body.lower()
        for w in weak:
            if w in body_low:
                return fail(f"invented pattern leaked into output: {w}")

        # Confirm reasonable number of templates
        lines = [ln for ln in out.splitlines() if ln.strip().startswith("- ") and "Recommended" not in ln and "RECOMMENDED" not in ln and "allowed_changes" not in ln]
        if len(lines) < 2:
            return fail("fewer than 2 hypothesis templates")

        # Confirm no writes to the idea.md
        if idea.stat().st_mtime != before:
            return fail("experiment_hypothesis_suggest.py modified idea.md")

    print("EXPERIMENT HYPOTHESIS SUGGEST CONTRACT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
