#!/usr/bin/env python3
"""Generate a grounded research verification checklist for a packet.

Reads idea.md and research.md (if present). Prints a concrete checklist
of verification steps for any sources or claims. Extracts potential quantitative
items (digit tokens in non-heading content) from the files for targeted review.
Does not invent sources, URLs, numbers, or citations. Optionally writes a sources.md skeleton if --write-skeleton is given and the file is absent.
Also prints suggested search queries grounded in the extracted claim excerpts (human use only).
Queries for statistical or research-like claims automatically append primary-source site operators (site:gov OR site:edu OR site:org).
When sources.md is present, classifies and ranks source candidates by type (primary / secondary / unknown) using domain and keyword heuristics. Prints type counts and warns if secondary dominate. No invented sources.

Reduces recurring human verification minutes by standardizing the process,
listing specific items that may need sourcing, surfacing ready-to-paste search queries, and ranking existing sources by preference.
Use before claim_scan and before promoting research.md from stub.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

try:
    from idea_utils import extract as idea_extract
except ImportError:
    def idea_extract(text: str):
        return "", "", ""


def extract_potential_claims(text: str, source_label: str) -> list[str]:
    """Return lines with digit tokens that are not obvious headings/timestamps."""
    claims = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        # Skip pure headings and common structural lines
        if stripped.startswith("#") or stripped.startswith("<!--") or re.match(r"^(Hook|Beat)\s+\d", stripped, re.I):
            continue
        if re.search(r"\(0:\d+–0:\d+\)", stripped) or re.search(r"Beat\s+\d+\s+—", stripped):
            continue
        if re.search(r"\b\d+(?:[.,]\d+)?%?", stripped):
            # Truncate
            display = stripped if len(stripped) <= 140 else stripped[:137] + "..."
            claims.append(f"({source_label}) {display}")
    return claims[:12]

def suggested_search_queries(claims: list[str]) -> list[str]:
    """Grounded search queries from claim excerpts. No invented sources or URLs.
    Appends primary-source preference operators when the claim looks statistical or research-like.
    """
    queries = []
    seen = set()
    primary_keywords = re.compile(r"\b(%|percent|percentage|study|studies|research|survey|data|statistic|average|median)\b", re.I)
    for item in claims[:8]:
        excerpt = item.split(") ", 1)[-1] if ") " in item else item
        # Clean for search: drop leading parenthetical label already handled, keep first ~8 words
        clean = re.sub(r"[^a-zA-Z0-9 %.,]", " ", excerpt)
        clean = re.sub(r"\s+", " ", clean).strip()
        words = clean.split()[:8]
        if len(words) < 3:
            continue
        query = " ".join(words)
        if query.lower() in seen:
            continue
        seen.add(query.lower())
        # Prefer primary sources for quantitative/research claims
        if primary_keywords.search(excerpt):
            query += " site:gov OR site:edu OR site:org"
        queries.append(query)
    return queries

def classify_source(url_or_text: str) -> str:
    """Heuristic classification of a source candidate. No invented sources.
    Returns: primary / primary-likely / secondary / unknown.
    """
    text = (url_or_text or "").lower()
    if not text.strip():
        return "unknown"
    primary_domains = (
        ".gov", ".edu", ".mil", "arxiv.org", "pubmed", "nih.gov", "who.int",
        "oecd.org", "worldbank.org", "imf.org", "nature.com", "science.org",
        "ieee.org", "acm.org", "ssrn.com"
    )
    secondary_hints = (
        "wikipedia.org", "reddit.com", "youtube.com", "medium.com", "blogspot",
        "wordpress", "substack", "news", "blog", "article", "opinion"
    )
    if any(d in text for d in primary_domains):
        return "primary"
    if any(h in text for h in secondary_hints):
        return "secondary"
    if any(k in text for k in ("study", "report", "paper", "survey", "data", "official", "government", "university")):
        return "primary-likely"
    return "unknown"

def extract_source_candidates(sources_text: str) -> list[str]:
    """Pull potential source lines (URLs or non-empty Source cells). No invention."""
    candidates = []
    for line in sources_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("|---"):
            continue
        # URL anywhere
        if "http://" in stripped or "https://" in stripped:
            candidates.append(stripped)
            continue
        # Table row with possible source
        if stripped.startswith("|") and "|" in stripped[1:]:
            parts = [p.strip() for p in stripped.split("|")]
            # Prefer later columns as Source
            for part in parts[2:]:
                if part and part.lower() not in ("", "source (fill)", "notes"):
                    candidates.append(part)
                    break
    # Dedup preserve order
    seen = set()
    out = []
    for c in candidates:
        key = c.lower()[:120]
        if key not in seen:
            seen.add(key)
            out.append(c)
    return out[:12]

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a research verification checklist grounded in the packet (no invented sources)."
    )
    parser.add_argument("packet", help="Packet folder")
    parser.add_argument(
        "--write-skeleton",
        action="store_true",
        help="If sources.md is absent, write a fillable skeleton with the claim table (no invented sources). Safe: never overwrites.",
    )
    args = parser.parse_args()
    packet = Path(args.packet)
    idea_path = packet / "idea.md"
    research_path = packet / "research.md"
    script_path = packet / "script.md"
    draft_path = packet / "draft.md"

    if not idea_path.is_file():
        print(f"No idea.md in {packet}")
        return 1

    idea_text = idea_path.read_text(encoding="utf-8", errors="replace")
    mech, problem, topic = idea_extract(idea_text)
    mech = mech or "unspecified mechanism"
    problem = problem or "unspecified problem"
    topic = topic or "unspecified topic"

    has_research = research_path.is_file()
    research_status = "present" if has_research else "absent"
    research_text = research_path.read_text(encoding="utf-8", errors="replace") if has_research else ""

    print("RESEARCH VERIFICATION CHECKLIST")
    print(f"Packet: {packet}")
    print(f"Topic: {topic}")
    print(f"Mechanism: {mech}")
    print(f"Problem: {problem}")
    print(f"research.md: {research_status}")
    print("=" * 60)
    print()
    print("Standard verification steps (do not invent sources):")
    print("1. Confirm every number or percentage in spoken WORDS (script.md / draft.md) has a matching source line in research.md or sources.md.")
    print("2. For each source URL or citation, open it and confirm it supports the exact claim (not just related).")
    print("3. Prefer primary sources or operational claims the viewer can test this week over secondary summaries.")
    print("4. Remove or qualitative-ize any unsourced statistic before apply_script --write.")
    print("5. Run after updates:")
    print(f"   python3 tools/claim_scan.py {packet}")
    print(f"   python3 tools/research_brief.py {packet}")
    print("6. Tick 'No unsourced statistics' in qa.md only after human read of the sources.")
    print()
    print("Packet-specific notes:")
    print(f"- Mechanism '{mech}' should be demonstrated with concrete scenes, not studies, unless a source is already present.")
    print(f"- Problem '{problem}' is the stall to show; keep claims operational.")
    if has_research:
        print("- research.md exists; review its Sources and Facts sections against the checklist above.")
    else:
        print("- No research.md yet. Use python3 tools/research_sources_starter.py to generate a template, then fill and verify.")
    print()

    # Targeted extraction
    potential = []
    if has_research:
        potential.extend(extract_potential_claims(research_text, "research.md"))
    potential.extend(extract_potential_claims(idea_text, "idea.md"))
    for pth in (script_path, draft_path):
        if pth.is_file():
            txt = pth.read_text(encoding="utf-8", errors="replace")
            potential.extend(extract_potential_claims(txt, pth.name))

    if potential:
        print("Potential quantitative items found (verify each or qualitative-ize):")
        for i, item in enumerate(potential, 1):
            print(f"  {i}. {item}")
        print()
        print("These are non-heading lines containing digits. Confirm sources exist or remove the numbers.")
        print()
        print("Fillable claim-to-source table (paste into sources.md / research.md; fill only Source):")
        print("| Claim excerpt | Source (fill) | Notes |")
        print("|---------------|---------------|-------|")
        for item in potential[:8]:  # limit for readability
            excerpt = item.split(") ", 1)[-1] if ") " in item else item
            excerpt = excerpt[:80].replace("|", "/") + ("..." if len(excerpt) > 80 else "")
            print(f"| {excerpt} |  |  |")
        print()
        print("For spoken WORDS claims specifically, also run: python3 tools/claim_source_table.py PATH")
        queries = suggested_search_queries(potential)
        if queries:
            print()
            print("Suggested search queries (human use only; paste into search engine; no invented sources):")
            print("  Queries for statistical/research-like claims include site:gov OR site:edu OR site:org preference.")
            for q in queries:
                print(f"  - {q}")
            print("Prefer primary sources (site:edu, site:gov, official reports) or operational claims the viewer can test.")
    else:
        print("No non-heading digit tokens found in idea.md / research.md / script.md / draft.md.")
        print("Keep it that way, or cite before adding any number to spoken WORDS.")
    print()
    # Cross-check against sources.md if present (reduces linking labor)
    sources_path = packet / "sources.md"
    if sources_path.is_file():
        sources_text = sources_path.read_text(encoding="utf-8", errors="replace")
        sources_lower = sources_text.lower()
        linked = []
        unlinked = []
        for item in potential:
            excerpt = item.split(") ", 1)[-1] if ") " in item else item
            key = excerpt[:60].lower().strip()
            if key and key in sources_lower:
                linked.append(item)
            else:
                unlinked.append(item)
        print(f"sources.md present. Linked (excerpt found): {len(linked)} / {len(potential)}")
        if unlinked:
            print("Unlinked potential items (add source or qualitative-ize):")
            for u in unlinked[:6]:
                print(f"  - {u}")
        else:
            print("All extracted potential items appear referenced in sources.md (still verify content).")
        # New: classify and rank source candidates
        candidates = extract_source_candidates(sources_text)
        if candidates:
            ranked = []
            for c in candidates:
                kind = classify_source(c)
                ranked.append((kind, c))
            # Prefer primary first
            order = {"primary": 0, "primary-likely": 1, "unknown": 2, "secondary": 3}
            ranked.sort(key=lambda x: order.get(x[0], 9))
            print()
            print("Source candidates ranked by type (primary preferred; heuristic only; human must still verify):")
            counts = {"primary": 0, "primary-likely": 0, "unknown": 0, "secondary": 0}
            for kind, c in ranked:
                counts[kind] = counts.get(kind, 0) + 1
                display = c if len(c) <= 100 else c[:97] + "..."
                print(f"  [{kind}] {display}")
            print(f"Type summary: primary={counts['primary']} primary-likely={counts['primary-likely']} secondary={counts['secondary']} unknown={counts['unknown']}")
            if counts["secondary"] > counts["primary"] + counts["primary-likely"]:
                print("WARNING: More secondary than primary/primary-likely candidates. Prefer replacing secondary with primary sources where possible.")
            print("Prefer primary / primary-likely. Secondary or unknown still require human confirmation of exact support.")
        else:
            print("No extractable source candidates found in sources.md (URLs or filled Source cells).")
    else:
        print("No sources.md yet. Paste the table above into a new sources.md, then fill the Source column.")
        print("Or run: python3 tools/claim_source_table.py PATH for a spoken-WORDS-focused table.")
        if args.write_skeleton and potential:
            skeleton_lines = [
                "# sources.md",
                "",
                "Fillable claim-to-source table generated by research_verification_checklist.py --write-skeleton.",
                "Do not invent sources. Fill only the Source column with verifiable citations, then re-run the checklist.",
                "",
                "| Claim excerpt | Source (fill) | Notes |",
                "|---------------|---------------|-------|",
            ]
            for item in potential[:8]:
                excerpt = item.split(") ", 1)[-1] if ") " in item else item
                excerpt = excerpt[:80].replace("|", "/") + ("..." if len(excerpt) > 80 else "")
                skeleton_lines.append(f"| {excerpt} |  |  |")
            skeleton_lines.append("")
            skeleton_lines.append("Next: fill Source column, then python3 tools/claim_scan.py PATH")
            sources_path.write_text("\n".join(skeleton_lines) + "\n", encoding="utf-8")
            print(f"Wrote sources.md skeleton ({len(potential[:8])} rows). Review and fill sources. Never overwrites existing files.")
        elif args.write_skeleton:
            print("--write-skeleton requested but no potential claims found; no file written.")
    print()
    print("This checklist standardizes verification, surfaces linking status, and ranks source candidates so future packets spend fewer human minutes on source checking.")
    print("Do not treat this output as verified sources. Human confirmation is still required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
