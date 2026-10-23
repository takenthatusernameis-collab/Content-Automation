#!/usr/bin/env python3
"""Report weak, generic, or engagement-bait end-screen / final CTA text.

Scans ## End screen or ## CTA section in publish.md (or last part of Description).
Does not rewrite files. A hit is a revision signal.
Default exit is 0 so a clear packet cannot fail the build.
--strict exits 1 when any hit remains.

Checks: presence, placeholder, high-precision engagement-bait / generic CTA patterns.
Output includes short context so the revision signal is immediately actionable.
Uses shared phrase_utils.END_SCREEN_WEAK_PATTERNS, normalize, and context_snippet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import END_SCREEN_WEAK_PATTERNS, context_snippet, normalize  # noqa: E402

# High-precision weak / engagement-bait patterns live in phrase_utils.END_SCREEN_WEAK_PATTERNS.
# Matching uses word boundaries. Text is normalized so one straight entry covers variants.
_WEAK_RES = tuple(
    re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE) for phrase in END_SCREEN_WEAK_PATTERNS
)

END_RE = re.compile(r"## (?:End screen|End Screen|CTA|Call to action|Final CTA)\s*\n(.*?)(?=\n## |\Z)", re.S)


def end_text(text: str) -> str:
    m = END_RE.search(text.replace("\r\n", "\n"))
    return m.group(1).strip() if m else ""


def hits(text: str) -> list[tuple[str, str, str]]:
    body = normalize(end_text(text))
    if not body:
        return [("missing", "no end-screen/CTA section", "")]
    found = []
    if len(body) < 10 or "(add" in body.lower() or body.lower() in ("cta", "end screen", "tbd"):
        found.append(("placeholder", body[:60], body[:60]))
    for phrase, cre in zip(END_SCREEN_WEAK_PATTERNS, _WEAK_RES):
        m = cre.search(body)
        if m:
            ctx = context_snippet(body, m, max_len=80)
            found.append(("weak", phrase, ctx))
    return found


def scan_path(path: Path) -> list[tuple[str, str, str]]:
    pub = path / "publish.md"
    if pub.is_file():
        return hits(pub.read_text(encoding="utf-8"))
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Report end-screen / CTA quality issues.")
    parser.add_argument("packet", nargs="?", help="Packet folder. Default: every videos/* with publish.md")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any hit remains.")
    args = parser.parse_args()
    if args.packet:
        folders = [Path(args.packet)]
    else:
        videos = ROOT / "videos"
        folders = sorted(
            p for p in videos.iterdir()
            if p.is_dir() and (p / "publish.md").is_file()
        )
    print("END SCREEN / CTA SCAN")
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
    print("rewrites: 0")
    if args.strict and total:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
