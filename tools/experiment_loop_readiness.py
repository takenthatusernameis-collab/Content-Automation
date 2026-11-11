#!/usr/bin/env python3
"""Local structural readiness check for the post-publish experiment / learning loop.

Verifies presence of key templates, starters, validators, and the loop itself.
Prints a concise readiness summary and the exact fail-closed sequence to run
after a real provider_video_id and feedback_state.json exist.
Does not invent metrics, baselines, decisions, or video ids.
Does not poll secrets, dispatch, write files, or call external services.
Reusable to reduce rediscovery of the learning-loop path across stalled runs.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
DOCS = ROOT / "docs"

KEY_ITEMS = [
    ("docs/experiment_baseline.template.json", DOCS / "experiment_baseline.template.json"),
    ("docs/experiment_decision.template.json", DOCS / "experiment_decision.template.json"),
    ("tools/experiment_loop.py", TOOLS / "experiment_loop.py"),
    ("tools/experiment_baseline_starter.py", TOOLS / "experiment_baseline_starter.py"),
    ("tools/experiment_baseline_scaffold.py", TOOLS / "experiment_baseline_scaffold.py"),
    ("tools/experiment_template_validator.py", TOOLS / "experiment_template_validator.py"),
    ("tools/experiment_metric_suggest.py", TOOLS / "experiment_metric_suggest.py"),
    ("tools/feedback_to_baseline_suggest.py", TOOLS / "feedback_to_baseline_suggest.py"),
    ("tools/feedback_to_decision_suggest.py", TOOLS / "feedback_to_decision_suggest.py"),
    ("tools/next_from_decision.py", TOOLS / "next_from_decision.py"),
    ("tools/post_publish_prep_summary.py", TOOLS / "post_publish_prep_summary.py"),
]


def main() -> int:
    print("EXPERIMENT LOOP READINESS (structural only; no invent, no poll, no writes)")
    print()
    missing = []
    present = []
    for name, path in KEY_ITEMS:
        if path.is_file():
            present.append(name)
        else:
            missing.append(name)
    print(f"Present: {len(present)} / {len(KEY_ITEMS)}")
    for name in present:
        print(f"  PRESENT  {name}")
    if missing:
        print()
        print("MISSING (repair before relying on the loop):")
        for name in missing:
            print(f"  MISSING  {name}")
    else:
        print()
        print("All key experiment-loop files are present.")
    print()
    print("Fail-closed sequence after a real private provider_video_id and uploaded_at + 10d window:")
    print("  1. python3 tools/post_publish_sequence.py <packet>")
    print("  2. (after collect) python3 tools/feedback_review_brief.py <packet>")
    print("  3. python3 tools/feedback_to_baseline_suggest.py <packet>")
    print("  4. # fill experiment_baseline.json with real numeric baseline + documented source")
    print("  5. python3 tools/experiment_template_validator.py <packet>/experiment_baseline.json")
    print("  6. python3 tools/experiment_loop.py <packet>")
    print("  7. python3 tools/feedback_to_decision_suggest.py <packet>")
    print("  8. # fill experiment_decision.json, validate, then python3 tools/next_from_decision.py ...")
    print()
    print("Do not invent baselines, sources, metrics, or decisions. experiment_loop.py rejects them.")
    print("Human OAuth remains the only blocker for first publish. Do not poll secrets.")
    print("EXPERIMENT LOOP READINESS complete.")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
