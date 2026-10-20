#!/usr/bin/env python3
"""Lock the mechanism-aligned chapters suggestion tool.

Verifies output shape, presence of operational chapter language (0:00 start, concrete default, under-two-minute install, same-day test),
avoidance of weak titles, and that the tool writes nothing.
Does not scaffold, poll secrets, or modify any live packets.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
TOOL = TOOLS / "chapters_suggest.py"


def fail(msg: str) -> int:
    print("CHAPTERS SUGGEST CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("chapters_suggest.py missing")

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
            "CHAPTERS SUGGESTION",
            "mechanism:",
            "Suggested YouTube lines",
            "paste into chapters.md",
            "chapters_scan.py",
            "0:00",
        ]
        for phrase in required:
            if phrase not in out:
                return fail(f"output missing required phrase: {phrase!r}")

        # Confirm operational chapter language
        low = out.lower()
        operational = ["name the stall", "concrete default", "under-two-minute", "same-day test", "write the"]
        if not any(op in low for op in operational):
            return fail("missing expected operational chapter language")

        # Confirm no weak titles leaked
        weak = ["intro", "outro", "hook", "cta", "subscribe", "what you will learn", "in this video", "let's dive in"]
        body = out.split("Suggested YouTube lines", 1)[-1] if "Suggested YouTube lines" in out else out
        body_low = body.lower()
        for w in weak:
            if w in body_low:
                return fail(f"weak title pattern leaked into output: {w}")

        # Confirm starts with 0:00 and has reasonable lines
        lines = [ln.strip() for ln in out.splitlines() if ln.strip() and ":" in ln and ln.strip()[0].isdigit()]
        if not any(ln.startswith("0:00") for ln in lines):
            return fail("no 0:00 chapter line")
        if len(lines) < 4:
            return fail("fewer than 4 chapter lines")

        # Confirm no writes to the idea.md
        if idea.stat().st_mtime != before:
            return fail("chapters_suggest.py modified idea.md")

    print("CHAPTERS SUGGEST CONTRACT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
