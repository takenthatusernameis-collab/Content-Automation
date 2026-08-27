#!/usr/bin/env python3
"""Turn a one-line topic into a video packet with a filled idea card and empty beats.

No LLM. Structure only. Script WORDS stay empty until a writer (human or prompt) fills them.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "videos" / "_template"
VIDEOS = ROOT / "videos"

DEFAULT_VIEWER = "Someone who wants focused work but stalls after planning"
DEFAULT_MECHANISM = "A written default that removes one daily decision"
WORKING_NICHE = "systems for doing focused work"


def slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:60] or "untitled"


def next_id(videos_dir: Path) -> str:
    highest = 0
    for p in videos_dir.iterdir():
        if not p.is_dir() or p.name.startswith("_"):
            continue
        m = re.match(r"^(\d+)", p.name)
        if m:
            highest = max(highest, int(m.group(1)))
    return f"{highest + 1:03d}"


def existing_topics() -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if not VIDEOS.is_dir():
        return found
    for p in sorted(VIDEOS.iterdir()):
        idea = p / "idea.md"
        if not p.is_dir() or p.name.startswith("_") or not idea.is_file():
            continue
        text = idea.read_text(encoding="utf-8")
        m = re.search(r"^- topic:\s*(.*)$", text, re.M)
        topic = (m.group(1).strip() if m else p.name)
        found.append((p.name, topic))
    return found


def tokens(text: str) -> set[str]:
    stop = {
        "a", "an", "the", "and", "or", "for", "to", "of", "in", "on", "is",
        "your", "you", "that", "this", "with", "from", "how", "why", "what",
    }
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in stop and len(w) > 2}


def overlap_note(topic: str) -> tuple[str, int]:
    t = tokens(topic)
    best_name, best = "none", 0
    for name, other in existing_topics():
        n = len(t & tokens(other))
        if n > best:
            best, best_name = n, f"{name} ({other})"
    return best_name, best


def problem_line(topic: str) -> str:
    t = topic.rstrip(".")
    low = t[0].lower() + t[1:] if t else t
    return f"They keep facing this without a default process: {low}"


def idea_markdown(topic: str, related: str, overlap: int) -> str:
    rec = "skip" if overlap >= 4 else "draft"
    spec = "high" if len(tokens(topic)) >= 5 else "medium"
    return f"""# Idea

- topic: {topic.rstrip(".")}
- viewer: {DEFAULT_VIEWER}
- problem: {problem_line(topic)}
- mechanism (the system, not the pep talk): {DEFAULT_MECHANISM}
- why now: working niche — {WORKING_NICHE}
- related videos to avoid repeating: {related}

## Intake score (heuristic, not audience data)

- specificity: {spec}
- mechanism_clarity: template-default (edit before writing script)
- overlap_with_existing: {overlap} shared content words; closest = {related}
- recommended: {rec}
"""


BEAT_TITLES = [
    "Name the stall",
    "The default that replaces the decision",
    "Install it in one place",
    "Measure the start, not the mood",
    "Failure modes",
    "Make it smaller",
    "First week protocol",
]


def script_markdown(topic: str, beat_count: int) -> str:
    titles = BEAT_TITLES[:beat_count]
    beats = []
    for i, title in enumerate(titles, start=1):
        beats.append(f"## Beat {i} — {title}\nWORDS:\n\nVISUAL:\n")
    body = "\n".join(beats)
    return f"""# Script

Spoken words only under each beat. Visual notes in italics.
Topic seed: {topic}

## Hook (0:00–0:12)
WORDS:

VISUAL:

## Payoff promise
WORDS:

{body}
## CTA
WORDS:
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a packet from a one-line topic and fill the idea card"
    )
    parser.add_argument("topic", help="One-line topic or working title")
    parser.add_argument("--id", help="Numeric id like 002 (default: next)")
    parser.add_argument("--beats", type=int, default=4, help="Beat count 4–7 (default 4)")
    args = parser.parse_args()

    if not 4 <= args.beats <= 7:
        print("--beats must be 4–7", file=sys.stderr)
        return 1
    if not TEMPLATE.is_dir():
        print(f"Template missing: {TEMPLATE}", file=sys.stderr)
        return 1

    vid = args.id or next_id(VIDEOS)
    slug = slugify(args.topic)
    dest = VIDEOS / f"{vid}-{slug}"
    if dest.exists():
        print(f"Already exists: {dest}", file=sys.stderr)
        return 1

    related, overlap = overlap_note(args.topic)
    shutil.copytree(TEMPLATE, dest)
    today = dt.date.today().isoformat()

    packet = dest / "packet.md"
    text = packet.read_text(encoding="utf-8")
    text = text.replace("- id:", f"- id: {vid}", 1)
    text = text.replace("- slug:", f"- slug: {slug}", 1)
    text = text.replace("- working_title:", f"- working_title: {args.topic}", 1)
    text = text.replace("- created:", f"- created: {today}", 1)
    text = text.replace("- updated:", f"- updated: {today}", 1)
    packet.write_text(text, encoding="utf-8")

    (dest / "idea.md").write_text(idea_markdown(args.topic, related, overlap), encoding="utf-8")
    (dest / "script.md").write_text(script_markdown(args.topic, args.beats), encoding="utf-8")

    print(dest.relative_to(ROOT))
    print(f"overlap={overlap} recommended={'skip' if overlap >= 4 else 'draft'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
