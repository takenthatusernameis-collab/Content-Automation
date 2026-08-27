#!/usr/bin/env python3
"""Structural QA for a video packet.

Default mode is a publish/completeness gate: empty spoken WORDS fail.
--draft / --incomplete is an intake/structure gate: empty spoken WORDS
(and empty title/thumb copy) are reported as draft-incomplete, not FAIL.
Missing files, invalid status, beat-count, and empty packet identity
still FAIL in both modes.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "packet.md",
    "idea.md",
    "script.md",
    "titles.md",
    "thumbnail.md",
    "qa.md",
)
VALID_STATUS = {
    "draft",
    "ready_for_vo",
    "ready_for_edit",
    "ready_to_publish",
    "published",
    "abandoned",
}


def field(text: str, name: str) -> str:
    # Values stay on one line. Do not let \s* after ":" eat the newline
    # and swallow the next field when the value is empty.
    m = re.search(rf"^-\s*{re.escape(name)}:[ \t]*([^\n]*)$", text, re.M)
    return (m.group(1).strip() if m else "")


def section(text: str, heading: str) -> str:
    parts = re.split(rf"^##\s+{re.escape(heading)}\s*$", text, maxsplit=1, flags=re.M)
    if len(parts) < 2:
        return ""
    rest = re.split(r"^##\s+", parts[1], maxsplit=1, flags=re.M)[0]
    return rest.strip()


def spoken_words(block: str) -> list[str]:
    m = re.search(r"WORDS:\s*(.*?)(?:VISUAL:|\Z)", block, re.S)
    blob = m.group(1) if m else block
    blob = re.sub(r"\*[^*]+\*", " ", blob)
    words = re.findall(r"[A-Za-z0-9']+", blob)
    return words


def titles_from(text: str) -> list[str]:
    found: list[str] = []
    prim = re.search(r"^Primary:[ \t]*([^\n]*)$", text, re.M)
    if prim and prim.group(1).strip():
        found.append(prim.group(1).strip())
    for m in re.finditer(r"^\d+\.\s+(.+)$", text, re.M):
        found.append(m.group(1).strip())
    return [t for t in found if t]


def on_image_text(thumb: str) -> str:
    m = re.search(r"^On-image text.*:[ \t]*([^\n]*)$", thumb, re.M)
    return m.group(1).strip() if m else ""


def validate(path: Path, draft: bool = False) -> tuple[list[str], list[str]]:
    """Return (errors, incompletes). Errors fail both modes."""
    errors: list[str] = []
    incompletes: list[str] = []
    if not path.is_dir():
        return [f"not a directory: {path}"], incompletes

    for name in REQUIRED_FILES:
        if not (path / name).is_file():
            errors.append(f"missing {name}")
    if errors:
        return errors, incompletes

    packet = (path / "packet.md").read_text(encoding="utf-8")
    script = (path / "script.md").read_text(encoding="utf-8")
    titles_text = (path / "titles.md").read_text(encoding="utf-8")
    thumb = (path / "thumbnail.md").read_text(encoding="utf-8")

    status = field(packet, "status")
    if status not in VALID_STATUS:
        errors.append(f"invalid status: {status!r}")
    if not field(packet, "id"):
        errors.append("packet id empty")
    if not field(packet, "working_title"):
        errors.append("working_title empty")
    if "Remaining human work" not in packet:
        errors.append("missing Remaining human work")

    hook = section(script, "Hook (0:00–0:12)") or section(script, "Hook")
    hook_words = spoken_words(hook)
    n = len(hook_words)
    if n == 0:
        msg = "hook word count 0 not in 20–35"
        if draft:
            incompletes.append("hook WORDS empty (draft-incomplete)")
        else:
            errors.append(msg)
    elif n < 20 or n > 35:
        errors.append(f"hook word count {n} not in 20–35")

    if not section(script, "Payoff promise"):
        errors.append("missing Payoff promise section")

    beats = re.findall(r"^##\s+Beat\s+\d+", script, re.M)
    if not (4 <= len(beats) <= 7):
        errors.append(f"beat count {len(beats)} not in 4–7")

    cta = section(script, "CTA")
    cta_words = spoken_words(cta)
    if not cta_words:
        if draft:
            incompletes.append("CTA WORDS empty (draft-incomplete)")
        else:
            errors.append("CTA has no spoken words")

    titles = titles_from(titles_text)
    if len(titles) == 0:
        if draft:
            incompletes.append("titles empty (draft-incomplete)")
        else:
            errors.append("only 0 titles, need >=5")
    elif len(titles) < 5:
        errors.append(f"only {len(titles)} titles, need >=5")
    if titles and not any(len(t) < 50 for t in titles):
        errors.append("need one title under 50 characters")

    text_line = on_image_text(thumb)
    tw = re.findall(r"[A-Za-z0-9']+", text_line)
    if not tw:
        if draft:
            incompletes.append("thumbnail on-image text empty (draft-incomplete)")
        else:
            errors.append("thumbnail on-image text missing")
    elif len(tw) > 5:
        errors.append(f"thumbnail text has {len(tw)} words, max 5")

    return errors, incompletes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a video packet. Default = publish gate. --draft = intake gate."
    )
    parser.add_argument("packet", nargs="?", help="Path to packet folder")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate every videos/* packet except _template",
    )
    parser.add_argument(
        "--draft",
        "--incomplete",
        dest="draft",
        action="store_true",
        help="Treat empty spoken WORDS / empty title-thumb copy as draft-incomplete, not FAIL",
    )
    args = parser.parse_args()

    targets: list[Path] = []
    if args.all:
        videos = ROOT / "videos"
        if videos.is_dir():
            for p in sorted(videos.iterdir()):
                if p.is_dir() and not p.name.startswith("_"):
                    targets.append(p)
    elif args.packet:
        targets.append(Path(args.packet).resolve())
    else:
        parser.error("provide a packet path or --all")

    failed = 0
    for t in targets:
        errs, incompletes = validate(t, draft=args.draft)
        rel = t.name if t.parent.name == "videos" else str(t)
        if errs:
            failed += 1
            print(f"FAIL {rel}")
            for e in errs:
                print(f"  - {e}")
            for i in incompletes:
                print(f"  - {i}")
        elif incompletes:
            print(f"DRAFT-INCOMPLETE {rel}")
            for i in incompletes:
                print(f"  - {i}")
        else:
            print(f"PASS {rel}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
