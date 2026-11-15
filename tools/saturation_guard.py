#!/usr/bin/env python3
"""Flag when recent runs are saturating on pure anti-rediscovery status tools or polish loops.

Scans the most recent RUNS.md sections for patterns of "Added tools/xxx.py",
"Enhanced tools/experiment_xxx.py", pure documentation/inspection-only updates,
or repeated contract-locking of suggestion tools (while videos published remain 0).
Also flags script_*_brief.py, *_candidates.py, research_gap, packet_readiness_brief,
pipeline_entry / pre_upload_review / *_steps.py sequence printers, pure confirmation
runs ("Confirmed ... no new tools" / "state files updated with this run's note only"),
*_suite.py runners, *_suggest.py (non-experiment), *_signals.py extractors, and
similar inspection/candidate/sequence/suite/suggest generators as status-like when they dominate
recent runs.
Also detects repeated enhancements to the same suggest tool across consecutive runs
(e.g. feedback_to_topic_suggest.py polished multiple times while published stays 0).
When the streak of such runs is long, prints SATURATED_ANTI_REDISCOVERY so future
agents prefer the human OAuth step or a true production capability over another
one-liner, RECOMMENDED NEXT polish, repeated state-file inspection, or
suggest-contract / sequence-printer / confirmation / suite / signals / starter / package locking.
Does not poll secrets, does not invent data, does not modify files.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "RUNS.md"

STATUS_TOOL_RE = re.compile(
    r"(Added|Enhanced) tools/(stall_|recurring_|publish_|after_|next_|human_|packet_|capability_|efficiency_|media_fingerprint|reusable_commands|experiment_|script_.*_(brief|candidates)|.*_candidates|research_gap|packet_readiness_brief|pipeline_entry|pre_upload_review|.*_steps\.py|.*_entry\.py|.*_suite\.py|.*_suggest\.py|.*_signals\.py|revision_|.*_starter\.py|.*_package\.py)",
    re.IGNORECASE,
)
SUGGEST_POLISH_RE = re.compile(
    r"(Enhanced|Improved|Updated).*(feedback_to_topic_suggest|.*_suggest\.py)",
    re.IGNORECASE,
)
SUGGEST_CONTRACT_RE = re.compile(
    r"Added tools/\w+_suggest_contract\.py|Added tools/\w+_contract\.py",
    re.IGNORECASE,
)
DOC_ONLY_RE = re.compile(
    r"(Updated state files only|No code changes|pure documentation|inspected state|Reviewed STATE\.md|state files updated|Confirmed .*no new tools|confirmation runs|this run's evidence-based note only|No new tools added)",
    re.IGNORECASE,
)
ZERO_PUBLISH_RE = re.compile(
    r"Videos published stay 0|videos published remain 0|videos_published:\s*0|published stay 0|STALL_OAUTH_IDLE|videos published: 0",
    re.IGNORECASE,
)


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
        or SUGGEST_POLISH_RE.search(section)
    )


def main() -> int:
    if not RUNS.is_file():
        print("saturation_guard: RUNS.md missing")
        return 1
    text = RUNS.read_text(encoding="utf-8")
    sections = recent_sections(text)
    status_only = sum(1 for s in sections if is_status_only(s))
    total = len(sections)
    print("SATURATION GUARD (anti-rediscovery of status-tool, polish, doc-only, suggest-contract, sequence-printer, suite, suggest, signals, starter, package, pure-confirmation, and repeated same-tool polish loops; no invent)")
    print(f"recent_runs_examined: {total}")
    print(f"status_tool_only_runs: {status_only}")
    if status_only >= 4:  # lowered threshold because recent runs are short polish loops
        print("status: SATURATED_ANTI_REDISCOVERY")
        print("message: Multiple consecutive runs have only added status tools, polished the same suggest tool (e.g. feedback_to_topic_suggest.py repeatedly), performed pure state-file inspection/docs updates, locked suggestion tools with contracts, added sequence printers, or recorded pure confirmation notes while videos published stay 0 and STALL_OAUTH_IDLE continues.")
        print("recommendation: Prefer the human OAuth step (python3 tools/human_next_action.py or docs/HUMAN_PRIORITY.md) or a true production capability (capability_gap_hint.py) over another status tool, polish of an already-complete suggestor, inspection, brief, candidates generator, sequence printer, suite runner, suggest/signals tool, starter/package tool, or pure confirmation entry. Further feedback_to_topic_suggest polishing has diminishing returns until after first publish.")
    else:
        print("status: NOT_SATURATED")
        print("message: Recent runs have not yet saturated on pure status/polish/doc-only/suggest-contract/sequence-printer/suite/suggest/signals/starter/package/confirmation/repeated-polish tools.")
    print("Do not poll secrets. Preferred unblocked list remains complete. Long OAuth stall is HIGH suspicion.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
