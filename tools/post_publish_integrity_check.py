#!/usr/bin/env python3
"""Check integrity of the post-publish learning path guidance.

Verifies that key post-publish files and tools exist, are non-empty,
and contain expected keywords (collect_feedback, observation window, experiment loop, etc.).
Protects the next stage after the first private video id appears.
Soft informational; exit 1 only on clear missing/empty or missing keywords.
Does not invent data, poll secrets, or write files.
Compounds reliability of the post-OAuth path.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Critical post-publish files
REQUIRED_FILES = [
    "tools/after_upload_steps.py",
    "tools/post_publish_path_ready.py",
    "tools/observation_window.py",
    "tools/experiment_loop.py",
    "tools/complete.py",
    "docs/q1_post_publish_prep.md",
    "docs/experiments.md",
]

# Keywords that must appear in guidance
GUIDANCE_KEYWORDS = [
    "collect_feedback=true",
    "observation_window",
    "experiment_loop",
    "provider_video_id",
    "feedback_state.json",
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
    print("POST-PUBLISH INTEGRITY CHECK (next-stage path; no invent, no poll)")
    print("=" * 70)
    issues: list[str] = []

    for rel in REQUIRED_FILES:
        issues.extend(check_file(ROOT / rel))

    # Keyword presence in key guidance
    for rel in ["tools/after_upload_steps.py", "docs/q1_post_publish_prep.md"]:
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
        print("Fix the post-publish path before relying on it after first video id.")
        return 1

    print("PASS: all critical post-publish files present, non-empty, and contain expected keywords.")
    print("Next-stage path remains consistent. After OAuth + video id + window, use after_upload_steps.py.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
