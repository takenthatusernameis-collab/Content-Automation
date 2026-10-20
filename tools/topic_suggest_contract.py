#!/usr/bin/env python3
"""Lock the data-driven topic suggestion tool.

Verifies candidates load from JSON, existing queue titles are skipped,
output format is stable, and the tool writes nothing.
Does not scaffold, poll secrets, or modify the live queue.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
TOOL = TOOLS / "topic_suggest.py"
CANDIDATES = TOOLS / "topic_candidates.json"
QUEUE = ROOT / "docs" / "topic_queue.md"


def fail(msg: str) -> int:
    print("TOPIC SUGGEST CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("topic_suggest.py missing")
    if not CANDIDATES.is_file():
        return fail("topic_candidates.json missing")

    sys.path.insert(0, str(TOOLS))
    from topic_suggest import load_candidates, existing_titles  # noqa: E402

    candidates = load_candidates()
    if len(candidates) < 10:
        return fail(f"expected at least 10 candidates, got {len(candidates)}")
    for title, one, prob in candidates[:3]:
        if not (title and one and prob):
            return fail(f"incomplete candidate: {title!r}")

    if QUEUE.is_file():
        existing = existing_titles(QUEUE.read_text(encoding="utf-8"))
        if "stop deciding what to work on every morning" not in existing:
            return fail("Q1 title not detected in existing titles")
        # Confirm loader skips it
        from topic_suggest import suggestions, extract_niche_promise
        channel = (ROOT / "docs" / "channel.md").read_text(encoding="utf-8")
        niche, promise = extract_niche_promise(channel)
        sugg = suggestions(niche, promise, existing)
        titles = [t.lower() for t, _, _ in sugg]
        if "stop deciding what to work on every morning" in titles:
            return fail("existing Q1 title was not skipped")

    # Run the CLI and lock output shape
    proc = subprocess.run(
        [sys.executable, str(TOOL), "--count", "3"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        return fail(f"CLI exited {proc.returncode}: {proc.stderr}")
    out = proc.stdout
    required = [
        "TOPIC SUGGEST",
        "Niche:",
        "Promise:",
        "Existing titles skipped:",
        "Next id starts at:",
        "| id | status | working_title | one_line | problem |",
        "These are suggestions only.",
        "Do not scaffold until Q1 ships.",
        "Ready idea.md skeletons",
        "paste_block",
    ]
    for phrase in required:
        if phrase not in out:
            return fail(f"output missing required phrase: {phrase!r}")
    if "Q1" in out and "Stop deciding" in out:
        return fail("output contained an already-queued title")

    # Confirm no writes (queue mtime unchanged if present)
    if QUEUE.is_file():
        before = QUEUE.stat().st_mtime
        subprocess.run(
            [sys.executable, str(TOOL)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if QUEUE.stat().st_mtime != before:
            return fail("topic_suggest.py modified topic_queue.md")

    print("TOPIC SUGGEST CONTRACT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
