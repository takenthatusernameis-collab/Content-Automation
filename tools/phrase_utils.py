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
    # Prefer natural clause breaks; added more seps for higher quality shorts
    for sep in (". ", ", ", " so ", " that ", " and ", " — ", " - ", "; ", ": ", " but ", " because "):
        if sep in text:
            cand = text.split(sep)[0].strip()
            if 8 <= len(cand) <= max_len:
                return cand
    # Fallback: whole words up to max_len
    words = text.split()
    out = []
    for w in words:
        trial = " ".join(out + [w])
        if len(trial) > max_len:
            break
        out.append(w)
    result = " ".join(out) if out else text[:max_len].rstrip()
    # Prefer not ending on a tiny fragment if possible
    if len(result) < 10 and len(text) > max_len:
        return text[:max_len].rsplit(" ", 1)[0] if " " in text[:max_len] else text[:max_len]
    return result


def normalize(text: str) -> str:
    """Normalize common variants so patterns match more reliably without duplicating entries.

    Converts curly apostrophes/quotes and en/em dashes to straight equivalents.
    Shared by quality_scan, claim_scan, and any future scanners.
    """
    text = text.replace("’", "'").replace("‘", "'")  # curly single quotes
    text = text.replace("“", '"').replace("”", '"')  # curly double
    text = text.replace("–", "-").replace("—", "-")  # en/em dash
    return text


def context_snippet(text: str, match, before: int = 40, after: int = 40, max_len: int = 90) -> str:
    """Return a short context snippet around a regex match for actionable revision signals.

    Shared by quality_scan, claim_scan, and any future scanners to avoid duplicated window logic.
    """
    start = max(0, match.start() - before)
    end = min(len(text), match.end() + after)
    context = text[start:end].replace("\n", " ").strip()
    if len(context) > max_len:
        context = context[: max_len - 3] + "..."
    return context


WORD_RE = re.compile(r"WORDS:\s*(.*?)(?:\nVISUAL:|\n## |\Z)", re.S | re.I)


def spoken_words(text: str) -> str:
    """Extract and normalize spoken WORDS blocks from a script or draft.

    Shared by quality_scan, claim_scan, cadence_repetition_scan, and any future scanners.
    Removes local WORD_RE + spoken copies so extraction and normalization stay consistent.
    """
    parts = WORD_RE.findall(text.replace("\r\n", "\n"))
    body = "\n".join(part.strip() for part in parts if part.strip())
    return normalize(body)


def count_spoken_words(text: str) -> int:
    """Count words in already-extracted or normalized spoken text.

    Applies normalize then a simple word split. Do not pass a full script;
    use spoken_words first for full files, or pass a section's spoken body.
    Shared so duration tools do not re-apply spoken_words to section text
    (which previously produced false zero counts).
    """
    cleaned = re.sub(r"[^\w\s'-]", " ", normalize(text or ""))
    return len([w for w in cleaned.split() if w.strip()])


def extract_sections(text: str) -> list[dict[str, str]]:
    """Extract ## sections with title, spoken body, and optional visual need.

    Shared by end-screen, timeline, and other structure tools so section
    boundaries and WORDS extraction stay identical. Spoken text is normalized.
    Does not invent content.
    """
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


# Shared narration rate constants and selector.
# Single source of truth so duration tools cannot diverge on human vs generated WPM.
# Observed Q1 generated take ~199 wpm; 190 is the calibrated default for generated origin.
HUMAN_WPM = 140  # typical clear explanatory narration rate
GENERATED_WPM = 190  # calibrated default when vo_origin marks generated


def select_rate(packet_path: Path) -> tuple[int, str]:
    """Return (wpm, label) based on vo_origin.md if present.

    Shared by speaking_time_estimate, end_screen_reserve_check, minimum_timeline_estimate,
    and any future duration planners so rate selection stays identical.
    Does not invent content or call external services.
    """
    origin_path = packet_path / "vo_origin.md"
    is_generated = False
    if origin_path.is_file():
        origin_text = origin_path.read_text(encoding="utf-8").lower()
        is_generated = "kind: generated" in origin_text or "kind=generated" in origin_text
    if is_generated:
        return GENERATED_WPM, "generated"
    return HUMAN_WPM, "human"


def _selected_vo_path(packet_path: Path) -> Path | None:
    """Return the canonical Selected VO path if the packet layout is standard. Does not invent files."""
    # Prefer the shared helper when available to stay consistent with render_brief.
    try:
        from render_brief import selected_vo_drop  # type: ignore
        rel = selected_vo_drop(packet_path)
        return (Path(__file__).resolve().parents[1] / rel) if not rel.startswith("/") else Path(rel)
    except Exception:
        # Fallback: standard naming from packet directory name
        name = packet_path.name
        cand = packet_path / "vo" / f"{name}-take-selected.wav"
        return cand if cand.parent.is_dir() else None


