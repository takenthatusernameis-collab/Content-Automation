#!/usr/bin/env python3
"""Fill titles.md and thumbnail.md from idea + packet fields.

Heuristic copy only. No API. Output is required to satisfy validate_packet.py
title count / length and thumbnail word-count rules.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BANNED_PHRASES = (
    "never need motivation",
    "secret hack",
    "you won't believe",
    "make money",
    "grind",
)
STOP = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "for",
    "to",
    "of",
    "in",
    "on",
    "is",
    "are",
    "it",
    "as",
    "be",
    "by",
    "your",
    "you",
    "that",
    "this",
    "with",
    "from",
    "how",
    "why",
    "what",
    "they",
    "their",
    "them",
    "then",
    "when",
    "because",
    "so",
    "not",
    "but",
}


def field(text: str, name: str) -> str:
    m = re.search(rf"^-\s*{re.escape(name)}:\s*(.*)$", text, re.M)
    return (m.group(1).strip() if m else "")


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9']+", text)


def title_case(text: str) -> str:
    small = {"a", "an", "the", "and", "or", "for", "to", "of", "in", "on", "vs"}
    parts = words(text)
    out = []
    for i, w in enumerate(parts):
        low = w.lower()
        if i != 0 and low in small:
            out.append(low)
        else:
            out.append(low[:1].upper() + low[1:])
    return " ".join(out)


def clip_title(text: str, limit: int = 70) -> str:
    text = re.sub(r"\s+", " ", text).strip(" .")
    if len(text) <= limit:
        return text
    cut = text[: limit - 1]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut.strip(" -:,")


def content_tokens(text: str) -> list[str]:
    seen: list[str] = []
    for w in words(text.lower()):
        if w in STOP or len(w) < 3:
            continue
        if w not in seen:
            seen.append(w)
    return seen


def first_clause(text: str) -> str:
    text = re.split(r"[.;:]", text, maxsplit=1)[0]
    return text.strip()


def short_noun_phrase(text: str, n: int = 5) -> str:
    clause = first_clause(text)
    kept = []
    for w in words(clause):
        low = w.lower()
        if low in STOP and kept:
            continue
        kept.append(low)
        if len(kept) >= n:
            break
    return " ".join(kept) if kept else "the default"


def load_packet_inputs(packet: Path) -> dict[str, str]:
    idea = (packet / "idea.md").read_text(encoding="utf-8") if (packet / "idea.md").is_file() else ""
    pkt = (packet / "packet.md").read_text(encoding="utf-8") if (packet / "packet.md").is_file() else ""
    topic = field(idea, "topic") or field(pkt, "working_title") or packet.name
    problem = field(idea, "problem")
    mechanism = field(idea, "mechanism (the system, not the pep talk)") or field(idea, "mechanism")
    viewer = field(idea, "viewer")
    working = field(pkt, "working_title") or topic
    return {
        "topic": topic.rstrip("."),
        "problem": problem.rstrip("."),
        "mechanism": mechanism.rstrip("."),
        "viewer": viewer.rstrip("."),
        "working": working.rstrip("."),
    }


# Glue words may appear in a generated title. Every other word must come from this packet.
GLUE = {
    "stop",
    "write",
    "one",
    "before",
    "first",
    "rule",
    "name",
    "today",
    "without",
    "step",
}


def packet_blob(src: dict[str, str]) -> str:
    return " ".join(src.get(key, "") for key in ("topic", "problem", "mechanism", "viewer", "working"))


def grounded(phrase: str, blob_tokens: set[str]) -> bool:
    tokens = content_tokens(phrase)
    if not tokens:
        return False
    return all(token in blob_tokens or token in GLUE for token in tokens)


def candidate_titles(src: dict[str, str]) -> list[str]:
    topic = src["topic"]
    problem = src["problem"]
    mechanism = src["mechanism"]
    working = src["working"]
    blob_tokens = set(content_tokens(packet_blob(src)))
    topic_looks_like_title = 3 <= len(words(topic)) <= 12
    raw = [
        working or topic,
        topic if topic_looks_like_title and topic.lower() != (working or "").lower() else "",
        first_clause(problem),
        first_clause(mechanism),
        short_noun_phrase(problem, 6),
        short_noun_phrase(mechanism, 6),
    ]
    tokens = content_tokens(packet_blob(src))
    if tokens:
        raw.append(" ".join(tokens[:4]))
        # Run 399: stop/name/write are first-video verbs. Emit them only when
        # this packet already uses that verb, so a later card is not titled Stop X.
        if "stop" in blob_tokens:
            raw.append(f"stop {tokens[0]}")
        if "name" in blob_tokens:
            raw.append(f"name the {tokens[0]}")
        if "write" in blob_tokens:
            raw.append(f"write the {tokens[0]}")
        if len(tokens) > 1:
            raw.append(f"{tokens[0]} before {tokens[1]}")
            raw.append(f"one {tokens[0]} {tokens[1]}")
            raw.append(f"{tokens[0]} {tokens[1]} first")
    cleaned: list[str] = []
    seen: set[str] = set()
    for item in raw:
        t = clip_title(title_case(item)) if item else ""
        if not t or not grounded(t, blob_tokens):
            continue
        if any(b in t.lower() for b in BANNED_PHRASES):
            continue
        if any(w.isupper() and len(w) > 1 and not w.isalpha() for w in t.split()):
            continue
        key = t.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(t)
    if cleaned and not any(len(t) < 50 for t in cleaned) and tokens:
        short = clip_title(title_case(" ".join(tokens[:3])), 49)
        if short and short.lower() not in seen and grounded(short, blob_tokens):
            cleaned.insert(0, short)
            seen.add(short.lower())
    n = 0
    while len(cleaned) < 6 and tokens:
        extra = title_case(f"{tokens[n % len(tokens)]} step {n + 1}")
        n += 1
        if n > 8:
            break
        if extra.lower() in seen or not grounded(extra, blob_tokens):
            continue
        cleaned.append(extra)
        seen.add(extra.lower())
    return cleaned[:6]


def contrast_line(src: dict[str, str]) -> str:
    """Visual contrast from this packet. The first video's panel line is not the default."""
    blob = packet_blob(src).lower()
    borrowed = "calm empty panel vs leftover planning clutter"
    if "planning clutter" in blob or ("empty panel" in blob and "morning" in blob):
        return borrowed
    stall = first_clause(src.get("problem") or src.get("topic") or "this stall")
    step = first_clause(src.get("mechanism") or src.get("topic") or "this step")
    return f"{clip_title(stall, 42)} vs {clip_title(step, 42)}"


