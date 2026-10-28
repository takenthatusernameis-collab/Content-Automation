#!/usr/bin/env python3
"""Assemble a paste-ready metadata pack from packet files.

Combines mechanism-aligned title candidates, tags, thumbnail text, end-screen/CTA,
plus a short operational summary and estimated chapters (at 150 wpm) from script.md
when present. Writes a local metadata_pack.txt.

No invented claims, no external services. Reduces recurring human labor of running
multiple suggestors and assembling publish.md / Studio metadata on every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from idea_utils import extract
    from phrase_utils import shorten
except ImportError:
    def extract(text: str) -> tuple[str, str, str]:
        return "", "", ""
    def shorten(text: str, max_len: int = 140) -> str:
        return text[:max_len]

WPM = 150
WEAK_TITLE = (
    "secret hack", "you won't believe", "must see", "this changes everything",
    "one weird trick", "will shock you", "the secret to",
)
WEAK_TAGS = (
    "video", "youtube", "tutorial", "how to", "subscribe", "free", "best",
    "amazing", "viral", "secret", "hack",
)
WEAK_THUMB = (
    "you won't believe", "must watch", "must see", "click here", "don't miss",
    "shocking", "insane", "mind blown",
)
WEAK_END = (
    "smash the like", "don't forget to", "leave a comment", "subscribe for more",
    "hit the subscribe", "like and subscribe", "comment below",
)


def extract_spoken_sections(text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_header = None
    capturing = False
    current_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("##"):
            if current_header is not None and current_lines:
                spoken = " ".join(current_lines).strip()
                sections.append((current_header, spoken))
            current_header = stripped.lstrip("#").strip()
            current_lines = []
            capturing = False
            continue
        if current_header is None:
            continue
        if stripped.startswith("WORDS"):
            capturing = True
            continue
        if stripped.startswith("VISUAL") or stripped.startswith("*"):
            capturing = False
            continue
        if capturing and stripped:
            current_lines.append(stripped)
    if current_header is not None and current_lines:
        spoken = " ".join(current_lines).strip()
        sections.append((current_header, spoken))
    return sections


def extract_summary(sections: list[tuple[str, str]], max_sents: int = 2) -> str:
    texts = []
    for header, spoken in sections:
        if not spoken:
            continue
        if any(k in header.lower() for k in ("hook", "payoff", "beat 1", "intro")):
            texts.append(spoken)
            if len(texts) >= 1:
                break
    if not texts and sections:
        texts = [sections[0][1]]
    full = " ".join(texts)
    sents = re.split(r"(?<=[.!?])\s+", full.strip())
    chosen = []
    for s in sents:
        s = s.strip()
        if len(s) > 25:
            chosen.append(shorten(s, 160))
            if len(chosen) >= max_sents:
                break
    if not chosen:
        chosen = [shorten(full, 180)]
    return " ".join(chosen)


def chapters_block(sections: list[tuple[str, str]]) -> str:
    out = ["# Estimated chapters (150 wpm from section spoken text)"]
    cum = 0
    for header, spoken in sections:
        cnt = len(spoken.split()) if spoken else 0
        m, s = divmod(max(0, cum), 60)
        out.append(f"{m}:{s:02d} {header} ({cnt} words)")
        cum += round(cnt / WPM * 60)
    total_m, total_s = divmod(cum, 60)
    out.append("")
    out.append(f"# Total estimated: {total_m}:{total_s:02d}")
    return "\n".join(out)


def suggest_titles(mech: str, problem: str, topic: str) -> list[str]:
    if not mech:
        mech = "the written next-action default"
    core = topic.strip() if topic and len(topic) <= 60 else shorten(mech, 45)
    base = core.lower()
    candidates = [
        topic if topic else f"Write the {base}",
        f"Install one default: {shorten(mech, 35)}",
        f"The stall is naming what to work on. The default is {shorten(mech, 28)}",
        f"Stop deciding. Write the {shorten(mech, 30)}",
        f"{shorten(mech, 40)} on a sticky note",
        f"One note that installs the {shorten(mech, 32)}",
    ]
    short = topic if topic and len(topic) < 50 else f"Write the {shorten(mech, 35)}"
    if len(short) >= 50:
        short = shorten(short, 48)
    candidates.insert(0, short)
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower()
        if any(w in low for w in WEAK_TITLE):
            continue
        words = re.findall(r"[A-Za-z]+", c)
        if any(w.isupper() and len(w) >= 5 for w in words):
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())
    return cleaned[:6]


def suggest_tags(mech: str, problem: str, topic: str) -> list[str]:
    if not mech:
        mech = "written next-action default"
    base = mech.lower()
    candidates = [
        base[:40],
        f"install {base[:30]}",
        "sticky note default",
        "before next tab",
        "under two minutes",
        "written next action",
        "name the stall",
        "one concrete default",
    ]
    if problem:
        short_prob = problem.lower()[:35]
        candidates.append(f"stall: {short_prob}")
    if topic:
        candidates.append(topic.lower()[:40])
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower().strip()
        if not low or len(low) < 3 or len(low) > 40:
            continue
        if any(w in low for w in WEAK_TAGS):
            continue
        if low not in seen:
            seen.add(low)
            cleaned.append(c.strip())
    extras = ["operational default", "mechanism install", "no decision stall"]
    for e in extras:
        if len(cleaned) >= 8:
            break
        if e not in seen and len(e) <= 40:
            cleaned.append(e)
            seen.add(e)
    return cleaned[:8]


def suggest_thumbs(mech: str, problem: str, topic: str) -> list[str]:
    if not mech:
        mech = "written next-action default"
    base = mech.lower()
    candidates = [
        f"Write the {base[:25]}",
        "Name the stall",
        f"Install: {base[:20]}",
        "One default on disk",
        f"Stop deciding. {base[:15]}",
        "Same-day install",
    ]
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower()
        if any(w in low for w in WEAK_THUMB):
            continue
        words = c.split()
        if len(words) > 8:
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())
    return cleaned[:5]


def suggest_ends(mech: str, problem: str, topic: str) -> list[str]:
    if not mech:
        mech = "written next-action default"
    base = mech.lower()
    candidates = [
        f"Write the {base[:30]} on disk today.",
        f"Install the {base[:25]} before the next decision.",
        "Name the stall in one sentence and write the default.",
        f"Same-day install: {base[:20]}",
        "One concrete default beats another open decision.",
    ]
    cleaned = []
    seen = set()
    for c in candidates:
        low = c.lower()
        if any(w in low for w in WEAK_END):
            continue
        words = c.split()
        if len(words) > 15 or len(words) < 4:
            continue
        key = low.strip()
        if key and key not in seen:
            seen.add(key)
            cleaned.append(c.strip())
    return cleaned[:4]


def main() -> int:
    p = argparse.ArgumentParser(description="Assemble paste-ready metadata pack from packet")
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    p.add_argument("--out", type=Path, default=None, help="Optional output path")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print("ERROR: idea.md missing", file=sys.stderr)
        return 1

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = extract(idea_text)

    titles = suggest_titles(mech, problem, topic)
    tags = suggest_tags(mech, problem, topic)
    thumbs = suggest_thumbs(mech, problem, topic)
    ends = suggest_ends(mech, problem, topic)

    script_path = packet / "script.md"
    summary = ""
    chapters = ""
    sections_count = 0
    if script_path.is_file():
        script_text = script_path.read_text(encoding="utf-8")
        sections = extract_spoken_sections(script_text)
        sections_count = len(sections)
        if sections:
            summary = extract_summary(sections)
            chapters = chapters_block(sections)

    lines = [
        "# Metadata pack draft (local; review before paste)",
        "",
        f"mechanism: {mech or '(none)'}",
        f"problem: {problem or '(none)'}",
        f"topic: {topic or '(none)'}",
        "",
        "## Title candidates (mechanism-aligned; at least one short; no clickbait)",
    ]
    for i, t in enumerate(titles, 1):
        lines.append(f"{i}. {t}  ({len(t)} chars)")
    lines.extend(["", "## Tags (specific; no weak/generic)",])
    for t in tags:
        lines.append(f"- {t}")
    lines.extend(["", "## Thumbnail text (short/readable; no clickbait)",])
    for i, t in enumerate(thumbs, 1):
        lines.append(f"{i}. {t}  ({len(t.split())} words)")
    lines.extend(["", "## End-screen / CTA (concrete action; no engagement bait)",])
    for i, t in enumerate(ends, 1):
        lines.append(f"{i}. {t}")
    if summary:
        lines.extend(["", "## Description summary (from script spoken)", summary])
    if chapters:
        lines.extend(["", chapters])
    lines.extend([
        "",
        "Write the next-action sentence tonight. Use it tomorrow before any list.",
        "",
        "# Draft only — human confirms voice, accuracy, and Primary choices before publishing.",
    ])
    out_text = "\n".join(lines) + "\n"

    out_path = args.out or (packet / "metadata_pack.txt")
    out_path.write_text(out_text, encoding="utf-8")

    print(out_text)
    print(f"wrote: {out_path}")
    print(f"titles: {len(titles)} tags: {len(tags)} thumbs: {len(thumbs)} ends: {len(ends)} sections: {sections_count}")
    print("Metadata pack ready (local; gitignore if desired).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