def observed_wpm(packet_path: Path, word_count: int) -> int | None:
    """Return observed WPM from Selected VO if the file exists and word_count > 0. No invented durations."""
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
    """Return (wpm, label) preferring observed rate from Selected VO when available, else select_rate.

    Shared so all duration tools automatically calibrate to a real take on the same packet
    without manual rate overrides. Falls back cleanly when no VO exists.
    Does not invent content or call external services.
    """
    obs = observed_wpm(packet_path, word_count)
    if obs is not None and 80 <= obs <= 250:  # sanity bounds for speech
        return obs, "observed"
    rate, label = select_rate(packet_path)
    return rate, label


def compile_word_boundary_patterns(phrases):
    """Compile high-precision word-boundary, case-insensitive regexes for a list of phrases.

    Shared by all scanners (quality_scan, claim_scan, title_scan, etc.) to avoid duplicated
    re.compile logic and ensure consistent matching (escape + \b + IGNORECASE).
    """
    return tuple(
        re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE) for phrase in phrases
    )


# Canonical high-precision anti-slop phrases.
# Single source of truth for quality_scan, suggestors, and starters.
# Matching is word-boundary, case-insensitive. Do not add broad regexes.
# quality_scan normalizes curly apostrophes/quotes/dashes so one straight entry covers common variants.
# Curly duplicates removed for maintainability (Run 752).
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


# Canonical high-precision hedge phrases for unsourced claim detection.
# Single source of truth for claim_scan. Matching is word-boundary, case-insensitive.
# claim_scan normalizes curly apostrophes/quotes/dashes so one straight entry covers common variants.
# Extracted for DRY consistency with ANTI_SLOP_PATTERNS (Run 756).
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


# Canonical high-precision weak/clickbait patterns for titles.
# Single source of truth for title_scan. Matching is word-boundary, case-insensitive.
# title_scan normalizes curly apostrophes/quotes/dashes so one straight entry covers common variants.
# Extracted for DRY consistency (Run 759). Curly duplicates removed.
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


# Canonical high-precision weak/clickbait patterns for thumbnail text.
# Single source of truth for thumbnail_scan. Matching is word-boundary, case-insensitive.
# thumbnail_scan normalizes curly apostrophes/quotes/dashes so one straight entry covers common variants.
# Extracted for DRY consistency (Run 759). Curly duplicates removed.
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


# Canonical high-precision weak patterns for chapter titles.
# Single source of truth for chapters_scan. Matching is word-boundary, case-insensitive.
# chapters_scan normalizes curly apostrophes/quotes/dashes so one straight entry covers common variants.
# Extracted for DRY consistency (Run 759). Curly duplicates removed.
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


# Canonical extras for description anti-slop beyond the shared ANTI_SLOP_PATTERNS.
# Single source of truth for description_scan additional matches.
# Matching is word-boundary, case-insensitive. Text is normalized so one straight entry covers variants.
# Extracted for DRY consistency (Run 760). Curly duplicates removed.
DESCRIPTION_EXTRA_PATTERNS = (
    "don't forget to",
    "leave a comment",
    "let me know",
)


# Canonical high-precision weak / engagement-bait patterns for end-screen / CTA.
# Single source of truth for end_screen_scan. Matching is word-boundary, case-insensitive.
# end_screen_scan normalizes curly apostrophes/quotes/dashes so one straight entry covers common variants.
# Extracted for DRY consistency (Run 760). Curly duplicates removed.
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


# Canonical high-precision engagement-bait / reply-prompt patterns for first comment.
# Single source of truth for first_comment_scan. Matching is word-boundary, case-insensitive.
# first_comment_scan normalizes curly apostrophes/quotes/dashes so one straight entry covers common variants.
# Extracted for DRY consistency (Run 760). Curly duplicates removed.
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


def extract_recommended_end_screen(fill_text: str) -> str | None:
    """Pull the End screen section from recommended_publish_fill.md if present and reasonable length.

    Shared by card_generator, cta_preview, end_screen_preview so ranking preference stays consistent.
    """
    match = re.search(
        r"^## End screen\s*\n(.+?)(?:\n##|\n\n|\Z)",
        fill_text,
        re.M | re.S,
    )
    if match:
        text = match.group(1).strip()
        text = re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()
        if text and 4 <= len(text.split()) <= 15:
            return text
    return None


def extract_recommended_thumbnail(fill_text: str) -> str | None:
    """Pull the Thumbnail section from recommended_publish_fill.md if present and short.

    Shared by thumbnail_generator so ranking preference stays consistent.
    """
    match = re.search(
        r"^## Thumbnail\s*\n(.+?)(?:\n##|\n\n|\Z)",
        fill_text,
        re.M | re.S,
    )
    if match:
        text = match.group(1).strip()
        text = re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()
        # Prefer short for on-image
        if text and 2 <= len(text.split()) <= 8:
            return text
    return None