def thumb_line(src: dict[str, str]) -> str:
    """On-image words from this packet. A one-word step is not renamed Name The Step."""
    pool = content_tokens(src["mechanism"]) or content_tokens(src["topic"]) or content_tokens(src["working"])
    line = [w[:1].upper() + w[1:] for w in pool[:4]]
    if not line:
        line = ["This", "Step"]
    return " ".join(line[:5])


def render_titles(titles: list[str]) -> str:
    primary = titles[0]
    alts = titles[1:6]
    lines = ["# Titles", "", f"Primary: {primary}", "Alts:"]
    for i, t in enumerate(alts, start=1):
        lines.append(f"{i}. {t}")
    while len([ln for ln in lines if re.match(r"^\d+\.\s+\S", ln)]) < 5:
        n = len([ln for ln in lines if re.match(r"^\d+\.", ln)]) + 1
        lines.append(f"{n}. {titles[0]}")
    lines += [
        "",
        "Notes (promise vs clickbait risk):",
        "Heuristic brief from idea/packet fields. Avoid guru slogans. Human picks Primary.",
        "",
    ]
    return "\n".join(lines)


def render_thumb(src: dict[str, str], line: str, primary: str) -> str:
    subject = src["mechanism"] or src["topic"]
    return (
        "# Thumbnail\n"
        "\n"
        f"On-image text (max 5 words): {line}\n"
        f"Subject: Text card for: {clip_title(subject, 80)}\n"
        f"Contrast: {contrast_line(src)}\n"
        "Do not include: lightning bolts, GRIND, screaming faces, fake income\n"
        f"Matches title: Yes \u2014 {clip_title(primary, 60)}\n"
    )


def titles_from(text: str) -> list[str]:
    found: list[str] = []
    prim = re.search(r"^Primary:\s*(.+)$", text, re.M)
    if prim and prim.group(1).strip():
        found.append(prim.group(1).strip())
    for m in re.finditer(r"^\d+\.\s+(.+)$", text, re.M):
        found.append(m.group(1).strip())
    return [t for t in found if t]


def self_check(titles_text: str, thumb_text: str) -> list[str]:
    errors: list[str] = []
    titles = titles_from(titles_text)
    if len(titles) < 5:
        errors.append(f"only {len(titles)} titles, need >=5")
    if titles and not any(len(t) < 50 for t in titles):
        errors.append("need one title under 50 characters")
    text_line = ""
    m = re.search(r"^On-image text.*:\s*(.+)$", thumb_text, re.M)
    if m:
        text_line = m.group(1).strip()
    tw = words(text_line)
    if not tw:
        errors.append("thumbnail on-image text missing")
    elif len(tw) > 5:
        errors.append(f"thumbnail text has {len(tw)} words, max 5")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Write title + thumbnail brief from packet idea fields")
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--dry-run", action="store_true", help="Print files; do not write")
    parser.add_argument("--force", action="store_true", help="Overwrite even if titles already look filled")
    args = parser.parse_args()

    packet = Path(args.packet).resolve()
    if not packet.is_dir():
        print(f"not a directory: {packet}", file=sys.stderr)
        return 1

    src = load_packet_inputs(packet)
    titles = candidate_titles(src)
    line = thumb_line(src)
    titles_text = render_titles(titles)
    thumb_text = render_thumb(src, line, titles[0])
    errors = self_check(titles_text, thumb_text)
    if errors:
        print("generated brief failed its own field rules:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    existing = packet / "titles.md"
    if existing.is_file() and not args.force and not args.dry_run:
        cur = existing.read_text(encoding="utf-8")
        if titles_from(cur):
            print(f"titles already filled in {existing}; pass --force to overwrite", file=sys.stderr)
            return 1

    if args.dry_run:
        print(titles_text)
        print(thumb_text)
        print("SELF_CHECK PASS")
        return 0

    (packet / "titles.md").write_text(titles_text, encoding="utf-8")
    (packet / "thumbnail.md").write_text(thumb_text, encoding="utf-8")
    print(packet.relative_to(ROOT) if ROOT in packet.parents or packet.parent == ROOT else packet)
    print(f"primary={titles[0]}")
    print(f"thumb={line}")
    print("SELF_CHECK PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
