#!/usr/bin/env python3
"""Report unsourced quantitative or survey claims in script.md WORDS.

Does not rewrite script.md or research.md. A digit token or hedge phrase in
spoken WORDS is a hit unless a non-placeholder Sources bullet cites that
same token or phrase. A missing script is not a hit. Default exit is 0 so a
clear packet cannot fail the build. --strict exits 1 when any hit remains.
set_status.py refuses ready_for_vo while a hit remains.

Output includes a short context snippet around the first match of each
hit so the revision signal is immediately actionable.

Also scans sources.md (if present) in addition to research.md so that
structured sources from research_sources_starter.py or research_brief_starter.py
can satisfy citations. Extracts Source column values from tables and
non-placeholder bullets from either file and injects them as ## Sources
bullets so human_sources can use them.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from research_brief import human_sources, numbers_in_spoken_words, is_placeholder_source  # noqa: E402

WORD_RE = re.compile(r"WORDS:\s*(.*?)(?:\nVISUAL:|\n## |\Z)", re.S)
HEDGES = (
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
)
# Precompile word-boundary patterns once (case-insensitive) for higher precision.
_HEDGE_RES = tuple(
    re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE) for phrase in HEDGES
)


def spoken(text: str) -> str:
    parts = WORD_RE.findall(text.replace("\r\n", "\n"))
    return "\n".join(part.strip() for part in parts)


def hedges_in_spoken(script: str) -> list[tuple[str, str]]:
    body = spoken(script)
    found = []
    for phrase, cre in zip(HEDGES, _HEDGE_RES):
        matches = list(cre.finditer(body))
        if matches:
            m = matches[0]
            start = max(0, m.start() - 40)
            end = min(len(body), m.end() + 40)
            context = body[start:end].replace("\n", " ").strip()
            if len(context) > 90:
                context = context[:87] + "..."
            found.append((phrase, context))
    return found


def cited(sources: list[str], token: str) -> bool:
    needle = token.lower()
    return any(needle in item.lower() for item in sources)


def hits(script: str, research: str) -> list[tuple[str, str, str]]:
    sources = human_sources(research)
    body = spoken(script)
    found: list[tuple[str, str, str]] = []
    # Digits: extract context around the token if possible
    for token in numbers_in_spoken_words(script):
        if not cited(sources, token):
            # Simple context: search for the token
            m = re.search(r"\b" + re.escape(token) + r"\b", body)
            if m:
                start = max(0, m.start() - 40)
                end = min(len(body), m.end() + 40)
                context = body[start:end].replace("\n", " ").strip()
                if len(context) > 90:
                    context = context[:87] + "..."
            else:
                context = ""
            found.append(("digit", token, context))
    for phrase, ctx in hedges_in_spoken(script):
        if not cited(sources, phrase):
            found.append(("hedge", phrase, ctx))
    return found


def extract_sources_from_md(sources_text: str) -> list[str]:
    """Extract usable source strings from research.md or sources.md skeletons or filled files.

    Pulls non-empty Source column values from any table that has a Source column
    and non-placeholder bullet lines. These are injected so human_sources can
    treat them as citations. Works for both the research_sources_starter Source log
    and the research_brief_starter Primary claims table.
    """
    extras: list[str] = []
    seen = set()
    # Table rows: look for lines starting with | that have a Source-like column
    for line in sources_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        parts = [p.strip() for p in stripped.split("|")]
        # Skip header rows that contain the word Source as a column name
        if any(p.lower() in ("source", "source (title + link or citation)", "source column") for p in parts):
            continue
        # Prefer the second non-empty part after the leading empty (typical Claim | Source ...)
        # or scan for a part that looks like a source (non-empty, not placeholder)
        candidates = [p for p in parts[1:] if p and p.lower() not in ("claim", "source", "retrieved", "notes", "how it supports the claim")]
        for src in candidates:
            if src and not is_placeholder_source(src):
                key = src.lower()
                if key not in seen:
                    seen.add(key)
                    extras.append(src)
                break  # take the first plausible source cell per row
    # Any bullet lines that are not placeholders
    for m in re.finditer(r"^-\s+(.+)$", sources_text, re.M):
        item = m.group(1).strip()
        if item and not is_placeholder_source(item):
            key = item.lower()
            if key not in seen:
                seen.add(key)
                extras.append(item)
    return extras


def scan_path(path: Path) -> list[tuple[str, str, str]]:
    script = path / "script.md"
    if not script.is_file():
        return []
    research_parts = []
    extras = []
    research_path = path / "research.md"
    if research_path.is_file():
        research_text = research_path.read_text(encoding="utf-8")
        research_parts.append(research_text)
        extras.extend(extract_sources_from_md(research_text))
    sources_path = path / "sources.md"
    if sources_path.is_file():
        sources_text = sources_path.read_text(encoding="utf-8")
        research_parts.append(sources_text)
        extras.extend(extract_sources_from_md(sources_text))
    if extras:
        # Deduplicate while preserving order
        seen = set()
        unique_extras = []
        for s in extras:
            key = s.lower()
            if key not in seen:
                seen.add(key)
                unique_extras.append(s)
        if unique_extras:
            research_parts.append("## Sources\n" + "\n".join(f"- {s}" for s in unique_extras))
    research = "\n".join(research_parts)
    return hits(script.read_text(encoding="utf-8"), research)


def main() -> int:
    parser = argparse.ArgumentParser(description="Report unsourced claims in script WORDS.")
    parser.add_argument("packet", nargs="?", help="Packet folder. Default: every videos/* with script.md")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any hit remains.")
    args = parser.parse_args()
    if args.packet:
        folders = [Path(args.packet)]
    else:
        videos = ROOT / "videos"
        folders = sorted(p for p in videos.iterdir() if p.is_dir() and (p / "script.md").is_file())
    print("CLAIM SCAN")
    total = 0
    for folder in folders:
        found = scan_path(folder)
        total += len(found)
        if not found:
            print(f"{folder.name}: clear")
            continue
        details = []
        for kind, token, ctx in found:
            details.append(f"{kind}:{token} [{ctx}]")
        detail = "; ".join(details)
        print(f"{folder.name}: hits {detail}")
    print(f"hits: {total}")
    print("CLAIM SCAN DONE")
    if args.strict and total:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
