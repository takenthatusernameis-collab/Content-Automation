#!/usr/bin/env python3
"""One-command full pre-production package starter for a packet.

Aggregates research_package_starter (sources + research brief skeletons)
and script_package_starter (beat budget + draft candidates) into a single
concise view so agents can obtain the complete research documentation and
pre-script starting point without sequential package calls.
Does not invent URLs, numbers, citations, spoken lines, statistics, or anecdotes.
Does not write files. Does not call APIs.
Complements the individual package tools without replacing them.
Useful for preparing the full factual support and structure before the first WORDS or expand_brief.
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
    """Provide concrete copy-paste next steps after the full pre-production package."""
    p = packet
    return [
        f"research sources: python3 tools/research_sources_starter.py {p} --write  # fill then write sources.md skeleton",
        f"research brief: python3 tools/research_brief_starter.py {p} --write  # fill then write research.md skeleton",
        f"skeleton: python3 tools/draft_md_starter.py {p}  # ready-to-copy draft.md with starting WORDS",
        f"expand checklist: python3 tools/draft_beat_expansion_starter.py {p}  # per-beat expansion items",
        f"coach: python3 tools/draft_expansion_coach.py {p} or python3 tools/draft_short_beat_coach.py {p}",
        f"quality: python3 tools/draft_pre_apply_coach.py {p} for full signals before apply",
        f"apply: python3 tools/apply_script.py {p} --from {p}/draft.md --write --refresh once signals clear",
    ]

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate full pre-production package: research skeletons + pre-script package. No invented content."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    packet = args.packet
    path = Path(packet).resolve()
    if not path.is_dir() or not (path / "idea.md").is_file():
        print(f"No idea.md in {packet}", file=sys.stderr)
        return 1

    print("PRE-PRODUCTION PACKAGE STARTER (research documentation + beat budget + draft candidates; no invented sources or spoken lines)")
    print("Use the research skeletons to capture real sources and the structure/candidates as the starting point before drafting WORDS.")
    print("=" * 72)

    # Research package first
    rc, out = run_tool("research_package_starter.py", packet)
    print("\n## RESEARCH PACKAGE (sources.md skeleton + research.md skeleton)")
    print(out or "(no output)")

    # Script package (structure + drafts)
    rc, out = run_tool("script_package_starter.py", packet)
    print("\n## SCRIPT PACKAGE (beat budget/structure + mechanism-aligned draft candidates)")
    print(out or "(no output)")

    print("\n" + "=" * 72)
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    print("Next steps (do not invent sources, numbers, citations, spoken lines, statistics, or anecdotes):")
    print("1. Fill research skeletons with real verifiable sources and qualitative claims supporting the mechanism.")
    print("2. Optionally write them with the individual starters' --write flags.")
    print("3. Copy preferred draft candidates into draft.md, preserving exact ## headings.")
    print("4. Expand body beats to the word targets so total spoken WORDS land in 900–1500 (~1200).")
    print("5. After headings exist, python3 tools/expand_brief.py", packet, "writes the live budget from actual WORDS.")
    print("6. Run tools/quality_scan.py and tools/claim_scan.py before apply_script.py --write.")
    print("Filled Source column values (non-empty, non-placeholder) in the Primary claims table or Source log table from research.md or sources.md, and non-placeholder bullets, are auto-extracted by claim_scan.py and treated as citations. The extractor is header-aware (detects Source from the table header) and combines Claim + Source strings so Primary claims / Source log tables reliably clear both quantitative digits and hedge phrases. No need to also rewrite a ## Sources section.")
    print("7. Prefer mechanism-aligned operational language; avoid anti-slop phrases.")
    print("This package writes nothing. Preferred unblocked path remains human OAuth for publish.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
