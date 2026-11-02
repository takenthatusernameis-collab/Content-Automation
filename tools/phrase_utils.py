#!/usr/bin/env python3
"""Shared text helpers for mechanism-aligned suggestions.

Provides whole-word / first-clause shortening so starters and suggestors
produce natural phrases without mid-word cuts.
Also provides canonical section extraction and spoken-word counting so
duration estimators and scanners stay consistent.
"""

from __future__ import annotations

import re
from pathlib import Path


def shorten(text: str, max_len: int = 40) -> str:
    """Return a natural short phrase, preferring whole words or first clause.

    Prefers the first clause or segment that fits, then falls back to whole words.
    Added extra separators for better natural breaks.
    """
    text = text.strip()
    if len(text) <= max_len:
        return text
    for sep in (". ", ", ", " so ", " that ", " and ", " — ", " - ", "; ", ": ", " but ", " because "):
        if sep in text:
            cand = text.split(sep)[0].strip()
            if 8 <= len(cand) <= max_len:
                return cand
    words = text.split()
    out = []
    for w in words:
        trial = " ".join(out + [w])
        if len(trial) > max_len:
            break
        out.append(w)
    result = " ".join(out) if out else text[:max_len].rstrip()
    if len(result) < 10 and len(text) > max_len:
        return text[:max_len].rsplit(" ", 1)[0] if " " in text[:max_len] else text[:max_len]
    return result


def normalize(text: str) -> str:
    """Normalize common variants so patterns match more reliably without duplicating entries."""
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    return text


def context_snippet(text: str, match, before: int = 40, after: int = 40, max_len: int = 90) -> str:
    """Return a short context snippet around a regex match for actionable revision signals."""
    start = max(0, match.start() - before)
    end = min(len(text), match.end() + after)
    context = text[start:end].replace("\n", " ").strip()
    if len(context) > max_len:
        context = context[: max_len - 3] + "..."
    return context


WORD_RE = re.compile(r"WORDS:\s*(.*?)(?:\nVISUAL:|\n## |\Z)", re.S | re.I)


def spoken_words(text: str) -> str:
    """Extract and normalize spoken WORDS blocks from a script or draft."""
    parts = WORD_RE.findall(text.replace("\r\n", "\n"))
    body = "\n".join(part.strip() for part in parts if part.strip())
    return normalize(body)


def count_spoken_words(text: str) -> int:
    """Count words in already-extracted or normalized spoken text."""
    cleaned = re.sub(r"[^\w\s'-]", " ", normalize(text or ""))
    return len([w for w in cleaned.split() if w.strip()])


def extract_sections(text: str) -> list[dict[str, str]]:
    """Extract ## sections with title, spoken body, and optional visual need."""
    sections: list[dict[str, str]] = []
    parts = re.split(r"^##[ \t]+", text.replace("\r\n", "\n"), flags=re.M)
    for part in parts[1:]:
        lines = part.splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:])
        words_m = re.search(r"^WORDS:\s*\n(.*?)(?=^VISUAL:|^##|\Z)", body, re.M | re.S)
        spoken = (words_m.group(1).strip() if words_m else body)
        spoken = re.sub(r"\s+", " ", spoken).strip()
        vis_m = re.search(r"VISUAL:\s*(.*?)(?:WORDS:|ON SCREEN:|\Z)", body, re.S | re.I)
        need = re.sub(r"\s+", " ", vis_m.group(1)).strip() if vis_m else ""
        sections.append({
            "title": title,
            "spoken": normalize(spoken),
            "need": need,
        })
    return sections


HUMAN_WPM = 140
GENERATED_WPM = 190


def select_rate(packet_path: Path) -> tuple[int, str]:
    """Return (wpm, label) based on vo_origin.md if present."""
    origin_path = packet_path / "vo_origin.md"
    is_generated = False
    if origin_path.is_file():
        origin_text = origin_path.read_text(encoding="utf-8").lower()
        is_generated = "kind: generated" in origin_text or "kind=generated" in origin_text
    if is_generated:
        return GENERATED_WPM, "generated"
    return HUMAN_WPM, "human"


def _selected_vo_path(packet_path: Path) -> Path | None:
    """Return the canonical Selected VO path if the packet layout is standard."""
    try:
        from render_brief import selected_vo_drop  # type: ignore
        rel = selected_vo_drop(packet_path)
        return (Path(__file__).resolve().parents[1] / rel) if not rel.startswith("/") else Path(rel)
    except Exception:
        name = packet_path.name
        cand = packet_path / "vo" / f"{name}-take-selected.wav"
        return cand if cand.parent.is_dir() else None


