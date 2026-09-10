#!/usr/bin/env python3
"""Contract check for scaffold + queue-mark handoff.

Read-only versus the repo videos/ tree. May import new_packet.mark_followup
and new_packet.idea_followup which read docs/topic_queue.md. Never writes
the queue, idea.md, or sample-001.

Locks:
- new_packet does not call mark_topic --write
- new_packet does not write idea.md
- mark_followup prints a dry-run line then a commented --write
- idea_followup reprints topic + Q1 problem + matching queue one_line
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

from new_packet import idea_followup, mark_followup  # noqa: E402
from queue_lib import next_id, slugify  # noqa: E402

try:
    from operator_pin_contract import Q1_PROBLEM  # noqa: E402
except Exception:
    Q1_PROBLEM = "they reopen the whole work list every morning instead of starting"


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
                if 'f"  # ' in line or '"  # ' in line or "'  # " in line:
                    continue
                if stripped.startswith("lines.append") and "--write" in stripped and "#" in stripped:
                    continue
                problems.append(f"line {i} mentions mark_topic --write un-commented: {stripped}")
    return problems


def main() -> int:
    failures: list[str] = []

    src = (TOOLS / "new_packet.py").read_text(encoding="utf-8")
    fail(failures, "def mark_followup" in src, "mark_followup missing")
    fail(failures, "def idea_followup" in src, "idea_followup missing")
    fail(failures, "does not mark the topic queue used" in src, "no-mark banner missing")
    fail(failures, "does not write idea.md" in src, "no-write-idea banner missing")
    if re.search(r"idea\.md.*write_text|write_text\(.*idea", src):
        failures.append("new_packet appears to write idea.md")

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

    ideas = idea_followup(title)
    idea_blob = "\n".join(ideas)
    fail(failures, "does not write idea.md" in idea_blob.lower(), f"idea no-write banner missing: {ideas}")
    fail(
        failures,
        any("topic:" in ln and "Stop deciding what to work on every morning" in ln for ln in ideas),
        f"idea topic reprint missing: {ideas}",
    )
    fail(
        failures,
        any("problem:" in ln and Q1_PROBLEM in ln for ln in ideas),
        f"idea problem reprint missing Q1 problem: {ideas}",
    )
    fail(
        failures,
        any("next-action default" in ln for ln in ideas),
        f"idea mechanism reprint missing Q1 one_line: {ideas}",
    )

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
    print("new_packet: reprint idea topic + problem + one_line; no idea.md write")
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
