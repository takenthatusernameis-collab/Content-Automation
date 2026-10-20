#!/usr/bin/env python3
"""Lock the mechanism-aligned hook suggestion tool.

Verifies output shape, presence of operational hook language (name the stall, concrete default, write the, install),
avoidance of anti-slop/weak patterns, reasonable word count, and that the tool writes nothing.
Does not scaffold, poll secrets, or modify any live packets.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
TOOL = TOOLS / "hook_suggest.py"


def fail(msg: str) -> int:
    print("HOOK SUGGEST CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("hook_suggest.py missing")

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
            "HOOK SUGGESTION",
            "mechanism:",
            "Suggested Hook WORDS",
            "paste into draft.md ## Hook",
            "quality_scan.py",
        ]
        for phrase in required:
            if phrase not in out:
                return fail(f"output missing required phrase: {phrase!r}")

        # Confirm operational hook language
        low = out.lower()
        operational = ["name the stall", "concrete", "write the", "install", "stall", "default", "before you open"]
        if not any(op in low for op in operational):
            return fail("missing expected operational hook language")

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
        body = out.split("Suggested Hook WORDS", 1)[-1] if "Suggested Hook WORDS" in out else out
        body_low = body.lower()
        for w in weak:
            if w in body_low:
                return fail(f"weak pattern leaked into output: {w}")

        # Confirm reasonable number of suggestions and word count roughly in range
        lines = [ln.strip() for ln in out.splitlines() if ln.strip() and ln[0].isdigit() and ". " in ln]
        if len(lines) < 3:
            return fail("fewer than 3 hook suggestions")
        for ln in lines:
            parts = ln.split(". ", 1)
            if len(parts) > 1:
                text = parts[1].split("  (")[0].strip()
                wc = len(text.split())
                if wc < 12 or wc > 45:
                    return fail(f"suggestion word count out of range ({wc}): {text[:60]}...")

        # Confirm no writes to the idea.md
        if idea.stat().st_mtime != before:
            return fail("hook_suggest.py modified idea.md")

    print("HOOK SUGGEST CONTRACT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