def observed_wpm(packet_path: Path, word_count: int) -> int | None:
    """Return observed WPM from Selected VO if the file exists and word_count > 0."""
    if word_count <= 0:
        return None
    vo = _selected_vo_path(packet_path)
    if vo is None or not vo.is_file():
        return None
    try:
        import wave
        with wave.open(str(vo), "rb") as w:
            duration = w.getnframes() / float(w.getframerate())
            if duration <= 0:
                return None
            return int(round(word_count / (duration / 60.0)))
    except Exception:
        return None


def effective_rate(packet_path: Path, word_count: int = 0) -> tuple[int, str]:
    """Return (wpm, label) preferring observed rate from Selected VO when available."""
    obs = observed_wpm(packet_path, word_count)
    if obs is not None and 80 <= obs <= 250:
        return obs, "observed"
    rate, label = select_rate(packet_path)
    return rate, label


def compile_word_boundary_patterns(phrases):
    """Compile high-precision word-boundary, case-insensitive regexes for a list of phrases."""
    return tuple(
        re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE) for phrase in phrases
    )


ANTI_SLOP_PATTERNS = (
    "unlock your potential",
    "in today's fast-paced world",
    "we all struggle",
    "in this video",
    "you will learn",
    "the key is",
    "work smarter",
    "smash the like",
    "hit subscribe",
    "game changer",
    "at the end of the day",
    "in conclusion",
    "to summarize",
    "the bottom line is",
    "let's dive in",
    "without further ado",
    "it goes without saying",
    "as we all know",
    "it's no secret that",
    "needless to say",
    "the fact of the matter is",
    "to put it simply",
    "in other words",
    "the reality is",
    "here's the thing",
    "the truth is",
    "make no mistake",
    "in a nutshell",
    "long story short",
    "when all is said and done",
    "the point is",
    "let me be clear",
    "as it turns out",
    "believe it or not",
    "to be honest",
    "the thing is",
    "all in all",
    "moving forward",
    "going forward",
    "first and foremost",
    "it is important to note",
    "it should be noted",
    "as a matter of fact",
    "for what it's worth",
    "that being said",
    "having said that",
    "in fact",
    "of course",
    "obviously",
    "clearly",
    "simply put",
    "in short",
    "to be clear",
    "all things considered",
    "it's worth noting",
    "at its core",
    "when it comes to",
    "keep in mind",
    "in essence",
    "the fact remains",
    "let's be honest",
    "here's the kicker",
    "bear in mind",
    "take note that",
    "as you can see",
    "as we can see",
    "the takeaway is",
    "to put it in perspective",
    "it's important to remember",
    "in the modern world",
    "in today's society",
    "it's safe to say",
    "suffice it to say",
    "one thing is clear",
    "in a perfect world",
    "when push comes to shove",
    "to be fair",
    "last but not least",
    "with that said",
    "to that end",
    "as previously mentioned",
    "it is worth mentioning",
    "in reality",
    "as a result",
    "for instance",
    "in particular",
    "on the other hand",
    "that said",
    "the bottom line",
    "it is important",
    "to sum up",
    "in summary",
    "put simply",
    "what this means is",
    "the implication is",
    "case in point",
    "in the final analysis",
    "when you think about it",
    "in any event",
    "at any rate",
    "for the most part",
    "generally speaking",
    "as a general rule",
    "in today's world",
    "the secret is",
    "the secret to",
    "trust me",
    "believe me",
    "here's why",
    "here's what you need to know",
    "let me break it down",
    "the long and short of it",
    "to make a long story short",
    "in the grand scheme of things",
    "for all intents and purposes",
    "at this point in time",
    "with that in mind",
    "when it comes down to it",
    "the truth of the matter is",
    "plain and simple",
    "in layman's terms",
    "let me explain",
    "the reason is",
    "to put it another way",
    "so basically",
    "what I'm saying is",
    "the idea here is",
    "the point being",
    "here's the deal",
    "let's get into it",
    "to wrap things up",
    "as I mentioned",
    "what it all comes down to",
    "the one thing to remember",
    "comment below",
    "let me know in the comments",
    "drop a comment",
    "hit the bell",
    "what if I told you",
    "buckle up",
    "stay tuned",
    "let's get started",
    "to begin with",
    "first of all",
    "by the way",
    "as a side note",
    "moving on",
    "with that out of the way",
    "let me tell you",
    "here's a secret",
    "the key takeaway",
    "without wasting any time",
    "jumping right in",
    "let's jump in",
    "with all that said",
    "picture this",
    "imagine if",
    "have you ever",
    "did you know",
    "the secret sauce",
    "don't get me wrong",
    "the hard truth",
    "here's the catch",
    "spoiler alert",
    "but wait",
    "have you ever wondered",
    "most people don't realize",
    "in a world where",
    "let that sink in",
    "to understand why",
)

