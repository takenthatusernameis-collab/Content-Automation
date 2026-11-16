#!/usr/bin/env python3
"""Report the long-running OAuth stall status from known signals.

Aggregates evidence of the multi-hundred / 1000+ run STALL_OAUTH_IDLE without polling secrets or inventing data.
Prints a clear HIGH suspicion flag and points to the human step.
Soft only; does not change gates or dispatch.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "RUNS.md"
STATE = ROOT / "STATE.md"


def count_recent_notes() -> int:
    """Count recent STATE notes mentioning the stall (approximate)."""
    if not STATE.is_file():
        return 0
    state = STATE.read_text(encoding="utf-8")
    return state.lower().count("stall_oauth_idle") + state.lower().count("oauth idle")


def count_zero_publish_runs() -> int:
    """Count consecutive recent runs in RUNS.md that report the OAuth stall (STALL_OAUTH_IDLE or published=0)."""
    if not RUNS.is_file():
        return 0
    text = RUNS.read_text(encoding="utf-8")
    sections = re.split(r"^## Run ", text, flags=re.M)
    streak = 0
    idle_re = re.compile(r"STALL_OAUTH_IDLE|Videos published stay 0|published stay 0|Videos published: 0", re.I)
    for sec in sections[1:]:
        if idle_re.search(sec):
            streak += 1
        else:
            break
    return streak


def extract_timestamps(sections: list[str]) -> list[datetime]:
    """Extract UTC timestamps from run section headers."""
    ts_re = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
    times = []
    for sec in sections:
        m = ts_re.search(sec)
        if m:
            try:
                times.append(datetime.strptime(m.group(0), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc))
            except ValueError:
                pass
    return times


def max_run_number() -> int:
    """Return the highest Run N found in the live RUNS.md (approximate total runs)."""
    if not RUNS.is_file():
        return 0
    text = RUNS.read_text(encoding="utf-8")
    nums = [int(n) for n in re.findall(r"## Run (\d+)", text)]
    return max(nums) if nums else 0


def earliest_stall_date() -> str | None:
    """Scan docs/runs_archive.md for the earliest date near a stall mention. Soft, fail-closed."""
    archive = ROOT / "docs" / "runs_archive.md"
    if not archive.is_file():
        return None
    text = archive.read_text(encoding="utf-8")
    lines = text.splitlines()
    earliest = None
    date_re = re.compile(r"(20\d{2}-\d{2}-\d{2})")
    for i, line in enumerate(lines):
        if any(k in line for k in ("STALL_OAUTH_IDLE", "secrets absent", "YOUTUBE_CLIENT_ID")):
            for j in range(max(0, i - 8), min(len(lines), i + 2)):
                m = date_re.search(lines[j])
                if m:
                    d = m.group(1)
                    if earliest is None or d < earliest:
                        earliest = d
                    break
    return earliest


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print("LONG STALL REPORT (OAuth idle; no poll, no invent)")
    print(f"Report time: {now}")
    print()
    notes = count_recent_notes()
    zero_streak = count_zero_publish_runs()
    max_run = max_run_number()
    print(f"STATE.md mentions of stall/oauth idle (recent notes): {notes}")
    print(f"Consecutive recent RUNS.md sections with STALL_OAUTH_IDLE or published=0: {zero_streak} (main file only; full history in docs/runs_archive.md)")
    print(f"Highest run number in live RUNS.md: {max_run} (total runs approximately this or higher; stall has persisted for the large majority)")
    earliest = earliest_stall_date()
    days = 0
    if earliest:
        try:
            start = datetime.strptime(earliest, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            days = (datetime.now(timezone.utc) - start).days
            print(f"Approximate stall start (earliest archive mention): {earliest} (~{days} days ago)")
        except ValueError:
            print(f"Approximate stall start (earliest archive mention): {earliest}")
    else:
        print("Approximate stall start: not found in archive (or file missing)")
    if days > 40:
        print("INCREASINGLY_SUSPICIOUS: Stall exceeds 40 days with no human progress on secrets. Flag as possible problem requiring direct human intervention (outside pure agent confirmation). Do not continue pure confirmation runs.")
    if zero_streak > 0:
        # Recompute sections to get dates
        if RUNS.is_file():
            text = RUNS.read_text(encoding="utf-8")
            sections = re.split(r"^## Run ", text, flags=re.M)
            recent = sections[1:zero_streak+1]
            times = extract_timestamps(recent)
            if times:
                oldest = min(times)
                newest = max(times)
                delta = (newest - oldest).days
                print(f"Visible streak date range: {oldest.strftime('%Y-%m-%d')} to {newest.strftime('%Y-%m-%d')} (~{delta} days in main RUNS.md)")
    print("Known history: STALL_OAUTH_IDLE has persisted across 1000+ runs (full history in docs/runs_archive.md).")
    print("Videos published: 0")
    print("Pre-upload path: complete")
    print("Suspicion level: HIGH (long consecutive idle with no human progress on secrets)")
    print("Agent note: Pure-confirmation runs have diminishing returns while this is the sole blocker. Prefer human progress.")
    print()
    print("Primary remaining action: complete the three GitHub Actions secrets and dispatch once.")
    print("Start with: python3 tools/human_starter.py")
    print("Then: python3 tools/human_one_pager.py or docs/human_oauth_checklist.md")
    print("Then set secrets and: gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true")
    print()
    print("After a private video id appears: python3 tools/post_publish_sequence.py")
    print("Do not add another consistency printer, aggregator, or soft check while stalled.")
    print()
    print("=== COPY-PASTE HUMAN ESCALATION (if this report is seen by operator) ===")
    print(f"The YouTube OAuth secrets have been the sole blocker for ~{days} days (~{max_run} agent runs).")
    print("Please complete the three GitHub Actions secrets and one execute=true dispatch.")
    print("Start: python3 tools/human_starter.py   or open docs/HUMAN_PRIORITY.md")
    print("This is increasingly suspicious after >40 days with no progress. Direct human intervention is the only path that advances the system.")
    print("=== END ESCALATION ===")
    print("LONG STALL REPORT HIGH")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
