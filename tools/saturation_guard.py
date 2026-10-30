#!/usr/bin/env python3
"""Flag when recent runs are saturating on pure anti-rediscovery status tools or polish loops.

Scans the most recent RUNS.md sections for patterns of "Added tools/xxx.py",
"Enhanced tools/experiment_xxx.py", pure documentation/inspection-only updates,
or repeated contract-locking of suggestion tools (while videos published remain 0).
Also flags script_*_brief.py, *_candidates.py, research_gap, packet_readiness_brief,
pipeline_entry / pre_upload_review / *_steps.py sequence printers, and similar
inspection/candidate/sequence generators as status-like when they dominate recent runs.
When the streak of such runs is long, prints SATURATED_ANTI_REDISCOVERY so future
agents prefer the human OAuth step or a true production capability over another
one-liner, RECOMMENDED NEXT polish, repeated state-file inspection, or
suggest-contract / sequence-printer locking.
Does not poll secrets, does not invent data, does not modify files.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "RUNS.md"

STATUS_TOOL_RE = re.compile(
    r"(Added|Enhanced) tools/(stall_|recurring_|publish_|after_|next_|human_|packet_|capability_|efficiency_|media_fingerprint|reusable_commands|experiment_|script_.*_(brief|candidates)|.*_candidates|research_gap|packet_readiness_brief|pipeline_entry|pre_upload_review|.*_steps\.py|.*_entry\.py)",
    re.IGNORECASE,
)
SUGGEST_CONTRACT_RE = re.compile(
    r"Added tools/\w+_suggest_contract\.py|Added tools/\w+_contract\.py",
    re.IGNORECASE,
)
DOC_ONLY_RE = re.compile(
    r"(Updated state files only|No code changes|pure documentation|inspected state|Reviewed STATE\.md|state files updated)",
    re.IGNORECASE,
)
ZERO_PUBLISH_RE = re.compile(r"Videos published stay 0|videos published remain 0", re.IGNORECASE)


def recent_sections(text: str, max_n: int = 8) -> list[str]:
    parts = re.split(r"(?=^## Run )", text, flags=re.M)
    sections = [p for p in parts if p.strip().startswith("## Run")]
    return sections[:max_n]


def is_status_only(section: str) -> bool:
    if not ZERO_PUBLISH_RE.search(section):
        return False
    return bool(
        STATUS_TOOL_RE.search(section)
        or DOC_ONLY_RE.search(section)
        or SUGGEST_CONTRACT_RE.search(section)
    )


def main() -> int:
    if not RUNS.is_file():
        print("saturation_guard: RUNS.md missing")
        return 1
    text = RUNS.read_text(encoding="utf-8")
    sections = recent_sections(text)
    status_only = sum(1 for s in sections if is_status_only(s))
    total = len(sections)
    print("SATURATION GUARD (anti-rediscovery of status-tool, polish, doc-only, suggest-contract, and sequence-printer loops; no invent)")
    print(f"recent_runs_examined: {total}")
    print(f"status_tool_only_runs: {status_only}")
    if status_only >= 6:
        print("status: SATURATED_ANTI_REDISCOVERY")
        print("message: Multiple consecutive runs have only added status tools (including script_*_brief, *_candidates, research_gap, packet_readiness, pipeline_entry, pre_upload_review, *_steps.py), polished experiment documentation (RECOMMENDED NEXT), performed pure state-file inspection/docs updates, locked suggestion tools with contracts, or added sequence printers while videos published stay 0.")
        print("recommendation: Prefer the human OAuth step (python3 tools/human_next_action.py) or a true production capability (capability_gap_hint.py) over another status tool, polish, inspection, brief, candidates generator, or sequence printer.")
    else:
        print("status: NOT_SATURATED")
        print("message: Recent runs have not yet saturated on pure status/polish/doc-only/suggest-contract/sequence-printer tools.")
    print("Do not poll secrets. Preferred unblocked list remains complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
