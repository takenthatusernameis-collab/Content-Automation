#!/usr/bin/env python3
"""Materialize durable Q1 release artifacts into the ignored packet paths.

Fail-closed: requires authenticated gh access, verifies every checksum, never
commits media, never regenerates matching artifacts, and never installs the
known-truncated r249 master.

The r249 release still contains that truncated master. Its presence is expected.
Do not abort the wav/card fetch because the banned asset was downloaded.
Refuse only if it is installed as export/master.mp4 or if its checksum changes.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO = "takenthatusernameis-collab/Content-Automation"
R249 = "q1-media-r249"
R253 = "q1-media-r253"
PACKET = Path("videos/002-stop-deciding-what-to-work-on-every-morning")
VO_NAME = "002-stop-deciding-what-to-work-on-every-morning-take-selected.wav"
MASTER_NAME = "q1-master-r253.mp4"
VO_SHA = "758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2"
MASTER_SHA = "4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546"
BANNED_MASTER_SHA = "abec4eb94199d0cbbf00659891d4e79c0040a6b1bb5450fa6e1db0e54c4b4d53"
CARD_SHA = {
    "hook-card-on-a-closed-laptop-one-handwritte.png": "820cb09df9806151ed43336deab9dac656cae2dc8d9f6b6c38dee64c02d51982",
    "payoff-same-card-stop-rule-under-the-sentenc.png": "a8e6660f152afac65981b2eee6ec34efc9eacc151b19aa1af0ba23fa7aafaf9a",
    "beat1-split-open-task-board-vs-one-index-car.png": "6fb7611f515ceee6682e140f9e14c637238143555b542851cfbb7fc031a8e20d",
    "beat2-hand-writing-verb-object-place-on-a-ca.png": "e0f306a8c5d41dde81edbab5e2fa70544be075ebcad98dd5a38dc50e69f3af3d",
    "beat3-four-crossed-out-themes-replaced-by-on.png": "96e2ff34fe8f84b9f99f4094ed443a4606cb979758e084451d0fc1e3b5cc6b33",
    "beat4-night-card-morning-start-shutdown-rewr.png": "0510c7d67b550a6c87fff801238fd5da1430db8c06a417f404bacba8522a74cc",
    "cta-cta-card-write-tomorrow-s-next-action-on.png": "b0f67d7c5ad085f5e2882fdcda67a2e363a171d544d854b8c43d3b5d492e56e9",
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def gh_download(release: str, out_dir: Path) -> None:
    proc = subprocess.run(
        ["gh", "release", "download", release, "--repo", REPO, "-D", str(out_dir)],
        capture_output=True,
        text=True,
        timeout=180,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()[-1000:]
        raise RuntimeError(f"gh release download {release} failed: {detail}")

def copy_verified(src: Path, dst: Path, expected: str) -> None:
    if not src.is_file():
        raise RuntimeError(f"missing release asset: {src.name}")
    got = sha256(src)
    if got != expected:
        raise RuntimeError(f"checksum mismatch {src.name}: expected {expected}, got {got}")
    if got == BANNED_MASTER_SHA:
        raise RuntimeError("refuse known-truncated r249 q1-master.mp4")
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        current = sha256(dst)
        if current == expected:
            return
        raise RuntimeError(f"refuse overwrite of existing wrong artifact: {dst}")
    shutil.copy2(src, dst)

def ignore_truncated_r249_master(r249: Path) -> None:
    """r249 still ships the truncated master. Presence is not an install."""
    bad = r249 / "q1-master.mp4"
    if not bad.is_file():
        print("r249 q1-master.mp4 absent; continuing with wav and cards only")
        return
    got = sha256(bad)
    if got != BANNED_MASTER_SHA:
        raise RuntimeError(
            f"unexpected r249 q1-master.mp4 sha256={got}; refusing to continue"
        )
    print("ignored known-truncated r249 q1-master.mp4; installing r253 master only")

def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize verified Q1 release media locally.")
    parser.add_argument("--keep-temp", action="store_true", help="Retain temporary downloads for debugging.")
    parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="q1-release-") as tmp:
        base = Path(tmp)
        r249, r253 = base / R249, base / R253
        gh_download(R249, r249)
        gh_download(R253, r253)
        ignore_truncated_r249_master(r249)

        copy_verified(r249 / VO_NAME, PACKET / "vo" / VO_NAME, VO_SHA)
        for name, expected in CARD_SHA.items():
            copy_verified(r249 / name, PACKET / "cards" / name, expected)
        copy_verified(r253 / MASTER_NAME, PACKET / "export" / "master.mp4", MASTER_SHA)
        installed = PACKET / "export" / "master.mp4"
        if sha256(installed) == BANNED_MASTER_SHA:
            raise RuntimeError("refuse known-truncated r249 q1-master.mp4 installed as export")

    print(f"materialized: {PACKET / 'vo' / VO_NAME}")
    print(f"cards: {len(CARD_SHA)}")
    print(f"master: {PACKET / 'export' / 'master.mp4'}")
    print("media remains ignored; no repository media commit is performed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
