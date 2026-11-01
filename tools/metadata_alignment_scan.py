#!/usr/bin/env python3
"""Scan local metadata options for alignment with the canonical assignment source.

Reads the primary assignment statement from assignment_source.md (via shared
assignment_utils.read_primary) when present. Then inspects title_options.md,
description_options.md, thumbnail_options.md, first_comment_options.md,
end_screen_options.md, and tags_options.md (if they exist) and reports whether
candidates appear to prefer or contain key terms from the primary.

Does not write files, invent content, or rewrite options. Pure inspection
to reduce future review labor and detect drift after human edits or older
generation. Aligns with no-invent rule and mechanism consistency goals.

Exit 0 always (informational); use for human or agent review before final
selection into publish.md.

Run 956: extended to cover first_comment, end_screen, and tags options for fuller coverage.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from assignment_utils import read_primary  # noqa: E402
from phrase_utils import shorten  # noqa: E402


def extract_key_terms(primary: str) -> list[str]:
    """Extract a few short distinctive terms from the primary for matching.
    Prefers whole words longer than 3 letters, lowercased, excluding stop words.
    """
    stops = {"the", "a", "an", "so", "stops", "reopening", "the", "list", "install", "with", "for"}
    words = re.findall(r"\b[a-zA-Z']{4,}\b", primary.lower())
    terms = [w for w in words if w not in stops][:4]
    return terms or [shorten(primary, 20).lower()]


def scan_options_file(path: Path, terms: list[str]) -> tuple[int, int, list[str]]:
    """Return (candidate_count, aligned_count, sample_misaligned)."""
    if not path.is_file():
        return 0, 0, []
    text = path.read_text(encoding="utf-8")
    # Simple candidate detection: numbered lines under ## Candidates or similar
    candidates = []
    in_cands = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## Candidates") or stripped.startswith("## Options") or "candidates" in stripped.lower() and stripped.startswith("##"):
            in_cands = True
            continue
        if in_cands and stripped.startswith("##"):
            break
        if in_cands and re.match(r"^\d+\.\s+", stripped):
            candidates.append(stripped)
    if not candidates:
        # fallback: any numbered lines
        candidates = [line.strip() for line in text.splitlines() if re.match(r"^\d+\.\s+", line.strip())]
    aligned = 0
    mis = []
    for cand in candidates:
        lower = cand.lower()
        if any(term in lower for term in terms):
            aligned += 1
        else:
            if len(mis) < 2:
                mis.append(cand[:80])
    return len(candidates), aligned, mis


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan local title/description/thumbnail/first-comment/end-screen/tags options for alignment with assignment primary"
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"FAIL: not a directory: {packet}", file=sys.stderr)
        return 1

    primary = read_primary(packet)
    if not primary:
        print("INFO: no assignment_source.md primary found. Run tools/assignment_source_writer.py first for stronger alignment checks.")
        print("Scan skipped (no canonical source).")
        return 0

    terms = extract_key_terms(primary)
    print(f"Primary: {primary}")
    print(f"Key terms for match: {terms}")

    files = [
        ("title_options.md", packet / "title_options.md"),
        ("description_options.md", packet / "description_options.md"),
        ("thumbnail_options.md", packet / "thumbnail_options.md"),
        ("first_comment_options.md", packet / "first_comment_options.md"),
        ("end_screen_options.md", packet / "end_screen_options.md"),
        ("tags_options.md", packet / "tags_options.md"),
    ]
    any_found = False
    for name, path in files:
        count, aligned, mis = scan_options_file(path, terms)
        if count == 0:
            print(f"{name}: not present or no candidates detected")
            continue
        any_found = True
        pct = int(100 * aligned / count) if count else 0
        status = "ALIGNED" if pct >= 70 else "DRIFT" if pct < 40 else "PARTIAL"
        print(f"{name}: {aligned}/{count} candidates contain key terms ({pct}%) [{status}]")
        if mis and status != "ALIGNED":
            print(f"  sample less-aligned: {mis[0]}")

    if not any_found:
        print("No options files with candidates found. Generate with the *options_writer.py tools after assignment_source_writer.py.")
    else:
        print("Alignment scan complete (informational; no files written). Prefer high alignment before selecting into publish.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
