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

# First-video viewer. A later topic must not inherit it unless the topic says planning.
Q1_VIEWER = "Someone who wants focused work but stalls after planning"
# First-video mechanism. A later topic must not inherit it unless the topic says it.
Q1_MECHANISM = "A written default that removes one daily decision"
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



def viewer_line(topic: str) -> str:
    """Name the viewer from this topic. Do not stamp the planning stall unless the topic says it."""
    low = topic.lower()
    if "planning" in low or "after planning" in low:
        return Q1_VIEWER
    short = " ".join(topic.strip().rstrip(".").split()[:10])
    return f"Someone who wants focused work but stalls on this: {short}"


def problem_line(topic: str) -> str:
    t = topic.rstrip(".")
    low = t[0].lower() + t[1:] if t else t
    return f"They keep hitting this without a named step: {low}"


def mechanism_line(topic: str) -> str:
    """Use a queued one_line only when this topic already matches that row.

    Otherwise name the step from the topic. Do not stamp the first video's
    written-default line onto a later idea.
    """
    t = tokens(topic)
    best = ""
    best_n = 0
    queue = ROOT / "docs" / "topic_queue.md"
    if queue.is_file():
        for line in queue.read_text(encoding="utf-8").splitlines():
            if not line.startswith("| Q"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 4:
                continue
            title, one = cells[2], cells[3]
            n = len(t & (tokens(title) | tokens(one)))
            if n > best_n:
                best_n, best = n, one
    if best and best_n >= 3:
        return best
    cleaned = topic.strip().rstrip(".")
    return f"A named step for this topic: {cleaned}"


def idea_markdown(topic: str, related: str, overlap: int) -> str:
    rec = "skip" if overlap >= 4 else "draft"
    spec = "high" if len(tokens(topic)) >= 5 else "medium"
    return f"""# Idea

- topic: {topic.rstrip(".")}
- viewer: {viewer_line(topic)}
- problem: {problem_line(topic)}
- mechanism (the system, not the pep talk): {mechanism_line(topic)}
- why now: working niche — {WORKING_NICHE}
- related videos to avoid repeating: {related}

## Intake score (heuristic, not audience data)

- specificity: {spec}
- mechanism_clarity: template-default (edit before writing script)
- overlap_with_existing: {overlap} shared content words; closest = {related}
- recommended: {rec}
"""


def beat_titles(topic: str, beat_count: int) -> list[str]:
    """Structural beats named from this topic, not the first video's default."""
    short = " ".join(topic.strip().rstrip(".").split()[:8])
    pool = [
        "Name the stall",
        f"The move: {short}",
        "Put that move in one place",
        "Check it after one use",
        "Failure modes",
        "Make the move smaller",
        "First week of that move",
    ]
    return pool[:beat_count]


def script_markdown(topic: str, beat_count: int) -> str:
    titles = beat_titles(topic, beat_count)
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
    parser.add_argument(
        "--no-generate",
        action="store_true",
        help="Copy template only; do not write generated qa.md / research.md",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the idea card and beat titles. Do not create a packet folder.",
    )
    args = parser.parse_args()

    if not 4 <= args.beats <= 7:
        print("--beats must be 4–7", file=sys.stderr)
        return 1
    if args.dry_run:
        related, overlap = overlap_note(args.topic)
        print(idea_markdown(args.topic, related, overlap))
        print(script_markdown(args.topic, args.beats))
        print("dry-run: no packet folder written")
        return 0
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

    if not args.no_generate:
        from after_scaffold import generate

        for line in generate(dest, draft=True):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
