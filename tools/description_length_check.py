#!/usr/bin/env python3
"""Check YouTube description lengths against recommended best practices.

Reads publish.md, extracts the Description section, and reports character counts.
Flags total length against the 5000-char hard limit and the first visible portion
(approx first 150 chars / first 1-2 lines) for the pre-"show more" search/CTR zone.
Provides context for revision. Does not rewrite files. Reduces recurring
manual length checks before publish on every future packet.
Uses shared phrase_utils.normalize.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import normalize  # noqa: E402

DESC_RE = re.compile(r"## Description\s*\n(.*?)(?=\n## |\Z)", re.S)
VISIBLE_TARGET = 150  # approx chars before "show more"
IDEAL_VISIBLE_MIN = 40
IDEAL_VISIBLE_MAX = 200
HARD_TOTAL_MAX = 5000


def description_text(text: str) -> str:
    m = DESC_RE.search(text.replace("\r\n", "\n"))
    return m.group(1).strip() if m else ""


def check_description(body: str) -> list[tuple[str, str]]:
    body = normalize(body)
    issues = []
    total = len(body)
    if total == 0:
        issues.append(("empty", "no description body"))
        return issues
    if total > HARD_TOTAL_MAX:
        issues.append(("too_long", f"{total} chars (hard max {HARD_TOTAL_MAX})"))
    # First line or first VISIBLE_TARGET chars for the visible zone
    first_line = body.split("\n", 1)[0].strip()
    visible = first_line if first_line else body[:VISIBLE_TARGET]
    vlen = len(visible)
    if vlen < IDEAL_VISIBLE_MIN:
        issues.append(("visible_short", f"{vlen} chars in first line (prefer {IDEAL_VISIBLE_MIN}-{IDEAL_VISIBLE_MAX} for pre-show-more)"))
    elif vlen > IDEAL_VISIBLE_MAX:
        issues.append(("visible_long", f"{vlen} chars in first line (prefer <= {IDEAL_VISIBLE_MAX})"))
    else:
        issues.append(("visible_ok", f"{vlen} chars in first line"))
    issues.append(("total", f"{total} chars total"))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report YouTube description length vs recommended band. No file writes."
    )
    parser.add_argument("packet", type=Path)
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any non-ok")
    args = parser.parse_args()

    path = args.packet.resolve()
    pub_path = path / "publish.md"
    if not pub_path.is_file():
        print("no publish.md")
        return 0

    text = pub_path.read_text(encoding="utf-8")
    body = description_text(text)
    if not body:
        print("no Description section extracted")
        return 0

    print("DESCRIPTION LENGTH CHECK (YouTube: first ~150 chars visible; hard max 5000)")
    print(f"Packet: {path.name}")
    print()
    results = check_description(body)
    issues = 0
    for status, detail in results:
        mark = "OK" if status in ("visible_ok", "total") else status.upper()
        print(f"[{mark}] {detail}")
        if status not in ("visible_ok", "total"):
            issues += 1
    print()
    if issues == 0:
        print("Description length within recommended bands.")
        return 0
    print(f"{issues} length issue(s). Prefer a strong first line of 40-200 chars and stay under 5000 total.")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
