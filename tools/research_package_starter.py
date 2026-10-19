#!/usr/bin/env python3
"""One-command full research package starter for a packet.

Aggregates research_sources_starter and research_brief_starter into a single
concise view so agents can obtain the complete research documentation
starting point (sources.md skeleton + full research.md skeleton) without
sequential tool calls.
Does not invent URLs, numbers, citations, or results. Does not write files
unless individual starters are called with --write separately. Does not call APIs.
Complements the individual tools without replacing them.
Useful for preparing factual-claim support and the full research brief
before script drafting and claim_scan.
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
    """Provide concrete copy-paste next steps after the research package."""
    p = packet
    return [
        f"write sources: python3 tools/research_sources_starter.py {p} --write  # after filling skeleton with real sources",
        f"write brief: python3 tools/research_brief_starter.py {p} --write  # after filling research.md skeleton",
        f"pre-script: python3 tools/script_package_starter.py {p}  # beat budget + draft candidates",
        f"or full package: python3 tools/pre_production_package_starter.py {p}  # research + script in one view",
        f"then expand: python3 tools/draft_md_starter.py {p} and python3 tools/draft_beat_expansion_starter.py {p}",
        f"quality: python3 tools/claim_scan.py {p} and python3 tools/quality_scan.py {p} before apply  # Source columns/bullets in research.md or sources.md auto-clear citations",
        f"apply: python3 tools/apply_script.py {p} --from {p}/draft.md --write --refresh once signals clear",
    ]

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate full research package starters. No invented sources or numbers."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    packet = args.packet
    path = Path(packet).resolve()
    if not path.is_dir() or not (path / "idea.md").is_file():
        print(f"No idea.md in {packet}", file=sys.stderr)
        return 1

    print("RESEARCH PACKAGE STARTER (sources skeleton + full research brief skeleton; no invented URLs, numbers, or citations)")
    print("Use the skeletons to capture real sources and claims before drafting script WORDS.")
    print("=" * 72)

    # Sources skeleton first (lighter)
    rc, out = run_tool("research_sources_starter.py", packet)
    print("\n## SOURCES SKELETON (sources.md; fill with real verifiable sources)")
    print(out or "(no output)")

    # Full research brief skeleton
    rc, out = run_tool("research_brief_starter.py", packet)
    print("\n## RESEARCH BRIEF SKELETON (research.md; overview, claims, evidence, source table, claim_scan notes)")
    print(out or "(no output)")

    print("\n" + "=" * 72)
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    print("Next steps (do not invent sources, numbers, or citations):")
    print("1. Fill the sources skeleton with real primary/secondary references that support consequential claims.")
    print("2. Optionally write it: python3 tools/research_sources_starter.py", packet, "--write")
    print("3. Fill the research brief skeleton with qualitative claims, evidence preferences, and the source table.")
    print("4. Optionally write it: python3 tools/research_brief_starter.py", packet, "--write")
    print("5. Draft script WORDS using the research, then run tools/claim_scan.py and tools/quality_scan.py.")
    print("claim_scan.py flags unsupported digits and survey/authority hedges unless sourced in research.md or sources.md.")
    print("Filled Source column values (non-empty, non-placeholder) in the Primary claims table or Source log table, and non-placeholder bullets, are auto-extracted by claim_scan.py and treated as citations. No need to also rewrite a ## Sources section in either file.")
    print("Preferred unblocked path remains human OAuth (secrets + dispatch) before any live publish.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
