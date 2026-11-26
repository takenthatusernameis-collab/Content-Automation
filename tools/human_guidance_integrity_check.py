#!/usr/bin/env python3
"""Check integrity of the critical human OAuth guidance path.

Verifies that key guidance files and the tools they reference exist,
are non-empty, and contain the expected commands (three secrets + dispatch).
Addresses risk that the sole remaining human step becomes broken or inconsistent.
Soft informational; exit 1 only on clear missing/empty or missing keywords.
Does not invent data, poll secrets, or write files.
Compounds reliability of the human-facing path while STALL_OAUTH_IDLE persists.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Critical files that must exist and be non-trivial
REQUIRED_FILES = [
    "NEXT.md",
    "HANDOFF.md",
    "docs/HUMAN_PRIORITY.md",
    "tools/human_starter.py",
    "tools/oauth_complete_guide.py",
    "tools/human_preflight.py",
    "tools/oauth_exchange.py",
    "tools/long_stall_report.py",
]

# Tools referenced by human_starter.py that must exist
STARTER_REFS = [
    "human_preflight.py",
    "long_stall_report.py",
    "recurring_pattern_flag.py",
    "contract_streak_detector.py",
    "publish_readiness.py",
    "human_one_pager.py",
]

# Keywords that must appear in guidance files (exact phrases for the human step)
GUIDANCE_KEYWORDS = [
    "YOUTUBE_CLIENT_ID",
    "YOUTUBE_CLIENT_SECRET",
    "YOUTUBE_REFRESH_TOKEN",
    "execute=true",
    "youtube-production.yml",
]

def check_file(path: Path, min_size: int = 100) -> list[str]:
    issues = []
    if not path.is_file():
        issues.append(f"MISSING {path.relative_to(ROOT)}")
        return issues
    try:
        size = path.stat().st_size
        if size < min_size:
            issues.append(f"TOO_SMALL {path.relative_to(ROOT)} size={size}")
        text = path.read_text(encoding="utf-8", errors="replace")
        if not text.strip():
            issues.append(f"EMPTY {path.relative_to(ROOT)}")
    except OSError as e:
        issues.append(f"UNREADABLE {path.relative_to(ROOT)}: {e}")
    return issues

def main() -> int:
    print("HUMAN GUIDANCE INTEGRITY CHECK (critical OAuth path; no invent, no poll)")
    print("=" * 70)
    issues: list[str] = []

    for rel in REQUIRED_FILES:
        issues.extend(check_file(ROOT / rel))

    for rel in STARTER_REFS:
        issues.extend(check_file(ROOT / "tools" / rel, min_size=50))

    # Keyword presence in key guidance
    for rel in ["NEXT.md", "docs/HUMAN_PRIORITY.md", "tools/oauth_complete_guide.py"]:
        path = ROOT / rel
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            for kw in GUIDANCE_KEYWORDS:
                if kw not in text:
                    issues.append(f"MISSING_KEYWORD '{kw}' in {rel}")

    if issues:
        print("FAIL: integrity issues found")
        for i in issues:
            print(f"  - {i}")
        print("Fix the guidance path before relying on it for the human OAuth step.")
        return 1

    print("PASS: all critical human guidance files present, non-empty, and contain expected commands.")
    print("Human path remains consistent. STALL_OAUTH_IDLE continues; only human action advances publish.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
