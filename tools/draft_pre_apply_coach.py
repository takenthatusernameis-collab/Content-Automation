#!/usr/bin/env python3
"""Pre-apply coach for draft.md: expansion progress + quality + claim + originality + cadence signals.

Combines the draft expansion coach view with anti-slop (quality_scan patterns),
unsourced-claim (claim_scan hedges/digits), packet-grounded originality extracts,
and cadence/repetition signals on the draft spoken WORDS.
Works on draft.md before promotion to script.md. Does not invent lines, numbers,
sources, or anecdotes. Does not write files. One-command pre-apply quality view that
compounds by catching padding, slop, unsupported claims, generic drafts, and monotonous
delivery early for every future packet.
"""

from __future__ import annotations

import argparse
import subprocess
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

def run_tool(name: str, path: Path) -> str:
    tool = ROOT / "tools" / name
    if not tool.is_file():
        return f"({name} missing; skipped)\n"
    proc = subprocess.run([sys.executable, str(tool), str(path)], capture_output=True, text=True)
    out = proc.stdout or ""
    if proc.returncode != 0 and proc.stderr:
        out += f"\n[{name} stderr]: {proc.stderr}"
    return out

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pre-apply coach: expansion + quality + claim + originality + cadence signals on draft.md. No writes."
    )
    parser.add_argument("packet", help="Packet folder containing draft.md (or script.md), idea.md, research.md")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    draft = path / "draft.md"
    source = draft if draft.is_file() else path / "script.md"
    if not source.is_file():
        print(f"No draft.md or script.md in {args.packet}", file=sys.stderr)
        return 1

    print("DRAFT PRE-APPLY COACH (expansion + quality + claim + originality + cadence signals on draft; no invented content)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print()

    # Expansion view
    print(run_tool("draft_expansion_coach.py", path))

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

    # Originality extracts
    print("## ORIGINALITY EXTRACTS")
    print(run_tool("originality_checklist.py", path))

    # Cadence / repetition
    print("## CADENCE & REPETITION SIGNALS")
    print(run_tool("cadence_repetition_scan.py", path))

    print("Next (do not invent sources, numbers, anecdotes, or spoken lines):")
    print("- Revise draft.md for any SHORT beats, quality hits, claim hits, originality 'no' answers, or cadence signals.")
    print("- Prefer concrete mechanism language. Vary sentence length. Cut repeated phrases.")
    print("- Then run apply_script.py --write after signals are clear.")
    print("This tool writes nothing. Preferred unblocked path remains human OAuth for publish.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
