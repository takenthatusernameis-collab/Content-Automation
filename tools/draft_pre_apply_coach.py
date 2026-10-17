#!/usr/bin/env python3
"""Pre-apply coach for draft.md: expansion progress + quality + claim signals.

Combines the draft expansion coach view with anti-slop (quality_scan patterns)
and unsourced-claim (claim_scan hedges/digits) checks on the draft spoken WORDS.
Works on draft.md before promotion to script.md. Does not invent lines, numbers,
or sources. Does not write files. One-command pre-apply quality view that
compounds by catching padding, slop, and unsupported claims early for every
future packet.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

try:
    from quality_scan import hits as quality_hits
    from claim_scan import hits as claim_hits
except ImportError as e:
    print(f"import error: {e}", file=sys.stderr)
    sys.exit(1)

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pre-apply coach: expansion + quality + claim signals on draft.md. No writes."
    )
    parser.add_argument("packet", help="Packet folder containing draft.md (or script.md), idea.md, research.md")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    draft = path / "draft.md"
    source = draft if draft.is_file() else path / "script.md"
    if not source.is_file():
        print(f"No draft.md or script.md in {args.packet}", file=sys.stderr)
        return 1

    print("DRAFT PRE-APPLY COACH (expansion progress + quality + claim signals on draft; no invented content)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print()

    # Delegate expansion view
    import subprocess
    coach = ROOT / "tools" / "draft_expansion_coach.py"
    if coach.is_file():
        proc = subprocess.run([sys.executable, str(coach), str(path)], capture_output=True, text=True)
        print(proc.stdout or "")
        if proc.returncode != 0:
            print(proc.stderr or "")
    else:
        print("(draft_expansion_coach.py missing; skipping progress view)")

    # Quality and claim on the draft text
    text = source.read_text(encoding="utf-8")
    research = ""
    research_path = path / "research.md"
    if research_path.is_file():
        research = research_path.read_text(encoding="utf-8")

    q_hits = quality_hits(text)
    c_hits = claim_hits(text, research)

    print("## QUALITY SIGNALS (anti-slop phrases in draft WORDS)")
    if not q_hits:
        print("clear")
    else:
        for phrase, count, ctx in q_hits:
            print(f"- {phrase} x{count} [{ctx}]")
    print()

    print("## CLAIM SIGNALS (unsourced digits or hedges in draft WORDS)")
    if not c_hits:
        print("clear")
    else:
        for kind, token, ctx in c_hits:
            print(f"- {kind}:{token} [{ctx}]")
    print()

    print("Next (do not invent sources, numbers, or anecdotes):")
    print("- Revise draft.md for any SHORT beats, quality hits, or claim hits.")
    print("- Prefer concrete mechanism language.")
    print("- Then run apply_script.py --write after signals are clear.")
    print("This tool writes nothing. Preferred unblocked path remains human OAuth for publish.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
