# End-to-end production capability contract

## Completion definition

A video is not considered “completed” merely because its text packet passes. The pipeline must be able to move a packet from a validated idea to a finished local master, publish it when authorized, ingest real feedback, and use that feedback to improve a later packet.

Local printer: `tools/complete.py` (PLAN_BUILT; fail-closed). Markdown-only packets are INCOMPLETE_MEDIA. A named export path is INCOMPLETE_EXPORT until the file exists. A missing provider_video_id is INCOMPLETE_PUBLISH. Empty metrics are INCOMPLETE_FEEDBACK. A pending experiment is INCOMPLETE_LEARNING. COMPLETE requires VO + cards + master + provider_video_id + metrics + a non-None experiment result.

## Required capabilities

### 1. Editorial / research
- topic queue with explicit problem, viewer, mechanism, and relation to prior videos
- research/source capture for factual claims
- script generation with the anti-slop contract
- mechanical script validation and read-aloud editorial review
- title/thumbnail/publish metadata generation

### 2. Narration
- one pluggable narration adapter supporting either a human recording or explicitly authorized generated narration
- WAV/FLAC validation: decodable audio, expected sample rate/bit depth/channels, non-zero duration, no empty file
- loudness/silence/clipping checks before assembly (`tools/media_qa.py` vo_peak / vo_rms / vo_silence / vo_clip; hard-gated when a WAV decodes)
- generated narration must be recorded as generated in packet state and never described as human-recorded

### 3. Visual assets
- deterministic generation of the seven planned text/diagram cards from assets.md
- card dimensions and readable text validation
- optional B-roll adapter that is never required for basic completion
- asset provenance recorded for anything externally sourced
- local generator: `tools/card_generator.py` (READY_FOR_MEDIA; Pillow; gitignored PNGs)

### 4. Assembly / rendering
- deterministic timeline construction from selected VO, cards, captions, and optional music/SFX
- local planner: `tools/timeline.py` (PLAN_BUILT / READY_FOR_MEDIA; WORDS clock; no ffmpeg)
- local encoder planner: `tools/assemble.py` (PLAN_BUILT / READY_FOR_MEDIA; dry-run ffmpeg argv; `--execute` refused unless media_qa PASS and ready_to_assemble=yes)
- export to the locked 1920x1080, 30fps, stereo 48kHz target at `export/master.mp4`
- last 20 seconds reserved for YouTube end-screen elements
- render verification: file opens, duration is plausible, video/audio streams exist, no missing frame/audio stream, and expected packet fingerprint is recorded
- master export must remain local / outside Git unless the repository later chooses an artifact store
- ffmpeg `--execute` stays gated until timeline ready_to_assemble=yes and media_qa PASS on a real packet

### 5. QA
- packet gate: script, status, metadata, selected VO, cards, export
- media gate: `tools/media_qa.py` (READY_FOR_MEDIA; fail-closed VO header + PCM levels + 1920x1080 PNG IHDR + assembly readiness; no ffmpeg; no status bump)
- completion gate: `tools/complete.py` (PLAN_BUILT; fail-closed evidence rollup; no writes; no APIs)
- content-quality gate: anti-slop/originality/read-aloud review
- factual-claim gate: every consequential number or factual assertion has a source or is rewritten qualitatively
- publish gate must fail closed on any missing prerequisite
- a named export path is not a completed master

### 6. YouTube publishing
- metadata mapping from publish.md
- dry-run adapter: `tools/youtube_upload.py` (READY_FOR_CREDENTIAL; no API call; no secrets printed)
- OAuth configuration loader and authenticated upload adapter
- dry-run mode with zero provider writes
- idempotency fingerprint to prevent duplicate uploads
- initial privacy state controlled explicitly by policy (`private` in the dry-run adapter)
- redacted upload state containing attempt time, provider ID, privacy state, and result/error class
- never store secrets in Git or logs
- live `videos.insert` remains NOT_BUILT until a local master and OAuth env exist

### 7. Feedback ingestion
- dry-run adapter: `tools/youtube_feedback.py` (READY_FOR_CREDENTIAL; no API call; no invented metrics)
- missing provider_video_id fails closed as `HOLD_UNPUBLISHED`
- missing OAuth fails closed as `YOUTUBE_AUTH_REQUIRED`
- YouTube Analytics ingestion after publication (live fetch still NOT_BUILT)
- video-level views, likes/dislikes where available, watch-time and average-view-duration / percentage metrics, plus subscriber-related metrics where useful
- comment-thread ingestion for viewer language, objections, requests, confusion, and recurring questions
- collection of a comparable observation window for each video rather than mixing different ages
- all imported data must retain source, retrieval time, window, and video ID

### 8. Improvement / experimentation
- convert feedback into explicit hypotheses rather than automatically rewriting everything
- distinguish content-signal feedback from platform noise
- log experiment ID, hypothesis, change, target metric, guardrails, observation window, and result
- compare new videos against appropriate prior videos or a documented baseline
- avoid optimizing to a single metric or a single early outlier
- preserve successful mechanisms while testing one material change at a time where practical
- feed repeated viewer questions and measured weak points back into the topic queue and script prompts
- keep failures and null results so the system does not repeat them
- dry-run ledger: `tools/experiment_loop.py` (PLAN_BUILT; no invented keep/discard)

## Capability states

Use these states in the roadmap/state files:
- BUILT — implemented and mechanically validated
- READY_FOR_CREDENTIAL — implementation exists but requires provider credentials
- READY_FOR_MEDIA — implementation exists but requires local/generated media input
- PLAN_BUILT — planner/contract exists; encoder or provider step still missing
- BLOCKED — a real external dependency prevents progress
- NOT_BUILT — capability does not yet exist

Do not mark the pipeline AUTOMATED or SELF-IMPROVING until the required capabilities above are either BUILT or explicitly READY_FOR_CREDENTIAL/READY_FOR_MEDIA with a documented reason.

## Autonomous construction rule

The daily unstick agent may build any repository-side capability that is missing and can be implemented without unavailable third-party credentials. It must use the smallest safe increment, run the relevant contract/self-tests, and record the capability state.

The final provider boundary is credentials/authentication. A missing credential must not prevent construction of the surrounding adapter, dry-run validation, idempotency logic, or redacted state handling.

After the completion gate exists, prefer advancing Q1 media over adding another dry-run adapter.

## Do not fake completion

Do not mark a video complete because metadata files exist. Do not mark a render complete because an output path is named. Do not mark feedback collected because a placeholder exists. Do not mark improvement because a new script sounds better. Completion requires the corresponding evidence. `tools/complete.py` is the mechanical reminder of that rule.
