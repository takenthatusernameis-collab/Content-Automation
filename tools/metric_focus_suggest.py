#!/usr/bin/env python3
"""Soft suggestion of primary metric and guardrails for the first experiment.

Extracts mechanism from idea.md via idea_utils. Suggests a primary metric
focused on the operational default (e.g., start rate or stall reduction)
and simple guardrails. No invented numbers or baselines.
Reduces post-publish labor of choosing what to measure against the channel niche.
Does not write files, poll, or invent data. Exit 0.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Assume idea_utils is importable when run from repo root or adjust path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
try:
    from idea_utils import extract
except ImportError:
    print("idea_utils not found; run from repo root", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"

def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print(f"No idea.md in {packet}", file=sys.stderr)
        return 1
    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = extract(idea_text)
    print("METRIC FOCUS SUGGEST (soft; no invent, no numbers)")
    print(f"packet: {packet.name}")
    print(f"mechanism: {mech or '(none)'}")
    print(f"problem: {problem or '(none)'}")
    print()
    print("Suggested primary metric (operational, tied to niche):")
    if mech:
        print(f"  - Start-completion or stall-reduction rate for viewers who install the default described in: {mech[:80]}...")
    else:
        print("  - Viewer-reported ability to start the planned work the same day (qualitative or simple yes/no)")
    print("  - Prefer a single primary: e.g. % of viewers who try the cue within 24h, or comment mentions of reduced reopen.")
    print()
    print("Simple guardrails (do not optimize solely for):")
    print("  - Retention / average view duration (secondary; avoid optimizing at expense of clarity)")
    print("  - Comment quality / objections (surface for next topics)")
    print("  - Do not chase likes or subscriber spikes as primary for this niche.")
    print()
    print("Next: after real metrics arrive, fill experiment_baseline.json using tools/baseline_source_example.py")
    print("     and tools/experiment_full_prep.py for the full skeleton.")
    print("METRIC FOCUS SUGGEST complete.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
