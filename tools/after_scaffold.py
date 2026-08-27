#!/usr/bin/env python3
"""Fill generated packet files after a folder is copied from template.

Writes titles.md + thumbnail.md only when titles.md is still empty.
Writes publish.md only when it is still empty.
Writes captions.md only when it is still empty.
Writes research.md (keeps a filled file) then qa.md.
Reuses title_thumb_brief renderers — not a second title generator.
Reuses publish_brief — not an uploader.
Reuses caption_brief — not Whisper / SRT export.

Does not scrape, score, invent sources, or call YouTube. Intended for
new_idea.py / new_packet.py.
"""

from __future__ import annotations

import re
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
from title_thumb_brief import (  # noqa: E402
    candidate_titles,
    load_packet_inputs,
    render_thumb,
    render_titles,
    self_check,
    thumb_line,
)
from publish_brief import write_empty_publish  # noqa: E402
from caption_brief import write_empty_captions  # noqa: E402


def titles_filled(text: str) -> bool:
    """Same one-line rule as validate_packet.titles_from. Empty `1.` is not a title."""
    prim = re.search(r"^Primary:[ \t]*([^\n]*)$", text, re.M)
    if prim and prim.group(1).strip():
        return True
    return bool(re.search(r"^\d+\.[ \t]+\S", text, re.M))


def write_empty_title_brief(dest: Path) -> str:
    existing = dest / "titles.md"
    cur = existing.read_text(encoding="utf-8") if existing.is_file() else ""
    if titles_filled(cur):
        return f"kept {dest.name}/titles.md+thumbnail.md (already filled)"

    src = load_packet_inputs(dest)
    titles = candidate_titles(src)
    line = thumb_line(src)
    titles_text = render_titles(titles)
    thumb_text = render_thumb(src, line, titles[0])
    errors = self_check(titles_text, thumb_text)
    if errors:
        return f"skipped {dest.name}/titles.md (self-check failed: {'; '.join(errors)})"
    (dest / "titles.md").write_text(titles_text, encoding="utf-8")
    (dest / "thumbnail.md").write_text(thumb_text, encoding="utf-8")
    return f"wrote {dest.name}/titles.md+thumbnail.md"


def generate(dest: Path, *, draft: bool = True) -> list[str]:
    """Write generated qa/research/publish/captions and empty-only titles/thumbs."""
    dest = dest.resolve()
    notes: list[str] = []

    # Titles first so publish.md can use Primary and qa boxes see filled fields.
    notes.append(write_empty_title_brief(dest))
    notes.append(write_empty_publish(dest))
    notes.append(write_empty_captions(dest))

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
