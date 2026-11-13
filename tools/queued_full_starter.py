#!/usr/bin/env python3
"""Generate a combined full starter for a queued topic (Q2+).

Pulls working_title, one_line, and problem from docs/topic_queue.md.
Emits idea paste, research skeleton (with search prompts + verification checklist),
script outline, title options, thumbnail concepts, description skeleton,
first-comment options, and tag options.

Uses phrase_utils.shorten for whole-word / clause-aware truncation so phrases
stay complete and grammatical. No invented sources, numbers, hype, or WORDS.
Does not scaffold packets. Soft only.

Usage:
  python3 tools/queued_full_starter.py --id Q2
  python3 tools/queued_full_starter.py --id Q2 --write-doc   # updates docs/q2_prepared_starter.md
  python3 tools/queued_full_starter.py --regenerate-all      # Q2 through Q5
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from queue_lib import parse_queue  # type: ignore
from phrase_utils import shorten  # type: ignore


def suggest_titles(title: str, one_line: str, problem: str) -> list[str]:
    """Mechanism-focused titles. No shouted words, no weak patterns, no numbers.
    Uses whole-word shorten so options stay complete and grammatical.
    """
    ol = shorten(one_line, 40).rstrip(".") or title
    return [
        title,
        ol,
        "Install one visible start cue",
        "One cue on the work ends the reopen",
        "Put the cue where the stall happens",
    ]


def suggest_thumb_concepts(title: str, one_line: str, problem: str) -> list[str]:
    """Short thumbnail text and visual notes. Avoid long text and clickbait."""
    ol_short = shorten(one_line, 35).rstrip(".") or shorten(title, 35)
    return [
        f"Text: '{ol_short}'  |  Visual: single object or file with a clear start marker; rest of list faded or closed.",
        f"Text: 'Start cue on the work'  |  Visual: before (open list) vs after (one marked first action) split, no faces, no metrics.",
        f"Text: '{shorten(title, 30)}'  |  Visual: physical or digital cue placed directly on the task surface or file.",
        "Text: none or very short  |  Visual: close-up of the installed cue alone; clean background.",
    ]


def suggest_description(title: str, one_line: str, problem: str) -> str:
    """Mechanism-focused description skeleton. No shouted words, no weak patterns, no numbers."""
    ol = shorten(one_line, 70).rstrip(".") or title
    pr = shorten(problem, 60).rstrip(".") or "the morning stall"
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


def suggest_claims(one_line: str, problem: str, title: str) -> list[str]:
    """Qualitative claim templates. No numbers or invented results."""
    ol = shorten(one_line, 70) or title
    pr = shorten(problem, 70) or "the described stall"
    return [
        f"The stall '{pr}' occurs when no concrete, visible default is present at the moment of starting.",
        f"Naming and installing '{ol}' as a physical or file cue reduces the reopen-the-list cycle.",
        f"A single under-two-minute install of the cue ends the decision delay on the same day for this viewer.",
        f"The cue must live on the work itself (not in a separate system) so the delay has something to hit.",
    ]


def suggest_search_prompts(title: str, one_line: str, problem: str) -> list[str]:
    """Grounded research search prompts. Word-boundary truncated. No invented results."""
    ol = shorten(one_line, 50)
    pr = shorten(problem, 40)
    return [
        f'implementation intention "{ol}" start cue',
        f'decision fatigue "{pr}" morning list',
        f'environmental cue physical file start action',
        f'visible default next action productivity',
        f'"{title}" mechanism start cue',
    ]


def suggest_comments(one_line: str, problem: str) -> list[str]:
    """First-comment options. Mechanism-focused, no hype."""
    ol = shorten(one_line, 50)
    pr = shorten(problem, 40)
    return [
        f"Try the install: put '{ol}' on the work itself before you open the list. Report back what the first two minutes looked like.",
        f"The stall is '{pr}'. The fix is one cue on the work, not another checklist. What cue are you placing today?",
        f"One visible default ends the reopen. If you finished the under-two-minute step, drop the exact cue you used.",
    ]


def suggest_tags(title: str, one_line: str, problem: str) -> str:
    """Comma-separated tag options. No invented trends."""
    base = [
        "start cue",
        "work start",
        "visible default",
        "morning stall",
        "next action",
        "productivity system",
        "decision fatigue",
    ]
    extra = shorten(one_line, 25).lower().replace(" ", ",")
    return ", ".join(base + [extra])


def generate_full(row: dict) -> str:
    """Return the full markdown starter for one topic row."""
    tid = row["id"]
    title = row.get("working_title", "").strip()
    one_line = row.get("one_line", "").strip()
    problem = row.get("problem", "").strip()

    titles = suggest_titles(title, one_line, problem)
    thumbs = suggest_thumb_concepts(title, one_line, problem)
    desc = suggest_description(title, one_line, problem)
    claims = suggest_claims(one_line, problem, title)
    searches = suggest_search_prompts(title, one_line, problem)
    comments = suggest_comments(one_line, problem)
    tags = suggest_tags(title, one_line, problem)

    lines = [
        f"# {tid} Prepared Full Starter (regenerated with shared phrase_utils.shorten)",
        "",
        f"> Generated by `python3 tools/queued_full_starter.py --id {tid}` . Grounded in topic_queue.md only. No invented content. Do not scaffold while STALL_OAUTH_IDLE. Use after Q1 ships to reduce setup labor. Regenerate anytime with the tool; this snapshot is for reference.",
        "",
        f"# Combined full starter for {tid}: {title}",
        f"# (generated by queued_full_starter.py; no invented hype, numbers, clickbait, scenes, sources, or WORDS)",
        f"# Copy preferred sections into the packet after scaffolding. Do not treat any of this as script.md or WORDS.",
        f"# Aligns with production_rules word targets. Pairs with individual starters if you need only one section.",
        "",
        "========================================================================",
        "## 1. IDEA.MD PASTE (copy into idea.md after scaffold)",
        "========================================================================",
        "# Idea",
        "",
        f"- topic: {title}",
        f"- viewer: People who already plan their week, then stall when it is time to start.",
        f"- problem: {problem}",
        f"- mechanism (the system, not the pep talk): {one_line}",
        f"- why now: The week is already planned. The stall to install is this: {problem}",
        f"- related videos to avoid repeating: none published yet",
        "",
        "========================================================================",
        "## 2. RESEARCH.MD STARTER",
        "========================================================================",
        f"# Research starter for {tid}: {title}",
        "# (no invented sources or numbers)",
        "",
        "## Overview",
        f"- Working title: {title}",
        f"- One-line: {one_line}",
        f"- Problem: {problem}",
        "- Viewer: (fill from channel.md / idea.md once scaffolded)",
        "",
        "## Qualitative claims to support (no numbers)",
    ]
    for c in claims:
        lines.append(f"- {c}")
    lines.extend([
        "",
        "## Evidence preferences",
        "- Prefer primary sources, studies, or documented practices over secondary summaries.",
        "- Prefer sources that describe the stall mechanism or a concrete install of a start cue.",
        "- Avoid invented statistics; if a number is needed later, mark it as requiring a source.",
        "",
        "## Fillable claim-to-source table",
        "| Claim | Source (URL or citation) | Notes |",
        "|-------|--------------------------|-------|",
    ])
    for c in claims:
        lines.append(f"| {c} |  |  |")
    lines.extend([
        "",
        "## Suggested search prompts (copy into search engines; verify sources yourself)",
    ])
    for s in searches:
        lines.append(f"- {s}")
    lines.extend([
        "",
        "## Source verification checklist (apply to every candidate)",
        "- [ ] Primary or high-quality secondary source?",
        "- [ ] Publication date recent enough for the mechanism?",
        "- [ ] Describes the stall mechanism or a concrete cue install (not restatement only)?",
        "- [ ] Paywall / access notes recorded?",
        "- [ ] Exact citation ready (author, title, year, URL or DOI)?",
        "- [ ] Any numbers flagged as needing verification before use?",
        "- [ ] Discard if it only restates the problem without mechanism or install guidance.",
        "",
        "========================================================================",
        "## 3. SCRIPT OUTLINE STARTER",
        "========================================================================",
        f"# Script outline starter for {tid}: {title}",
        "# (no invented scenes or WORDS)",
        "# Aligns with production_rules: Hook 20-35, Payoff 40-70, body 140-220 each, CTA 40-80, total 900-1500.",
        "",
        "## Overview",
        f"- Topic: {title}",
        f"- Mechanism focus: {one_line}",
        f"- Stall: {problem}",
        "",
        "## Structure (preserve these headings after scaffold)",
        "",
        "### Hook (20-35 words)",
        f"Name the stall: {shorten(problem, 50)}.",
        "",
        "### Payoff (40-70 words)",
        f"The same-day install: {shorten(one_line, 60)}.",
        "",
        "### Beat 1 — where the cue lives (140-220 words)",
        f"Focus: the cue must be on the work itself. {shorten(one_line, 50)}.",
        "",
        "### Beat 2 — the under-two-minute step (140-220 words)",
        "Focus: the concrete install that ends the reopen.",
        "",
        "### Beat 3 — what reopens the list when the cue is missing (140-220 words)",
        f"Focus: {shorten(problem, 50)} returns without the cue.",
        "",
        "### CTA (40-80 words)",
        "Do the install now. Report the exact cue used.",
        "",
        "## Alignment notes",
        "- Keep every section mechanism-focused (the system, not the pep talk).",
        "- No invented numbers, testimonials, or scene descriptions.",
        "- Word targets are ranges; stay inside them after drafting.",
        "",
        "========================================================================",
        "## 4. TITLE OPTIONS (pick one or adapt; no shouted words)",
        "========================================================================",
    ])
    for i, t in enumerate(titles, 1):
        lines.append(f"{i}. {t}")
    lines.extend([
        "",
        "========================================================================",
        "## 5. THUMBNAIL CONCEPTS",
        "========================================================================",
    ])
    for i, th in enumerate(thumbs, 1):
        lines.append(f"{i}. {th}")
    lines.extend([
        "",
        "========================================================================",
        "## 6. DESCRIPTION SKELETON",
        "========================================================================",
        desc,
        "",
        "========================================================================",
        "## 7. FIRST-COMMENT OPTIONS (pick one or adapt)",
        "========================================================================",
    ])
    for i, c in enumerate(comments, 1):
        lines.append(f"{i}. {c}")
    lines.extend([
        "",
        "========================================================================",
        "## 8. TAG OPTIONS (comma-separated; pick 5-8; no invented trends)",
        "========================================================================",
        tags,
        "",
        "========================================================================",
        "## NEXT ACTIONS AFTER SCAFFOLDING",
        "========================================================================",
        "- python3 tools/idea_brief.py videos/NNN-slug --check",
        "- Fill draft.md from the outline above + research claims.",
        "- python3 tools/draft_starter.py videos/NNN-slug   # or draft_md_starter.py",
        "- python3 tools/draft_pre_apply_coach.py videos/NNN-slug",
        "- python3 tools/title_scan.py videos/NNN-slug && python3 tools/thumbnail_scan.py videos/NNN-slug",
        "- python3 tools/description_consistency.py videos/NNN-slug",
        "- Do not treat this full starter as WORDS or as script.md.",
        "",
        "Preferred human next remains OAuth (python3 tools/oauth_complete_guide.py). Do not scaffold Q2 while STALL_OAUTH_IDLE.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Full starter generator for queued topics.")
    parser.add_argument("--id", help="Topic id (e.g. Q2)")
    parser.add_argument("--write-doc", action="store_true", help="Write docs/qN_prepared_starter.md")
    parser.add_argument("--regenerate-all", action="store_true", help="Regenerate Q2-Q5 docs")
    args = parser.parse_args()

    queue_path = ROOT / "docs" / "topic_queue.md"
    if not queue_path.is_file():
        print(f"Missing queue: {queue_path}", file=sys.stderr)
        return 1

    rows = parse_queue(queue_path.read_text(encoding="utf-8"))

    if args.regenerate_all:
        targets = ["Q2", "Q3", "Q4", "Q5"]
        for tid in targets:
            row = next((r for r in rows if r["id"].upper() == tid), None)
            if not row:
                print(f"No row for {tid}", file=sys.stderr)
                continue
            content = generate_full(row)
            out = ROOT / "docs" / f"{tid.lower()}_prepared_starter.md"
            out.write_text(content, encoding="utf-8")
            print(f"Wrote {out}")
        return 0

    if not args.id:
        print("Provide --id or --regenerate-all", file=sys.stderr)
        return 1

    row = next((r for r in rows if r["id"].upper() == args.id.upper()), None)
    if not row:
        print(f"No row for id {args.id} in topic queue.", file=sys.stderr)
        return 1

    content = generate_full(row)
    if args.write_doc:
        out = ROOT / "docs" / f"{args.id.lower()}_prepared_starter.md"
        out.write_text(content, encoding="utf-8")
        print(f"Wrote {out}")
    else:
        print(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
