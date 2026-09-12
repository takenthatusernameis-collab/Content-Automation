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


def load_source(source: str | None) -> tuple[str | None, int]:
    """Load --from text. Missing file -> (None, 2). No source -> stdin."""
    if not source:
        return sys.stdin.read(), 0
    path = Path(source)
    if not path.is_file():
        print(missing_source_error(path), file=sys.stderr)
        return None, 2
    return path.read_text(encoding="utf-8"), 0


def _lock_tokens(value: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9']{4,}", value.lower()) if t not in BLANK_LOCK]


def idea_lock_notes(packet: Path, incoming: str) -> list[str]:
    """Read-only overlap notes. Never added to check() errors."""
    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        return ["INFO idea.md missing; paste idea_brief --block before treating this draft as locked"]
    idea = idea_path.read_text(encoding="utf-8")
    notes: list[str] = []
    mechanism = (
        field(idea, "mechanism (the system, not the pep talk)")
        or field(idea, "mechanism")
        or ""
    ).strip()
    topic = (field(idea, "topic") or "").strip()
    body = incoming.lower()
    mech_low = mechanism.lower()
    if not mechanism or mech_low in BLANK_LOCK or mech_low.startswith("template-default"):
        notes.append("INFO idea.md mechanism is blank; run idea_brief --check before expand")
    else:
        tokens = _lock_tokens(mechanism)
        hits = sum(1 for t in tokens if t in body)
        if mechanism.lower() in body or (tokens and hits >= min(2, len(tokens))):
            notes.append("INFO idea lock: mechanism tokens present in incoming draft")
        else:
            notes.append(
                "INFO idea lock miss: mechanism phrase not visible in incoming draft "
                "(does not block --write; rewrite hook/payoff to name the system)"
            )
    if topic and topic.lower() not in BLANK_LOCK:
        topic_tokens = _lock_tokens(topic)
        hits = sum(1 for t in topic_tokens if t in body)
        if topic.lower() in body or (topic_tokens and hits >= min(2, len(topic_tokens))):
            notes.append("INFO idea lock: topic tokens present in incoming draft")
        else:
            notes.append(
                "INFO idea lock miss: topic phrase not visible in incoming draft "
                "(does not block --write)"
            )
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

    incoming_raw, src_code = load_source(args.source)
    if incoming_raw is None:
        return src_code
    incoming = extract_script(incoming_raw)
    current = (path / "script.md").read_text(encoding="utf-8") if (path / "script.md").is_file() else ""
    errors = check(path, incoming)
    sys.stdout.write(report(path, current, incoming, errors))
    if errors:
        return 1
    if not args.write:
        sys.stdout.write("Dry-run only. Pass --write to replace script.md.\n")
        return 0

    dest = path / "script.md"
    dest.write_text(incoming, encoding="utf-8")
    print(dest)
    if args.refresh:
        for note in refresh_derived(path):
            print(note)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
