#!/usr/bin/env python3
"""Lock the mechanism-aligned end-screen / CTA suggestion tool.

Verifies output shape, presence of operational CTA language (concrete default, name the stall, same-day install, write the),
avoidance of engagement-bait patterns, and that the tool writes nothing.
Does not scaffold, poll secrets, or modify any live packets.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
TOOL = TOOLS / "end_screen_suggest.py"


def fail(msg: str) -> int:
    print("END SCREEN SUGGEST CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("end_screen_suggest.py missing")

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
            "END SCREEN / CTA SUGGESTION",
            "mechanism:",
            "Suggested end-screen / final CTA",
            "paste into publish.md",
            "end_screen_scan.py",
        ]
        for phrase in required:
            if phrase not in out:
                return fail(f"output missing required phrase: {phrase!r}")

        # Confirm operational CTA language
        low = out.lower()
        operational = ["name the stall", "concrete default", "same-day", "write the", "install the"]
        if not any(op in low for op in operational):
            return fail("missing expected operational CTA language")

        # Confirm no engagement bait leaked into suggestions
        weak = ["smash the like", "subscribe for", "leave a comment", "what do you think", "hit the", "ring the bell"]
        body = out.split("Suggested end-screen / final CTA", 1)[-1] if "Suggested end-screen / final CTA" in out else out
        body_low = body.lower()
        for w in weak:
            if w in body_low:
                return fail(f"engagement-bait pattern leaked into output: {w}")

        # Confirm reasonable number of suggestions
        lines = [ln.strip() for ln in out.splitlines() if ln.strip() and ln[0].isdigit() and ". " in ln]
        if len(lines) < 2:
            return fail("fewer than 2 CTA suggestions")

        # Confirm no writes to the idea.md
        if idea.stat().st_mtime != before:
            return fail("end_screen_suggest.py modified idea.md")

    print("END SCREEN SUGGEST CONTRACT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
