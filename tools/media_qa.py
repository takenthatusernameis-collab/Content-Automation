#!/usr/bin/env python3
"""Fail-closed media QA for a video packet.

Checks Selected VO presence/header, card PNG dimensions when files exist,
timeline assembly readiness, and (when present) export/master.mp4 ftyp.
When a WAV exists, also reports peak, RMS, clip fraction, silence
fraction, leading/trailing silence seconds, suggested trim offsets, and a
ready dry-run ffmpeg atrim command from PCM (stdlib only).

Never invents a pass. Never runs ffmpeg. Never bumps packet status.
Never re-implements selected_vo_drop.
"""

from __future__ import annotations

import argparse
import audioop
import struct
import sys
import wave
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from render_brief import selected_vo_drop  # noqa: E402
from timeline import plan  # noqa: E402

TARGET_W = 1920
TARGET_H = 1080
SILENCE_ABS = 0.02
CLIP_ABS = 0.99
MAX_SILENCE_FRAC = 0.60
MIN_PEAK = 0.05
MAX_PEAK = 0.999
MIN_RMS = 0.008
EXPORT_REL = "export/master.mp4"
# Soft thresholds for leading/trailing (report only; not hard-gated)
MAX_LEADING_SILENCE_S = 1.5
MAX_TRAILING_SILENCE_S = 2.0


def mp4_header_ok(path: Path) -> bool:
    """True only when the file starts with an ISO BMFF ftyp box. Stdlib only."""
    try:
        data = path.read_bytes()[:12]
    except OSError:
        return False
    return len(data) >= 8 and data[4:8] == b"ftyp"


