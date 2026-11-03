#!/usr/bin/env python3
"""CTA / description-close consistency check.

Read-only. Extracts the CTA section spoken words from script.md and compares
significant words to the last non-timestamp paragraph of the Description in publish.md.
Reports overlap so future packets can surface CTA/metadata drift before upload.
Does not invent text, rewrite files, poll secrets, or extend production_readiness.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from phrase_utils import extract_sections, normalize  # noqa: E402

STOP = {
    "a", "an", "the", "to", "of", "and", "or", "for", "on", "in", "with",
    "what", "every", "stop", "deciding", "work", "morning", "your", "you",
    "this", "that", "it", "is", "are", "be", "before", "after", "write",
}

def extract_cta_spoken(script_text: str) -> str:
    sections = extract_sections(script_text)
    for sec in sections:
        title_l = sec["title"].lower()
        if "cta" in title_l or "call to action" in title_l or "close" in title_l:
            return sec["spoken"]
    if sections:
        return sections[-1]["spoken"]
    return ""

def extract_closing(publish_text: str) -> str:
    desc_m = re.search(r"^##[ \t]*Description[^\n]*\n(.*?)(?=^##|\Z)", publish_text, re.M | re.S | re.I)
    if not desc_m:
        return ""
    body = desc_m.group(1)
    # Drop timestamp chapter lines
    lines = []
    for line in body.splitlines():
        if re.match(r"^\d+:\d+", line.strip()):
            continue
        lines.append(line)
    text = "\n".join(lines)
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if paras:
        return normalize(paras[-1])
    return ""

def significant_words(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z']+", text.lower())
    return {w for w in words if len(w) > 2 and w not in STOP}

def inspect(packet: Path) -> dict:
    script_path = packet / "script.md"
    pub_path = packet / "publish.md"
    if not script_path.is_file() or not pub_path.is_file():
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "missing script.md or publish.md",
            "cta": "",
            "closing": "",
            "shared": [],
        }
    cta = extract_cta_spoken(script_path.read_text(encoding="utf-8"))
    closing = extract_closing(pub_path.read_text(encoding="utf-8"))
    if not cta or not closing:
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "could not extract CTA spoken or description closing",
            "cta": (cta[:100] + "...") if len(cta) > 100 else cta,
            "closing": (closing[:100] + "...") if len(closing) > 100 else closing,
            "shared": [],
        }
    c_words = significant_words(cta)
    cl_words = significant_words(closing)
    shared = sorted(c_words & cl_words)
    overlap_ok = bool(shared)
    issues = []
    if not overlap_ok:
        issues.append("no significant word overlap between CTA and description close")
    if len(closing.split()) > 30:
        issues.append("closing paragraph long for a tight CTA")
    warn = bool(issues)
    return {
        "ok": not warn,
        "code": "WARN" if warn else "OK",
        "detail": "; ".join(issues) if issues else "CTA shares significant words with description close",
        "cta": cta,
        "closing": closing,
        "shared": shared,
        "overlap_ok": overlap_ok,
    }

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check CTA section vs description closing text. No writes."
    )
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    rep = inspect(path)
    print(f"packet: {path.name}")
    print(f"cta_spoken: {rep.get('cta', '')[:140]}")
    print(f"closing: {rep.get('closing', '')[:140]}")
    print(f"shared_words: {', '.join(rep.get('shared') or []) or 'none'}")
    print(f"consistency: {rep['code']} ({rep['detail']})")
    print("Does not invent text, rewrite files, or poll OAuth.")
    return 0 if rep["code"] != "NO_DATA" else 2

if __name__ == "__main__":
    raise SystemExit(main())
