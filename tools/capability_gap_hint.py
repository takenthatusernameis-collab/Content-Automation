#!/usr/bin/env python3
"""Hint at high-value unblocked capability gaps from production_capabilities.md.

Parses structured capability descriptions and state markers so agents can choose
a small reusable improvement instead of restating the stall when suspicion is HIGH.
Prefers PLAN_BUILT / READY_FOR_MEDIA local steps that do not require credentials.
Does not invent capabilities, does not poll secrets, does not write files.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT / "docs" / "production_capabilities.md"

STATE_RE = re.compile(
    r"(PLAN_BUILT|READY_FOR_MEDIA|READY_FOR_CREDENTIAL|NOT_BUILT|BLOCKED)",
    re.IGNORECASE,
)
TOOL_RE = re.compile(r"`(tools/[^`]+)`")


def extract_gaps(text: str) -> list[str]:
    """Return up to 6 clean, prioritized gap summaries."""
    candidates: list[tuple[int, str]] = []  # (priority, text); lower priority = better
    lines = text.splitlines()
    current_section = ""
    for i, raw in enumerate(lines):
        line = raw.strip()
        if line.startswith("###"):
            current_section = line.lstrip("#").strip()
            continue
        m = STATE_RE.search(line)
        if not m:
            continue
        state = m.group(1).upper()
        # Prefer local non-credential gaps
        priority = 10
        if state in ("PLAN_BUILT", "READY_FOR_MEDIA"):
            priority = 1
        elif state == "NOT_BUILT":
            priority = 3
        elif "CREDENTIAL" in state or "BLOCKED" in state:
            priority = 8
        # Extract tool if present
        tool_m = TOOL_RE.search(line)
        tool = tool_m.group(1) if tool_m else ""
        # Clean description: take the capability phrase before the state or the line itself
        desc = re.sub(r"\(.*\)", "", line).strip(" -|")
        if len(desc) < 20 and i > 0:
            prev = lines[i - 1].strip(" -|")
            if prev and not prev.startswith("#"):
                desc = prev[:100] + " → " + desc
        summary = f"{state}: {desc}"
        if tool:
            summary += f" [{tool}]"
        if current_section:
            summary = f"[{current_section}] {summary}"
        candidates.append((priority, summary[:180]))
    # Sort by priority, then stable
    candidates.sort(key=lambda x: x[0])
    seen = set()
    out = []
    for _, s in candidates:
        key = s[:60]
        if key not in seen:
            seen.add(key)
            out.append(s)
        if len(out) >= 6:
            break
    return out


def main() -> int:
    if not CAP.is_file():
        print("capability_gap_hint: production_capabilities.md missing")
        return 1
    text = CAP.read_text(encoding="utf-8")
    gaps = extract_gaps(text)
    print("CAPABILITY GAP HINT (cleaner parse; no invent)")
    if not gaps:
        print("No structured PLAN_BUILT / READY_FOR_* / NOT_BUILT markers found.")
    else:
        print("Prioritized unblocked-leaning gaps (prefer smallest that compounds after publish):")
        for i, g in enumerate(gaps, 1):
            print(f"  {i}. {g}")
    print()
    print("Current external blocker remains OAuth secrets. Prefer human step or a gap that reduces labor after publish.")
    print("Full contract in docs/production_capabilities.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