HEDGE_PATTERNS = (
    "studies show",
    "study shows",
    "research shows",
    "most people",
    "scientists found",
    "according to a study",
    "percent of people",
    "experts say",
    "data shows",
    "research indicates",
    "studies indicate",
    "according to experts",
    "research suggests",
    "evidence shows",
    "it has been shown",
    "scientists say",
    "a study found",
    "surveys indicate",
    "many studies show",
    "research has shown",
    "it is known that",
    "widely known that",
    "statistics show",
    "data indicates",
    "as research shows",
    "studies have shown",
    "researchers found",
    "according to a survey",
    "data reveals",
    "experts agree",
    "studies suggest",
    "researchers say",
    "a recent study",
    "according to research",
    "evidence suggests",
    "data suggests",
    "most experts agree",
    "studies have found",
    "it is widely accepted",
    "according to data",
    "researchers suggest",
)

TITLE_WEAK_PATTERNS = (
    "secret hack",
    "you won't believe",
    "must see",
    "this changes everything",
    "one weird trick",
    "will shock you",
    "you need to see",
    "this will change",
    "the secret to",
)

THUMBNAIL_WEAK_PATTERNS = (
    "you won't believe",
    "must watch",
    "must see",
    "click here",
    "don't miss",
    "shocking",
    "insane",
    "mind blown",
    "number one",
    "best ever",
)

CHAPTER_WEAK_PATTERNS = (
    "intro",
    "outro",
    "hook",
    "cta",
    "subscribe",
    "like and subscribe",
    "what you will learn",
    "in this video",
    "let's dive in",
)

DESCRIPTION_EXTRA_PATTERNS = (
    "don't forget to",
    "leave a comment",
    "let me know",
)

END_SCREEN_WEAK_PATTERNS = (
    "smash the like",
    "don't forget to",
    "leave a comment",
    "subscribe for more",
    "hit the subscribe",
    "like and subscribe",
    "comment below",
    "what do you think",
    "let me know",
    "turn on notifications",
    "ring the bell",
)

FIRST_COMMENT_BAIT_PATTERNS = (
    "reply with",
    "let me know",
    "comment below",
    "what do you think",
    "smash the like",
    "don't forget to",
    "leave a comment",
    "tell me in the comments",
    "drop a comment",
    "your thoughts",
    "let's discuss",
)


def _strip_fill_comments(text: str) -> str:
    """Remove HTML comments (score/runner-up notes) from a ranked fill section body."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()


def extract_recommended_end_screen(fill_text: str) -> str | None:
    """Pull the End screen section from recommended_publish_fill.md if present and reasonable length."""
    match = re.search(
        r"^## End screen\s*\n(.+?)(?:\n##|\n\n|\Z)",
        fill_text,
        re.M | re.S,
    )
    if match:
        text = _strip_fill_comments(match.group(1).strip())
        if text and 4 <= len(text.split()) <= 15:
            return text
    return None


def extract_recommended_thumbnail(fill_text: str) -> str | None:
    """Pull Thumbnail text from recommended_publish_fill.md.

    Matches both '## Thumbnail text' (writer label) and '## Thumbnail'.
    Run 964: fixed mismatch where fill wrote 'Thumbnail text' but extractor
    only matched bare 'Thumbnail', so ranked text was silently ignored.
    """
    match = re.search(
        r"^## Thumbnail(?: text)?\s*\n(.+?)(?:\n##|\n\n|\Z)",
        fill_text,
        re.M | re.S,
    )
    if match:
        text = _strip_fill_comments(match.group(1).strip())
        if text and 1 <= len(text.split()) <= 10:
            return text
    return None


def extract_recommended_first_comment(fill_text: str) -> str | None:
    """Pull the First comment section from recommended_publish_fill.md if present."""
    match = re.search(
        r"^## First comment\s*\n(.+?)(?:\n##|\n\n|\Z)",
        fill_text,
        re.M | re.S,
    )
    if match:
        text = _strip_fill_comments(match.group(1).strip())
        if text and 4 <= len(text.split()) <= 80:
            return text
    return None


def extract_recommended_title(fill_text: str) -> str | None:
    """Pull the Title section from recommended_publish_fill.md if present."""
    match = re.search(
        r"^## Title\s*\n(.+?)(?:\n##|\n\n|\Z)",
        fill_text,
        re.M | re.S,
    )
    if match:
        text = _strip_fill_comments(match.group(1).strip())
        if text and 3 <= len(text.split()) <= 20:
            return text
    return None


def extract_recommended_description(fill_text: str) -> str | None:
    """Pull the Description section from recommended_publish_fill.md if present."""
    match = re.search(
        r"^## Description\s*\n(.+?)(?:\n##|\n\n|\Z)",
        fill_text,
        re.M | re.S,
    )
    if match:
        text = _strip_fill_comments(match.group(1).strip())
        if text and 10 <= len(text.split()) <= 120:
            return text
    return None
