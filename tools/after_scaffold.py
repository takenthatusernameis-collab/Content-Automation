#!/usr/bin/env python3
"""Fill qa.md and research.md after a packet folder is copied from template.

Does not scrape, score, or invent sources. Intended for new_idea.py / new_packet.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from qa_checklist import render as render_qa  # noqa: E402
from research_brief import (  # noqa: E402
    human_sources,
    render as render_research,
    research_is_filled,
)


def generate(dest: Path, *, draft: bool = True) -> list[str]:
    """Write generated qa.md + research.md. Returns human-readable lines."""
    dest = dest.resolve()
    notes: list[str] = []

    qa_text = render_qa(dest, draft=draft, prior=set())
    (dest / "qa.md").write_text(qa_text, encoding="utf-8")
    notes.append(f"wrote {dest.name}/qa.md")

    existing = (dest / "research.md").read_text(encoding="utf-8") if (dest / "research.md").is_file() else ""
    if research_is_filled(existing):
        notes.append(f"kept {dest.name}/research.md (already filled)")
    else:
        preserve = human_sources(existing) if existing else []
        research_text = render_research(dest, extra_sources=[], preserve_sources=preserve)
        (dest / "research.md").write_text(research_text, encoding="utf-8")
        notes.append(f"wrote {dest.name}/research.md")
    return notes
