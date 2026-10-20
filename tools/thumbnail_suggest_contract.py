#!/usr/bin/env python3
"""Lock the mechanism-aligned thumbnail suggestion tool.

Verifies output shape, presence of operational thumbnail language (name the stall, concrete default, same-day install, write the),
avoidance of clickbait patterns, short length, and that the tool writes nothing.
Does not scaffold, poll secrets, or modify any live packets.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
TOOL = TOOLS / "thumbnail_suggest.py"


def fail(msg: str) -> int:
    print("THUMBNAIL SUGGEST CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("thumbnail_suggest.py missing")

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
            "THUMBNAIL SUGGESTION",
            "mechanism:",
            "Suggested thumbnail text",
            "paste into publish.md",
            "thumbnail_scan.py",
        ]
        for phrase in required:
            if phrase not in out:
                return fail(f"output missing required phrase: {phrase!r}")

        # Confirm operational thumbnail language
        low = out.lower()
        operational = ["name the stall", "concrete default", "same-day", "write the", "install", "one default"]
        if not any(op in low for op in operational):
            return fail("missing expected operational thumbnail language")

        # Confirm no clickbait leaked into suggestions
        weak = ["you won't believe", "must watch", "shocking", "secret hack", "this changes everything", "one weird trick", "will shock you", "don't miss", "watch till the end"]
        body = out.split("Suggested thumbnail text", 1)[-1] if "Suggested thumbnail text" in out else out
        body_low = body.lower()
        for w in weak:
            if w in body_low:
                return fail(f"clickbait pattern leaked into output: {w}")

        # Confirm reasonable number of suggestions and short length
        lines = [ln.strip() for ln in out.splitlines() if ln.strip() and ln[0].isdigit() and ". " in ln]
        if len(lines) < 3:
            return fail("fewer than 3 thumbnail suggestions")
        for ln in lines:
            # extract text after number.
            parts = ln.split(". ", 1)
            if len(parts) > 1:
                text = parts[1].split("  (")[0].strip()
                if len(text.split()) > 8:
                    return fail(f"suggestion too long: {text}")

        # Confirm no writes to the idea.md
        if idea.stat().st_mtime != before:
            return fail("thumbnail_suggest.py modified idea.md")

    print("THUMBNAIL SUGGEST CONTRACT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
