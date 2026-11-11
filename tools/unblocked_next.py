#!/usr/bin/env python3
"""Print concrete unblocked next actions while STALL_OAUTH_IDLE.

Focuses on capabilities that can be advanced without credentials or inventing media.
Does not poll, dispatch, write files, or scaffold packets. Soft guidance only.
Reusable to reduce rediscovery of high-leverage unblocked work across stalled runs.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    print("UNBLOCKED NEXT (while STALL_OAUTH_IDLE; published=0; no invent, no poll)")
    print()
    print("Highest-leverage unblocked (compounds after first publish):")
    print("  1. Strengthen experiment prep: run python3 tools/experiment_baseline_scaffold.py on a future packet after id exists;")
    print("     then fill from real feedback via tools/feedback_to_baseline_suggest.py (already built, fail-closed).")
    print("  2. Caption quality: human spot-check of silence-proportional aligner (tools/caption_align.py);")
    print("     do not treat as uploaded. Improve if a clear mechanical gap appears.")
    print("  3. Media QA for non-Q1: ensure card_generator.py + media_qa.py work on a dry-run new packet")
    print("     without committing pngs. Test via tempfile if needed.")
    print()
    print("Medium (documentation / anti-drift):")
    print("  - Keep HUMAN_PRIORITY.md and oauth_complete_guide.py as the single human entry.")
    print("  - Prefer tools/while_stalled_preferred.py + tools/stall_pattern_detector.py over new printers.")
    print()
    print("Avoid while published=0:")
    print("  - New consistency printers, aggregators, or contracts for already-green locks.")
    print("  - Scaffolding Q2 or inventing VO/cards/master.")
    print("  - Restating the stall without a new reusable capability.")
    print()
    print("After secrets + execute=true and private id appears:")
    print("  python3 tools/contracts_suite.py && python3 tools/human_success_check.py")
    print("  python3 tools/post_publish_sequence.py")
    print("Then feedback tools in sequence.")
    print()
    print("UNBLOCKED NEXT printed. Prefer one concrete capability advance over confirmation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
