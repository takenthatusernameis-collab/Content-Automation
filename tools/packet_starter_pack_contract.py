#!/usr/bin/env python3
"""Lock the packet starter pack consolidator.

Verifies it writes a local packet_starter.md containing spoken structure,
visual sequence, and install pack sections extracted only from idea.md
mechanism/problem/topic. Fail-closed on missing idea.md. No invented
claims. Does not modify packet content beyond the designated output.
Does not poll secrets or scaffold.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
TOOL = TOOLS / "packet_starter_pack.py"


def fail(msg: str) -> int:
    print("PACKET STARTER PACK CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("packet_starter_pack.py missing")

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

        proc = subprocess.run(
            [sys.executable, str(TOOL), str(packet)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if proc.returncode != 0:
            return fail(f"CLI exited {proc.returncode}: {proc.stderr}")

        out_path = packet / "packet_starter.md"
        if not out_path.is_file():
            return fail("packet_starter.md was not written")

        text = out_path.read_text(encoding="utf-8")
        required = [
            "# Packet Starter Pack (consolidated)",
            "## Spoken Structure",
            "### Hook",
            "### Payoff",
            "### Body Beats",
            "### CTA",
            "## Visual Sequence",
            "## Install Pack",
            "### Short assignment",
            "### Same-day steps",
            "### Verification checks",
            "Channel voice: calm, specific, operational",
            "Assignment, not a reply prompt",
            "text-card first",
            "install and verify same day",
        ]
        for phrase in required:
            if phrase not in text:
                return fail(f"output missing required phrase: {phrase!r}")

        # Confirm fields from idea.md appear (no invention)
        if "Close the extra tab before you open the work" not in text:
            return fail("topic not preserved")
        if "the extra tab is still open" not in text:
            return fail("problem not preserved")
        if "close that tab before the work file" not in text:
            return fail("mechanism not preserved")

        # Confirm no weak/anti-slop patterns
        weak = [
            "unlock your potential",
            "in today's fast-paced",
            "let's dive in",
            "without further ado",
            "you will learn",
            "work smarter",
        ]
        low = text.lower()
        for w in weak:
            if w in low:
                return fail(f"weak pattern leaked: {w}")

        # Fail-closed on missing idea.md
        bad_packet = Path(tmp) / "bad"
        bad_packet.mkdir()
        proc2 = subprocess.run(
            [sys.executable, str(TOOL), str(bad_packet)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if proc2.returncode == 0:
            return fail("tool succeeded without idea.md")
        if "idea.md missing" not in proc2.stderr and "FAIL: idea.md missing" not in proc2.stderr:
            return fail(f"expected fail-closed message, got: {proc2.stderr}")

    print("PACKET STARTER PACK CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
