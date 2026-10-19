#!/usr/bin/env python3
"""Suggest appropriate primary metrics for an experiment based on the change type.

Reads idea.md (or experiment_baseline.json if present) to identify the single allowed change.
Prints 2-4 recommended primary_metric names that fit the change, without inventing numeric values,
baselines, or results. Does not write files. Does not call APIs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from experiment_loop import ALLOWED_CHANGES  # noqa: E402

# Mapping from change type to useful primary metrics (YouTube Analytics-friendly).
# These are suggestions only; the human or agent must still document a real baseline.
METRIC_MAP = {
    "hook": [
        "average_view_duration_seconds",
        "average_percentage_viewed",
        "views",
    ],
    "mechanism_framing": [
        "average_view_duration_seconds",
        "average_percentage_viewed",
        "likes",
    ],
    "example_density": [
        "average_view_duration_seconds",
        "average_percentage_viewed",
        "comments",
    ],
    "title_promise": [
        "impressions_click_through_rate",
        "views",
        "average_view_duration_seconds",
    ],
    "visual_explanation": [
        "average_view_duration_seconds",
        "average_percentage_viewed",
        "likes",
    ],
    "pacing": [
        "average_view_duration_seconds",
        "average_percentage_viewed",
        "views",
    ],
    "cta": [
        "end_screen_element_click_rate",
        "subscribers_gained",
        "average_view_duration_seconds",
    ],
    "topic_selection": [
        "views",
        "average_view_duration_seconds",
        "impressions",
    ],
}


def field_line(text: str, name: str) -> str:
    m = re.search(rf"^-?\s*{re.escape(name)}:[ \t]*([^\n]*)$", text, re.M | re.I)
    return m.group(1).strip() if m else ""


def detect_change(packet: Path) -> str:
    """Prefer an existing baseline change, else fall back to idea.md mechanism framing."""
    baseline = packet / "experiment_baseline.json"
    if baseline.is_file():
        try:
            data = json.loads(baseline.read_text(encoding="utf-8"))
            ch = str(data.get("change") or "").strip()
            if ch in ALLOWED_CHANGES:
                return ch
        except json.JSONDecodeError:
            pass
    idea = packet / "idea.md"
    if idea.is_file():
        text = idea.read_text(encoding="utf-8")
        # Simple heuristic: look for keywords that map to changes
        low = text.lower()
        if "hook" in low:
            return "hook"
        if "title" in low:
            return "title_promise"
        if "cta" in low or "call to action" in low:
            return "cta"
        if "visual" in low or "card" in low:
            return "visual_explanation"
        if "pace" in low or "pacing" in low:
            return "pacing"
        if "example" in low:
            return "example_density"
        if "topic" in low:
            return "topic_selection"
        return "mechanism_framing"  # default safe single variable
    return "mechanism_framing"


def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after the metric suggestions."""
    p = packet
    return [
        f"pick one primary_metric from the list above and document a real numeric baseline + source",
        f"baseline skeleton: python3 tools/experiment_baseline_starter.py {p}",
        f"notes skeleton: python3 tools/experiment_notes_starter.py {p}",
        f"guardrails: python3 tools/experiment_guardrail_suggest.py {p}",
        f"package view: python3 tools/experiment_package_starter.py {p}",
        f"setup suggestions: python3 tools/experiment_setup_report.py {p}",
        f"quality scans: python3 tools/quality_scan.py {p} && python3 tools/claim_scan.py {p}",
        f"full production if needed: python3 tools/full_production_starter.py {p}",
        "do not invent numeric baselines or results; experiment_loop.py rejects placeholder sources",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest primary metrics for an experiment change. No invented values."
    )
    parser.add_argument("packet", help="Packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    change = detect_change(path)
    metrics = METRIC_MAP.get(change, METRIC_MAP["mechanism_framing"])
    print("EXPERIMENT METRIC SUGGEST (suggestions only; no invented baseline)")
    print(f"packet: {path.name}")
    print(f"detected_change: {change}")
    print(f"allowed_changes: {', '.join(ALLOWED_CHANGES)}")
    print()
    print("Recommended primary_metric candidates (choose one, then document a real numeric baseline and source):")
    for m in metrics:
        print(f"  - {m}")
    print()
    print("These are common YouTube Analytics fields that can be compared numerically.")
    print("Do not invent a baseline value. Use experiment_baseline_starter.py then edit.")
    print("experiment_loop.py will reject placeholder sources and missing numeric baselines.")
    print()
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
