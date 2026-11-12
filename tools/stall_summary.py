#!/usr/bin/env python3
"""Concise one-command summary of the current STALL_OAUTH_IDLE status.

Prints videos published, primary blocker, exact human next action, and recommended
unblocked work. Reduces rediscovery labor for agents and humans across long stalls.
Does not poll secrets, dispatch, write files, or invent data. Exit 0 always.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    print("STALL SUMMARY (informational only; no poll, no dispatch, no writes)")
    print()
    print("Videos published: 0")
    print("Primary blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent)")
    print("Suspicion: HIGH after 1000+ runs with no progress")
    print("Pre-upload path: reliable (Q1 media materialize + media_qa PASS + contracts 96/96)")
    print()
    print("Exact human next action (10-20 minutes):")
    print("  python3 tools/oauth_complete_guide.py")
    print("  # or: python3 tools/human_starter.py")
    print("  # or: docs/HUMAN_PRIORITY.md")
    print("Then: gh secret set the three values, then one dispatch:")
    print("  gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false")
    print()
    print("Recommended unblocked (while stalled):")
    print("  python3 tools/unblocked_next.py")
    print("  python3 tools/niche_metric_bridge.py videos/002-stop-deciding-what-to-work-on-every-morning")
    print("  python3 tools/same_day_install_observability.py videos/002-stop-deciding-what-to-work-on-every-morning")
    print("  python3 tools/niche_consistency_scan.py")
    print("  python3 tools/metric_focus_suggest.py videos/002-stop-deciding-what-to-work-on-every-morning")
    print("  python3 tools/feedback_to_topic_suggest.py videos/002-stop-deciding-what-to-work-on-every-morning")
    print("  python3 tools/experiment_full_prep.py videos/002-stop-deciding-what-to-work-on-every-morning")
    print("  python3 tools/topic_queue_mechanism_check.py")
    print("  python3 tools/packet_niche_check.py videos/002-stop-deciding-what-to-work-on-every-morning")
    print("  python3 tools/first_experiment_suggest.py videos/002-stop-deciding-what-to-work-on-every-morning")
    print("  python3 tools/packet_prep_summary.py videos/002-stop-deciding-what-to-work-on-every-morning")
    print("  python3 tools/post_publish_prep_summary.py videos/002-stop-deciding-what-to-work-on-every-morning")
    print("  python3 tools/experiment_json_examples.py")
    print("  python3 tools/baseline_source_example.py")
    print("  python3 tools/decision_source_example.py")
    print()
    print("Do not poll secrets. Do not rematerialize media if present. Do not scaffold Q2.")
    print("STALL SUMMARY complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
