#!/usr/bin/env python3
"""Apply a human-pasted script.md body to a non-fixture packet.

Does not invent WORDS. Does not expand the sample fixture. Does not bump
packet status. A dry-run is the default so a bad paste cannot land.
Missing --from paths exit 2 with a draft.md hint instead of a traceback.

Run 091: dry-run also prints idea-lock INFO (mechanism / topic tokens
from idea.md vs incoming draft). INFO never blocks write. A missing
lock is not apply --write and is not a status bump.
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

from caption_brief import WPM, fmt_ts, script_cues  # noqa: E402
from validate_packet import FORMAT_SPOKEN_WORDS, duration_note, field  # noqa: E402
from phrase_utils import ANTI_SLOP_PATTERNS  # noqa: E402

FIXTURE_PREFIX = "sample-001"
PROMPT_MARKERS = (
    "script expand prompt (assembled, not a draft)",
    "fixture lock:",
    "you are expanding an existing youtube explainer script",
    "## beat budget (size hint only)",
    "## writer contract (follow)",
)
BLANK_LOCK = {
    "",
    "(blank)",
    "template-default",
    "generic",
    "tbd",
    "todo",
    "none published yet",
}


def headings(text: str) -> list[str]:
    return [m.strip() for m in re.findall(r"^##\s+(.+)$", text, re.M)]


def heading_key(label: str) -> str:
    low = label.lower().strip()
    if low.startswith("hook"):
        return "hook"
    if "payoff" in low:
        return "payoff"
    m = re.match(r"beat\s+(\d+)", low)
    if m:
        return f"beat-{m.group(1)}"
    if low.startswith("cta"):
        return "cta"
    return f"other:{low}"


def looks_like_expand_prompt(text: str) -> bool:
    low = text.lower()
    return any(m in low for m in PROMPT_MARKERS)


def extract_script(text: str) -> str:
    """Take a pasted body; strip a wrapping fence if the model added one."""
    raw = text.replace("\r\n", "\n").strip()
    fence = re.search(r"```(?:markdown|md)?\n(# Script\b.*?)```", raw, re.S)
    if fence:
        return fence.group(1).strip() + "\n"
    if raw.startswith("# Script"):
        return raw + ("\n" if not raw.endswith("\n") else "")
    if re.search(r"^##\s+Hook", raw, re.M):
        return "# Script\n\nSpoken words only under each beat. Visual notes in italics.\n\n" + raw + (
            "\n" if not raw.endswith("\n") else ""
        )
    return raw + ("\n" if raw and not raw.endswith("\n") else "")


def spoken_total(script: str) -> int:
    return sum(int(c["words"]) for c in script_cues(script))


def is_fixture(packet: Path) -> bool:
    return packet.name.startswith(FIXTURE_PREFIX)


def missing_source_error(source: Path) -> str:
    """Read-only message when --from points at a file that is not on disk."""
    return (
        f"missing source file: {source}\n"
        "Save the off-repo expand draft to this path first (usually PATH/draft.md).\n"
        "draft.md is not script.md. Dry-run apply after that file exists.\n"
        "This command writes nothing."
    )


def idea_lock_notes(packet: Path, incoming: str) -> list[str]:
    """Non-blocking INFO comparing idea.md mechanism/topic to incoming draft."""
    notes = []
    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        return ["INFO idea lock: no idea.md"]
    idea_text = idea_path.read_text(encoding="utf-8", errors="replace")
    try:
        from idea_utils import extract as idea_extract
        mech, problem, topic = idea_extract(idea_text)
    except Exception:
        return ["INFO idea lock: extract failed"]
    body = incoming.lower()
    if mech and mech.lower() not in BLANK_LOCK:
        if mech.lower()[:30] in body or any(w in body for w in mech.lower().split()[:2] if len(w) > 3):
            notes.append("INFO idea lock: mechanism tokens present in incoming draft")
        else:
            notes.append("INFO idea lock miss: mechanism phrase not visible in incoming draft (does not block --write)")
    if topic and topic.lower() not in BLANK_LOCK:
        if topic.lower()[:20] in body or any(w in body for w in topic.lower().split()[:2] if len(w) > 3):
            notes.append("INFO idea lock: topic tokens present in incoming draft")
        else:
            notes.append("INFO idea lock miss: topic phrase not visible in incoming draft (does not block --write)")
    return notes or ["INFO idea lock: checked"]


def anti_slop_notes(incoming: str) -> list[str]:
    """Non-blocking INFO for common weak phrases in spoken text. Never blocks write."""
    if not incoming:
        return []
    body = incoming.lower()
    hits = []
    for pattern in ANTI_SLOP_PATTERNS:
        if pattern.lower() in body:
            hits.append(pattern)
            if len(hits) >= 5:
                break
    if not hits:
        return ["INFO anti-slop: no common weak phrases detected in incoming draft"]
    notes = ["INFO anti-slop hits (does not block --write; consider tightening):"]
    for h in hits:
        notes.append(f"  - {h}")
    return notes


def originality_notes(packet: Path, incoming: str) -> list[str]:
    """Non-blocking INFO pointer to originality checklist + basic mechanism presence + concrete markers & lived-experience flags + sentence density + problem echo. Never blocks write."""
    notes = ["INFO originality: run python3 tools/originality_checklist.py on draft.md for the full 7-item review before promotion"]
    idea_path = packet / "idea.md"
    body_lower = incoming.lower()
    mech = ""
    problem = ""
    if idea_path.is_file():
        idea_text = idea_path.read_text(encoding="utf-8", errors="replace")
        try:
            from idea_utils import extract as idea_extract
            mech, problem, _ = idea_extract(idea_text)
            if mech and mech.lower() not in ("", "(blank)", "template-default", "generic", "tbd", "todo"):
                if mech.lower()[:40] in body_lower or any(w in body_lower for w in mech.lower().split()[:3] if len(w) > 4):
                    notes.append("INFO originality: mechanism token appears present in incoming draft")
                else:
                    notes.append("INFO originality: mechanism phrase not clearly visible in incoming draft (review with checklist)")
            else:
                notes.append("INFO originality: idea.md mechanism missing or blank — fix before deep review")
        except Exception:
            notes.append("INFO originality: could not extract mechanism for basic check")
    else:
        notes.append("INFO originality: no idea.md for mechanism check")
    # Concrete markers (mirroring originality_report.py patterns)
    concrete_patterns = [
        r"\b(write|put|open|start|send|record|reply|close|hide|cover|rewrite|pick|name)\b",
        r"\b(verb|sentence|card|surface|file|folder|list|board|planner)\b",
    ]
    hits = sum(len(re.findall(p, incoming, re.IGNORECASE)) for p in concrete_patterns)
    if hits >= 8:
        notes.append(f"INFO originality deeper: strong concrete markers ({hits})")
    elif hits >= 4:
        notes.append(f"INFO originality deeper: moderate concrete markers ({hits})")
    else:
        notes.append(f"INFO originality deeper: weak concrete markers ({hits}) — consider adding specific verbs/objects")
    # Lived-experience flags
    fake = re.findall(r"\b(i tried|i tested|my clients|users reported|in my experience)\b", incoming, re.IGNORECASE)
    if not fake:
        notes.append("INFO originality deeper: no lived-experience claims detected")
    else:
        notes.append(f"INFO originality deeper: review {len(fake)} potential lived-experience claims")
    # Sentence density / cuttable signal (from originality_report #5)
    sentences = [s.strip() for s in re.split(r"[.!?]", incoming) if s.strip()]
    if len(sentences) > 40:
        notes.append(f"INFO originality deeper: long draft ({len(sentences)} sentences) — look for repeated conclusions")
    else:
        notes.append(f"INFO originality deeper: compact draft ({len(sentences)} sentences)")
    # Problem language echo (from originality_report #4)
    if problem and any(w in body_lower for w in problem.lower().split() if len(w) > 4):
        notes.append("INFO originality deeper: problem language echoed in draft")
    elif problem:
        notes.append("INFO originality deeper: problem language not clearly echoed (check consistency)")
    return notes


def check(packet: Path, incoming: str) -> list[str]:
    errors: list[str] = []
    if is_fixture(packet):
        errors.append(
            f"refusing fixture {packet.name}: do not write expanded WORDS onto sample-001"
        )
    if looks_like_expand_prompt(incoming):
        errors.append(
            "incoming text looks like expand_prompt.py stdout, not a script.md body"
        )
    current_path = packet / "script.md"
    current = current_path.read_text(encoding="utf-8") if current_path.is_file() else ""
    cur_keys = [heading_key(h) for h in headings(current)]
    new_keys = [heading_key(h) for h in headings(incoming)]
    if not new_keys:
        errors.append("incoming text has no ## headings")
    else:
        need = {"hook", "payoff", "cta"}
        have = set(new_keys)
        missing = sorted(need - have)
        if missing:
            errors.append(f"incoming script missing sections: {', '.join(missing)}")
        beats = [k for k in new_keys if k.startswith("beat-")]
        if not (4 <= len(beats) <= 7):
            errors.append(f"incoming beat count {len(beats)} not in 4-7")
        if cur_keys:
            cur_beats = [k for k in cur_keys if k.startswith("beat-")]
            if cur_beats and beats and cur_beats != beats:
                errors.append(
                    f"incoming beat ids {beats} do not match current {cur_beats}"
                )
    hook_cues = [c for c in script_cues(incoming) if heading_key(str(c["label"])) == "hook"]
    if hook_cues:
        n = int(hook_cues[0]["words"])
        if n and (n < 20 or n > 35):
            errors.append(f"hook word count {n} not in 20-35")
    return errors


def report(packet: Path, current: str, incoming: str, errors: list[str]) -> str:
    packet_text = (packet / "packet.md").read_text(encoding="utf-8") if (packet / "packet.md").is_file() else ""
    fmt = field(packet_text, "format") or "explainer-6-10min"
    band = FORMAT_SPOKEN_WORDS.get(fmt, (900, 1500))
    before = spoken_total(current)
    after = spoken_total(incoming)
    before_note = duration_note(fmt, before) or "in band"
    after_note = duration_note(fmt, after) or "in band"
    lines = [
        f"Packet: {packet.name}",
        f"Format: {fmt} band {band[0]}-{band[1]}",
        f"Spoken before: {before} (~{fmt_ts((before / WPM) * 60.0 if before else 0)} at {int(WPM)} wpm) {before_note}",
        f"Spoken after:  {after} (~{fmt_ts((after / WPM) * 60.0 if after else 0)} at {int(WPM)} wpm) {after_note}",
        f"Headings in: {', '.join(headings(incoming)) or '(none)'}",
    ]
    for note in idea_lock_notes(packet, incoming):
        lines.append(note)
    for note in anti_slop_notes(incoming):
        lines.append(note)
    for note in originality_notes(packet, incoming):
        lines.append(note)
    if errors:
        lines.append("Result: BLOCKED")
        lines.extend(f"  - {e}" for e in errors)
    else:
        lines.append("Result: OK to write script.md (does not bump status)")
    return "\n".join(lines) + "\n"


def refresh_derived(packet: Path) -> list[str]:
    notes: list[str] = []
    from expand_brief import render as render_expand
    from vo_session import render as render_vo
    from caption_brief import render as render_cap

    (packet / "expand.md").write_text(render_expand(packet), encoding="utf-8")
    notes.append(f"refreshed {packet.name}/expand.md")
    (packet / "vo_session.md").write_text(render_vo(packet), encoding="utf-8")
    notes.append(f"refreshed {packet.name}/vo_session.md")
    (packet / "captions.md").write_text(render_cap(packet), encoding="utf-8")
    notes.append(f"refreshed {packet.name}/captions.md")
    return notes


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Apply a pasted script.md body to a non-fixture packet. "
            "Default is dry-run. Does not invent WORDS or bump status. "
            "Convention: --from PATH/draft.md after an off-repo expand."
        )
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument(
        "--from",
        dest="source",
        help="File with the new script body (convention: PATH/draft.md; default: stdin)",
    )
    parser.add_argument("--write", action="store_true", help="Write script.md. Without this flag, print a report only.")
    parser.add_argument("--refresh", action="store_true", help="After --write, refresh expand.md, vo_session.md, captions.md")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    if args.source:
        source = Path(args.source)
        if not source.is_file():
            print(missing_source_error(source), file=sys.stderr)
            return 2
        incoming_raw = source.read_text(encoding="utf-8", errors="replace")
    else:
        incoming_raw = sys.stdin.read()

    incoming = extract_script(incoming_raw)
    current_path = path / "script.md"
    current = current_path.read_text(encoding="utf-8") if current_path.is_file() else ""
    errors = check(path, incoming)
    print(report(path, current, incoming, errors))
    if errors:
        return 1
    if not args.write:
        print("Dry-run only. Pass --write to replace script.md.")
        return 0
    current_path.write_text(incoming, encoding="utf-8")
    print(f"wrote {current_path}")
    if args.refresh:
        for note in refresh_derived(path):
            print(note)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
