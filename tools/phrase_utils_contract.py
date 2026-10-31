#!/usr/bin/env python3
"""Contract lock for the shared phrase_utils helpers.

Future runs can prove tools/phrase_utils stays consistent
(shorten, normalize, spoken_words, count_spoken_words, extract_sections,
compile_word_boundary_patterns, context_snippet)
instead of allowing local copies to drift again.
Writes nothing. Exits 0 on pass, 1 on failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from phrase_utils import (  # noqa: E402
    shorten,
    normalize,
    spoken_words,
    count_spoken_words,
    extract_sections,
    compile_word_boundary_patterns,
    context_snippet,
    ANTI_SLOP_PATTERNS,
    HEDGE_PATTERNS,
)


def check() -> list[str]:
    failures: list[str] = []

    # --- shorten (existing) ---
    if shorten("Short phrase", 40) != "Short phrase":
        failures.append("short text mutated")

    long = "Write the next action on a sticky note. Then the stall disappears."
    if shorten(long, 40) != "Write the next action on a sticky note":
        failures.append(f"clause shorten failed: {shorten(long, 40)!r}")

    no_sep = "This is a longer phrase without any separators that needs shortening"
    result = shorten(no_sep, 30)
    if " " not in result or len(result) > 30:
        failures.append(f"word-boundary shorten failed: {result!r}")

    if shorten("", 10) != "":
        failures.append("empty not empty")
    if shorten("   ", 10) != "":
        failures.append("whitespace not stripped to empty")

    # --- normalize ---
    curly = "it\u2019s \u201chello\u201d \u2014 dash"
    straight = normalize(curly)
    if "'" not in straight or '"' not in straight or "-" not in straight:
        failures.append(f"normalize failed on curly: {straight!r}")
    if "\u2019" in straight or "\u201c" in straight or "\u2014" in straight:
        failures.append("normalize left curly/dash characters")

    # --- spoken_words ---
    sample = "WORDS:\nit\u2019s a test.\nVISUAL: card\nWORDS:\nanother."
    spoken = spoken_words(sample)
    if "it's a test" not in spoken or "another" not in spoken:
        failures.append(f"spoken_words failed: {spoken!r}")
    if "\u2019" in spoken:
        failures.append("spoken_words did not normalize")

    # --- count_spoken_words ---
    if count_spoken_words("one two three") != 3:
        failures.append("count_spoken_words simple failed")
    if count_spoken_words("it\u2019s a test") != 3:
        failures.append("count_spoken_words normalize failed")
    if count_spoken_words("") != 0:
        failures.append("count_spoken_words empty failed")

    # --- extract_sections ---
    script = "## Hook\nWORDS:\nHello world.\nVISUAL: title card\n## CTA\nWORDS:\nThanks for watching."
    secs = extract_sections(script)
    if len(secs) != 2:
        failures.append(f"extract_sections count failed: {len(secs)}")
    else:
        if secs[0]["title"] != "Hook" or "Hello world" not in secs[0]["spoken"]:
            failures.append("extract_sections hook failed")
        if secs[1]["title"] != "CTA" or "Thanks" not in secs[1]["spoken"]:
            failures.append("extract_sections cta failed")
        if count_spoken_words(secs[0]["spoken"]) != 2:
            failures.append("extract_sections word count failed")

    # --- compile_word_boundary_patterns ---
    pats = compile_word_boundary_patterns(("the key", "unlock"))
    if len(pats) != 2:
        failures.append("compile returned wrong length")
    text = "The key is here. Unlock potential. Thekey is not matched."
    if not pats[0].search(text) or not pats[1].search(text):
        failures.append("compile did not match expected phrases")
    if pats[0].search("Thekey"):
        failures.append("word boundary failed on partial word")

    # --- context_snippet ---
    m = re.search(r"key", "the key is important here")
    if m is None:
        failures.append("test regex match missing")
    else:
        ctx = context_snippet("the key is important here", m, before=6, after=6, max_len=25)
        if "key" not in ctx or len(ctx) > 25:
            failures.append(f"context_snippet bad: {ctx!r}")

    # --- lists non-empty ---
    if not ANTI_SLOP_PATTERNS or not HEDGE_PATTERNS:
        failures.append("canonical pattern lists empty")

    return failures


def main() -> int:
    fails = check()
    if fails:
        print("PHRASE_UTILS_CONTRACT FAIL")
        for f in fails:
            print(f"- {f}")
        return 1
    print("PHRASE_UTILS_CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
