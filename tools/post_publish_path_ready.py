#!/usr/bin/env python3
"""Soft check that the post-publish experiment / learning path is ready.

Verifies presence of key reusable tools and templates so agents and humans
do not rediscover whether the learning loop infrastructure exists after the
first private video id appears. Does not invent metrics, baselines, or
decisions. Does not poll secrets or dispatch. Exit 0 if core path present.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CORE = [
    "tools/experiment_loop.py",
    "tools/experiment_template_validator.py",
    "tools/after_upload_steps.py",
    "tools/observation_window.py",
    "tools/feedback_review_brief.py",
    "tools/feedback_to_baseline_suggest.py",
    "tools/feedback_to_decision_suggest.py",
    "tools/next_from_decision.py",
    "tools/feedback_to_topic_suggest.py",
    "docs/experiment_baseline.template.json",
    "docs/experiment_decision.template.json",
]

def main() -> int:
    print("POST-PUBLISH PATH READY CHECK (soft; no invent, no poll)")
    missing = []
    for rel in CORE:
        p = ROOT / rel
        if p.is_file():
            print(f"  PRESENT: {rel}")
        else:
            print(f"  MISSING: {rel}")
            missing.append(rel)
    print()
    if missing:
        print(f"FAIL: {len(missing)} core post-publish files missing. Path not fully ready.")
        return 1
    print("PASS: Core post-publish experiment/learning path files are present.")
    print("After first private video id + observation window DUE, use:")
    print("  python3 tools/after_upload_steps.py videos/002-...")
    print("Then fill templates only from real comparison evidence.")
    print("Validate filled files with tools/experiment_template_validator.py")
    print("Do not invent baselines or decisions.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
