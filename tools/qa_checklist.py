#!/usr/bin/env python3
"""Write qa.md mechanical + human checklist for a video packet.

Mechanical boxes are computed from packet files (same rules as
validate_packet.py). Human boxes stay unchecked unless an existing
qa.md already has a matching [x] line — the tool never invents a
pass, score, or completed human tick.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_packet import (  # noqa: E402
    REQUIRED_FILES,
    VALID_STATUS,
    field,
    on_image_text,
    section,
    spoken_words,
    titles_from,
    validate,
)

HUMAN_ITEMS = (
    "VO take selected (usable take; no obvious clip or room noise noted)",
    "Hook card readable at 1920x1080 and matches the hook promise",
    "Beat cards max 5 words and taken from beat titles",
    "CTA card shows the assignment, not subscribe",
    "Planned cards listed in assets.md match script VISUAL lines (files may still be missing)",
    "Cards held at least 1.5s; cuts on sentence ends",
    "Last 20s reserved for YouTube end screen; CTA still readable",
    "Export named exports/NNN-slug-vN.mp4 (1920x1080, 30fps, 48kHz)",
    "Captions reviewed against selected VO (stub times are not final)",
    "No unsourced statistics in spoken WORDS (cite in research.md)",
    "Primary title locked for upload",
    "Thumbnail on-image text designed (contrast + subject + exclusions)",
)


def numbers_in_spoken_words(script: str) -> list[str]:
    """Digits inside WORDS blocks only. Headings like 0:00 or Beat 1 do not count."""
    hits: list[str] = []
    for block in re.finditer(r"WORDS:\s*(.*?)(?:VISUAL:|^##|\Z)", script, re.S | re.M):
        blob = block.group(1)
        blob = re.sub(r"\*[^*]+\*", " ", blob)
        for m in re.finditer(r"\b\d+(?:[.,]\d+)?%?\b", blob):
            hits.append(m.group(0))
    return hits


def existing_checked(text: str) -> set[str]:
    found: set[str] = set()
    for m in re.finditer(r"^- \[x\]\s+(.+)$", text, re.M | re.I):
        found.add(m.group(1).strip().lower())
    return found


def box(ok: bool) -> str:
    return "[x]" if ok else "[ ]"


def human_box(label: str, prior: set[str]) -> str:
    mark = "[x]" if label.strip().lower() in prior else "[ ]"
    return f"- {mark} {label}"


def mechanical_rows(path: Path, draft: bool) -> tuple[list[str], list[str], list[str], str]:
    errs, incompletes = validate(path, draft=draft)
    packet = (path / "packet.md").read_text(encoding="utf-8") if (path / "packet.md").is_file() else ""
    script = (path / "script.md").read_text(encoding="utf-8") if (path / "script.md").is_file() else ""
    titles_text = (path / "titles.md").read_text(encoding="utf-8") if (path / "titles.md").is_file() else ""
    thumb = (path / "thumbnail.md").read_text(encoding="utf-8") if (path / "thumbnail.md").is_file() else ""

    missing = [n for n in REQUIRED_FILES if not (path / n).is_file()]
    status = field(packet, "status")
    hook = section(script, "Hook (0:00–0:12)") or section(script, "Hook")
    hook_n = len(spoken_words(hook))
    payoff = bool(section(script, "Payoff promise"))
    beats = re.findall(r"^##\s+Beat\s+\d+", script, re.M)
    cta_n = len(spoken_words(section(script, "CTA")))
    titles = titles_from(titles_text)
    tw = re.findall(r"[A-Za-z0-9']+", on_image_text(thumb))
    remaining = "Remaining human work" in packet

    rows = [
        f"- {box(not missing)} Packet files present",
        f"- {box(status in VALID_STATUS)} Status valid",
        f"- {box(20 <= hook_n <= 35)} Hook word count 20–35",
        f"- {box(payoff)} Payoff before beat 2",
        f"- {box(4 <= len(beats) <= 7)} 4–7 beats",
        f"- {box(cta_n > 0)} CTA present",
        f"- {box(len(titles) >= 5 and any(len(t) < 50 for t in titles))} >=5 titles, one <50 chars",
        f"- {box(1 <= len(tw) <= 5)} Thumbnail text <=5 words",
        f"- {box(remaining)} Remaining human work listed",
    ]
    return rows, errs, incompletes, status


def render(path: Path, draft: bool, prior: set[str]) -> str:
    rows, errs, incompletes, status = mechanical_rows(path, draft)
    if errs:
        gate = "FAIL"
    elif incompletes:
        gate = "DRAFT-INCOMPLETE"
    else:
        gate = "PASS"

    script = (path / "script.md").read_text(encoding="utf-8") if (path / "script.md").is_file() else ""
    research_exists = (path / "research.md").is_file()
    captions_exists = (path / "captions.md").is_file()
    assets_exists = (path / "assets.md").is_file()
    nums = numbers_in_spoken_words(script)

    notes = [
        f"- Packet folder: `{path.name}`",
        f"- Status field: `{status or 'missing'}`",
        f"- Structural gate (`validate_packet.py{' --draft' if draft else ''}`): **{gate}**",
        f"- research.md present: {'yes' if research_exists else 'no'}",
        f"- captions.md present: {'yes' if captions_exists else 'no'}",
        f"- assets.md present: {'yes' if assets_exists else 'no'}",
    ]
    if nums:
        notes.append(
            f"- Digits found in script.md (not a verdict): {', '.join(nums)}. "
            "Human must confirm a source line in research.md or remove them."
        )
    else:
        notes.append("- No digit tokens found in script.md (still tick the human stats box after a read).")

    human = [human_box(label, prior) for label in HUMAN_ITEMS]
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    parts = [
        "# QA",
        "",
        "Generated by `tools/qa_checklist.py`. Mechanical boxes are computed from files. "
        "Human boxes are never auto-checked. No scores.",
        "",
        f"Generated: {generated}",
        "",
        "## Notes",
        *notes,
        "",
        "## Mechanical (from packet files)",
        *rows,
        "",
        "## Human (must tick; tool does not mark these done)",
        *human,
        "",
        "## Commands",
        f"- `python3 tools/validate_packet.py videos/{path.name}`",
        f"- `python3 tools/validate_packet.py --draft videos/{path.name}`",
        f"- `python3 tools/qa_checklist.py videos/{path.name}`",
        "",
    ]
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write qa.md checklist from production rules + editor conventions."
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--dry-run", action="store_true", help="Print qa.md; do not write")
    parser.add_argument(
        "--draft",
        action="store_true",
        help="Report structural gate using validate_packet --draft rules",
    )
    parser.add_argument(
        "--reset-human",
        action="store_true",
        help="Do not preserve existing [x] marks on human items",
    )
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    qa_path = path / "qa.md"
    prior: set[str] = set()
    if qa_path.is_file() and not args.reset_human:
        prior = existing_checked(qa_path.read_text(encoding="utf-8"))
        allowed = {h.lower() for h in HUMAN_ITEMS}
        prior = {p for p in prior if p in allowed}

    text = render(path, draft=args.draft, prior=prior)
    if args.dry_run:
        sys.stdout.write(text)
        return 0

    qa_path.write_text(text, encoding="utf-8")
    print(qa_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
