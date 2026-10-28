#!/usr/bin/env python3
"""Generate a local recording-session checklist consolidating key pre-VO extracts.

Pulls section timings and clean spoken text cues from script.md WORDS (at 150 wpm),
flags long sentences and numbers, highlights the CTA window, and (when idea.md
is present) includes the same-day viewer install steps. Writes a single
paste-ready recording_session_checklist.md.

No invented content. Output stays local and gitignored. Reduces recurring
human labor of opening multiple prep files before a recording session on
every future packet before a Selected VO take exists.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WPM = 150
MAX_WORDS = 22
END_SCREEN_SECONDS = 20

MECH_RE = re.compile(r"mechanism[^\n]*:\s*(.+)", re.I)
PROBLEM_RE = re.compile(r"problem:\s*(.+)", re.I)


def extract_spoken_blocks(text: str) -> list[tuple[str, str]]:
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
    return sections


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def find_numbers(text: str) -> list[str]:
    return re.findall(r"\b\d+(?:\.\d+)?%?\b", text)


def format_time(seconds: float) -> str:
    if seconds < 0:
        seconds = 0.0
    total = int(round(seconds))
    m, s = divmod(total, 60)
    return f"{m}:{s:02d}"


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


def build_viewer_steps(mech: str, problem: str, cta: str) -> list[str]:
    steps: list[str] = []
    if problem:
        steps.append(f"Name the stall in one sentence: {problem}.")
    if mech:
        steps.append(f"Write the default on a note you already see: {mech}.")
        steps.append("Place the note where your cursor or eyes already land when the stall starts.")
        steps.append("Use that note as the only next action before reopening any list.")
    if cta:
        first = re.split(r"(?<=[.!?])\s+", cta.strip())[0]
        if first and len(first.split()) <= 25:
            steps.append(first)
    return steps[:5]


def main() -> int:
    p = argparse.ArgumentParser(description="Generate recording session checklist from packet")
    p.add_argument("packet", type=Path, help="Path to packet directory")
    p.add_argument("--force", action="store_true", help="Overwrite existing recording_session_checklist.md")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    script_path = packet / "script.md"
    if not script_path.is_file():
        print("FAIL: script.md missing", file=sys.stderr)
        return 2

    out_path = packet / "recording_session_checklist.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    text = script_path.read_text(encoding="utf-8")
    blocks = extract_spoken_blocks(text)
    if not blocks:
        print("FAIL: no spoken WORDS found in script.md", file=sys.stderr)
        return 2

    # Timings and flags
    cumulative = 0.0
    section_rows: list[str] = []
    flag_count_long = 0
    flag_count_num = 0
    cta_spoken = ""
    for idx, (header, spoken) in enumerate(blocks, 1):
        wc = len(spoken.split())
        dur = (wc / WPM) * 60.0
        start = cumulative
        cumulative += dur
        section_rows.append(f"| {idx} | {header} | {wc} | {format_time(start)} | {format_time(dur)} |")

        for sent in split_sentences(spoken):
            if len(sent.split()) > MAX_WORDS:
                flag_count_long += 1
            if find_numbers(sent):
                flag_count_num += 1

        if re.search(r"cta|call.to.action|end|install|default", header, re.I):
            cta_spoken = spoken

    if not cta_spoken and blocks:
        cta_spoken = blocks[-1][1]

    total_sec = cumulative
    end_window = max(0.0, total_sec - END_SCREEN_SECONDS)

    # Optional idea.md
    mech, problem = "", ""
    idea_path = packet / "idea.md"
    if idea_path.is_file():
        mech, problem = extract_fields(idea_path.read_text(encoding="utf-8"))
    viewer_steps = build_viewer_steps(mech, problem, cta_spoken)

    lines = [
        "# Recording Session Checklist",
        "",
        "Generated locally from script.md WORDS (and idea.md when present). Estimated at 150 wpm.",
        "One-file prep before recording. Not a rewrite. Review flags and markers.",
        "",
        "## Pre-recording",
        "",
        "- [ ] Confirm quiet space and mic levels",
        "- [ ] Open this checklist + script.md side-by-side",
        f"- [ ] Estimated total: {format_time(total_sec)} ({int(round(total_sec))}s) — plan breaks around long sections",
        f"- [ ] End-screen window starts ~{format_time(end_window)} (last 20s reserved)",
        f"- [ ] Flagged sentences: {flag_count_long} long (>22 words), {flag_count_num} with numbers — mark pauses",
        "",
        "## Section overview",
        "",
        "| # | Section | Words | Start | Duration |",
        "|---|---|---|---|---|",
    ]
    lines.extend(section_rows)
    lines.append("")

    if viewer_steps:
        lines.append("## Same-day viewer install (channel promise)")
        lines.append("")
        for i, step in enumerate(viewer_steps, 1):
            lines.append(f"{i}. {step}")
        lines.append("")

    if cta_spoken:
        lines.append("## CTA highlight (for end card / final delivery)")
        lines.append("")
        lines.append(cta_spoken)
        lines.append("")

    lines.extend([
        "## Recording notes",
        "",
        "- Pause briefly after long sentences or before numbers.",
        "- Keep the calm operational voice: name the stall, name the default.",
        "- After take, compare against these markers before selecting.",
        "",
        "---",
        "Use with vo_prep.md / read_aloud_flags.md / end_screen_prep.md if needed. Estimates only.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"sections: {len(blocks)}")
    print(f"est_total: {format_time(total_sec)}")
    print(f"flags_long: {flag_count_long} flags_num: {flag_count_num}")
    print(f"viewer_steps: {len(viewer_steps)}")
    print("Recording session checklist ready (local; estimated only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
