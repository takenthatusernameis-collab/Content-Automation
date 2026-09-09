#!/usr/bin/env python3
"""Contract check for scaffold + queue-mark handoff.

Read-only versus the repo videos/ tree. May import new_packet.mark_followup
which reads docs/topic_queue.md. Never writes the queue or sample-001.

Locks:
- new_packet does not call mark_topic --write
- mark_followup prints a dry-run line then a commented --write
- empty titles `1.` stay untitled
- next_id treats sample-001 as 001
"""

from __future__ import annotations

import ast
import re
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from new_packet import mark_followup  # noqa: E402
from queue_lib import next_id, slugify  # noqa: E402


def titles_filled(text: str) -> bool:
    """Must stay identical to after_scaffold.titles_filled."""
    prim = re.search(r"^Primary:[ \t]*([^\n]*)$", text, re.M)
    if prim and prim.group(1).strip():
        return True
    return bool(re.search(r"^\d+\.[ \t]+\S", text, re.M))


def fail(failures: list[str], cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


def source_does_not_write_queue(src: str) -> list[str]:
    problems: list[str] = []
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = ""
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr
            if name in {"run", "call", "Popen", "system"}:
                problems.append(f"subprocess-like call {name}")
    if "mark_topic.py --write" in src:
        for i, line in enumerate(src.splitlines(), 1):
            stripped = line.strip()
            if "mark_topic.py --write" in stripped and not stripped.startswith("#"):
                if "f\"  # " in line or "\"  # " in line or "'  # " in line:
                    continue
                if stripped.startswith("lines.append") and "--write" in stripped and "#" in stripped:
                    continue
                problems.append(f"line {i} mentions mark_topic --write un-commented: {stripped}")
    return problems


def main() -> int:
    failures: list[str] = []

    src = (TOOLS / "new_packet.py").read_text(encoding="utf-8")
    fail(failures, "def mark_followup" in src, "mark_followup missing")
    fail(failures, "does not mark the topic queue used" in src, "no-mark banner missing")
    for problem in source_does_not_write_queue(src):
        failures.append(problem)

    title = "Stop deciding what to work on every morning"
    lines = mark_followup(title)
    blob = "\n".join(lines)
    fail(failures, any("mark_topic.py --id Q1" in ln and "--write" not in ln for ln in lines), f"dry-run Q1 missing: {lines}")
    fail(
        failures,
        any(ln.strip().startswith("#") and "mark_topic.py --id Q1 --write" in ln for ln in lines)
        or any("  # python3 tools/mark_topic.py --id Q1 --write" in ln for ln in lines),
        f"commented write missing: {lines}",
    )
    fail(failures, "does not mark the topic queue used" in blob.lower() or "does not mark" in blob, "banner")

    unknown = mark_followup("A title that is not in the queue")
    fail(
        failures,
        any("mark_topic.py" in ln and "--id" not in ln for ln in unknown),
        f"unknown title should print generic mark_topic: {unknown}",
    )

    after = TOOLS / "after_scaffold.py"
    if after.is_file():
        after_src = after.read_text(encoding="utf-8")
        fail(
            failures,
            r"^\d+\.[ \t]+\S" in after_src or r"^\\d+\\.[ \\t]+\\S" in after_src,
            "after_scaffold titles_filled regex missing",
        )

    fail(failures, not titles_filled("# Titles\n\n1.\n2.\n"), "empty 1. treated as filled")
    fail(failures, titles_filled("1. Stop deciding this morning\n"), "filled 1. not detected")
    fail(failures, titles_filled("Primary: A real title\n"), "Primary not detected")
    fail(failures, not titles_filled("Primary:\n"), "empty Primary treated as filled")

    with tempfile.TemporaryDirectory() as tmp:
        videos = Path(tmp) / "videos"
        sample = videos / "sample-001-why-systems-beat-motivation"
        sample.mkdir(parents=True)
        fail(failures, next_id(videos) == "002", f"next_id expected 002 got {next_id(videos)}")
        slug = slugify(title)
        fail(failures, slug == "stop-deciding-what-to-work-on-every-morning", f"slug {slug}")
        leak = ROOT / "videos" / f"002-{slug}"
        fail(failures, not leak.exists(), f"scaffold leaked {leak}")

    print("Scaffold contract")
    print("new_packet: reprint mark_topic dry-run; no auto --write")
    print("titles_filled: empty 1. stays untitled")
    print("next_id: sample-001 => 002")
    if failures:
        print("SCAFFOLD CONTRACT FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("SCAFFOLD CONTRACT PASS")
    print("This command writes nothing in videos/ and does not mark the queue.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
