#!/usr/bin/env python3
"""Lock the mechanism-aligned description suggestion tool.

Verifies output shape, presence of operational install language, avoidance of filler/bait patterns,
and that the tool writes nothing.
Does not scaffold, poll secrets, or modify any live packets.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
TOOL = TOOLS / "description_suggest.py"


def fail(msg: str) -> int:
    print("DESCRIPTION SUGGEST CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("description_suggest.py missing")

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
            "DESCRIPTION SUGGESTION",
            "mechanism:",
            "Suggested ## Description:",
            "under two minutes",
            "Paste into the ## Description section of publish.md",
            "description_scan.py",
        ]
        for phrase in required:
            if phrase not in out:
                return fail(f"output missing required phrase: {phrase!r}")

        # Confirm operational language present and no weak filler/bait
        low = out.lower()
        if "sticky note" not in low and "device note" not in low:
            return fail("missing operational install cue (sticky/device note)")
        if "stall" not in low:
            return fail("missing stall reference")

        weak_hits = [
            "in this video",
            "you will learn",
            "unlock your potential",
            "game changer",
            "smash the like",
            "hit subscribe",
            "don't forget to",
            "let me know",
        ]
        for w in weak_hits:
            if w in low:
                return fail(f"weak/filler pattern leaked into output: {w}")

        # Confirm no writes to the idea.md
        if idea.stat().st_mtime != before:
            return fail("description_suggest.py modified idea.md")

    print("DESCRIPTION SUGGEST CONTRACT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
