#!/usr/bin/env python3
"""Lock the mechanism-aligned tags suggestion tool.

Verifies output shape, presence of specific operational tags, avoidance of weak/generic patterns,
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
TOOL = TOOLS / "tags_suggest.py"


def fail(msg: str) -> int:
    print("TAGS SUGGEST CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("tags_suggest.py missing")

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
            "TAGS SUGGESTION",
            "mechanism:",
            "Suggested ## Tags",
            "Paste into the ## Tags section",
            "tags_scan.py",
        ]
        for phrase in required:
            if phrase not in out:
                return fail(f"output missing required phrase: {phrase!r}")

        # Confirm at least 5 tags (lines starting with - )
        tag_lines = [ln for ln in out.splitlines() if ln.strip().startswith("- ")]
        if len(tag_lines) < 5:
            return fail(f"fewer than 5 tag suggestions: {len(tag_lines)}")

        # Confirm no weak patterns leaked
        weak_hits = ["video", "youtube", "tutorial", "how to", "subscribe", "free", "best", "amazing", "viral", "secret", "hack"]
        low = out.lower()
        for w in weak_hits:
            if w in low:
                return fail(f"weak pattern leaked into output: {w}")

        # Confirm operational language present (examples from the tool)
        operational = ["sticky note", "under two minutes", "written next action", "name the stall"]
        if not any(op in low for op in operational):
            return fail("missing expected operational install language")

        # Confirm no writes to the idea.md
        if idea.stat().st_mtime != before:
            return fail("tags_suggest.py modified idea.md")

    print("TAGS SUGGEST CONTRACT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
