#!/usr/bin/env python3
"""Print a combined packaging starter for a queued topic (no packet folder required).

Pulls working_title, one_line, and problem from docs/topic_queue.md for the given id.
Emits in one output:
- Title options (mechanism-focused)
- Thumbnail concepts
- Description skeleton (stall + mechanism + same-day outcome + chapters placeholder + CTA)
- First-comment options

Grounded in queue data only. Does not invent hype, numbers, clickbait, anecdotes, or full WORDS.
Does not write files. Does not scaffold. Does not call APIs.

Useful while STALL_OAUTH_IDLE persists: one command prepares the full packaging stage
(titles, thumbnail, description, first comment) for Q2+ so that when the human later scaffolds,
publish.md / titles.md / thumbnail.md start from grounded options instead of blank.
Reduces recurring setup labor and tool-switching for every subsequent video.
Complements the individual queued_title_thumbnail_starter.py and queued_description_starter.py.
After scaffold, run the relevant consistency scans.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from queue_lib import parse_queue  # type: ignore


def suggest_titles(title: str, one_line: str, problem: str) -> list[str]:
    """Mechanism-focused titles. No shouted words, no weak patterns, no numbers."""
    ol = one_line[:70].rstrip(".") or title
    pr = problem[:60].rstrip(".") or "the morning stall"
    return [
        title,
        f"Install the start cue so {pr} stops",
        f"{ol}",
        f"Put the cue on the work itself",
        f"One visible default ends {pr}",
    ]


def suggest_thumb_concepts(title: str, one_line: str, problem: str) -> list[str]:
    """Short thumbnail text and visual notes. Avoid long text and clickbait."""
    ol_short = one_line[:40].rstrip(".") or title[:40]
    return [
        f"Text: '{ol_short}'  |  Visual: single object or file with a clear start marker; rest of list faded or closed.",
        f"Text: 'Start cue on the work'  |  Visual: before (open list) vs after (one marked first action) split, no faces, no metrics.",
        f"Text: '{title[:35]}'  |  Visual: physical or digital cue placed directly on the task surface or file.",
        "Text: none or very short  |  Visual: close-up of the installed cue alone; clean background.",
    ]


def suggest_description(title: str, one_line: str, problem: str) -> str:
    """Mechanism-focused description skeleton. No shouted words, no weak patterns, no numbers."""
    ol = one_line[:80].rstrip(".") or title
    pr = problem[:70].rstrip(".") or "the morning stall"
    return f"""The stall is real: {pr}.

This video shows how to install one concrete default so the list does not reopen.
Mechanism: {ol}.

Same-day outcome: place the cue on the work itself and start the first two minutes without reopening the whole list.

## Chapters
0:00 Hook — name the stall
0:30 Payoff — the install you can finish today
1:15 Beat 1 — where the cue lives
2:30 Beat 2 — the under-two-minute step
4:00 Beat 3 — what reopens the list when the cue is missing
5:30 CTA — do the install now

Prefer a single visible start cue over another list. No metrics, no testimonials."""


def suggest_first_comments(title: str, one_line: str, problem: str) -> list[str]:
    """Short first-comment options. Operational, not promotional."""
    ol_short = one_line[:50].rstrip(".") or title[:50]
    return [
        f"Try the install: put '{ol_short}' on the work itself before you open the list. Report back what the first two minutes looked like.",
        f"The stall is '{problem[:40]}...'. The fix is one cue on the work, not another checklist. What cue are you placing today?",
        f"One visible default ends the reopen. If you finished the under-two-minute step, drop the exact cue you used.",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a combined packaging starter (titles + thumbnail + description + first-comment) for a queued topic id. No packet, no writes, no invented hype."
    )
    parser.add_argument("--id", required=True, help="Topic id from docs/topic_queue.md (e.g. Q2)")
    args = parser.parse_args()

    queue_path = ROOT / "docs" / "topic_queue.md"
    if not queue_path.is_file():
        print(f"Missing queue: {queue_path}", file=sys.stderr)
        return 1

    rows = parse_queue(queue_path.read_text(encoding="utf-8"))
    row = next((r for r in rows if r["id"].upper() == args.id.upper()), None)
    if not row:
        print(f"No row for id {args.id} in topic queue.", file=sys.stderr)
        return 1
    if row["status"] == "used":
        print(f"# Note: {args.id} is already marked used. Packaging pack is still valid for reference.\n")

    title = row["working_title"]
    one_line = row["one_line"]
    problem = row["problem"] or "unspecified problem from queue"

    titles = suggest_titles(title, one_line, problem)
    thumbs = suggest_thumb_concepts(title, one_line, problem)
    desc = suggest_description(title, one_line, problem)
    comments = suggest_first_comments(title, one_line, problem)

    print(f"# Combined packaging starter for {args.id}: {title}")
    print("# (generated by queued_packaging_starter.py; no invented hype, numbers, clickbait, or WORDS)")
    print("# Copy preferred sections into titles.md, thumbnail.md, and publish.md after scaffolding.")
    print("# Keep language specific and mechanism-focused. Prefer under ~60 chars for titles, short thumb text, ~150 words for description body.")
    print("# After scaffold: python3 tools/title_scan.py videos/NNN-slug && python3 tools/thumbnail_scan.py videos/NNN-slug && python3 tools/description_consistency.py videos/NNN-slug")
    print()
    print("=" * 72)
    print("## 1. TITLE OPTIONS (pick one or adapt; no shouted words)")
    print("=" * 72)
    for i, t in enumerate(titles, 1):
        print(f"{i}. {t}")
    print()
    print("=" * 72)
    print("## 2. THUMBNAIL CONCEPTS")
    print("=" * 72)
    for i, th in enumerate(thumbs, 1):
        print(f"{i}. {th}")
    print()
    print("=" * 72)
    print("## 3. DESCRIPTION SKELETON")
    print("=" * 72)
    print(desc)
    print()
    print("=" * 72)
    print("## 4. FIRST-COMMENT OPTIONS (pick one or adapt)")
    print("=" * 72)
    for i, c in enumerate(comments, 1):
        print(f"{i}. {c}")
    print()
    print("=" * 72)
    print("## NOTES")
    print("=" * 72)
    print("- Titles and description must name the mechanism and the concrete stall from the queue.")
    print("- Thumbnail text should support the chosen title; visuals show the cue or the stall without metrics or faces.")
    print("- Chapters timestamps are placeholders; replace after a real timeline exists.")
    print("- First comment should invite one specific operational reply, not generic engagement.")
    print("- Do not invent statistics, testimonials, or personal stories.")
    print("- Preferred human next remains OAuth (python3 tools/oauth_complete_guide.py). Do not scaffold Q2 while STALL_OAUTH_IDLE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
