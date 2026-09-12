#!/usr/bin/env python3
"""Unmapped lock for tools/words.py.

Catches a placeholder or emptied words.py (Run 076) and proves Grow/Cut
still print on temp drafts. Writes nothing under videos/. Not a reconstruct
wave. Not mapped in needed.py.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
WORDS = TOOLS / "words.py"
MIN_BYTES = 8000

BELOW_DRAFT = """# Script

## Hook (0:00–0:12)

WORDS: Morning starts by reopening the whole list again.

## Payoff promise

WORDS: A written next action stops the reopen.

## Beat 1 — reopen

WORDS: You scan every task because nothing is already chosen.

## Beat 2 — default

WORDS:

## Beat 3 — start

WORDS: Start the written line before you look at the rest.

## Beat 4 — protect

WORDS: Keep the default visible overnight.

## CTA

WORDS: Write tomorrow's first move before you close the laptop.
"""

ABOVE_PAD = " surplus " * 1600
ABOVE_DRAFT = f"""# Script

## Hook (0:00–0:12)

WORDS: Morning starts by reopening the whole list again tonight.

## Payoff promise

WORDS: A written next action stops the reopen loop.

## Beat 1 — reopen

WORDS:{ABOVE_PAD}

## Beat 2 — default

WORDS: Write one default.

## Beat 3 — start

WORDS: Start that line.

## Beat 4 — protect

WORDS: Keep it visible.

## CTA

WORDS: Write tomorrow first.
"""


def run_words(draft: Path, strict: bool = True) -> tuple[int, str]:
    cmd = [sys.executable, str(WORDS), str(draft)]
    if strict:
        cmd.append("--strict")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def main() -> int:
    failures: list[str] = []
    if not WORDS.is_file():
        print("WORDS CONTRACT FAIL")
        print(f"  - missing {WORDS}")
        return 1
    size = WORDS.stat().st_size
    print(f"words.py bytes: {size}")
    if size < MIN_BYTES:
        failures.append(f"words.py is {size} bytes; expected >= {MIN_BYTES}")
    body = WORDS.read_text(encoding="utf-8")
    for marker in (
        "def cut_line",
        "def grow_line",
        "def hook_delta_line",
        "def print_idea_lock_notes",
        "This command writes nothing.",
    ):
        if marker not in body:
            failures.append(f"words.py missing marker: {marker}")
    if "PLACEHOLDER" in body or body.strip() in {"see-next", "404: Not Found"}:
        failures.append("words.py looks like a placeholder")

    with tempfile.TemporaryDirectory(prefix="words-contract-") as tmp:
        tmp_path = Path(tmp)
        below = tmp_path / "below.md"
        above = tmp_path / "above.md"
        below.write_text(BELOW_DRAFT, encoding="utf-8")
        above.write_text(ABOVE_DRAFT, encoding="utf-8")

        code_b, out_b = run_words(below)
        print("--- below ---")
        print(out_b.strip() or "(no stdout)")
        if "Result: BELOW" not in out_b:
            failures.append("below draft should print Result: BELOW")
        if "Grow:" not in out_b:
            failures.append("below draft should print Grow")
        if "Cut:" in out_b:
            failures.append("below draft should not print Cut")
        if "Delta:" not in out_b:
            failures.append("below draft should print Delta")
        if "INFO" not in out_b:
            failures.append("below draft should print idea-lock INFO (or unavailable fallback)")
        if code_b != 2:
            failures.append(f"below --strict should exit 2, got {code_b}")

        code_a, out_a = run_words(above)
        print("--- above ---")
        print(out_a.strip() or "(no stdout)")
        if "Result: ABOVE" not in out_a:
            failures.append("above draft should print Result: ABOVE")
        if "Cut:" not in out_a:
            failures.append("above draft should print Cut")
        if "Grow:" in out_a:
            failures.append("above draft should not print Grow")
        if "INFO" not in out_a:
            failures.append("above draft should print idea-lock INFO (or unavailable fallback)")
        if code_a != 2:
            failures.append(f"above --strict should exit 2, got {code_a}")

    if failures:
        print("WORDS CONTRACT FAIL")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("WORDS CONTRACT PASS")
    print("This command writes nothing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
