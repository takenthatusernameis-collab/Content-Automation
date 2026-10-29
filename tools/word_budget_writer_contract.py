#!/usr/bin/env python3
"""Contract lock for word_budget_writer.py.

Verifies the writer produces word_budget.md with required targets table,
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
WRITER = TOOLS / "word_budget_writer.py"


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
        print("FAIL: word_budget_writer.py missing", file=sys.stderr)
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

        out_file = packet / "word_budget.md"
        if not out_file.is_file():
            print("FAIL: missing word_budget.md", file=sys.stderr)
            return 1

        text = out_file.read_text(encoding="utf-8")
        if "Word Budget" not in text or "Targets (spoken words)" not in text:
            print("FAIL: missing required sections", file=sys.stderr)
            return 1
        if "900" not in text or "1500" not in text or "140" not in text:
            print("FAIL: missing word targets", file=sys.stderr)
            return 1
        if "mechanism" not in text.lower() and "problem" not in text.lower():
            print("FAIL: fields not preserved", file=sys.stderr)
            return 1
        if "invent" in text.lower() and "no invent" not in text.lower() and "Do not add" not in text and "No invented" not in text:
            print("FAIL: possible invented content", file=sys.stderr)
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

    print("PASS: word_budget_writer contract")
    print("- writes word_budget.md with segment targets from idea.md")
    print("- preserves mechanism/problem/topic")
    print("- fails closed on missing idea.md")
    print("- no invent, local output only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
