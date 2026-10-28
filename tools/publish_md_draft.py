#!/usr/bin/env python3
"""Generate a paste-ready publish.md draft from packet idea.md + script.md.

Writes a local publish_draft.md with title candidate, operational description
(summary + chapters estimate at 150 wpm), tags, first-comment/CTA candidate,
and end-screen notes. Human reviews and copies into publish.md.

No invented claims, no external services, no packet content edits by design.
Reduces recurring human labor of assembling full publish metadata for Studio
or publish.md on every future packet.
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
        # fallback simple parse
        topic = problem = mech = ""
        for line in text.splitlines():
            if line.lower().startswith("- topic:"):
                topic = line.split(":", 1)[1].strip()
            elif line.lower().startswith("- problem:"):
                problem = line.split(":", 1)[1].strip()
            elif "mechanism" in line.lower() and ":" in line:
                mech = line.split(":", 1)[1].strip()
        return topic, problem, mech

    def shorten(text: str, max_len: int = 140) -> str:
        return text[:max_len]

WPM = 150


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
    lines = []
    cum = 0
    for header, spoken in sections:
        cnt = len(spoken.split()) if spoken else 0
        m, s = divmod(max(0, cum), 60)
        lines.append(f"{m}:{s:02d} {header}")
        cum += round(cnt / WPM * 60)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local publish_draft.md")
    parser.add_argument("packet", type=Path, help="Path to packet directory (must contain idea.md)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing publish_draft.md")
    args = parser.parse_args()

    packet = args.packet.resolve()
    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print(f"FAIL: idea.md missing in {packet}", file=sys.stderr)
        return 2

    idea_text = idea_path.read_text(encoding="utf-8")
    topic, problem, mech = extract(idea_text)
    if not any((topic, problem, mech)):
        print("FAIL: could not extract topic/problem/mechanism from idea.md", file=sys.stderr)
        return 2

    script_path = packet / "script.md"
    sections: list[tuple[str, str]] = []
    summary = ""
    chapters = ""
    if script_path.is_file():
        script_text = script_path.read_text(encoding="utf-8")
        sections = extract_spoken_sections(script_text)
        if sections:
            summary = extract_summary(sections)
            chapters = chapters_block(sections)

    # Simple candidates (reuse pattern from metadata_pack)
    title_cand = topic if topic and len(topic) < 70 else (shorten(mech, 50) if mech else "Untitled")
    tags = []
    if mech:
        tags.append(mech.lower()[:40])
    if topic:
        tags.append(topic.lower()[:40])
    tags.extend(["operational default", "systems", "mechanism"])
    tags = list(dict.fromkeys(t.strip() for t in tags if t.strip()))[:8]

    cta = f"Install the default: {shorten(mech, 60) if mech else 'the next-action note'} before the next work block."
    if problem:
        cta += f" Reply with the stall you named."

    out_path = packet / "publish_draft.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    lines = [
        "# Publish Draft (local; review before copying to publish.md)",
        "",
        "Status: draft",
        "Source: idea.md + script.md (if present). No invented claims.",
        "",
        "## Title to upload (candidate)",
        title_cand,
        "",
        "## Description",
        summary or (topic or "See idea.md"),
        "",
    ]
    if chapters:
        lines.extend([
            "### Chapters (estimated at 150 wpm)",
            chapters,
            "",
        ])
    lines.extend([
        "## Tags",
    ])
    for t in tags:
        lines.append(f"- {t}")
    lines.extend([
        "",
        "## First comment / CTA candidate",
        cta,
        "",
        "## End screen / cards",
        "- Last 20s reserved for YouTube end screen",
        "- Do not auto-subscribe-CTA in spoken WORDS",
        "",
        "## Human before upload",
        "- [ ] Lock primary title",
        "- [ ] Edit description for honesty and search",
        "- [ ] Trim tags",
        "- [ ] Approve first comment",
        "- [ ] Copy reviewed text into publish.md",
        "",
        "No upload happened. This file is a local draft only.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"title_candidate: {title_cand}")
    if summary:
        print(f"summary_chars: {len(summary)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
