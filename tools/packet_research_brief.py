#!/usr/bin/env python3
"""Packet research brief aggregator.

Prints the curated niche source list plus (when a packet with script.md or draft.md
is supplied) the fillable claim-to-source table. One command replaces sequential
calls to niche_source_suggest.py and claim_source_table.py before filling
research.md or sources.md.
Does not invent packet-specific citations, numbers, or URLs. Does not write files.
Does not call APIs. Reduces blank-page and claim-listing friction for every future packet.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"


def run_tool(script: str, extra: list[str] | None = None) -> tuple[int, str]:
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path)]
    if extra:
        cmd.extend(extra)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out.strip()
    except Exception as e:
        return 1, f"EXCEPTION {script}: {e}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate niche sources and (optional) claim-to-source table. No invented sources."
    )
    parser.add_argument("packet", nargs="?", help="Optional packet folder for claim table")
    args = parser.parse_args()

    print("PACKET RESEARCH BRIEF (niche sources + optional claim table; no invented citations)")
    print("Use this before filling research.md or sources.md. Verify every source.")
    print("=" * 72)

    # Always show niche sources
    rc, out = run_tool("niche_source_suggest.py")
    print("\n## NICHE SOURCE STARTERS")
    print(out or "(no output)")

    overall = 0
    if args.packet:
        p = Path(args.packet).resolve()
        if not p.is_dir():
            print(f"\nPacket not found: {args.packet}", file=sys.stderr)
            overall = 1
        else:
            rc, out = run_tool("claim_source_table.py", [str(p)])
            print("\n## CLAIM-TO-SOURCE TABLE (fill Source column only)")
            print(out or "(no output)")
            if rc != 0:
                overall = max(overall, rc)

    print("\n" + "=" * 72)
    print("NEXT: pick 1-3 niche sources relevant to the packet mechanism, read them,")
    print("then fill the Source column above (or paste the table into research.md).")
    print("Tools: python3 tools/research_package_starter.py PATH for full skeletons.")
    print("This tool writes nothing.")
    return overall


if __name__ == "__main__":
    sys.exit(main())
