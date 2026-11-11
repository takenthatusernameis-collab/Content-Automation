#!/usr/bin/env python3
"""One-command post-publish preparation summary for a packet.

Combines experiment hypothesis skeleton (from idea.md) and feedback.md structure
starter into a single concise view, plus the fixed observation-window rules and
the exact tool sequence to run after a real collect.
Reduces future human/agent sequential invocations for preparing the feedback and
experiment records once the first private video id exists.
Does not invent metrics, comments, baselines, decisions, or video ids.
Does not write files, poll secrets, dispatch, or call external services.
Fail-closed informational only. Reusable across future packets.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def run_tool(script: str, packet: Path) -> str:
    path = TOOLS / script
    if not path.is_file():
        return f"MISSING {script}"
    try:
        proc = subprocess.run(
            [sys.executable, str(path), str(packet)],
            capture_output=True,
            text=True,
            check=False,
            cwd=ROOT,
        )
        out = (proc.stdout or "").strip()
        if proc.returncode != 0:
            out += f"\n(exit {proc.returncode})"
        return out or "(no output)"
    except Exception as exc:
        return f"EXCEPTION {script}: {exc}"


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"Not a directory: {packet}", file=sys.stderr)
        return 1

    print("POST-PUBLISH PREP SUMMARY (informational only; no invent, no writes)")
    print(f"packet: {packet.name}")
    print()
    print("=== Observation window (fixed rule) ===")
    print("First collect is due at uploaded_at + 10 days (7 calendar + 3 Analytics lag).")
    print("Early collect returns OBSERVATION_WINDOW_NOT_DUE. Do not invent dates or metrics.")
    print("After a real provider_video_id appears in upload_state.json:")
    print("  python3 tools/post_publish_sequence.py", packet)
    print()
    print("=== Experiment hypothesis skeleton (from idea.md; fill after real metrics) ===")
    print(run_tool("experiment_prep.py", packet))
    print()
    print("=== Feedback.md structure starter (anticipated questions from script; fill with real comments only) ===")
    print(run_tool("feedback_review_starter.py", packet))
    print()
    print("=== Exact sequence after a real collect produces feedback_state.json with comments ===")
    print("  python3 tools/feedback_review_brief.py", packet)
    print("  python3 tools/feedback_to_baseline_suggest.py", packet)
    print("  python3 tools/feedback_topic_suggest.py", packet)
    print("  # Review signals, then fill experiment_baseline.json with real numeric baseline + documented source")
    print("  python3 tools/experiment_template_validator.py", packet / "experiment_baseline.json")
    print("  python3 tools/experiment_loop.py", packet)
    print("  python3 tools/feedback_to_decision_suggest.py", packet)
    print("  # Fill chosen experiment_decision.json, validate, then:")
    print("  python3 tools/next_from_decision.py", packet / "experiment_decision.json")
    print()
    print("Do not invent comments, metrics, baselines, or decisions.")
    print("This summary writes nothing and does not advance any gate.")
    print("POST-PUBLISH PREP SUMMARY complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
