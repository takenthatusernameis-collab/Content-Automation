#!/usr/bin/env python3
"""Check that key mechanism tokens appear in publish.md metadata sections.

Extracts the named mechanism from idea.md, derives key tokens, and reports
whether those tokens appear in the Title, Description, End screen / CTA,
and First comment sections of publish.md. Reduces recurring labor of
manually verifying metadata coherence before the human OAuth step and
execute dispatch on every future packet. Does not invent text, rewrite
files, poll secrets, or call external services. Exit 0 always;
informational only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

try:
    from idea_utils import extract as idea_extract  # type: ignore
except Exception:
    idea_extract = None  # type: ignore


def extract_field(text: str, key: str) -> str:
    m = re.search(rf"^-?\s*{re.escape(key)}:\s*(.+)$", text, re.M | re.I)
    return m.group(1).strip() if m else ""


def section(text: str, heading: str) -> str:
    parts = re.split(rf"^##\s+{re.escape(heading)}\s*$", text, maxsplit=1, flags=re.M | re.I)
    if len(parts) < 2:
        return ""
    rest = re.split(r"^##\s+", parts[1], maxsplit=1, flags=re.M)[0]
    return rest.strip()


def mechanism_tokens(mech: str) -> list[str]:
    stop = {"the", "a", "an", "of", "to", "and", "or", "for", "in", "on", "with", "that", "this"}
    words = re.findall(r"\b\w{4,}\b", mech.lower())
    return [w for w in words if w not in stop][:5]


def present(text: str, tokens: list[str]) -> bool:
    low = text.lower()
    return any(tok in low for tok in tokens)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check mechanism token presence in publish.md metadata sections. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("METADATA MECHANISM CONSISTENCY (informational only; no writes)")
    print(f"Packet: {path.name}")
    print()

    idea = path / "idea.md"
    mechanism = ""
    if idea.is_file() and idea_extract is not None:
        mechanism, _, _ = idea_extract(idea.read_text(encoding="utf-8"))
    elif idea.is_file():
        mechanism = extract_field(idea.read_text(encoding="utf-8"), "mechanism")
    print(f"Named mechanism: {mechanism or '(missing from idea.md)'}")
    if not mechanism:
        print("No mechanism to check.")
        print("This tool writes nothing.")
        return 0

    tokens = mechanism_tokens(mechanism)
    print(f"Key tokens: {', '.join(tokens) or '(none extracted)'}")
    print()

    publish = path / "publish.md"
    if not publish.is_file():
        print("No publish.md found.")
        print("This tool writes nothing.")
        return 0

    ptext = publish.read_text(encoding="utf-8")
    # Title may also live in titles.md
    titles = path / "titles.md"
    title_text = ""
    if titles.is_file():
        title_text = extract_field(titles.read_text(encoding="utf-8"), "title") or extract_field(titles.read_text(encoding="utf-8"), "primary")
    if not title_text:
        title_text = section(ptext, "Title") or extract_field(ptext, "title")

    desc = section(ptext, "Description") or section(ptext, "description")
    end = section(ptext, "End screen") or section(ptext, "End Screen") or section(ptext, "CTA") or section(ptext, "Call to action")
    first = section(ptext, "First comment") or section(ptext, "First Comment") or section(ptext, "Pin")

    checks = [
        ("Title", title_text),
        ("Description", desc),
        ("End screen / CTA", end),
        ("First comment", first),
    ]

    any_present = False
    for name, body in checks:
        ok = present(body, tokens) if body else False
        any_present = any_present or ok
        status = "yes" if ok else ("empty" if not body else "no")
        print(f"{name}: {status}")
        if body and not ok:
            print(f"  preview: {body[:80].replace(chr(10), ' ')}...")

    print()
    if any_present:
        print("Result: mechanism tokens appear in at least one metadata section.")
    else:
        print("Result: mechanism tokens not detected in title/description/end-screen/first-comment. Consider aligning before dispatch.")
    print()
    print("This check is a starting point. It does not rewrite publish.md.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
