# PROGRESS

## Efficiency ledger

| When | Human min / video | Automated steps | Notes |
|------|-------------------|-----------------|-------|
| 2026-09-20 Run 236 | ~3.9 estimate | 94 | WAVE 3 queue_status/next_topic hold Q2 and name gate_machine |
| 2026-09-20 Run 235 | ~4.0 estimate | 94 | needed.py bootstrap + doctor reconstruct fetch docs/gate_machine.md |
| 2026-09-20 Run 234 | ~4.1 estimate | 94 | next_action.py ready_for_edit now names existing post-VO CLIs |
| 2026-09-20 Run 233 | ~4.2 estimate | 94 | hint.py build-cards/edit now name existing post-VO CLIs |
| 2026-09-20 Run 232 | ~4.3 estimate | 94 | pipeline_status missing-VO DROP now names docs/gate_machine.md |
| 2026-09-20 Run 231 | ~4.4 estimate | 94 | hint.py / next_action.py record-vo now name docs/gate_machine.md |
| 2026-09-19 Run 230 | ~4.5 estimate | 94 | human_session/agent_session no longer ban the authorized gate_machine TTS drop |
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
- Run 236: `tools/queue_status.py` footer/report and `tools/next_topic.py` print that Q1 remaining labor is `docs/gate_machine.md` and must not scaffold Q2. No new printer. No invented media.
- Run 235: `tools/needed.py` BOOTSTRAP and doctor UNMAPPED_PATHS include `docs/gate_machine.md`. WAVE 3 plan comment names that page. README live packet names it. No new printer. No invented media.
- Run 234: `tools/next_action.py` ready_for_edit Why text names `card_generator.py --write-manifest` and timeline/media_qa/assemble. No new printer. No invented media. hint.py Why text inherits the sentence.
- Run 233: `tools/hint.py` build-cards prints `card_generator.py --write-manifest`; edit prints timeline/media_qa/assemble. No new printer. No invented media. doctor.py inherits via hint.commands_for.
- Run 232: `tools/pipeline_status.py` missing-VO DROP and footer now point at `docs/gate_machine.md`. No new printer. No invented media.
- Run 231: `tools/next_action.py` and `tools/hint.py` record-vo output now point at `docs/gate_machine.md` and name the authorized generated fallback. No new printer. No invented media.
- Run 230: `docs/human_session.md` and `docs/agent_session.md` no longer treat recording as the only remaining gate or ban every ffmpeg one-liner. Dummy `export/master.mp4` stays forbidden. Optional TTS stays on `docs/gate_machine.md`, not under tools/.
- Run 229: `docs/gate_machine.md` now includes optional already-installed TTS one-liners (espeak-ng+ffmpeg, macOS say+ffmpeg, or cp). Still not a repo TTS tool. No invented media.
- Run 228: `docs/gate_machine.md` is the copy-paste Selected VO drop recipe. `docs/human_session.md` now matches OPERATOR_HOLD: generated local audio at the packet DROP path is authorized after the deadline. No new printer. No invented media.
- Run 227: No new printer. Recorded that further dry-run adapters before on-disk Selected VO are the 213–226 treadmill, not SHIP progress.
- Run 226: `tools/selftest.py` imports `inspect_upload` and runs `check_upload_fail_closed()` from `main()`.
- Earlier capability rows remain in prior commits.
