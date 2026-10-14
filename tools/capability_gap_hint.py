#!/usr/bin/env python3
"""Hint at one high-value unblocked capability gap from production_capabilities.md.

Scans for PLAN_BUILT / READY_FOR_MEDIA / NOT_BUILT mentions so agents can choose
a small reusable improvement instead of restating the stall when suspicion is HIGH.
Does not invent capabilities, does not poll secrets, does not write files.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT / "docs" / "production_capabilities.md"


def main() -> int:
    if not CAP.is_file():
        print("capability_gap_hint: production_capabilities.md missing")
        return 1
    text = CAP.read_text(encoding="utf-8")
    candidates = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        lower = line.lower()
        if any(s in lower for s in ("plan_built", "ready_for_media", "not_built", "ready_for_credential")):
            context = line.strip()
            if i > 0:
                context = lines[i-1].strip()[:80] + " | " + context
            candidates.append(context[:160])
        if len(candidates) >= 8:
            break
    print("CAPABILITY GAP HINT (from production_capabilities.md; no invent)")
    if not candidates:
        print("No PLAN_BUILT / READY_FOR_* / NOT_BUILT markers found in scanned lines.")
    else:
        print("Possible unblocked gaps (prefer smallest reusable one that compounds):")
        for i, c in enumerate(candidates[:5], 1):
            print(f"  {i}. {c}")
    print()
    print("Current external blocker remains OAuth secrets. Prefer human step or a gap that reduces labor after publish.")
    print("Full contract in docs/production_capabilities.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