def _png_size(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", data[16:24])
    return int(w), int(h)


def _wav_info(path: Path) -> dict:
    info = {"ok": False, "frames": 0, "rate": 0, "channels": 0, "width": 0, "seconds": 0.0, "error": ""}
    try:
        with wave.open(str(path), "rb") as wf:
            info["frames"] = wf.getnframes()
            info["rate"] = wf.getframerate()
            info["channels"] = wf.getnchannels()
            info["width"] = wf.getsampwidth()
            if info["rate"] > 0:
                info["seconds"] = round(info["frames"] / float(info["rate"]), 2)
            info["ok"] = info["frames"] > 0 and info["rate"] > 0 and info["channels"] > 0
    except Exception as exc:  # noqa: BLE001 — fail closed on any decode issue
        info["error"] = str(exc)
    return info


def _wav_levels(path: Path) -> dict:
    """Peak / RMS / silence / clip / leading / trailing / suggested trim from PCM. Stdlib only. Fail-closed."""
    out = {
        "peak": 0.0,
        "rms": 0.0,
        "silence_frac": 1.0,
        "clip_frac": 0.0,
        "leading_silence_s": 0.0,
        "trailing_silence_s": 0.0,
        "suggested_trim_start_s": 0.0,
        "suggested_trim_end_s": 0.0,
        "ok": False,
        "error": "",
    }
    try:
        with wave.open(str(path), "rb") as wf:
            width = wf.getsampwidth()
            nchan = wf.getnchannels()
            frames = wf.getnframes()
            rate = wf.getframerate()
            raw = wf.readframes(frames)
        if frames <= 0 or width <= 0 or nchan <= 0 or not raw or rate <= 0:
            out["error"] = "empty pcm"
            return out
        max_abs = float((1 << (8 * width - 1)) - 1)
        if max_abs <= 0:
            out["error"] = "bad sample width"
            return out
        try:
            peak_int = audioop.max(raw, width)
        except audioop.error:
            peak_int = 0
            if width == 3:
                step = width
                for i in range(0, len(raw) - step + 1, step):
                    val = int.from_bytes(raw[i : i + step], "little", signed=True)
                    peak_int = max(peak_int, abs(val))
        peak = min(1.0, peak_int / max_abs)
        try:
            rms_int = audioop.rms(raw, width)
        except audioop.error:
            rms_int = 0
        rms = min(1.0, rms_int / max_abs)
        try:
            mono = audioop.tomono(raw, width, 0.5, 0.5) if nchan > 1 else raw
            pcm16 = audioop.lin2lin(mono, width, 2) if width != 2 else mono
        except audioop.error as exc:
            out["error"] = f"resample: {exc}"
            out["peak"] = round(peak, 4)
            out["rms"] = round(rms, 4)
            return out
        import array

        samples = array.array("h")
        samples.frombytes(pcm16)
        total = len(samples)
        if total <= 0:
            out["error"] = "no samples after mono"
            return out
        silent = 0
        clipped = 0
        thresh = int(SILENCE_ABS * 32767)
        clip_t = int(CLIP_ABS * 32767)
        for s in samples:
            a = s if s >= 0 else -s
            if a < thresh:
                silent += 1
            if a >= clip_t:
                clipped += 1

        # Leading silence: consecutive samples from start below thresh
        leading = 0
        for s in samples:
            a = s if s >= 0 else -s
            if a < thresh:
                leading += 1
            else:
                break
        # Trailing silence: consecutive from end
        trailing = 0
        for s in reversed(samples):
            a = s if s >= 0 else -s
            if a < thresh:
                trailing += 1
            else:
                break

        total_s = total / float(rate) if rate > 0 else 0.0
        lead_s = leading / float(rate) if rate > 0 else 0.0
        trail_s = trailing / float(rate) if rate > 0 else 0.0

        out["peak"] = round(peak, 4)
        out["rms"] = round(rms, 4)
        out["silence_frac"] = round(silent / float(total), 4)
        out["clip_frac"] = round(clipped / float(total), 4)
        out["leading_silence_s"] = round(lead_s, 3)
        out["trailing_silence_s"] = round(trail_s, 3)
        out["suggested_trim_start_s"] = round(lead_s, 3)
        out["suggested_trim_end_s"] = round(max(0.0, total_s - trail_s), 3)
        out["ok"] = True
    except Exception as exc:  # noqa: BLE001
        out["error"] = str(exc)
    return out


def inspect_media(packet: Path) -> dict:
    data = plan(packet)
    drop = selected_vo_drop(packet)
    vo_path = packet / data["vo_rel"]
    vo_file = vo_path if vo_path.is_file() and vo_path.stat().st_size > 0 else None

    vo = {
        "drop": drop,
        "rel": data["vo_rel"],
        "present": data["vo_on_disk"] == "yes",
        "kind": vo_file.suffix.lower() if vo_file else "",
        "bytes": vo_file.stat().st_size if vo_file else 0,
        "wav": None,
        "levels": None,
    }
    if vo_file and vo_file.suffix.lower() == ".wav":
        vo["wav"] = _wav_info(vo_file)
        vo["levels"] = _wav_levels(vo_file)

    cards = []
    for row in data["rows"]:
        rel = row["card"]
        item = {
            "beat": row["title"],
            "rel": rel,
            "present": row["card_on_disk"] == "yes",
            "size": None,
            "ok": False,
        }
        if rel and item["present"]:
            size = _png_size(packet / rel)
            item["size"] = size
            item["ok"] = size == (TARGET_W, TARGET_H)
        cards.append(item)

    export_path = packet / EXPORT_REL
    export_present = export_path.is_file() and export_path.stat().st_size > 0
    export_ok = export_present and mp4_header_ok(export_path)

    checks = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("selected_vo_present", vo["present"], vo["rel"])
    if vo["wav"] is None:
        if vo["present"] and vo["kind"] == ".flac":
            add("vo_decodable", True, "flac present; header decode not implemented (presence only)")
        elif vo["present"]:
            add("vo_decodable", False, f"unsupported or missing header for {vo['kind'] or 'unknown'}")
        else:
            add("vo_decodable", False, "no packet-relative Selected VO")
        add("vo_peak", False, "no wav levels")
        add("vo_rms", False, "no wav levels")
        add("vo_silence", False, "no wav levels")
        add("vo_clip", False, "no wav levels")
        add("vo_leading_silence", False, "no wav levels")
        add("vo_trailing_silence", False, "no wav levels")
        add("vo_suggested_trim", False, "no wav levels")
    else:
        w = vo["wav"]
        add("vo_decodable", bool(w["ok"]), w["error"] or f"{w['seconds']}s {w['rate']}Hz {w['channels']}ch")
        add("vo_nonempty", bool(w["ok"] and w["seconds"] > 0.2), f"{w['seconds']}s")
        lv = vo["levels"] or {}
        if not lv.get("ok"):
            add("vo_peak", False, lv.get("error") or "levels unavailable")
            add("vo_rms", False, lv.get("error") or "levels unavailable")
            add("vo_silence", False, lv.get("error") or "levels unavailable")
            add("vo_clip", False, lv.get("error") or "levels unavailable")
            add("vo_leading_silence", False, lv.get("error") or "levels unavailable")
            add("vo_trailing_silence", False, lv.get("error") or "levels unavailable")
            add("vo_suggested_trim", False, lv.get("error") or "levels unavailable")
        else:
            peak_ok = MIN_PEAK <= lv["peak"] <= MAX_PEAK
            rms_ok = lv["rms"] >= MIN_RMS
            sil_ok = lv["silence_frac"] <= MAX_SILENCE_FRAC
            clip_ok = lv["clip_frac"] < 0.01
            add("vo_peak", peak_ok, f"peak={lv['peak']}")
            add("vo_rms", rms_ok, f"rms={lv['rms']}")
            add("vo_silence", sil_ok, f"silence_frac={lv['silence_frac']}")
            add("vo_clip", clip_ok, f"clip_frac={lv['clip_frac']}")
            # Soft reporting only (not in hard_names): surfaces awkward pauses
            lead_ok = lv["leading_silence_s"] <= MAX_LEADING_SILENCE_S
            trail_ok = lv["trailing_silence_s"] <= MAX_TRAILING_SILENCE_S
            add("vo_leading_silence", lead_ok, f"leading={lv['leading_silence_s']}s (soft max {MAX_LEADING_SILENCE_S}s)")
            add("vo_trailing_silence", trail_ok, f"trailing={lv['trailing_silence_s']}s (soft max {MAX_TRAILING_SILENCE_S}s)")
            # Soft suggested trim + ready dry-run command (report only)
            start_s = lv["suggested_trim_start_s"]
            end_s = lv["suggested_trim_end_s"]
            trim_detail = f"start={start_s}s end={end_s}s (soft; for future packets)"
            add("vo_suggested_trim", True, trim_detail)
            # Actionable command only when there is meaningful silence to trim
            if start_s > 0.3 or (end_s > 0 and (lv.get("trailing_silence_s", 0) > 0.3)):
                vo_rel = vo["rel"]
                cmd = f"ffmpeg -y -i {vo_rel} -af atrim=start={start_s}:end={end_s} -c copy {vo_rel.replace('.wav', '-trimmed.wav')}"
                add("vo_suggested_trim_cmd", True, f"dry-run only: {cmd}")

    mapped = [c for c in cards if c["rel"]]
    present = [c for c in mapped if c["present"]]
    sized = [c for c in present if c["ok"]]
    add("cards_mapped", bool(mapped), f"{len(mapped)} mapped")
    add("cards_present", bool(mapped) and len(present) == len(mapped), f"{len(present)}/{len(mapped)}")
    add(
        "cards_1920x1080",
        bool(present) and len(sized) == len(present),
        f"{len(sized)}/{len(present)} correct size",
    )
    add("ready_to_assemble", bool(data["ready_to_assemble"]), "timeline gate")
    add("export_present", export_present, EXPORT_REL)
    if export_present:
        add("export_decodable", export_ok, "ftyp" if export_ok else "file present but no ftyp box")
    else:
        add("export_decodable", False, "no export")
    add("no_export_claimed", True, "media_qa does not treat a named export as a master")

    hard_names = {"selected_vo_present", "vo_decodable", "cards_present", "cards_1920x1080", "ready_to_assemble"}
    if vo["wav"] and vo["wav"].get("ok"):
        hard_names.update({"vo_peak", "vo_rms", "vo_silence", "vo_clip"})
    if export_present:
        hard_names.add("export_decodable")
    # Note: vo_leading_silence, vo_trailing_silence, vo_suggested_trim, and vo_suggested_trim_cmd are intentionally soft (report only)
    hard = [c for c in checks if c["name"] in hard_names]
    gate = "PASS" if hard and all(c["ok"] for c in hard) else "FAIL"
    return {
        "packet": packet.name,
        "drop": drop,
        "vo": vo,
        "cards": cards,
        "checks": checks,
        "gate": gate,
        "spoken": data["spoken"],
        "export": EXPORT_REL,
        "export_present": export_present,
        "export_decodable": export_ok,
        "ready_to_assemble": data["ready_to_assemble"],
    }


def render_text(report: dict) -> str:
    lines = [
        f"packet: {report['packet']}",
        f"gate: {report['gate']}",
        f"drop: {report['drop']}",
        f"ready_to_assemble: {'yes' if report['ready_to_assemble'] else 'no'}",
        f"export: {report['export']} present={'yes' if report['export_present'] else 'no'} decodable={'yes' if report['export_decodable'] else 'no'}",
        "repo-root vo/ is not Selected VO",
        "media_qa never runs ffmpeg and never bumps status",
        "vo_leading_silence / vo_trailing_silence / vo_suggested_trim / vo_suggested_trim_cmd are soft reports only (do not fail the gate)",
    ]
    for c in report["checks"]:
        mark = "PASS" if c["ok"] else "FAIL"
        lines.append(f"- {mark} {c['name']}: {c['detail']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed media QA. No ffmpeg. No status bump.")
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    report = inspect_media(path)
    sys.stdout.write(render_text(report))
    return 0 if report["gate"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
