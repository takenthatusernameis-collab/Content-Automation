#!/usr/bin/env python3
"""Extract actionable revision signals from strict scanners.

Runs the key no-write strict scanners (from quality, visual, and metadata
prep suites) and extracts only the hit/FAIL lines so agents and humans can
see exactly what needs revision without reading full suite output.
Does not invent text, write packet files, or poll secrets.
Reduces labor of digging through long scanner output on every future packet.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

# Scanners that produce useful revision signals under --strict
SCANNERS = [
    ("quality_scan.py", ["--strict"]),
    ("claim_scan.py", ["--strict"]),
    ("cadence_repetition_scan.py", ["--strict"]),
    ("mechanism_align_scan.py", ["--strict"]),
    ("thumbnail_scan.py", ["--strict"]),
    ("title_scan.py", ["--strict"]),
    ("visual_readability_check.py", []),  # no --strict in some
    ("description_scan.py", ["--strict"]),
    ("tags_scan.py", ["--strict"]),
    ("first_comment_scan.py", ["--strict"]),
    ("chapters_scan.py", ["--strict"]),
    ("end_screen_scan.py", ["--strict"]),
]


def run_scanner(script: str, extra: list[str], packet: str) -> tuple[int, str]:
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path), packet] + extra
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=30)
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out.strip()
    except Exception as e:
        return 1, f"EXCEPTION: {e}"


def extract_signals(output: str) -> list[str]:
    """Pull lines that look like hits, missing, bait, LONG, REPEATED, etc."""
    signals = []
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        low = line.lower()
        if any(k in low for k in (
            "hits ", "missing:", "bait:", "long", "repeated_", "status: fail",
            "overall: fail", "warn", "delta:", "clear", "aligned"
        )):
            # Prefer the informative ones
            if "hits:" in low or "missing:" in low or "bait:" in low or "long" in low or "repeated" in low:
                signals.append(line)
            elif "status:" in low and "fail" in low:
                signals.append(line)
    return signals


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: revision_signals.py PACKET", file=sys.stderr)
        return 1
    packet = sys.argv[1]
    path = Path(packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("REVISION SIGNALS (extracted from strict scanners; no invent, no write)")
    print(f"packet: {path.name}")
    print("Only hit/FAIL lines shown. Full suite output remains available via *_prep_suite.py.")
    print("=" * 72)
    print()

    any_signal = False
    for script, extra in SCANNERS:
        rc, output = run_scanner(script, extra, str(path))
        signals = extract_signals(output)
        if signals or rc != 0:
            any_signal = True
            print(f"## {script} (exit {rc})")
            if signals:
                for s in signals[:8]:  # cap per scanner
                    print(f"  {s}")
            elif rc != 0:
                print(f"  non-zero exit; see full output via suite")
            print()

    print("=" * 72)
    if any_signal:
        print("overall: SIGNALS_PRESENT (revision recommended before promotion)")
        print("These are the concrete items the strict scanners flagged.")
        print("Revise the corresponding files (script.md WORDS, titles.md, thumbnail.md, publish.md, etc.) then re-run the prep suites.")
    else:
        print("overall: NO_SIGNALS (strict scanners clean)")
    print("Does not write files. Does not invent content. Prefer human OAuth for publish.")
    return 0 if not any_signal else 1


if __name__ == "__main__":
    raise SystemExit(main())
