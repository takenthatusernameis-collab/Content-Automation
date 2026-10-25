#!/usr/bin/env python3
"""Print a pre-filled experiment hypothesis template from a packet's idea.

Extracts topic, mechanism, and problem from idea.md (or falls back to titles.md)
and emits a ready-to-copy experiment record skeleton for tools/experiment_loop.py
or docs/experiment_baseline.template.json. Reduces recurring labor of manually
drafting the hypothesis, change, target metric, and guardrails for every future
video once feedback arrives. Does not invent metrics, write files, poll secrets,
or call external services. Exit 0 always; informational only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


def extract_field(text: str, key: str) -> str:
    m = re.search(rf"^-?\s*{re.escape(key)}:\s*(.+)$", text, re.M | re.I)
    return m.group(1).strip() if m else ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a pre-filled experiment hypothesis template. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("EXPERIMENT PREP TEMPLATE (informational only; no writes)")
    print(f"Packet: {path.name}")
    print()

    idea = path / "idea.md"
    topic = mechanism = problem = ""
    if idea.is_file():
        itext = idea.read_text(encoding="utf-8")
        topic = extract_field(itext, "topic")
        mechanism = extract_field(itext, "mechanism")
        problem = extract_field(itext, "problem")

    if not topic:
        titles = path / "titles.md"
        if titles.is_file():
            ttext = titles.read_text(encoding="utf-8")
            m = re.search(r"^Primary:\s*(.+)$", ttext, re.M)
            if m:
                topic = m.group(1).strip()

    print(f"Topic: {topic or '(missing)'}")
    print(f"Mechanism: {mechanism or '(missing)'}")
    print(f"Problem: {problem or '(missing)'}")
    print()
    print("Suggested experiment skeleton (copy into experiment record; fill after real metrics):")
    print("---")
    print(f"hypothesis: Viewers who see the mechanism '{mechanism or 'the named mechanism'}' will act on the next verb more often than those who only hear the problem.")
    print("change: One material variation in the hook or CTA that names the mechanism earlier.")
    print("target_metric: average_view_duration_percent OR likes_per_view (choose one primary)")
    print("guardrails: do not drop below baseline watch-time; privacy remains private until decision")
    print("observation_window_days: 7")
    print("baseline: (paste from prior video or docs/experiment_baseline.template.json after first publish)")
    print("---")
    print()
    print("This template does not invent metrics or decide keep/discard.")
    print("Use only after a real provider_video_id and feedback_state.json exist.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
