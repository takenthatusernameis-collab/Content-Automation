#!/usr/bin/env python3
"""Lock the mechanism-aligned CTA suggestion tool.

Verifies output shape, presence of operational CTA language (write the exact words, sticky note, under two minutes, install the default, mechanism),
avoidance of anti-slop/weak patterns, reasonable word count for spoken CTA (15-80), and that the tool writes nothing.
Does not scaffold, poll secrets, or modify any live packets.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
TOOL = TOOLS / "cta_suggest.py"


def fail(msg: str) -> int:
    print("CTA SUGGEST CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("cta_suggest.py missing")

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
            "CTA SUGGESTION",
            "mechanism:",
            "Suggested spoken CTA WORDS:",
            "Suggested end-screen / final line:",
            "draft.md",
            "end_screen_scan.py",
        ]
        for phrase in required:
            if phrase not in out:
                return fail(f"output missing required phrase: {phrase!r}")

        # Confirm operational CTA language
        low = out.lower()
        operational = ["write the", "sticky note", "two minutes", "install", "default", "mechanism", "before you open"]
        if not any(op in low for op in operational):
            return fail("missing expected operational CTA language")

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
            "many people",
            "most people",
            "subscribe",
            "like and",
            "smash that",
        ]
        body = out.split("Suggested spoken CTA WORDS:", 1)[-1] if "Suggested spoken CTA WORDS:" in out else out
        body_low = body.lower()
        for w in weak:
            if w in body_low:
                return fail(f"weak pattern leaked into output: {w}")

        # Confirm reasonable word count for the spoken CTA
        spoken_section = ""
        if "Suggested spoken CTA WORDS:" in out and "Suggested end-screen" in out:
            spoken_section = out.split("Suggested spoken CTA WORDS:", 1)[1].split("Suggested end-screen", 1)[0]
        words = [w for w in spoken_section.split() if w]
        wc = len(words)
        if wc < 15 or wc > 80:
            return fail(f"spoken CTA word count out of range ({wc})")

        # Confirm no writes to the idea.md
        if idea.stat().st_mtime != before:
            return fail("cta_suggest.py modified idea.md")

    print("CTA SUGGEST CONTRACT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
