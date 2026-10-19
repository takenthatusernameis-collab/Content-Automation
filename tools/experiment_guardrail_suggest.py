#!/usr/bin/env python3
"""Suggest change-aligned guardrails for an experiment.

Reads idea.md (or experiment_baseline.json if present) to identify the single allowed change.
Prints 3-5 recommended guardrails that reduce common failure modes for that change type.
Does not invent numeric values, baselines, results, or decisions. Does not write files.
Does not call APIs. Complements experiment_metric_suggest.py and the baseline/decision starters.
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

# Mapping from change type to practical guardrails (anti-rediscovery of common mistakes).
GUARDRAIL_MAP = {
    "hook": [
        "Do not rewrite the body or payoff to make the hook look stronger.",
        "Keep the mechanism framing identical across the comparison videos.",
        "Measure average view duration or percentage viewed on the first 30s, not total views alone.",
        "Do not treat a single high-retention outlier as proof the hook worked.",
    ],
    "mechanism_framing": [
        "Do not change the title promise or hook at the same time.",
        "Preserve example density and visual card structure.",
        "Confirm the mechanism is still named in the first 15 seconds.",
        "Avoid optimizing for likes if the goal is longer watch time.",
    ],
    "example_density": [
        "Do not alter the core mechanism explanation or CTA.",
        "Keep total spoken words inside the format band.",
        "Verify every added example still has a source or is qualitative.",
        "Do not pad with low-value examples just to raise density.",
    ],
    "title_promise": [
        "Do not change the spoken hook or first-card visual.",
        "Match the title promise to what the first 30 seconds actually delivers.",
        "Track impressions CTR and early average percentage viewed separately.",
        "Do not A/B more than one title element.",
    ],
    "visual_explanation": [
        "Do not rewrite the spoken script to compensate for a card change.",
        "Keep card text readable at 1920x1080 and under the word limit per card.",
        "Confirm the visual still supports the named mechanism.",
        "Do not add B-roll that the assembly planner does not expect.",
    ],
    "pacing": [
        "Do not change content density or example count at the same time.",
        "Preserve the mechanism naming points and CTA placement.",
        "Measure average view duration and audience retention curve, not only total length.",
        "Avoid cutting so aggressively that the payoff is lost.",
    ],
    "cta": [
        "Do not alter the hook or early mechanism framing.",
        "Keep the last 20 seconds clear for end-screen elements.",
        "Track end-screen click rate and subscribers gained, not only views.",
        "Do not invent a CTA that was not in the script.",
    ],
    "topic_selection": [
        "Do not change the production format or mechanism style for the first test.",
        "Document why this topic is related to prior videos in the queue.",
        "Track views and average view duration against a comparable prior topic, not a random baseline.",
        "Do not treat early views as proof of long-term channel fit.",
    ],
}


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
    """Provide concrete copy-paste next steps after the guardrail suggestions."""
    p = packet
    return [
        "pick relevant guardrails from the list above and add them to experiment notes or decision reason",
        f"baseline skeleton: python3 tools/experiment_baseline_starter.py {p}",
        f"notes skeleton: python3 tools/experiment_notes_starter.py {p}",
        f"hypothesis templates: python3 tools/experiment_hypothesis_suggest.py {p}",
        f"package view: python3 tools/experiment_package_starter.py {p}",
        f"setup suggestions: python3 tools/experiment_setup_report.py {p}",
        f"quality scans: python3 tools/quality_scan.py {p} && python3 tools/claim_scan.py {p}",
        f"full production if needed: python3 tools/full_production_starter.py {p}",
        "do not invent numeric baselines, results, or decisions; experiment_loop.py rejects placeholder sources",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest guardrails for an experiment change. No invented results."
    )
    parser.add_argument("packet", help="Packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    change = detect_change(path)
    guards = GUARDRAIL_MAP.get(change, GUARDRAIL_MAP["mechanism_framing"])
    print("EXPERIMENT GUARDRAIL SUGGEST (suggestions only; no invented baseline or decision)")
    print(f"packet: {path.name}")
    print(f"detected_change: {change}")
    print(f"allowed_changes: {', '.join(ALLOWED_CHANGES)}")
    print()
    print("Recommended guardrails (add to experiment notes or decision reason as needed):")
    for g in guards:
        print(f"  - {g}")
    print()
    print("These reduce common single-variable violations and metric confusion.")
    print("Do not invent a baseline or result. Use experiment_baseline_starter.py and experiment_decision_starter.py.")
    print("experiment_loop.py still requires a documented numeric baseline and explicit decision file.")
    print()
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
