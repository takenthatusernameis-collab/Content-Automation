#!/usr/bin/env python3
"""Print a ready-to-edit experiment notes Markdown skeleton from a packet.

Reads idea.md for topic and mechanism. Detects or accepts a change type.
Prints a structured Markdown template with sections for hypothesis, change, metric,
guardrails, baseline (to fill), source, observation window, and decision notes.
Does not invent numeric values, results, or decisions. Does not write files
unless --write is given. Does not call APIs.
Complements experiment_setup_report.py and the JSON starters for documentation.
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

MECH_RE = re.compile(r"mechanism[^\n]*:\s*(.+)", re.I)
TOPIC_RE = re.compile(r"topic:\s*(.+)", re.I)

def extract(idea_text: str) -> tuple[str, str]:
    mech = ""
    topic = ""
    for line in idea_text.splitlines():
        m = MECH_RE.search(line)
        if m:
            mech = m.group(1).strip().rstrip(".")
        t = TOPIC_RE.search(line)
        if t:
            topic = t.group(1).strip().rstrip(".")
    return mech, topic

def detect_change(packet: Path) -> str:
    """Prefer an existing baseline change, else fall back to idea.md heuristic."""
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
        return "mechanism_framing"
    return "mechanism_framing"

def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after the notes skeleton."""
    p = packet
    return [
        f"edit skeleton: fill hypothesis, primary metric, guardrails, real numeric baseline, and documented source in the Markdown above",
        f"write notes: python3 tools/experiment_notes_starter.py {p} --write",
        f"baseline if needed: python3 tools/experiment_baseline_starter.py {p}",
        f"full package: python3 tools/experiment_package_starter.py {p}",
        f"setup suggestions: python3 tools/experiment_setup_report.py {p}",
        f"quality scans: python3 tools/quality_scan.py {p} && python3 tools/claim_scan.py {p}",
        f"full production if needed: python3 tools/full_production_starter.py {p}",
        "do not invent metrics or decisions; experiment_loop.py rejects placeholder sources and null baselines",
    ]

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print experiment notes Markdown skeleton. No invented values."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    parser.add_argument(
        "--change",
        default=None,
        help="Override detected change (must be in ALLOWED_CHANGES).",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write experiment_notes.md to the packet.",
    )
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}", file=sys.stderr)
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, topic = extract(text)
    change = args.change or detect_change(path)
    if change not in ALLOWED_CHANGES:
        change = "mechanism_framing"
    md = f"""# Experiment Notes for {path.name}

_generated_by: tools/experiment_notes_starter.py
_warning: TEMPLATE. Fill numeric baseline, documented source, and real decision after evidence. Do not invent metrics or results.

## Packet
- Topic: {topic or '(none)'}
- Mechanism: {mech or '(none)'}

## Change (single variable)
- Change type: {change}
- Allowed: {', '.join(ALLOWED_CHANGES)}

## Hypothesis
[Paste or edit one template from experiment_hypothesis_suggest.py here. Must name the mechanism '{mech[:40] or 'mechanism'}'.]

## Primary Metric
[Choose one from experiment_metric_suggest.py, e.g. average_view_duration_seconds or average_percentage_viewed]

## Guardrails
[List 3-5 from experiment_guardrail_suggest.py to protect the single-variable rule and metric clarity]

## Baseline
- Numeric value: [REPLACE with real number from prior video or documented observation]
- Source: [REPLACE with documented observation such as YouTube Studio analytics for video XYZ on YYYY-MM-DD; not placeholder/invented/guess]

## Observation Window
- Planned: 7 days after upload (youtube_feedback.py requires this)
- Actual: [fill after collection]

## Decision (after comparison)
- Decision: pending | keep | discard | retest
- Reason: [documented after reviewing the numeric delta and qualitative notes]
- Source: [review notes or Studio data; not invented]

## Notes
[Any other context that keeps the comparison interpretable. experiment_loop.py rejects invalid baselines, placeholder sources, and multi-variable changes.]
"""
    print("EXPERIMENT NOTES STARTER (Markdown skeleton only; edit before use)")
    print(f"packet: {path.name}")
    print(f"detected_or_set_change: {change}")
    print(f"mechanism: {mech or '(none)'}")
    print()
    print(md)
    print("Copy the Markdown above to videos/<id>-<slug>/experiment_notes.md after filling real values.")
    print("Run python3 tools/experiment_setup_report.py first for change-aligned suggestions.")
    print("Do not invent metrics or results. Preferred path remains human OAuth before live data.")
    print()
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    if args.write:
        dest = path / "experiment_notes.md"
        dest.write_text(md, encoding="utf-8")
        print(f"wrote: {dest}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
