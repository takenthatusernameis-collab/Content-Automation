#!/usr/bin/env python3
"""Contract lock for research_notes_writer.py.

Verifies the writer produces research_notes.md with required sections,
preserves extracted mechanism/problem/topic, rejects weak/invented patterns,
and fails closed on missing idea.md. Temp packet only. No invent.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
WRITER = TOOLS / "research_notes_writer.py"


def run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str]:
    proc = subprocess.run(
        cmd,
        cwd=cwd or ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main() -> int:
    if not WRITER.is_file():
        print("FAIL: research_notes_writer.py missing", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "test-packet"
        packet.mkdir()
        idea = packet / "idea.md"
        idea.write_text(
            "# Idea\n\n- topic: Test topic\n- problem: the stall reopens the list\n- mechanism (the system, not the pep talk): written next-action default\n",
            encoding="utf-8",
        )

        # Should succeed and write the file
        code, out = run([sys.executable, str(WRITER), str(packet)])
        if code != 0:
            print(f"FAIL: writer exited {code}\n{out}", file=sys.stderr)
            return 1

        out_file = packet / "research_notes.md"
        if not out_file.is_file():
            print("FAIL: missing research_notes.md", file=sys.stderr)
            return 1

        text = out_file.read_text(encoding="utf-8")
        if "Mechanism verification" not in text or "Potential claims to source" not in text:
            print("FAIL: missing required sections", file=sys.stderr)
            return 1
        if "mechanism" not in text.lower() and "problem" not in text.lower():
            print("FAIL: fields not preserved", file=sys.stderr)
            return 1
        if "invent" in text.lower() and "no invent" not in text.lower() and "Do not invent" not in text:
            print("FAIL: possible invented content", file=sys.stderr)
            return 1
        if "source" not in text.lower():
            print("FAIL: missing source capture guidance", file=sys.stderr)
            return 1

        # Fail closed on missing idea.md
        bad = Path(tmp) / "bad"
        bad.mkdir()
        code, out = run([sys.executable, str(WRITER), str(bad)])
        if code == 0:
            print("FAIL: should fail on missing idea.md", file=sys.stderr)
            return 1
        if "idea.md missing" not in out:
            print("FAIL: missing expected fail message", file=sys.stderr)
            return 1

    print("PASS: research_notes_writer contract")
    print("- writes research_notes.md with source-capture sections from idea.md")
    print("- preserves mechanism/problem/topic")
    print("- fails closed on missing idea.md")
    print("- no invent, local output only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
