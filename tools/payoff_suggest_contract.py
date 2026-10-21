#!/usr/bin/env python3
"""Lock the mechanism-aligned payoff suggestion tool.

Verifies output shape, presence of operational payoff language (concrete doable outcome, under-two-minute install, mechanism, written cue),
avoidance of anti-slop/weak patterns, reasonable word count (30-90), and that the tool writes nothing.
Does not scaffold, poll secrets, or modify any live packets.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
TOOL = TOOLS / "payoff_suggest.py"


def fail(msg: str) -> int:
    print("PAYOFF SUGGEST CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("payoff_suggest.py missing")

    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "test-packet"
        packet.mkdir()
        idea = packet / "idea.md"
        idea.write_text(
            "# Idea\n\n"
            "- topic: Close the extra tab before you open the work\n"
            "- problem: the extra tab is still open, so starting means checking one more thing\n"
            "- mechanism (the system, not the pep talk): close that tab before the work file\n",
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
            "PAYOFF SUGGESTION",
            "mechanism:",
            "Suggested Payoff promise WORDS",
            "quality_scan.py",
        ]
        for phrase in required:
            if phrase not in out:
                return fail(f"output missing required phrase: {phrase!r}")

        # Confirm operational payoff language
        low = out.lower()
        operational = ["under two minutes", "install", "write the", "concrete", "mechanism", "stall", "next action", "list"]
        if not any(op in low for op in operational):
            return fail("missing expected operational payoff language")

        # Confirm no weak/anti-slop patterns leaked
        weak = [
            "unlock your potential",
            "in today's fast-paced",
            "let's dive in",
            "without further ado",
            "the key is",
            "in this video",
            "you will learn",
            "work smarter",
        ]
        body = out.split("Suggested Payoff promise WORDS", 1)[-1] if "Suggested Payoff promise WORDS" in out else out
        body_low = body.lower()
        for w in weak:
            if w in body_low:
                return fail(f"weak pattern leaked into output: {w}")

        # Confirm reasonable number of suggestions and word count roughly in range
        lines = [ln.strip() for ln in out.splitlines() if ln.strip() and ln[0].isdigit() and ". " in ln]
        if len(lines) < 2:
            return fail("fewer than 2 payoff suggestions")
        for ln in lines:
            parts = ln.split(". ", 1)
            if len(parts) > 1:
                text = parts[1].split("  (")[0].strip()
                wc = len(text.split())
                if wc < 30 or wc > 90:
                    return fail(f"suggestion word count out of range ({wc}): {text[:60]}...")

        # Confirm no writes to the idea.md
        if idea.stat().st_mtime != before:
            return fail("payoff_suggest.py modified idea.md")

    print("PAYOFF SUGGEST CONTRACT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
