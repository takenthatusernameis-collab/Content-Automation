# ROADMAP

## Next (assisted production)
31-51cg. Prior write-path / DROP / packet work — **done (Runs 027-137)**
51ch. Narration adapter (WORDS extract, wav inspect, vo_origin sidecar) + labeled generated fallback after 24h deadline — **done (Run 213; READY_FOR_MEDIA)**
51ci. Deterministic local card generator from assets.md — **done (Run 214; READY_FOR_MEDIA)**
51cj. WORDS-based edit timeline planner (no ffmpeg) — **done (Run 215; READY_FOR_MEDIA)**
51ck. Fail-closed media QA (VO header + card size + assembly gate) — **done (Run 216; READY_FOR_MEDIA)**
51cl. Credential-ready YouTube dry-run uploader — **done (Run 217; READY_FOR_CREDENTIAL)**; ftyp-required master — **done (Run 225)**
51cm. Fail-closed ffmpeg assembly planner — **done (Run 218; PLAN_BUILT / READY_FOR_MEDIA)**
51cn. Fail-closed YouTube feedback collector — **done (Run 219; READY_FOR_CREDENTIAL)**
51co. Fail-closed experiment ledger — **done (Run 220; PLAN_BUILT)**
51cp. Fail-closed completion gate — **done (Run 221; PLAN_BUILT)**
51cq. HEAD selftest lock for experiment_loop.py + complete.py — **done (Run 222)**
51cr. media_qa PCM peak / RMS / silence / clip (stdlib; hard only when WAV decodes) — **done (Run 223)**
51cs. media_qa / assemble / complete export ftyp sniff (stdlib; hard only when a master file exists) — **done (Run 224)**
51ct. youtube_upload export ftyp sniff (same helper; junk master stays HOLD_LOCAL) — **done (Run 225)**

## Later (automation)
52. Human override of heuristic Primary (optional; already locked)
53. On-disk selected take (human replacement or local generated file) so gates can advance
54. Caption timing from a real selected take — draft aligner done (Run 261; silence-proportional, not ASR). Remaining: human spot-check; do not treat captions.srt as uploaded.
55. ffmpeg `--execute` after one packet has VO + cards and assemble.py prints READY_TO_ENCODE
56. YouTube upload after packet QA passes AND youtube_upload.py is no longer YOUTUBE_AUTH_REQUIRED. Run 279: caption/thumbnail/comment failure is POST_UPLOAD_INCOMPLETE and still persists the video id. Do not re-upload the master on that exit.
56b. Live Analytics/comment fetch after a real provider_video_id exists AND youtube_feedback.py is no longer YOUTUBE_AUTH_REQUIRED / HOLD_UNPUBLISHED / OBSERVATION_WINDOW_NOT_DUE / OBSERVATION_WINDOW_UNKNOWN. Run 276: dispatch `collect_feedback=true` instead of a manual CLI. Run 277: collect requires uploaded_at plus 10 days (7 calendar + 3 Analytics lag). Still not executed.
56c. Compare-and-decide after experiment_loop.py sees real metrics and a documented baseline. Run 271: collected feedback_state.json is visible. Run 273: a valid `experiment_baseline.json` loads fail-closed. Run 274: one numeric primary metric becomes `COMPARED` with decision still pending. Run 275: `experiment_decision.json` records keep/discard/retest only after that comparison. Q1 baseline and decision files still required and must not be invented.
56d. Mark COMPLETE only after `tools/complete.py` prints gate COMPLETE with real evidence

## Not yet
- Treating draft.md as script.md before apply --write
- Auto-scaffolding Q2 while Q1 has no on-disk VO
- WAVE 4
- Mapping doctor.py / words.py / prove_locks.py
- Bumping ready_for_edit without Selected VO on disk
- Treating a publish.md edit as an upload
- Treating repo-root `vo/` as Selected VO
- Force-adding ignored media to flip presence rows
- Describing generated VO as a human recording
- Re-implementing selected_vo_drop in a second module
- Committing generated card PNGs
- Running ffmpeg before VO + cards exist on the gate machine
- Treating media_qa FAIL as a reason to invent media
- Calling videos.insert from the dry-run adapter
- Treating an assemble recipe as a master export
- Writing a dummy export/master.mp4 to flip EXPORT_EXISTS
- Treating youtube_upload size>0 as a master
- Inventing analytics or comments before a published video ID exists
- Treating a pending experiment record as a keep/discard
- Treating complete.py INCOMPLETE_* as a completed video
- Adding another dry-run adapter before the first on-disk Selected VO
- Claiming a selftest lock is on HEAD when DROP_IMPORTERS still omits the printer

## End-to-end automation buildout

57. **Narration adapter** — READY_FOR_MEDIA (Run 213). Remaining: on-disk take. Loudness/silence/clip now live in media_qa (Run 223).
58. **Card/visual generator** — READY_FOR_MEDIA (Run 214). Remaining: run on gate machine; do not commit pngs.
59. **Render/assembly pipeline** — PLAN_BUILT / READY_FOR_MEDIA (Run 215 timeline.py + Run 218 assemble.py). Remaining: `--execute` only after ready_to_assemble=yes and media_qa PASS.
60. **Full media QA gate** — READY_FOR_MEDIA (Run 216 header + Run 223 levels + Run 224 export ftyp). Run 350: `export_probe.py` checks 1920x1080, h264, audio, and >=20s when a master exists. Run 351: it also refuses the r249 truncated sha and requires 30fps yuv420p with stereo AAC at 48000 Hz. Run 352: the production job runs `media_qa.py` after materialize. Q1 must pass. It does not encode. Remaining: live VO/card files on a non-Q1 packet.
61. **Credential-ready YouTube uploader** — READY_FOR_CREDENTIAL (Run 217 youtube_upload.py; Run 225 ftyp). Remaining: local master with ftyp + OAuth env; live videos.insert still NOT_BUILT.
62. **YouTube feedback ingestion** — READY_FOR_CREDENTIAL (Run 219 youtube_feedback.py). Remaining: published video ID + OAuth env; live Analytics/comment fetch still NOT_BUILT.
63. **Experiment/improvement loop** — PLAN_BUILT (Run 220 experiment_loop.py). Run 271 reads collected feedback_state.json only. Remaining: a real fetch plus a documented baseline before keep/discard. Selftest lock on HEAD (Run 222).
64. **Completion gate** — PLAN_BUILT (Run 221 complete.py). Remaining: real VO, cards, master with ftyp, publish ID, metrics, and experiment result before COMPLETE. Selftest lock on HEAD (Run 222).
