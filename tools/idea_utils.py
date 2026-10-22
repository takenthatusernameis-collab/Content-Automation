#!/usr/bin/env python3
"""Shared idea.md field extractors for mechanism-aligned suggestors.

Provides consistent parsing of mechanism, problem, and topic so all
suggestors stay aligned without copy-paste drift.
"""

from __future__ import annotations

import re

MECH_RE = re.compile(r"mechanism[^\n]*:\s*(.+)", re.I)
PROBLEM_RE = re.compile(r"problem:\s*(.+)", re.I)
TOPIC_RE = re.compile(r"topic:\s*(.+)", re.I)


def extract(idea_text: str) -> tuple[str, str, str]:
    """Return (mechanism, problem, topic) from idea.md text. Empty strings if absent."""
    mech = ""
    problem = ""
    topic = ""
    for line in idea_text.splitlines():
        m = MECH_RE.search(line)
        if m:
            mech = m.group(1).strip().rstrip(".")
        p = PROBLEM_RE.search(line)
        if p:
            problem = p.group(1).strip().rstrip(".")
        t = TOPIC_RE.search(line)
        if t:
            topic = t.group(1).strip().rstrip(".")
    return mech, problem, topic
