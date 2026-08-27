#!/usr/bin/env python3
"""Fill generated packet files after a folder is copied from template.

Writes qa.md + research.md always (research keeps a filled file).
Writes titles.md + thumbnail.md only when titles.md is still empty.
Reuses title_thumb_brief.write_brief — not a second generator.

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
from title_thumb_brief import write_brief  # noqa: E402


def generate(dest: Path, *, draft: bool = True) -> list[str]:
    """Write generated qa/research and empty-only titles/thumbs. Returns notes."""
    dest = dest.resolve()
    notes: list[str] = []

    # Titles first so qa mechanical boxes see filled title/thumb fields.
    notes.append(write_brief(dest, force=False))

    existing = (dest / "research.md").read_text(encoding="utf-8") if (dest / "research.md").is_file() else ""
    if research_is_filled(existing):
        notes.append(f"kept {dest.name}/research.md (already filled)")
    else:
        preserve = human_sources(existing) if existing else []
        research_text = render_research(dest, extra_sources=[], preserve_sources=preserve)
        (dest / "research.md").write_text(research_text, encoding="utf-8")
        notes.append(f"wrote {dest.name}/research.md")

    qa_text = render_qa(dest, draft=draft, prior=set())
    (dest / "qa.md").write_text(qa_text, encoding="utf-8")
    notes.append(f"wrote {dest.name}/qa.md")
    return notes
