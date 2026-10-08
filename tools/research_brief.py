#!/usr/bin/env python3
"""Write a research.md intake stub for a video packet.

Does not scrape the web. Does not treat listed URLs as verified.
Binds the production rule: no unverifiable statistics; numbers in
spoken WORDS need a source line in this file.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PLACEHOLDER_SOURCE_PREFIXES = (
    "(add ",
    "(url",
    "todo",
    "tbd",
    "placeholder",
    "add url",
    "add a source",
)

DEFAULT_AVOID = (
    "Any unsourced percentage, study result, or \"most people\" claim",
    "Any number in spoken WORDS that has no matching source line below",
    "Treating a URL in this file as verified just because it was typed",
)


def field_line(text: str, name: str) -> str:
    m = re.search(rf"^-?\s*{re.escape(name)}:[ \t]*([^\n]*)$", text, re.M | re.I)
    return m.group(1).strip() if m else ""


def section(text: str, heading: str) -> str:
    parts = re.split(rf"^##\s+{re.escape(heading)}\s*$", text, maxsplit=1, flags=re.M)
    if len(parts) < 2:
        return ""
    rest = re.split(r"^##\s+", parts[1], maxsplit=1, flags=re.M)[0]
    return rest.strip()


def bullets(block: str) -> list[str]:
    found: list[str] = []
    for m in re.finditer(r"^-\s+(.+)$", block, re.M):
        item = m.group(1).strip()
        if item:
            found.append(item)
    return found


def numbers_in_spoken_words(script: str) -> list[str]:
    """Digits inside WORDS blocks only. Headings like 0:00 or Beat 1 do not count."""
    hits: list[str] = []
    for block in re.finditer(r"WORDS:\s*(.*?)(?:VISUAL:|^##|\Z)", script, re.S | re.M):
        blob = block.group(1)
        blob = re.sub(r"\*[^*]+\*", " ", blob)
        for m in re.finditer(r"\b\d+(?:[.,]\d+)?%?", blob):
            hits.append(m.group(0))
    return hits


def is_placeholder_source(item: str) -> bool:
    low = item.lower().strip()
    if not low:
        return True
    return any(low.startswith(p) for p in PLACEHOLDER_SOURCE_PREFIXES)


def human_sources(research: str) -> list[str]:
    block = section(research, "Sources")
    if not block:
        m = re.search(r"^Sources:\s*(.*?)(?:^Facts allowed|^Claims to avoid|^## |\Z)", research, re.S | re.M)
        block = m.group(1) if m else ""
    return [b for b in bullets(block) if not is_placeholder_source(b)]


def research_is_filled(research: str) -> bool:
    if not research.strip():
        return False
    if human_sources(research):
        return True
    facts = section(research, "Facts allowed on camera") or ""
    fact_items = bullets(facts)
    if not fact_items:
        m = re.search(
            r"^Facts allowed on camera:\s*(.*?)(?:^Claims to avoid|^## |\Z)",
            research,
            re.S | re.M,
        )
        fact_items = bullets(m.group(1) if m else "")
    real_facts = [
        f
        for f in fact_items
        if f.lower() not in {"none", "none yet", "none that require a citation.", "none that require a citation"}
        and not f.lower().startswith("(add")
    ]
    return bool(real_facts)


def topic_from_packet(path: Path) -> str:
    idea = path / "idea.md"
    packet = path / "packet.md"
    if idea.is_file():
        t = field_line(idea.read_text(encoding="utf-8"), "topic")
        if t:
            return t
    if packet.is_file():
        t = field_line(packet.read_text(encoding="utf-8"), "working_title")
        if t:
            return t
    return path.name


def mechanism_from_idea(path: Path) -> str:
    idea = path / "idea.md"
    if not idea.is_file():
        return ""
    body = idea.read_text(encoding="utf-8")
    return field_line(body, "mechanism (the system, not the pep talk)") or field_line(body, "mechanism")


def render(
    path: Path,
    extra_sources: list[str],
    preserve_sources: list[str],
) -> str:
    topic = topic_from_packet(path)
    mechanism = mechanism_from_idea(path)
    script = (path / "script.md").read_text(encoding="utf-8") if (path / "script.md").is_file() else ""
    nums = numbers_in_spoken_words(script)
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    sources = []
    seen = set()
    for item in preserve_sources + extra_sources:
        key = item.strip()
        if not key or key.lower() in seen:
            continue
        seen.add(key.lower())
        sources.append(key)
    if not sources:
        sources.append("(add URL + the single claim it supports; listing a URL is not verification)")

    if nums:
        facts = [
            f"Spoken digit token(s) in WORDS: {', '.join(nums)}. Do not speak these until a source line exists."
        ]
        scan = (
            f"- Digits found in script.md WORDS: {', '.join(nums)}\n"
            "- Action: add a source line for each, or delete the number from the script"
        )
    else:
        facts = ["None that require a citation (no digit tokens in WORDS)."]
        scan = (
            "- Digits found in script.md WORDS: none\n"
            "- Action: keep it that way, or cite before adding a number"
        )

    mech_line = f"- Mechanism on the idea card: {mechanism}" if mechanism else "- Mechanism on the idea card: (missing)"

    return f"""# Research

Status: stub
Generated: {generated}

This file is an intake stub. It does not scrape the web. A URL written
here is a pointer for a human to check, not a verified source.

## Rule
No unverifiable statistics. If a number is used in spoken WORDS, cite
the source on a line under Sources. Production rule:
`docs/production_rules.md` (Script).

## Topic seed
- topic: {topic}
{mech_line}

## Sources
{chr(10).join(f'- {s}' for s in sources)}

## Facts allowed on camera
{chr(10).join(f'- {f}' for f in facts)}

## Claims to avoid
{chr(10).join(f'- {c}' for c in DEFAULT_AVOID)}

## Spoken-number scan
{scan}

## Notes
- Do not paste search-result prose into Facts as if it were checked.
- Prefer operational claims the viewer can test this week over studies.
- Human still ticks \"No unsourced statistics\" in qa.md after a read.
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write research.md stub (source list + no unverifiable-stats reminder)."
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--dry-run", action="store_true", help="Print research.md; do not write")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an already-filled research.md",
    )
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        help="Human-provided source line (repeatable). Not fetched.",
    )
    args = parser.parse_args()

    path = Path(args.packet)
    if not path.is_dir():
        path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {args.packet}", file=sys.stderr)
        return 1

    research_path = path / "research.md"
    existing = research_path.read_text(encoding="utf-8") if research_path.is_file() else ""
    filled = bool(existing) and research_is_filled(existing)
    if filled and not args.force and not args.dry_run:
        print(
            f"research.md already has sources/facts; pass --force to overwrite: {research_path}",
            file=sys.stderr,
        )
        return 1

    preserve = [] if args.force else (human_sources(existing) if existing else [])
    text = render(path, extra_sources=args.source, preserve_sources=preserve)

    if args.dry_run:
        sys.stdout.write(text)
        return 0

    research_path.write_text(text, encoding="utf-8")
    print(research_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
