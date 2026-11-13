#!/usr/bin/env python3
"""Print a combined full starter for a queued topic (no packet folder required).

Pulls working_title, one_line, and problem from docs/topic_queue.md for the given id.
Emits in one output:
- Paste-ready idea.md skeleton
- Research.md qualitative claims + fillable source table
- Script outline skeleton (Hook / Payoff / beats / CTA)
- Title options
- Thumbnail concepts
- Description skeleton + first-comment options + tags

Grounded in queue data only. Does not invent hype, numbers, clickbait, anecdotes, scenes, sources, or full WORDS.
Does not write files. Does not scaffold. Does not call APIs.

Useful while STALL_OAUTH_IDLE persists: one command prepares the full pre-scaffold path
(idea + research + outline + packaging) for Q2+ so that when the human later scaffolds,
the packet starts from grounded skeletons and packaging options instead of blank.
Reduces recurring setup labor and tool-switching for every subsequent video.
Complements the individual queued_*_starter.py tools and the separate prep/packaging packs.
After scaffold, run the relevant consistency scans and draft coaches.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from queue_lib import parse_queue  # type: ignore


def suggest_claims(one_line: str, problem: str, title: str) -> list[str]:
    """Qualitative claim templates. No numbers or invented results."""
    ol = one_line[:80] or title[:80]
    pr = problem[:80] or "the described stall"
    return [
        f"The stall '{pr}' occurs when no concrete, visible default is present at the moment of starting.",
        f"Naming and installing '{ol}' as a physical or file cue reduces the reopen-the-list cycle.",
        f"A single under-two-minute install of the cue ends the decision delay on the same day for this viewer.",
        f"The cue must live on the work itself (not in a separate system) so the delay has something to hit.",
    ]


def suggest_search_prompts(one_line: str, problem: str, title: str) -> list[str]:
    """Grounded search prompts for finding real sources. No invented results.
    Uses clean word-boundary truncation so prompts stay readable.
    """
    def clean_short(text: str, max_len: int = 50) -> str:
        if not text:
            return ""
        core = text.split(",")[0].split(".")[0].strip()
        if len(core) <= max_len:
            return core
        words = core.split()
        acc = []
        for w in words:
            trial = " ".join(acc + [w])
            if len(trial) > max_len:
                break
            acc.append(w)
        return " ".join(acc).rstrip(".")

    ol = clean_short(one_line, 55) or clean_short(title, 55) or "start cue"
    pr = clean_short(problem, 50) or "morning stall"
    return [
        f'"{pr}" "start cue" OR "implementation intention" OR "if-then plan"',
        f'"decision fatigue" OR "choice overload" morning routine OR "task initiation"',
        f'"{ol}" physical cue OR environmental design OR "default action"',
        'implementation intentions Gollwitzer OR "if then plans" productivity',
        'environmental cues behavior change OR "nudge" start task',
    ]


def suggest_beats(one_line: str, problem: str, title: str) -> list[str]:
    """Grounded beat suggestions. No invented examples."""
    ol = one_line[:60] or title[:60]
    pr = problem[:60] or "the stall"
    return [
        f"Name the stall: '{pr}' happens when the start has no visible default.",
        f"Show the cue: install '{ol}' as a physical or file marker on the work itself.",
        f"Worked install: one under-two-minute step that places the cue where the delay occurs.",
        f"Failure mode: what reopens the list when the cue is missing or lives in a separate system.",
        f"Same-day test: the viewer finishes the install and starts the first two minutes without reopening the list.",
    ]


def idea_paste(title: str, one_line: str, problem: str) -> str:
    """Paste-ready idea.md body. Grounded; no invented viewer details."""
    viewer = "People who already plan their week, then stall when it is time to start."
    why_now = f"The week is already planned. The stall to install is this: {problem.rstrip('.')}."
    if not problem or problem.startswith("("):
        why_now = "The week is already planned, but the morning still reopens the whole list."
    return (
        "# Idea\n\n"
        f"- topic: {title}\n"
        f"- viewer: {viewer}\n"
        f"- problem: {problem}\n"
        f"- mechanism (the system, not the pep talk): {one_line}\n"
        f"- why now: {why_now}\n"
        f"- related videos to avoid repeating: none published yet\n"
    )


def suggest_titles(title: str, one_line: str, problem: str) -> list[str]:
    """Mechanism-focused titles. No shouted words, no weak patterns, no numbers.
    Prefer short, grammatical options grounded in queue data only.
    Use clean short phrases from queue fields; avoid concatenating full clauses.
    """
    def clean_short(text: str, max_len: int = 50) -> str:
        if not text:
            return ""
        core = text.split(",")[0].split(".")[0].strip()
        if len(core) <= max_len:
            return core
        words = core.split()
        acc = []
        for w in words:
            trial = " ".join(acc + [w])
            if len(trial) > max_len:
                break
            acc.append(w)
        return " ".join(acc).rstrip(".")

    ol_short = clean_short(one_line, 48)
    # Safe, distinct, grounded options that stay grammatical
    options = [
        title,
        "Install one visible start cue",
        ol_short if ol_short and len(ol_short) > 10 else "Name the start cue on the work",
        "One start cue ends the reopen",
        "Put the start cue on the work",
    ]
    seen = set()
    result = []
    for o in options:
        key = o.lower().strip()
        if o and key not in seen:
            seen.add(key)
            result.append(o)
    return result[:5]


def suggest_thumb_concepts(title: str, one_line: str, problem: str) -> list[str]:
    """Short thumbnail text and visual notes. Avoid long text and clickbait.
    Use clean short phrases to avoid mid-word cuts.
    """
    def clean_short(text: str, max_len: int = 36) -> str:
        if not text:
            return ""
        core = text.split(",")[0].split(".")[0].strip()
        if len(core) <= max_len:
            return core
        words = core.split()
        acc = []
        for w in words:
            trial = " ".join(acc + [w])
            if len(trial) > max_len:
                break
            acc.append(w)
        return " ".join(acc).rstrip(".")

    ol_short = clean_short(one_line, 38) or clean_short(title, 38)
    title_short = clean_short(title, 32)
    return [
        f"Text: '{ol_short}'  |  Visual: single object or file with a clear start marker; rest of list faded or closed.",
        f"Text: 'Start cue on the work'  |  Visual: before (open list) vs after (one marked first action) split, no faces, no metrics.",
        f"Text: '{title_short}'  |  Visual: physical or digital cue placed directly on the task surface or file.",
        "Text: none or very short  |  Visual: close-up of the installed cue alone; clean background.",
    ]


def suggest_description(title: str, one_line: str, problem: str) -> str:
    """Mechanism-focused description skeleton. No shouted words, no weak patterns, no numbers.
    Truncate problem/one_line cleanly to avoid mid-phrase cuts.
    """
    ol = (one_line.split(".")[0] if one_line else title).strip()[:75].rstrip(".")
    pr = (problem.split(",")[0] if problem else "the morning stall").strip()[:65].rstrip(".")
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
    """Short first-comment options. Operational, not promotional.
    Use clean short phrases to avoid mid-word cuts.
    """
    def clean_short(text: str, max_len: int = 45) -> str:
        if not text:
            return ""
        core = text.split(",")[0].split(".")[0].strip()
        if len(core) <= max_len:
            return core
        words = core.split()
        acc = []
        for w in words:
            trial = " ".join(acc + [w])
            if len(trial) > max_len:
                break
            acc.append(w)
        return " ".join(acc).rstrip(".")

    ol_short = clean_short(one_line, 48) or clean_short(title, 48)
    pr_short = clean_short(problem, 42) or "the morning stall"
    return [
        f"Try the install: put '{ol_short}' on the work itself before you open the list. Report back what the first two minutes looked like.",
        f"The stall is '{pr_short}'. The fix is one cue on the work, not another checklist. What cue are you placing today?",
        f"One visible default ends the reopen. If you finished the under-two-minute step, drop the exact cue you used.",
    ]


def suggest_tags(title: str, one_line: str, problem: str) -> list[str]:
    """Grounded tag options from queue fields. No invented trends or numbers.
    Prefer short, mechanism-focused tags that match the niche.
    """
    def clean_words(text: str, max_words: int = 4) -> str:
        if not text:
            return ""
        core = text.split(",")[0].split(".")[0].strip().lower()
        words = [w for w in core.split() if len(w) > 2]
        return " ".join(words[:max_words])

    base = [
        "start cue",
        "work start",
        "visible default",
        "morning stall",
        "next action",
        "productivity system",
        "decision fatigue",
    ]
    ol_tag = clean_words(one_line, 3)
    pr_tag = clean_words(problem, 3)
    if ol_tag and ol_tag not in base:
        base.append(ol_tag)
    if pr_tag and pr_tag not in base:
        base.append(pr_tag)
    # Deduplicate while preserving order
    seen = set()
    result = []
    for t in base:
        k = t.lower().strip()
        if k and k not in seen:
            seen.add(k)
            result.append(t)
    return result[:8]



def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a combined full starter (prep + packaging) for a queued topic id. No packet, no writes, no invented hype."
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
        print(f"# Note: {args.id} is already marked used. Full starter is still valid for reference.\n")

    title = row["working_title"]
    one_line = row["one_line"]
    problem = row["problem"] or "unspecified problem from queue"

    claims = suggest_claims(one_line, problem, title)
    search_prompts = suggest_search_prompts(one_line, problem, title)
    beats = suggest_beats(one_line, problem, title)
    titles = suggest_titles(title, one_line, problem)
    thumbs = suggest_thumb_concepts(title, one_line, problem)
    desc = suggest_description(title, one_line, problem)
    comments = suggest_first_comments(title, one_line, problem)
    tags = suggest_tags(title, one_line, problem)

    print(f"# Combined full starter for {args.id}: {title}")
    print("# (generated by queued_full_starter.py; no invented hype, numbers, clickbait, scenes, sources, or WORDS)")
    print("# Copy preferred sections into the packet after scaffolding. Do not treat any of this as script.md or WORDS.")
    print("# Aligns with production_rules word targets. Pairs with individual starters if you need only one section.")
    print()
    print("=" * 72)
    print("## 1. IDEA.MD PASTE (copy into idea.md after scaffold)")
    print("=" * 72)
    print(idea_paste(title, one_line, problem))
    print()
    print("=" * 72)
    print("## 2. RESEARCH.MD STARTER")
    print("=" * 72)
    print(f"# Research starter for {args.id}: {title}")
    print("# (no invented sources or numbers)")
    print()
    print("## Overview")
    print(f"- Working title: {title}")
    print(f"- One-line: {one_line}")
    print(f"- Problem: {problem}")
    print("- Viewer: (fill from channel.md / idea.md once scaffolded)")
    print()
    print("## Qualitative claims to support (no numbers)")
    for c in claims:
        print(f"- {c}")
    print()
    print("## Evidence preferences")
    print("- Prefer primary sources, studies, or documented practices over secondary summaries.")
    print("- Prefer sources that describe the stall mechanism or a concrete install of a start cue.")
    print("- Avoid invented statistics; if a number is needed later, mark it as requiring a source.")
    print()
    print("## Fillable claim-to-source table")
    print("| Claim | Source (URL or citation) | Notes |")
    print("|-------|--------------------------|-------|")
    for c in claims:
        print(f"| {c} |  |  |")
    print()
    print("## Suggested search prompts (copy into search engines; verify sources yourself)")
    for sp in search_prompts:
        print(f"- {sp}")
    print()
    print("## Source verification checklist (apply to every candidate)")
    print("- Confirm the source is primary or clearly secondary with primary cited.")
    print("- Check publication date; prefer recent for practices, classic for mechanisms like Gollwitzer.")
    print("- Ensure relevance to the specific stall mechanism, not general productivity.")
    print("- Note any paywalls or access issues; prefer open sources when possible.")
    print("- Record exact citation and quote or paraphrase with page/section.")
    print("- Flag if the source supports a number; if not, keep qualitative.")
    print("- Discard sources that only restate the problem without describing an install.")
    print()
    print("=" * 72)
    print("## 3. SCRIPT OUTLINE STARTER")
    print("=" * 72)
    print(f"# Script outline starter for {args.id}: {title}")
    print("# (no invented scenes or WORDS)")
    print("# Aligns with production_rules: Hook 20-35, Payoff 40-70, body 140-220 each, CTA 40-80, total 900-1500.")
    print()
    print("## Overview")
    print(f"- Working title: {title}")
    print(f"- One-line / mechanism: {one_line}")
    print(f"- Problem / stall: {problem}")
    print("- Format: explainer-6-10min (target ~1200 spoken words)")
    print()
    print("## Structure (preserve these headings after scaffold)")
    print("### ## Hook (0:00\u20130:12)")
    print("- Name the mechanism and the concrete stall.")
    print("- 20\u201335 spoken words. One sentence plus a sting is enough.")
    print(f"- Suggested focus: the stall '{problem[:50]}...' has no visible start default.")
    print()
    print("### ## Payoff promise")
    print("- One doable outcome the viewer can finish the same day.")
    print("- Name the mechanism again. 40\u201370 spoken words.")
    print(f"- Suggested focus: install '{one_line[:50]}...' and start without reopening the list.")
    print()
    print("### ## Body beats (4\u20136; each 140\u2013220 spoken words)")
    for i, b in enumerate(beats, 1):
        print(f"#### ## Beat {i} \u2014 {b.split(':')[0] if ':' in b else b[:30]}")
        print(f"- {b}")
        print("- Show the viewer using the mechanism on this packet's stall.")
        print("- Include one concrete action, example, or test. No slogans.")
        print()
    print("### ## CTA")
    print("- One action finishable in under two minutes that installs the mechanism.")
    print("- 40\u201380 spoken words. Calm, operational.")
    print(f"- Suggested focus: place the cue '{one_line[:40]}...' on the work itself right now.")
    print()
    print("## Alignment notes")
    print("- Hook and payoff must name the mechanism from the one_line.")
    print("- Beats must demonstrate the viewer installing or using the cue on the stall.")
    print("- Do not invent personal anecdotes or numbers. Use qualitative language until research.md has sources.")
    print()
    print("=" * 72)
    print("## 4. TITLE OPTIONS (pick one or adapt; no shouted words)")
    print("=" * 72)
    for i, t in enumerate(titles, 1):
        print(f"{i}. {t}")
    print()
    print("=" * 72)
    print("## 5. THUMBNAIL CONCEPTS")
    print("=" * 72)
    for i, th in enumerate(thumbs, 1):
        print(f"{i}. {th}")
    print()
    print("=" * 72)
    print("## 6. DESCRIPTION SKELETON")
    print("=" * 72)
    print(desc)
    print()
    print("=" * 72)
    print("## 7. FIRST-COMMENT OPTIONS (pick one or adapt)")
    print("=" * 72)
    for i, c in enumerate(comments, 1):
        print(f"{i}. {c}")
    print()
    print("=" * 72)
    print("## 8. TAG OPTIONS (comma-separated; pick 5-8; no invented trends)")
    print("=" * 72)
    print(", ".join(tags))
    print()
    print("=" * 72)
    print("## NEXT ACTIONS AFTER SCAFFOLDING")
    print("=" * 72)
    print("- python3 tools/idea_brief.py videos/NNN-slug --check")
    print("- Fill draft.md from the outline above + research claims.")
    print("- python3 tools/draft_starter.py videos/NNN-slug   # or draft_md_starter.py")
    print("- python3 tools/draft_pre_apply_coach.py videos/NNN-slug")
    print("- python3 tools/title_scan.py videos/NNN-slug && python3 tools/thumbnail_scan.py videos/NNN-slug")
    print("- python3 tools/description_consistency.py videos/NNN-slug")
    print("- Do not treat this full starter as WORDS or as script.md.")
    print()
    print("Preferred human next remains OAuth (python3 tools/oauth_complete_guide.py). Do not scaffold Q2 while STALL_OAUTH_IDLE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
