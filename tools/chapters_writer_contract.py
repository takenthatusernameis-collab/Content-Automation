#!/usr/bin/env python3
"""Contract for tools/chapters_writer.py.

Verifies:
- Fails closed (exit 2) on missing idea.md.
- Writes chapters.md with required sections when idea.md has mechanism or problem.
- Preserves extracted fields in the output.
- Contains ## YouTube lines with 0:00 first line and operational titles.
- Does not invent claims or statistics.
No packet content edits by design. Text stays local.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent


def run_writer(packet: Path, force: bool = False) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(TOOLS / "chapters_writer.py"), str(packet)]
    if force:
        cmd.append("--force")
    return subprocess.run(cmd, capture_output=True, text=True)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "test-packet"
        packet.mkdir()

        # Missing idea.md must fail closed.
        result = run_writer(packet)
        if result.returncode != 2:
            print(f"FAIL: expected exit 2 on missing idea.md, got {result.returncode}")
            print(result.stderr)
            return 1

        # Minimal idea.md with mechanism and problem.
        idea = packet / "idea.md"
        idea.write_text(
            "topic: morning start\n"
            "problem: they reopen the whole work list every morning\n"
            "mechanism: written next-action default\n",
            encoding="utf-8",
        )

        result = run_writer(packet)
        if result.returncode != 0:
            print(f"FAIL: expected exit 0, got {result.returncode}")
            print(result.stdout)
            print(result.stderr)
            return 1

        out = packet / "chapters.md"
        if not out.is_file():
            print("FAIL: chapters.md not written")
            return 1

        text = out.read_text(encoding="utf-8")
        required = [
            "# Chapters",
            "## YouTube lines",
            "0:00",
            "Hook:",
            "Payoff:",
            "Beat 1:",
            "CTA:",
            "written next-action default",
            "they reopen the whole work list every morning",
        ]
        for req in required:
            if req not in text:
                print(f"FAIL: missing required fragment: {req}")
                return 1

        # No invented statistics.
        if any(x in text.lower() for x in ("%", "percent", "study shows", "research finds")):
            print("FAIL: invented claim-like text")
            return 1

        print("PASS: chapters_writer contract")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
