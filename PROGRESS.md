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

These numbers are **estimates**, not stopwatch data. Earlier rows remain in prior commits.

## Capability additions
- Run 220: `tools/experiment_loop.py` fail-closed experiment ledger. Reuses youtube_feedback. Missing provider_video_id is HOLD_UNPUBLISHED. Empty metrics are HOLD_NO_EVIDENCE. Never invents keep/discard. Experiment loop: PLAN_BUILT.
- Run 219: `tools/youtube_feedback.py` fail-closed analytics/comment collector. Reads upload_state.json. Missing provider_video_id is HOLD_UNPUBLISHED. Missing OAuth is YOUTUBE_AUTH_REQUIRED. Metrics stay empty. Never calls APIs. Feedback: READY_FOR_CREDENTIAL.
- Run 218: `tools/assemble.py` fail-closed ffmpeg planner. Reuses timeline + media_qa + selected_vo_drop. Default dry-run. `--execute` only at READY_TO_ENCODE. Assembly: PLAN_BUILT / READY_FOR_MEDIA.
- Run 217: `tools/youtube_upload.py` dry-run uploader. Parses publish.md, requires local master export, checks OAuth env without printing values, fingerprints the packet, writes optional redacted upload_state.json. Never calls videos.insert. Uploader: READY_FOR_CREDENTIAL.
- Run 216: `tools/media_qa.py` fail-closed media gate. WAV header via stdlib wave, PNG IHDR size without Pillow, timeline ready_to_assemble. Exit 2 on FAIL. Does not run ffmpeg, invent a pass, or bump status. Media QA: READY_FOR_MEDIA.
- Run 215: `tools/timeline.py` builds a beat cut list from script.md WORDS and assets.md, estimates duration at 150 wpm, reserves 20s end-screen, reports VO/card presence, optional `timeline.md`. Does not run ffmpeg or bump status. Assembly: PLAN_BUILT.
- Run 214: `tools/card_generator.py` parses assets.md, renders text-cards and vs-diagrams at 1920x1080, inspects dimensions, can write `card_manifest.md`. Does not commit binaries or bump status. Visual capability: READY_FOR_MEDIA.
- Run 213: `tools/narration_adapter.py` extracts WORDS, inspects a packet-relative take, writes `vo_origin.md`. Q1 origin labeled generated after deadline. Workspace TTS MP3 not committed. Status stayed ready_for_vo. Narration capability: READY_FOR_MEDIA.
- Run 137: `docs/narration.md` names the repo-root DROP. `tools/selftest.py` fails if narration.md drops the DROP line. No new CLI. No wav. Status stayed ready_for_vo.
