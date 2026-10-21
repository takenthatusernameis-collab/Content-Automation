#!/usr/bin/env python3
"""Lock the mechanism-aligned visual suggestion tool.

Verifies output shape, presence of operational visual language (close on, sticky note, list, desk, note placement, stall or default),
avoidance of anti-slop/weak patterns, reasonable word count for stage directions (8-45), and that the tool writes nothing.
Does not scaffold, poll secrets, or modify any live packets.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
TOOL = TOOLS / "visual_suggest.py"


def fail(msg: str) -> int:
    print("VISUAL SUGGEST CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("visual_suggest.py missing")

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
            "VISUAL SUGGESTION",
            "mechanism:",
            "Suggested VISUAL:",
            "italic stage directions",
            "Each direction must show the stall or the installed default",
        ]
        for phrase in required:
            if phrase not in out:
                return fail(f"output missing required phrase: {phrase!r}")

        # Confirm operational visual language
        low = out.lower()
        operational = ["close on", "sticky note", "list", "desk", "note", "stall", "default", "cursor", "hand places"]
        if not any(op in low for op in operational):
            return fail("missing expected operational visual language")

        # Confirm no weak/anti-slop patterns leaked
        weak = [
            "unlock your potential",
            "in today's fast-paced",
            "let's dive in",
            "the key is",
            "in this video",
            "you will learn",
            "work smarter",
            "stock footage",
            "person thinking",
            "laptop closeup",
        ]
        body = out.split("Suggested VISUAL:", 1)[-1] if "Suggested VISUAL:" in out else out
        body_low = body.lower()
        for w in weak:
            if w in body_low:
                return fail(f"weak pattern leaked into output: {w}")

        # Confirm reasonable number of suggestions and word count in range
        lines = [ln.strip() for ln in out.splitlines() if ln.strip() and ln[0].isdigit() and ". *" in ln]
        if len(lines) < 3:
            return fail("fewer than 3 visual suggestions")
        for ln in lines:
            # Extract text between * and * or before (words)
            if "*" in ln:
                text = ln.split("*", 2)[1] if ln.count("*") >= 2 else ln
                words = text.split()
                wc = len(words)
                if wc < 8 or wc > 45:
                    return fail(f"suggestion word count out of range ({wc}): {text[:60]}...")

        # Confirm no writes to the idea.md
        if idea.stat().st_mtime != before:
            return fail("visual_suggest.py modified idea.md")

    print("VISUAL SUGGEST CONTRACT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
