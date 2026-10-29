#!/usr/bin/env python3
"""Write a local research_notes.md with structured source-capture sections.

Extracts mechanism/problem/topic from idea.md and emits a structured
research_notes.md with sections for verifying the mechanism, concrete problem
examples, potential claims that need sources, and guidance to fill only with
real external sources. No invented sources, statistics, anecdotes, or claims.
Output stays local (gitignored). Reduces recurring human/agent labor of
structuring research notes and source capture for every future packet while
keeping content grounded. Aligns with channel voice (assignment, not reply
prompt), format, production_capabilities research section, and no-invent rule.
Complements claim_source_table.py and research_brief.py. Not a final script
or source list.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract as idea_extract  # noqa: E402


def shorten(s: str, n: int) -> str:
    s = (s or "").strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write local research_notes.md from idea.md fields only"
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"FAIL: not a directory: {packet}", file=sys.stderr)
        return 1

    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print("FAIL: idea.md missing", file=sys.stderr)
        return 2

    out_path = packet / "research_notes.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    base = shorten(mech or "the written next-action default", 60)
    stall = problem or "the stall reopens the list"

    lines = [
        "# Research Notes (local; source capture only)",
        "",
        "Generated locally from idea.md mechanism/problem/topic only.",
        "Structured sections for capturing real external sources that ground the",
        "mechanism, problem examples, and any factual claims. Do not invent sources,",
        "statistics, anecdotes, or claims. Fill placeholders with verified links or",
        "citations only. Channel voice: calm, specific, operational.",
        "Aligns with production_capabilities research/source capture and claim_source_table.py.",
        "Not a final script or source list. Use to keep expansions grounded.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem / stall: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "## Mechanism verification",
        f"- Confirm the operational meaning of: {base}",
        "- Source or reference that shows this default reduces the named stall (link or note):",
        "- What the source actually demonstrates (one sentence, no invention):",
        "",
        "## Problem examples",
        f"- Concrete observable scene of the stall: {stall}",
        "- Source or personal observation note (no invented anecdote):",
        "- Distinction from related stalls (if source supports it):",
        "",
        "## Potential claims to source",
        "- Any number, percentage, or factual assertion that might appear in expansion:",
        "  - Claim: (leave blank until grounded)",
        "  - Source: (link or citation only)",
        "  - Hedge if needed: (qualitative rewrite if no source)",
        "- Do not add claims without a source line.",
        "",
        "## Operational test note",
        f"- How a viewer can test the {base} the same day (from existing fields only):",
        "- Success signal (stall does not reopen):",
        "- Failure signal (list reopens):",
        "",
        "---",
        "After filling real sources: run tools/claim_source_table.py and",
        "tools/quality_scan.py before expanding into draft.md. Do not treat this file as script.md.",
        "Preferred unblocked path remains the human OAuth step for publish.",
    ]

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print(f"topic_found: {bool(topic)}")
    print("Research notes ready (local; estimated from packet fields only; fill sources next).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
