#!/usr/bin/env python3
"""One-command full draft package starter for a packet.

Aggregates draft_md_starter (ready-to-copy draft.md skeleton with starting WORDS)
and draft_beat_expansion_starter (per-beat expansion checklist of concrete elements)
into a single concise view so agents can obtain the complete draft starting point
and structured expansion guidance without sequential tool calls.
Does not invent spoken lines, statistics, anecdotes, or claims.
Does not write files. Does not call APIs.
Complements the individual tools without replacing them.
Useful for preparing the exact file shape and the concrete elements to add
when expanding starting WORDS to the 140–220 spoken-word targets, reducing
free-form padding and slop risk for every future packet.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

def run_tool(script: str, packet: str, extra: list[str] | None = None) -> tuple[int, str]:
    """Run a tool and return (returncode, output)."""
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path), packet]
    if extra:
        cmd.extend(extra)
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out.strip()
    except Exception as e:
        return 1, f"EXCEPTION {script}: {e}"

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate full draft package: ready-to-copy skeleton + per-beat expansion checklist. No invented spoken lines."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    packet = args.packet
    path = Path(packet).resolve()
    if not path.is_dir() or not (path / "idea.md").is_file():
        print(f"No idea.md in {packet}", file=sys.stderr)
        return 1

    print("DRAFT PACKAGE STARTER (ready-to-copy draft.md skeleton + per-beat expansion checklist; no invented spoken lines/stats)")
    print("Use the skeleton as the exact file shape and the checklist for concrete elements when expanding body beats to word targets.")
    print("=" * 72)

    # Draft.md skeleton first
    rc, out = run_tool("draft_md_starter.py", packet)
    print("\n## DRAFT.MD SKELETON (copy into packet/draft.md; expand body WORDS)")
    print(out or "(no output)")

    # Expansion checklist
    rc, out = run_tool("draft_beat_expansion_starter.py", packet)
    print("\n## BEAT EXPANSION CHECKLIST (concrete elements to add per body beat)")
    print(out or "(no output)")

    print("\n" + "=" * 72)
    print("Next steps (do not invent sources, numbers, spoken lines, statistics, or anecdotes):")
    print("1. Copy the DRAFT.MD SKELETON output into videos/<id>-<slug>/draft.md.")
    print("2. For each body beat, expand the starting WORDS using the matching checklist items (worked example, distinction, operational test, failure-mode scene).")
    print("3. Keep Hook / Payoff / CTA near their shorter targets; grow only the body beats so total lands in 900–1500 (~1200).")
    print("4. Replace TBD counts in the HTML comment after expansion.")
    print("5. Run python3 tools/quality_scan.py and python3 tools/claim_scan.py before apply_script.py --write.")
    print("6. Prefer concrete mechanism language; avoid anti-slop phrases listed in docs/content_quality.md.")
    print("This package writes nothing. Preferred unblocked path remains human OAuth for publish.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
