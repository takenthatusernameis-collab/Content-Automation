#!/usr/bin/env python3
"""Check integrity of the pre-upload production path.

Verifies that the main YouTube production workflow and critical supporting tools
exist, are non-empty, and contain expected keywords (execute, materialize, media_qa,
collect_feedback, etc.). Protects the path that runs once OAuth secrets exist.
Soft informational; exit 1 only on clear missing/empty or missing keywords.
Does not invent data, poll secrets, or write files.
Compounds reliability of the production workflow while STALL_OAUTH_IDLE persists.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Critical production files
REQUIRED_FILES = [
    ".github/workflows/youtube-production.yml",
    "tools/youtube_upload.py",
    "tools/media_qa.py",
    "tools/materialize_q1_release.py",
    "tools/export_probe.py",
    "tools/caption_gate.py",
    "tools/oauth_preflight.py",
    "tools/packet_path.py",
]

# Keywords that must appear in the production workflow
WORKFLOW_KEYWORDS = [
    "execute",
    "collect_feedback",
    "materialize_q1_release.py",
    "media_qa.py",
    "youtube_upload.py",
    "oauth_preflight.py",
]

def check_file(path: Path, min_size: int = 200) -> list[str]:
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
    print("PRODUCTION PATH INTEGRITY CHECK (pre-upload workflow; no invent, no poll)")
    print("=" * 70)
    issues: list[str] = []

    for rel in REQUIRED_FILES:
        issues.extend(check_file(ROOT / rel))

    # Keyword presence in the main workflow
    wf = ROOT / ".github/workflows/youtube-production.yml"
    if wf.is_file():
        text = wf.read_text(encoding="utf-8", errors="replace")
        for kw in WORKFLOW_KEYWORDS:
            if kw not in text:
                issues.append(f"MISSING_KEYWORD '{kw}' in youtube-production.yml")

    if issues:
        print("FAIL: integrity issues found")
        for i in issues:
            print(f"  - {i}")
        print("Fix the production path before relying on it after OAuth secrets are set.")
        return 1

    print("PASS: all critical production files present, non-empty, and contain expected keywords.")
    print("Pre-upload path remains consistent. After OAuth + execute=true, the workflow can run.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
