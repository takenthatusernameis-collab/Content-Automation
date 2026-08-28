#!/usr/bin/env python3
"""Structural QA for a video packet.

Default mode is a publish/completeness gate: empty spoken WORDS fail.
--draft / --incomplete is an intake/structure gate: empty spoken WORDS
(and empty title/thumb copy) are reported as draft-incomplete, not FAIL.
Missing files, invalid status, beat-count, and empty packet identity
still FAIL in both modes.

Spoken duration vs the locked format is a warning by default so the
sample fixture stays PASS. --duration promotes short/long scripts to FAIL.
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
WPM = 150
# Spoken-word bands for locked formats. 6–10 min at 150 wpm = 900–1500 words.
FORMAT_SPOKEN_WORDS = {
    "explainer-6-10min": (900, 1500),
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


def all_spoken_words(script: str) -> list[str]:
    words: list[str] = []
    for m in re.finditer(r"^##\s+(.+)$", script, re.M):
        words.extend(spoken_words(section(script, m.group(1).strip())))
    return words


def spoken_seconds(n_words: int, wpm: float = WPM) -> float:
    if n_words <= 0:
        return 0.0
    return (n_words / wpm) * 60.0


def fmt_mmss(seconds: float) -> str:
    if seconds < 0:
        seconds = 0
    whole = int(round(seconds))
    m, s = divmod(whole, 60)
    return f"{m:02d}:{s:02d}"


def duration_note(fmt: str, n_words: int) -> str | None:
    """Human line when spoken length is off the locked format band.

    Empty scripts are handled by the WORDS gates, not here.
    """
    if n_words <= 0:
        return None
    band = FORMAT_SPOKEN_WORDS.get(fmt)
    if not band:
        return None
    lo, hi = band
    if lo <= n_words <= hi:
        return None
    est = fmt_mmss(spoken_seconds(n_words))
    if n_words < lo:
        return (
            f"spoken {n_words} words (~{est} at {int(WPM)} wpm) "
            f"below {fmt} band {lo}–{hi}"
        )
    return (
        f"spoken {n_words} words (~{est} at {int(WPM)} wpm) "
        f"above {fmt} band {lo}–{hi}"
    )


def titles_from(text: str) -> list[str]:
    found: list[str] = []
    prim = re.search(r"^Primary:[ \t]*([^\n]*)$", text, re.M)
    if prim and prim.group(1).strip():
        found.append(prim.group(1).strip())
    # Spaces/tabs only after the number. `\s` includes newlines and would
    # turn empty `1.\n2.` template lines into fake titles.
    for m in re.finditer(r"^\d+\.[ \t]+(.+)$", text, re.M):
        found.append(m.group(1).strip())
    return [t for t in found if t]


def on_image_text(thumb: str) -> str:
    m = re.search(r"^On-image text.*:[ \t]*([^\n]*)$", thumb, re.M)
    return m.group(1).strip() if m else ""


def validate(
    path: Path, draft: bool = False, duration: bool = False
) -> tuple[list[str], list[str]]:
    """Return (errors, incompletes). Errors fail both modes.

    Duration-band misses are warnings unless --duration, so existing
    callers (pipeline_status) keep a 2-tuple and the sample fixture
    stays PASS.
    """
    errors: list[str] = []
    incompletes: list[str] = []
    warnings: list[str] = []
    if not path.is_dir():
        return [f"not a directory: {path}"], incompletes

    for name in REQUIRED_FILES:
        if not (path / name).is_file():
            errors.append(f"missing {name}")
    if errors:
        if duration:
            errors.extend(warnings)
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

    fmt = field(packet, "format") or "explainer-6-10min"
    note = duration_note(fmt, len(all_spoken_words(script)))
    if note:
        if duration:
            errors.append(note)
        else:
            warnings.append(note)
    return errors, incompletes


def packet_duration_warning(path: Path) -> str | None:
    packet_path = path / "packet.md"
    script_path = path / "script.md"
    if not packet_path.is_file() or not script_path.is_file():
        return None
    packet = packet_path.read_text(encoding="utf-8")
    script = script_path.read_text(encoding="utf-8")
    fmt = field(packet, "format") or "explainer-6-10min"
    return duration_note(fmt, len(all_spoken_words(script)))


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
    parser.add_argument(
        "--duration",
        action="store_true",
        help="Treat spoken length outside the locked format band as FAIL",
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
        errs, incompletes = validate(t, draft=args.draft, duration=args.duration)
        warn = None if args.duration else packet_duration_warning(t)
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
        if warn:
            print(f"  WARN {warn}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
