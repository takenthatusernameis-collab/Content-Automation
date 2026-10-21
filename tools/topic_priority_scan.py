#!/usr/bin/env python3
"""Score queued topics for channel fit and mechanism continuity from Q1.

Reads docs/topic_queue.md and docs/channel.md (and optional Q1 idea.md).
Prints ranked queued topics by keyword overlap with niche, promise, audience,
and Q1 mechanism language (start, stall, cue, default, constraint, list, morning, etc.).
Does not invent topics, numbers, or claims. Does not write files. Does not scaffold.
Useful for prioritizing which queued topic to scaffold next after Q1 ships.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from queue_lib import already_used, existing_slugs, next_id, slugify  # noqa: E402

QUEUE = ROOT / "docs" / "topic_queue.md"
CHANNEL = ROOT / "docs" / "channel.md"
Q1_IDEA = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning" / "idea.md"
VIDEOS = ROOT / "videos"

# Keywords that indicate strong channel fit (from niche/promise/voice)
CHANNEL_KEYWORDS = {
    "start", "stall", "cue", "default", "constraint", "checklist", "list",
    "morning", "work", "action", "next", "visible", "physical", "file",
    "desk", "tab", "shutdown", "reopen", "planned", "verb", "install",
    "system", "process", "focused", "operational", "small",
}

MECHANISM_PHRASES = (
    "next-action default", "written next-action", "reopen the whole list",
    "start cue", "visible start", "morning does not reopen",
    "constraint on the", "where the stall", "shutdown default",
)

def load_text(path: Path, lower: bool = True) -> str:
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8")
    return text.lower() if lower else text

def extract_keywords(text: str) -> set[str]:
    words = set(re.findall(r"\b[a-z]{3,}\b", text))
    return words & CHANNEL_KEYWORDS

def parse_queue_rows(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        if line.lower().startswith("| q") and "|" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 6:
                rows.append({
                    "id": parts[1],
                    "status": parts[2].lower(),
                    "title": parts[3],
                    "one_line": parts[4],
                    "problem": parts[5],
                })
    return rows

def score_topic(row: dict, channel_kws: set[str], q1_kws: set[str]) -> tuple[int, list[str]]:
    combined = (row["title"] + " " + row["one_line"] + " " + row["problem"]).lower()
    topic_kws = extract_keywords(combined)
    score = len(topic_kws & channel_kws) * 2
    score += len(topic_kws & q1_kws)
    # Bonus for explicit "start" or "stall" language
    if "start" in combined or "stall" in combined or "cue" in combined:
        score += 3
    # Stronger phrase continuity with Q1 mechanism language
    matched_phrases = []
    for phrase in MECHANISM_PHRASES:
        if phrase in combined:
            score += 4
            matched_phrases.append(phrase)
    return score, matched_phrases

def main() -> int:
    channel_text = load_text(CHANNEL)
    q1_text = load_text(Q1_IDEA)
    queue_text = load_text(QUEUE, lower=False) if QUEUE.is_file() else ""

    channel_kws = extract_keywords(channel_text)
    q1_kws = extract_keywords(q1_text)

    rows = parse_queue_rows(queue_text)
    queued = [r for r in rows if r["status"] == "queued"]

    scored = []
    for row in queued:
        s, phrases = score_topic(row, channel_kws, q1_kws)
        scored.append((s, phrases, row))

    scored.sort(key=lambda x: -x[0])

    print("TOPIC PRIORITY SCAN (channel fit + Q1 continuity; no invent, no writes)")
    print(f"channel keywords matched: {len(channel_kws)}")
    print(f"Q1 mechanism keywords: {len(q1_kws)}")
    print(f"queued topics scored: {len(scored)}")
    print()
    if not scored:
        print("No queued topics found. Add rows to docs/topic_queue.md.")
        return 0

    print("Ranked by fit (higher = better continuity with niche/promise/Q1):")
    for rank, (score, phrases, row) in enumerate(scored, 1):
        print(f"  {rank}. {row['id']} (score {score}) — {row['title']}")
        print(f"     one_line: {row['one_line'][:90]}")
        print(f"     problem: {row['problem'][:90]}")
        if phrases:
            print(f"     matched phrases: {', '.join(phrases)}")
        print()

    if scored:
        top_score, top_phrases, top_row = scored[0]
        print("TOP RECOMMENDATION (after Q1 ships and Selected VO exists on gate machine):")
        print(f"  {top_row['id']} (score {top_score}) — {top_row['title']}")
        print(f"  one_line: {top_row['one_line']}")
        if top_phrases:
            print(f"  Why this score (matched mechanism phrases): {', '.join(top_phrases)}")
        else:
            print("  Why this score: keyword overlap only (no exact mechanism phrases)")
        # Dynamic predicted path and commands (reuses queue_lib like next_topic.py)
        slugs = existing_slugs(VIDEOS)
        if not already_used(top_row["title"], slugs):
            predicted_id = next_id(VIDEOS)
            slug = slugify(top_row["title"])
            dest = f"videos/{predicted_id}-{slug}"
            print(f"  Predicted path: {dest}")
            print("  # Parked until Q1 ships (copy-paste only after Selected VO exists on the gate machine):")
            print("  Optional before scaffold (no folder required; writes nothing):")
            print(f"    python3 tools/idea_brief.py --queue {top_row['id']}")
            print("  Scaffold (human / instructed agent only; not the fixture):")
            print(f'    python3 tools/new_packet.py "{top_row["title"]}"')
            print(f'    python3 tools/new_idea.py "{top_row["one_line"]}"')
            print(f"    python3 tools/doctor.py {dest}")
        print("  Do not scaffold while Q1 has no on-disk Selected VO.")

    print()
    print("Use this ranking when choosing the next scaffold after Q1 ships.")
    print("Do not invent new topics here; only scores existing queued rows.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
