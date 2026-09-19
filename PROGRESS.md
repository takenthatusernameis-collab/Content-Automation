# PROGRESS

## Efficiency ledger

| When | Human min / video | Automated steps | Notes |
|------|-------------------|-----------------|-------|
| 2026-09-14 Run 137 | ~11 estimate | 85 | narration.md DROP + selftest page lock; VO still human |
| 2026-09-19 Run 213 | ~10 estimate | 86 | narration_adapter + labeled generated fallback after 24h; take still local-only |
| 2026-09-19 Run 214 | ~8 estimate | 87 | card_generator.py; 1920x1080 local PNGs; binaries gitignored |
| 2026-09-19 Run 215 | ~7 estimate | 88 | timeline.py cut list from WORDS + cards; no ffmpeg |
| 2026-09-19 Run 216 | ~6.5 estimate | 89 | media_qa.py fail-closed VO/card/assembly checks |
| 2026-09-19 Run 217 | ~6 estimate | 90 | youtube_upload.py dry-run; YOUTUBE_AUTH_REQUIRED |
| 2026-09-19 Run 218 | ~5.5 estimate | 91 | assemble.py dry-run ffmpeg recipe; HOLD_MEDIA without files |
| 2026-09-19 Run 219 | ~5.4 estimate | 92 | youtube_feedback.py dry-run; HOLD_UNPUBLISHED without video id |
| 2026-09-19 Run 220 | ~5.3 estimate | 93 | experiment_loop.py dry-run; HOLD_NO_EVIDENCE without metrics |
| 2026-09-19 Run 221 | ~5.2 estimate | 94 | complete.py fail-closed completion; experiment selftest lock claimed |
| 2026-09-19 Run 222 | ~5.2 estimate | 94 | HEAD selftest now locks experiment_loop.py + complete.py |
| 2026-09-19 Run 223 | ~5.1 estimate | 94 | media_qa PCM peak/RMS/silence/clip; silent or clipped takes fail before ffmpeg |
| 2026-09-19 Run 224 | ~5.0 estimate | 94 | media_qa/assemble/complete reject junk export/master.mp4 without ftyp |
| 2026-09-19 Run 225 | ~4.9 estimate | 94 | youtube_upload rejects junk export/master.mp4 without ftyp |

These numbers are **estimates**, not stopwatch data. Earlier rows remain in prior commits.

## Capability additions
- Run 225: `tools/youtube_upload.py` requires `media_qa.mp4_header_ok` before master_export_present. A size>0 junk file stays HOLD_LOCAL and is not fingerprinted as a master. No new adapter. No invented master. Selftest fixture for this case not yet in `main()`.
- Run 224: `tools/media_qa.py` reports export_present / export_decodable from a stdlib ISO BMFF ftyp sniff. Hard-gated only when an export file exists. `assemble.py` no longer treats size>0 as EXPORT_EXISTS. `complete.py` requires ftyp before master_export_present. Selftest writes a junk mp4 and asserts FAIL / not EXPORT_EXISTS / master_export_present false. No new adapter. No invented master.
- Run 223: `tools/media_qa.py` reports vo_peak / vo_rms / vo_silence / vo_clip from stdlib PCM (audioop + array). Hard-gated only when a WAV header decodes. Missing VO still FAIL. Selftest asserts the four rows exist and are false without a take. No new adapter. No invented wav.
- Run 222: HEAD `tools/selftest.py` now lists `experiment_loop.py` and `complete.py` in `DROP_IMPORTERS` and runs fail-closed fixtures. Closes the gap between Run 221's claim and the file on main. No new adapter.
- Run 221: `tools/complete.py` fail-closed completion gate. Reuses media_qa + assemble + feedback + experiment_loop. Markdown-only packets stay INCOMPLETE_MEDIA. A provider video ID alone is not COMPLETE. Completion gate: PLAN_BUILT.
- Run 220: `tools/experiment_loop.py` fail-closed experiment ledger. Reuses youtube_feedback. Missing provider_video_id is HOLD_UNPUBLISHED. Empty metrics are HOLD_NO_EVIDENCE. Never invents keep/discard. Experiment loop: PLAN_BUILT.
- Run 219: `tools/youtube_feedback.py` fail-closed analytics/comment collector. Reads upload_state.json. Missing provider_video_id is HOLD_UNPUBLISHED. Missing OAuth is YOUTUBE_AUTH_REQUIRED. Metrics stay empty. Never calls APIs. Feedback: READY_FOR_CREDENTIAL.
- Run 218: `tools/assemble.py` fail-closed ffmpeg planner. Reuses timeline + media_qa + selected_vo_drop. Default dry-run. `--execute` only at READY_TO_ENCODE. Assembly: PLAN_BUILT / READY_FOR_MEDIA.
- Run 217: `tools/youtube_upload.py` dry-run uploader. Parses publish.md, requires local master export, checks OAuth env without printing values, fingerprints the packet, writes optional redacted upload_state.json. Never calls videos.insert. Uploader: READY_FOR_CREDENTIAL.
- Run 216: `tools/media_qa.py` fail-closed media gate. WAV header via stdlib wave, PNG IHDR size without Pillow, timeline ready_to_assemble. Exit 2 on FAIL. Does not run ffmpeg, invent a pass, or bump status. Media QA: READY_FOR_MEDIA.
