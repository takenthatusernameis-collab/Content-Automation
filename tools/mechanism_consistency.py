#!/usr/bin/env python3
"""Check that the named mechanism from idea.md appears in the hook and CTA of the script.

Extracts the mechanism field and searches for key tokens in the first ~40 spoken words
of the Hook section and the CTA section. Reports presence/absence. Reduces recurring
labor of manually verifying that the mechanism is named early and late before final
review or upload on every future packet. Does not invent text, rewrite files, poll
secrets, or call external services. Exit 0 always; informational only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

try:
    from phrase_utils import spoken_words  # type: ignore
except Exception:
    spoken_words = None  # type: ignore


def extract_field(text: str, key: str) -> str:
    m = re.search(rf"^-?\s*{re.escape(key)}:\s*(.+)$", text, re.M | re.I)
    return m.group(1).strip() if m else ""


def section(text: str, heading: str) -> str:
    parts = re.split(rf"^##\s+{re.escape(heading)}\s*$", text, maxsplit=1, flags=re.M)
    if len(parts) < 2:
        return ""
    rest = re.split(r"^##\s+", parts[1], maxsplit=1, flags=re.M)[0]
    return rest.strip()


def first_spoken(text: str, n: int = 40) -> str:
    if spoken_words is not None:
        cleaned = spoken_words(text)
    else:
        cleaned = re.sub(r"[^\w\s'-]", " ", text)
    return " ".join(cleaned.split()[:n]).lower()


def mechanism_tokens(mech: str) -> list[str]:
    # Keep words longer than 3 chars, drop common stopwords
    stop = {"the", "a", "an", "of", "to", "and", "or", "for", "in", "on", "with", "that", "this"}
    words = re.findall(r"\b\w{4,}\b", mech.lower())
    return [w for w in words if w not in stop][:5]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check mechanism presence in hook and CTA. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("MECHANISM CONSISTENCY CHECK (informational only; no writes)")
    print(f"Packet: {path.name}")
    print()

    idea = path / "idea.md"
    mechanism = ""
    if idea.is_file():
        mechanism = extract_field(idea.read_text(encoding="utf-8"), "mechanism")
    print(f"Named mechanism: {mechanism or '(missing from idea.md)'}")
    if not mechanism:
        print("No mechanism to check.")
        print("This tool writes nothing.")
        return 0

    tokens = mechanism_tokens(mechanism)
    print(f"Key tokens: {', '.join(tokens) or '(none extracted)'}")
    print()

    script = path / "script.md"
    if not script.is_file():
        script = path / "draft.md"
    if not script.is_file():
        print("No script.md or draft.md found.")
        print("This tool writes nothing.")
        return 0

    stext = script.read_text(encoding="utf-8")
    hook = section(stext, "Hook") or section(stext, "hook")
    cta = section(stext, "CTA") or section(stext, "cta") or section(stext, "Call to action")

    hook_text = first_spoken(hook) if hook else ""
    cta_text = first_spoken(cta, 60) if cta else ""

    def present(text: str) -> bool:
        return any(tok in text for tok in tokens)

    hook_ok = present(hook_text)
    cta_ok = present(cta_text)

    print(f"Hook (early words): {hook_text[:120] or '(empty)'}")
    print(f"  Mechanism tokens present: {'yes' if hook_ok else 'no'}")
    print(f"CTA (early words): {cta_text[:120] or '(empty)'}")
    print(f"  Mechanism tokens present: {'yes' if cta_ok else 'no'}")
    print()
    if hook_ok and cta_ok:
        print("Result: mechanism named in both early hook and CTA (good).")
    else:
        print("Result: mechanism not clearly named in both places. Consider tightening before final review.")
    print()
    print("This check is a starting point. It does not rewrite the script.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
