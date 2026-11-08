#!/usr/bin/env python3
"""Read-only integrity check for docs/topic_queue.md fields.

No writes. No invent. No packet required. No secrets.
Checks every row for:
- non-empty id, status, working_title, one_line
- status is one of queued/used/parked
- problem field present (warn if empty for queued)
- one_line and problem length reasonable (not too short)
- no duplicate ids or working_titles
- slug uniqueness among queued/used

Prints issues with severity. Exit 0 if clean or only soft warnings; 1 on hard issues.
Useful to catch queue data problems before any starter or scaffold uses them.
Reduces future labor by preventing bad queue rows from propagating into packets.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from queue_lib import parse_queue, slugify  # type: ignore


def check_rows(rows: list[dict]) -> list[tuple[str, str, str]]:
    """Return list of (severity, id, message) issues. Pure; no I/O."""
    issues: list[tuple[str, str, str]] = []
    ids = set()
    titles = set()
    slugs = set()
    valid_status = {"queued", "used", "parked"}

    for r in rows:
        tid = r.get("id", "")
        status = r.get("status", "")
        title = r.get("working_title") or ""
        one_line = r.get("one_line") or ""
        problem = r.get("problem") or ""

        if not tid:
            issues.append(("HARD", "?", "Row missing id"))
            continue
        if tid in ids:
            issues.append(("HARD", tid, f"Duplicate id {tid}"))
        ids.add(tid)

        if status not in valid_status:
            issues.append(("HARD", tid, f"Invalid status '{status}' (must be queued/used/parked)"))

        if not title.strip():
            issues.append(("HARD", tid, "Empty working_title"))
        elif title in titles:
            issues.append(("HARD", tid, f"Duplicate working_title: {title}"))
        titles.add(title)

        if not one_line.strip():
            issues.append(("HARD", tid, "Empty one_line"))
        elif len(one_line) < 20:
            issues.append(("SOFT", tid, f"one_line very short ({len(one_line)} chars)"))

        if status == "queued" and not problem.strip():
            issues.append(("SOFT", tid, "Queued row has empty problem field"))

        if problem and len(problem) < 15:
            issues.append(("SOFT", tid, f"problem very short ({len(problem)} chars)"))

        slug = slugify(title)
        if slug in slugs:
            issues.append(("SOFT", tid, f"Slug collision risk: {slug}"))
        slugs.add(slug)

    return issues


def main() -> int:
    queue_path = ROOT / "docs" / "topic_queue.md"
    if not queue_path.is_file():
        print(f"Missing queue: {queue_path}", file=sys.stderr)
        return 1

    rows = parse_queue(queue_path.read_text(encoding="utf-8"))
    if not rows:
        print("No rows in topic queue.")
        return 0

    issues = check_rows(rows)

    print("# Topic queue field integrity (read-only)")
    print(f"Rows checked: {len(rows)}")
    if not issues:
        print("OK: no issues found.")
        print("All rows have required fields, valid status, unique ids/titles.")
        return 0

    hard = [i for i in issues if i[0] == "HARD"]
    soft = [i for i in issues if i[0] == "SOFT"]
    print(f"Issues: {len(hard)} hard, {len(soft)} soft")
    for sev, tid, msg in issues:
        print(f"  {sev} [{tid}]: {msg}")
    print()
    print("HARD issues should be fixed in docs/topic_queue.md before scaffolding or heavy use of starters.")
    print("SOFT are warnings. Do not invent content. Preferred human next remains OAuth.")
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
