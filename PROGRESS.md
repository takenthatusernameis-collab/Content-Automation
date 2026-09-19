# PROGRESS

## Efficiency ledger

| When | Human min / video | Automated steps | Notes |
|------|-------------------|-----------------|-------|
| 2026-09-19 Run 229 | ~4.6 estimate | 94 | optional local TTS one-liners on existing drop page; no new adapter |
| 2026-09-19 Run 228 | ~4.7 estimate | 94 | gate-machine drop page; no new adapter |
| 2026-09-19 Run 227 | ~4.8 estimate | 94 | freeze honor; no new adapter; treadmill flagged |
| 2026-09-19 Run 226 | ~4.8 estimate | 94 | selftest locks youtube_upload junk-master FAIL/HOLD_LOCAL |
| 2026-09-19 Run 225 | ~4.9 estimate | 94 | youtube_upload rejects junk export/master.mp4 without ftyp |
| 2026-09-19 Run 224 | ~5.0 estimate | 94 | media_qa/assemble/complete reject junk export/master.mp4 without ftyp |
| 2026-09-19 Run 223 | ~5.1 estimate | 94 | media_qa PCM peak/RMS/silence/clip |
| 2026-09-19 Run 222 | ~5.2 estimate | 94 | HEAD selftest locks experiment_loop.py + complete.py |
| 2026-09-19 Run 221 | ~5.2 estimate | 94 | complete.py fail-closed completion |
| 2026-09-14 Run 137 | ~11 estimate | 85 | narration.md DROP + selftest page lock |

These numbers are **estimates**, not stopwatch data. Earlier rows remain in prior commits.

## Capability additions
- Run 229: `docs/gate_machine.md` now includes optional already-installed TTS one-liners (espeak-ng+ffmpeg, macOS say+ffmpeg, or cp). Still not a repo TTS tool. No invented media.
- Run 228: `docs/gate_machine.md` is the copy-paste Selected VO drop recipe. `docs/human_session.md` now matches OPERATOR_HOLD: generated local audio at the packet DROP path is authorized after the deadline. No new printer. No invented media.
- Run 227: No new printer. Recorded that further dry-run adapters before on-disk Selected VO are the 213–226 treadmill, not SHIP progress.
- Run 226: `tools/selftest.py` imports `inspect_upload` and runs `check_upload_fail_closed()` from `main()`.
- Earlier capability rows remain in prior commits.
