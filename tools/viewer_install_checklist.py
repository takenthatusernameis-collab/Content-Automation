#!/usr/bin/env python3
"""Generate a local same-day viewer install checklist from idea.md + script CTA.

Extracts the mechanism and problem from idea.md, the CTA spoken text from
script.md WORDS (if present), and writes viewer_install_checklist.md with
3-5 concrete operational steps the viewer can do the same day.

Aligns with the channel promise: after each video the viewer can install
one small default. No invented mechanisms or claims. Output stays local
and gitignored. Reduces recurring human labor of rephrasing the core
action into a paste-ready checklist for description, comment, or end card
on every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MECH_RE = re.compile(r"mechanism[^\n]*:\s*(.+)", re.I)
PROBLEM_RE = re.compile(r"problem:\s*(.+)", re.I)


def extract_fields(idea_text: str) -> tuple[str, str]:
    mech = ""
    problem = ""
    for line in idea_text.splitlines():
        m = MECH_RE.search(line)
        if m:
            mech = m.group(1).strip().rstrip(".")
        p = PROBLEM_RE.search(line)
        if p:
            problem = p.group(1).strip().rstrip(".")
    return mech, problem


def extract_cta_spoken(text: str) -> str:
    """Return spoken WORDS from the first CTA-like section, or last section."""
    sections: list[tuple[str, str]] = []
    pattern = re.compile(r"^##\s+(.+?)\s*$", re.M)
    matches = list(pattern.finditer(text))
    for i, m in enumerate(matches):
        header = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        wm = re.search(r"WORDS:\s*(.*?)(?:\nVISUAL:|\n##|\Z)", block, re.S | re.I)
        if wm:
            spoken = re.sub(r"\s+", " ", wm.group(1).strip())
            if spoken:
                sections.append((header, spoken))
    if not sections:
        return ""
    for header, spoken in sections:
        if re.search(r"cta|call.to.action|end|install|default", header, re.I):
            return spoken
    return sections[-1][1]


def build_checklist(mech: str, problem: str, cta: str) -> list[str]:
    """Return 3-5 operational steps grounded in the extracted fields."""
    steps: list[str] = []
    if problem:
        steps.append(f"Name the stall in one sentence: {problem}.")
    if mech:
        steps.append(f"Write the default on a note you already see: {mech}.")
        steps.append("Place the note where your cursor or eyes already land when the stall starts.")
        steps.append("Use that note as the only next action before reopening any list.")
    else:
        steps.append("Write one concrete next action before the next decision.")
    if cta:
        first = re.split(r"(?<=[.!?])\s+", cta.strip())[0]
        if first and len(first.split()) <= 25 and first.lower() not in " ".join(steps).lower():
            steps.append(first)
    return steps[:5]


def main() -> int:
    p = argparse.ArgumentParser(description="Generate viewer install checklist from packet")
    p.add_argument("packet", type=Path, help="Path to packet directory")
    p.add_argument("--force", action="store_true", help="Overwrite existing viewer_install_checklist.md")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print("FAIL: idea.md missing", file=sys.stderr)
        return 2

    out_path = packet / "viewer_install_checklist.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem = extract_fields(idea_text)

    cta = ""
    script_path = packet / "script.md"
    if script_path.is_file():
        cta = extract_cta_spoken(script_path.read_text(encoding="utf-8"))

    steps = build_checklist(mech, problem, cta)
    if not steps:
        print("FAIL: no usable mechanism or problem found", file=sys.stderr)
        return 2

    lines = [
        "# Viewer Install Checklist",
        "",
        "Generated locally from idea.md mechanism/problem and script.md CTA spoken text.",
        "Channel promise: one small default the viewer can install the same day.",
        "Not a rewrite. Review and paste into description, pinned comment, or end card.",
        "",
        f"mechanism: {mech or '(none)'}",
        f"problem: {problem or '(none)'}",
        "",
        "## Same-day steps",
        "",
    ]
    for i, step in enumerate(steps, 1):
        lines.append(f"{i}. {step}")
    lines.extend([
        "",
        "---",
        "Use these as the concrete actions. Do not invent additional defaults.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"steps: {len(steps)}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print("Viewer install checklist ready (local; estimated from packet fields only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
