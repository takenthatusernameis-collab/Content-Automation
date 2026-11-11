#!/usr/bin/env python3
"""Local structural readiness check for the post-publish feedback ingestion path.

Verifies presence of the feedback adapter, observation window helpers, related
suggest/review tools, and state expectations.
Prints a concise readiness summary and the exact fail-closed sequence to run
after a real provider_video_id and uploaded_at exist (and the +10d window is due).
Does not invent metrics, video ids, comments, or baselines.
Does not poll secrets, dispatch, write files, or call external services.
Reusable to reduce rediscovery of the feedback collection and early review path
across stalled runs.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

KEY_ITEMS = [
    ("tools/youtube_feedback.py", TOOLS / "youtube_feedback.py"),
    ("tools/observation_window.py", TOOLS / "observation_window.py"),
    ("tools/post_upload_confirm.py", TOOLS / "post_upload_confirm.py"),
    ("tools/upload_date.py", TOOLS / "upload_date.py"),
    ("tools/feedback_review_brief.py", TOOLS / "feedback_review_brief.py"),
    ("tools/feedback_review_starter.py", TOOLS / "feedback_review_starter.py"),
    ("tools/comment_class_suggest.py", TOOLS / "comment_class_suggest.py"),
    ("tools/feedback_hypothesis_suggest.py", TOOLS / "feedback_hypothesis_suggest.py"),
    ("tools/feedback_to_baseline_suggest.py", TOOLS / "feedback_to_baseline_suggest.py"),
    ("tools/feedback_topic_suggest.py", TOOLS / "feedback_topic_suggest.py"),
    ("tools/post_publish_sequence.py", TOOLS / "post_publish_sequence.py"),
]


def main() -> int:
    print("FEEDBACK INGESTION READINESS (structural only; no invent, no poll, no writes)")
    print()
    missing = []
    present = []
    for name, path in KEY_ITEMS:
        if path.is_file():
            present.append(name)
        else:
            missing.append(name)
    print(f"Present: {len(present)} / {len(KEY_ITEMS)}")
    for name in present:
        print(f"  PRESENT  {name}")
    if missing:
        print()
        print("MISSING (repair before relying on the feedback path):")
        for name in missing:
            print(f"  MISSING  {name}")
    else:
        print()
        print("All key feedback-ingestion files are present.")
    print()
    print("Fail-closed sequence after a real private provider_video_id appears in upload_state.json:")
    print("  1. python3 tools/post_upload_confirm.py <packet>")
    print("  2. python3 tools/observation_window.py <packet>   # DUE only after uploaded_at + 10d")
    print("  3. (when DUE) gh workflow dispatch youtube-production.yml --repo ... -f execute=false -f collect_feedback=true")
    print("  4. (after collect) python3 tools/feedback_review_brief.py <packet>")
    print("  5. python3 tools/comment_class_suggest.py <packet>")
    print("  6. python3 tools/feedback_hypothesis_suggest.py <packet>")
    print("  7. python3 tools/feedback_to_baseline_suggest.py <packet>")
    print("  8. python3 tools/feedback_topic_suggest.py <packet>")
    print("  9. Then continue into experiment_loop_readiness sequence (baseline fill, validator, experiment_loop.py, decision).")
    print()
    print("youtube_feedback.py is dry-run by default; --execute requires OAuth and a due window.")
    print("Early collect is OBSERVATION_WINDOW_NOT_DUE. Do not invent metrics or comments.")
    print("Human OAuth remains the only blocker for first publish. Do not poll secrets.")
    print("FEEDBACK INGESTION READINESS complete.")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
