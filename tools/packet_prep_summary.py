#!/usr/bin/env python3
"""One-command pre-upload packet preparation summary.

Runs the key soft quality and consistency checks for a packet in one place:
- sources_validator (claim-to-source coverage)
- uncovered_claims_suggest (research directions for gaps)
- metadata_mechanism_align_suggest (mechanism language in title/desc/thumb)

Prints their outputs with clear section headers. Reduces the recurring labor
of remembering and sequencing these checks for every future packet while the
publish path remains blocked. Does not invent sources, text, or data. Does not
write files, poll secrets, dispatch, or call external services. Soft signals only.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"

CHECKS = [
    ("sources_validator.py", "SOURCES VALIDATOR"),
    ("uncovered_claims_suggest.py", "UNCOVERED CLAIMS SUGGEST"),
    ("metadata_mechanism_align_suggest.py", "METADATA MECHANISM ALIGN"),
]


def run_tool(script: str, packet: Path) -> str:
    path = TOOLS / script
    if not path.is_file():
        return f"MISSING {script}"
    try:
        proc = subprocess.run(
            [sys.executable, str(path), str(packet)],
            capture_output=True,
            text=True,
            check=False,
            cwd=ROOT,
        )
        out = (proc.stdout or "").strip()
        if proc.returncode != 0:
            out += f"\n(exit {proc.returncode})"
        return out or "(no output)"
    except Exception as exc:
        return f"EXCEPTION {script}: {exc}"


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"Not a directory: {packet}", file=sys.stderr)
        return 1

    print("PACKET PREP SUMMARY (soft pre-upload checks; no invent, no writes)")
    print(f"packet: {packet.name}")
    print()
    print("Use the sections below as signals only. Fill real sources and preserve voice.")
    print("Human OAuth remains the publish blocker. Do not poll secrets.")
    print()

    for script, title in CHECKS:
        print(f"=== {title} ===")
        print(run_tool(script, packet))
        print()

    print("Next recommended (if gaps remain):")
    print(f"  python3 tools/claim_source_table.py {packet}")
    print(f"  python3 tools/claim_scan.py {packet}")
    print(f"  python3 tools/quality_scan.py {packet}")
    print()
    print("PACKET PREP SUMMARY complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
