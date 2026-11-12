#!/usr/bin/env python3
"""Soft bridge from channel niche promise to measurable experiment signals.

Extracts mechanism via idea_utils. Suggests practical ways to observe the core
promise (viewer installs one small default the same day) without inventing
numbers or baselines. Complements generic Analytics metrics with niche-specific
qualitative and proxy signals.
Does not write files, poll, or invent data. Exit 0.
"""

from __future__ import annotations

import sys
from pathlib import Path

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
    print("NICHE METRIC BRIDGE (soft; no invent, no numbers)")
    print(f"packet: {packet.name}")
    print(f"channel promise: After each video the viewer can install one small default (cue, constraint, or checklist) the same day.")
    print(f"mechanism: {mech or '(none)'}")
    print(f"problem: {problem or '(none)'}")
    print()
    print("Primary operational signal (tied to promise; prefer over pure AVD for this niche):")
    print("  - Viewer comments or replies that mention installing, trying, starting, or using the named default the same day.")
    print("  - Qualitative count or rate of such mentions in the observation window (document source).")
    if mech:
        print(f"  - Specific cue from mechanism: look for language around '{mech[:60]}...'")
    print()
    print("Useful proxy Analytics fields (secondary; do not optimize solely for them):")
    print("  - average_view_duration_seconds or average_percentage_viewed (especially early if mechanism is front-loaded)")
    print("  - comments (volume + quality of operational replies)")
    print("  - Do not treat likes, CTR, or subscriber spikes as primary for the 'install default' promise.")
    print()
    print("How to use after real feedback arrives:")
    print("  1. Collect comments via tools/youtube_feedback.py (once credentials + id + window exist).")
    print("  2. Manually or with a later scanner count operational-install mentions.")
    print("  3. Document the count or rate as the baseline/source in experiment_baseline.json.")
    print("  4. Use tools/metric_focus_suggest.py and tools/experiment_full_prep.py for the full setup.")
    print()
    print("Do not invent counts or rates. experiment_loop.py requires documented numeric baseline and source.")
    print("NICHE METRIC BRIDGE complete.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
