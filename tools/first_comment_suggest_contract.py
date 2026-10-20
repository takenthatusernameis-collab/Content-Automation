#!/usr/bin/env python3
"""Lock the mechanism-aligned first-comment suggestion tool.

Verifies output shape, presence of operational install language (sticky/device note, assignment, before next tab),
avoidance of engagement bait or reply prompts, and that the tool writes nothing.
Does not scaffold, poll secrets, or modify any live packets.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
TOOL = TOOLS / "first_comment_suggest.py"


def fail(msg: str) -> int:
    print("FIRST COMMENT SUGGEST CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("first_comment_suggest.py missing")

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
            "FIRST COMMENT SUGGESTION",
            "mechanism:",
            "Suggested first comment",
            "Paste into the ## First comment section",
            "first_comment_scan.py",
        ]
        for phrase in required:
            if phrase not in out:
                return fail(f"output missing required phrase: {phrase!r}")

        # Confirm operational install language
        low = out.lower()
        operational = ["sticky note", "device note", "assignment", "before you open the next tab", "that is the whole install"]
        if not any(op in low for op in operational):
            return fail("missing expected operational install language")

        # Confirm no engagement bait or reply prompts (ignore the descriptive header)
        body = out.split("Suggested first comment", 1)[-1] if "Suggested first comment" in out else out
        body_low = body.lower()
        bait = ["like and subscribe", "comment below", "what do you think", "drop a comment", "let me know in the comments", "reply with"]
        for b in bait:
            if b in body_low:
                return fail(f"engagement bait leaked into output: {b}")

        # Confirm no writes to the idea.md
        if idea.stat().st_mtime != before:
            return fail("first_comment_suggest.py modified idea.md")

    print("FIRST COMMENT SUGGEST CONTRACT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
