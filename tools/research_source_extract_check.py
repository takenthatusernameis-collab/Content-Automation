#!/usr/bin/env python3
"""Check that research.md or sources.md tables/bullets will be extracted by claim_scan.

Reports the sources that extract_sources_from_md would inject as citations.
Does not rewrite files. Helps agents confirm Primary claims / Source log tables
are header-aware and will clear both digits and hedges before script drafting.
Useful early in the research-to-script path to avoid later claim_scan failures.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from claim_scan import extract_sources_from_md  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Preview sources that claim_scan will extract from research.md / sources.md."
    )
    parser.add_argument("packet", help="Packet folder containing research.md and/or sources.md")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    files = []
    for name in ("research.md", "sources.md"):
        f = path / name
        if f.is_file():
            files.append(f)

    if not files:
        print("No research.md or sources.md found.")
        print("Generate one with: python3 tools/research_package_starter.py PATH")
        return 0

    print("RESEARCH SOURCE EXTRACT CHECK (preview of claim_scan extraction)")
    print("Header-aware Source column + Claim+Source combination is active.")
    print("=" * 60)

    total = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        extras = extract_sources_from_md(text)
        print(f"\n## {f.name}")
        if extras:
            print(f"Extracted {len(extras)} citation string(s):")
            for i, s in enumerate(extras, 1):
                preview = s[:120] + ("..." if len(s) > 120 else "")
                print(f"  {i}. {preview}")
            total += len(extras)
        else:
            print("  (no non-placeholder sources extracted)")
            print("  Tip: use a table with a Source column header, or non-placeholder bullets.")

    print("\n" + "=" * 60)
    if total:
        print(f"Total extractable citations: {total}")
        print("These will be available to claim_scan without a separate ## Sources section.")
    else:
        print("No extractable citations. Fill Source columns or bullets before drafting script.")
    print("Then run: python3 tools/claim_scan.py PATH")
    return 0


if __name__ == "__main__":
    sys.exit(main())
