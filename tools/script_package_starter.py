#!/usr/bin/env python3
"""One-command full pre-script package starter for a packet.

Aggregates expand_starter (beat budget and structure skeleton) and
draft_starter (mechanism-aligned Hook/Payoff/Body/Failure/CTA candidates)
into a single concise view so agents can obtain the complete starting point
for script drafting without sequential tool calls.
Does not invent spoken lines, statistics, anecdotes, or written WORDS.
Does not write files. Does not call APIs.
Complements the individual tools without replacing them.
Useful before the first draft so agents know the shape, size, and
mechanism-aligned candidates before expanding into draft.md.
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

def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after the pre-script package."""
    p = packet
    return [
        f"skeleton: python3 tools/draft_md_starter.py {p}  # ready-to-copy draft.md with starting WORDS",
        f"expand checklist: python3 tools/draft_beat_expansion_starter.py {p}  # per-beat expansion items",
        f"coach: python3 tools/draft_expansion_coach.py {p} or python3 tools/draft_short_beat_coach.py {p}",
        f"quality: python3 tools/draft_pre_apply_coach.py {p} for full signals before apply",
        f"apply: python3 tools/apply_script.py {p} --from {p}/draft.md --write --refresh once signals clear",
    ]

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate full pre-script package: beat budget + draft candidates. No invented WORDS."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    packet = args.packet
    path = Path(packet).resolve()
    if not path.is_dir() or not (path / "idea.md").is_file():
        print(f"No idea.md in {packet}", file=sys.stderr)
        return 1

    print("SCRIPT PACKAGE STARTER (beat budget + mechanism-aligned draft candidates; no invented spoken lines)")
    print("Use the structure targets and preferred candidates as the starting point for draft.md.")
    print("=" * 72)

    # Beat budget / structure first
    rc, out = run_tool("expand_starter.py", packet)
    print("\n## BEAT BUDGET AND STRUCTURE (pre-script shape and word targets from idea.md)")
    print(out or "(no output)")

    # Mechanism-aligned draft candidates
    rc, out = run_tool("draft_starter.py", packet)
    print("\n## DRAFT CANDIDATES (Hook / Payoff / Body / Failure / CTA + VISUAL; expand into full WORDS)")
    print(out or "(no output)")

    print("\n" + "=" * 72)
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    print("Next steps (do not invent spoken lines, statistics, or anecdotes):")
    print("1. Copy preferred candidates into videos/<id>-<slug>/draft.md, preserving exact ## headings.")
    print("2. Expand body beats to the word targets so total spoken WORDS land in 900–1500 (~1200).")
    print("3. After headings exist, python3 tools/expand_brief.py", packet, "writes the live budget from actual WORDS.")
    print("4. Run tools/quality_scan.py and tools/claim_scan.py before apply_script.py --write.")
    print("5. Prefer mechanism-aligned operational language; avoid anti-slop phrases listed in quality_scan.py.")
    print("This package writes nothing. Preferred unblocked path remains human OAuth for publish.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
