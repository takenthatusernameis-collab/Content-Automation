#!/usr/bin/env python3
"""Flag when recent runs are saturating on pure anti-rediscovery status tools or polish loops.

Scans the most recent RUNS.md sections for patterns of "Added tools/xxx.py" or
"Enhanced tools/experiment_xxx.py" (or similar status/polish) while videos
published remain 0. When the streak of such runs is long, prints
SATURATED_ANTI_REDISCOVERY so future agents prefer the human OAuth step or a
true production capability over another one-liner or RECOMMENDED NEXT polish.

Does not poll secrets, does not invent data, does not modify files.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "RUNS.md"

STATUS_TOOL_RE = re.compile(
    r"(Added|Enhanced) tools/(stall_|recurring_|publish_|after_|next_|human_|packet_|capability_|efficiency_|media_fingerprint|reusable_commands|experiment_)",
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
    return bool(STATUS_TOOL_RE.search(section))


def main() -> int:
    if not RUNS.is_file():
        print("saturation_guard: RUNS.md missing")
        return 1
    text = RUNS.read_text(encoding="utf-8")
    sections = recent_sections(text)
    status_only = sum(1 for s in sections if is_status_only(s))
    total = len(sections)
    print("SATURATION GUARD (anti-rediscovery of status-tool and polish loops; no invent)")
    print(f"recent_runs_examined: {total}")
    print(f"status_tool_only_runs: {status_only}")
    if status_only >= 6:
        print("status: SATURATED_ANTI_REDISCOVERY")
        print("message: Multiple consecutive runs have only added status tools or polished experiment documentation (RECOMMENDED NEXT) while videos published stay 0.")
        print("recommendation: Prefer the human OAuth step (python3 tools/human_next_action.py) or a true production capability (capability_gap_hint.py) over another status tool or polish.")
    else:
        print("status: NOT_SATURATED")
        print("message: Recent runs have not yet saturated on pure status/polish tools.")
    print("Do not poll secrets. Preferred unblocked list remains complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
