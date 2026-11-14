#!/usr/bin/env python3
"""Detect recurring no-progress stall patterns in recent RUNS.md entries.

Flags long-running oauth_idle / videos_published=0 streaks as increasingly
suspicious so future agents prefer new reusable capability over restatement.
Does not poll secrets, dispatch, or modify files. Pure read of RUNS.md.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "RUNS.md"


def is_idle_section(sec: str, result: str) -> bool:
    """True when the section indicates continued OAuth/publish idle."""
    low = sec.lower()
    rlow = result.lower()
    if "stall_oauth_idle" in low:
        return True
    if "oauth" in low and ("secrets" in low or "blocker" in low):
        return True
    if any(
        p in rlow
        for p in (
            "stay 0",
            "published stay 0",
            "videos published: 0",
            "published: 0",
            "no change to human gate",
            "pre-upload path unchanged",
            "pre-upload path remains reliable",
        )
    ):
        return True
    return False


def extract_run_headers_and_results(text: str, max_runs: int = 20) -> list[dict]:
    sections = []
    current = []
    for line in text.splitlines():
        if line.startswith("## Run "):
            if current:
                sections.append("\n".join(current))
            current = [line]
        elif current:
            current.append(line)
    if current:
        sections.append("\n".join(current))
    parsed = []
    for sec in sections[:max_runs]:
        lines = sec.splitlines()
        header = lines[0] if lines else ""
        result = ""
        for l in lines:
            if l.strip().startswith("- Result:"):
                result = l.strip()[9:].strip()
                break
        idle = is_idle_section(sec, result)
        oauth_mention = "oauth" in sec.lower() or "secrets" in sec.lower() or "stall" in sec.lower()
        parsed.append({
            "header": header,
            "published_zero": idle,  # kept key name for compatibility
            "oauth_related": oauth_mention,
            "result": result[:120],
        })
    return parsed


def main() -> int:
    if not RUNS.is_file():
        print("RUNS.md missing")
        return 1
    text = RUNS.read_text(encoding="utf-8")
    runs = extract_run_headers_and_results(text, 15)
    if not runs:
        print("No runs found")
        return 0
    zero_streak = 0
    for r in runs:
        if r["published_zero"]:
            zero_streak += 1
        else:
            break
    suspicion = "LOW"
    if zero_streak >= 8:
        suspicion = (
            "HIGH (oauth_idle_without_publish recurring; pure confirmation has diminishing returns; "
            "prefer human step or one small post-publish compounder; do not re-verify materialize/contracts solely for confirmation)"
        )
    elif zero_streak >= 4:
        suspicion = "MEDIUM (repeated no-publish; continue anti-rediscovery only if it compounds)"
    else:
        suspicion = "LOW"
    print("STALL PATTERN DETECTOR (from recent RUNS.md; do not invent)")
    print(f"recent_runs_checked: {len(runs)}")
    print(f"consecutive_idle: {zero_streak}")
    print(f"suspicion_level: {suspicion}")
    print("Most recent headers:")
    for r in runs[:5]:
        print(f"  {r['header']}")
    print()
    print("If HIGH, do not spend the run only restating the stall or re-running materialize/contracts for confirmation.")
    print("Preferred: human OAuth step, or one small reusable tool that compounds after the first publish.")
    print("Full history in RUNS.md and docs/runs_archive.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
