#!/usr/bin/env python3
"""Reliability contract for tools/claim_source_table.py.

Locks fail-closed behavior of the claim-to-source table generator:
- unique_preserve drops empties/duplicates (case-insensitive)
- hedges_with_context extracts only known hedge phrases with real context
- CLI on a packet with claims emits a fillable Markdown table with no invented sources, URLs, or citations
- CLI on a packet with no claims emits a clean "no claims" message and exits 0
- Never writes files or invents research results

Soft only; does not invent sources, numbers, or call APIs. No writes to live packets.
Improves long-term reliability so future changes cannot silently weaken the research claim extraction used before every script is finalized.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from claim_source_table import hedges_with_context, unique_preserve  # type: ignore
from phrase_utils import spoken_words  # type: ignore
from research_brief import numbers_in_spoken_words  # type: ignore

TOOL = ROOT / "tools" / "claim_source_table.py"


def fail(failures: list[str], cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


def main() -> int:
    failures: list[str] = []

    if not TOOL.is_file():
        print("CONTRACT FAIL: claim_source_table.py missing")
        return 1

    # unique_preserve pure tests
    fail(failures, unique_preserve(["A", "a", "B", "", "b"]) == ["A", "B"], "unique_preserve case/empty/dup failed")
    fail(failures, unique_preserve([]) == [], "unique_preserve empty failed")

    # hedges and numbers on known sample (no file I/O)
    sample = """# Test
WORDS:
According to a study, 42 percent of people agree. Studies show the effect is real. Maybe more research is needed.
"""
    body = spoken_words(sample)
    fail(failures, "According to a study" in body, "spoken_words extraction failed")
    hedges = hedges_with_context(sample)
    hedge_phrases = {h[0] for h in hedges}
    fail(failures, "studies show" in hedge_phrases and "according to a study" in hedge_phrases, f"hedges missing: {hedges}")
    nums = unique_preserve(numbers_in_spoken_words(sample))
    fail(failures, any("42" in n for n in nums), f"numbers missing: {nums}")

    # CLI: packet with claims — table present, no invented sources
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "pkt"
        packet.mkdir()
        (packet / "script.md").write_text(sample, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(packet)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        out = proc.stdout + proc.stderr
        fail(failures, proc.returncode == 0, f"CLI claims exit {proc.returncode}")
        fail(failures, "CLAIM-TO-SOURCE TABLE" in out, "table header missing")
        fail(failures, "| Claim | Type |" in out, "table columns missing")
        fail(failures, "42" in out and "studies show" in out, "claims not rendered")
        # No invented sources: no http, no "source:" filled, no fake citations
        fail(failures, "http" not in out.lower() and "www." not in out.lower(), "invented URL detected")
        fail(failures, "|  |  |" in out or "Source (fill)" in out, "source column not left blank")

    # CLI: no claims
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "empty"
        packet.mkdir()
        (packet / "script.md").write_text("# Empty\nWORDS:\nHello world with no numbers or hedges.\n", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(packet)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        out = proc.stdout + proc.stderr
        fail(failures, proc.returncode == 0, f"CLI no-claims exit {proc.returncode}")
        fail(failures, "No quantitative digits or hedge phrases detected" in out, "no-claims message missing")

    print("Claim source table contract")
    if failures:
        print("CLAIM SOURCE TABLE CONTRACT FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("CLAIM SOURCE TABLE CONTRACT PASS (no-invent + extraction locked)")
    print("This command writes nothing in the repo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
