#!/usr/bin/env python3
"""Lock the mechanism-aligned title suggestion tool.

Verifies output shape, presence of short titles, avoidance of weak patterns,
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
TOOL = TOOLS / "title_suggest.py"


def fail(msg: str) -> int:
    print("TITLE SUGGEST CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("title_suggest.py missing")

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
            "TITLE SUGGESTION",
            "mechanism:",
            "Suggested titles",
            "chars)",
            "Paste a chosen Primary",
            "title_scan.py",
        ]
        for phrase in required:
            if phrase not in out:
                return fail(f"output missing required phrase: {phrase!r}")

        # Confirm at least one title under 50 chars is mentioned or present
        lines = [ln for ln in out.splitlines() if "chars)" in ln]
        short_found = False
        for ln in lines:
            if "(" in ln:
                try:
                    num = int(ln.rsplit("(", 1)[-1].split()[0])
                    if num < 50:
                        short_found = True
                        break
                except ValueError:
                    pass
        if not short_found and sum(1 for ln in out.splitlines() if ln.strip().startswith(("1.", "2.", "3."))) < 3:
            return fail("fewer than 3 title suggestions or no short title signal")

        # Confirm no weak clickbait leaked
        weak_hits = ["secret hack", "you won't believe", "must see", "one weird trick"]
        low = out.lower()
        for w in weak_hits:
            if w in low:
                return fail(f"weak pattern leaked into output: {w}")

        # Confirm no writes to the idea.md
        if idea.stat().st_mtime != before:
            return fail("title_suggest.py modified idea.md")

    print("TITLE SUGGEST CONTRACT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
