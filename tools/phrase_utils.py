#!/usr/bin/env python3
"""Shared text helpers for mechanism-aligned suggestions.

Provides whole-word / first-clause shortening so starters and suggestors
produce natural phrases without mid-word cuts.
"""

from __future__ import annotations


def shorten(text: str, max_len: int = 40) -> str:
    """Return a natural short phrase, preferring whole words or first clause."""
    text = text.strip()
    if len(text) <= max_len:
        return text
    for sep in (". ", ", ", " so ", " that ", " and ", " — ", " - "):
        if sep in text:
            cand = text.split(sep)[0].strip()
            if 10 <= len(cand) <= max_len:
                return cand
    words = text.split()
    out = []
    for w in words:
        trial = " ".join(out + [w])
        if len(trial) > max_len:
            break
        out.append(w)
    return " ".join(out) if out else text[:max_len].rstrip()
