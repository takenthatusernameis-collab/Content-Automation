# DECISIONS

## 2026-10-09 — Run 424: publish tags come from the title and mechanism

- 2026-10-09 | `publish_brief.py` builds lone tags from the title, topic, and mechanism. Problem prose stays in the description. The first word of the title or mechanism is not a lone tag. A mechanism-only word shorter than 4 letters is not a tag. STOP and TAG_GLUE are frozen closed classes. | Runs 420-423 appended one leak word at a time and the next packet still needed a human delete. | Revisit only if a later-packet dry-run still emits a machine sentence or a lone tag this rule does not drop. Do not regenerate Q1 publish.md.

## 2026-10-07 — Run 385: freeze the operator-card surface until a video is published

- 2026-10-07 | `tools/operator_card_freeze.py` fails selftest if `operator_card.py` grows a function, a second card module appears, or the card imports subprocess or a network client. | Runs 383-384 extended the card while videos published stayed 0. A prose lock did not stop the reprint.

## 2026-10-07 — Run 382: freeze the recovery surface until a video id is on main

- 2026-10-07 | `tools/recovery_freeze.py` fails selftest if `youtube-production.yml` grows a second `provider-upload-state` artifact or a second `persist_provider_state.py recover` call. | Runs 368-378 stacked recover paths and a later stall flag did not stop the next edge. | Revisit after a provider video id is on main. Do not add an edge to clear the freeze. Do not poll secrets.

## 2026-10-07 — Run 375: a rejected push needs an artifact, not only a green job

- 2026-10-07 | After videos.insert, upload `upload_state.json` as Actions artifact `provider-upload-state` (`actions: write`, continue-on-error, 90 days). Print `persist_provider_state.py recover` when the push is rejected. | Runs 370-374 exit 0 so a red job does not invite another insert. A green job with the id only on the runner still invites a second insert on the next checkout. | Revisit if the artifact name changes. Do not put the refresh token in that file. Do not poll secrets.



- 2026-10-05 | A present export/master.mp4 must pass `tools/export_probe.py` (1920x1080, h264, audio, duration >= 20s) before execute. Missing export fails execute only. | media_qa hard-fails a missing ftyp box and does not run ffprobe. A wrong-size file could still reach videos.insert. | Revisit if the format lock changes. Do not encode inside the probe. Do not add an upload-edge persist call while STALL_UPLOAD_EDGE is set.

## 2026-10-05 — Run 344: an open Location is commit state

- 2026-10-05 | Provider video id is early-persisted before caption wait when UPLOAD_EARLY_PERSIST=1. A 404/410 hold and a completed-without-id hold are early-persisted before the step returns. | Run 348: Location-only early persist still lost the id if the job died during caption wait, and a later 404 could hide a completed upload. | Do not print the URI. Do not start a second videos.insert when an id or Location exists.
A resumable session URI is a bearer for that upload. It is stored in private `upload_state.json` so a later execute can resume it. It is not printed in logs or run notes. A missing video id with that URI is `commit_resumable_session`, not a transient skip. Do not start another videos.insert while it is present and the export fingerprint matches.

## 2026-10-02 — Run 279: partial post-upload is not success
A provider video id with a failed caption, thumbnail, or requested comment is `POST_UPLOAD_INCOMPLETE`. The job fails after `upload_state.json` is written. Persist runs even when the execute step fails. Collect does not run in the same dispatch as execute. A later execute resumes the same video id; it must not upload the master again.

# DECISIONS

Format: date | decision | why | revisit when

- 2026-09-20 | After hold-before-scaffold is locked in WAVE 3 printers, queue_contract, and README first bash blocks, the default unblocked action is no commit. Executive trajectory is HOLD for packet-relative Selected VO, then SHIP. Documentation-order work is a recorded failure class, not production. | Runs 227–238 produced zero videos and only paper minute drops. Run 239 found no remaining first-command stall. Repeating alignment consumes runs without compounding capability. | Revisit when a proven HEAD regression sends operators to scaffold Q2 or invent media, or when an on-disk Selected VO exists on the gate machine
- 2026-09-19 | A master export is an ISO BMFF file with an ftyp box, not any non-empty path named export/master.mp4. media_qa, assemble, complete, and youtube_upload share `mp4_header_ok`. Missing export stays informational in media_qa; a present junk file is a hard FAIL there and HOLD_LOCAL in the uploader. | Run 224 closed assemble/complete; Run 225 closed the uploader size>0 hole. Header sniff is stdlib and reusable. | After a real ffmpeg encode exists; add stream probe then; do not write a dummy mp4 to flip gates
- 2026-09-19 | Completion is a fail-closed inspect tool (`tools/complete.py`). Markdown, a named export path, a video ID, empty metrics, and a pending experiment are all incomplete. COMPLETE requires VO + cards + master + provider_video_id + metrics + a non-None experiment result. | Run 221: production_capabilities.md already defined completion as evidence, not files existing. A single printer stops future runs from claiming a video is done. After this gate, more dry-run adapters would violate the SHIP-first decision. | After Q1 has on-disk VO, a local master, a real video ID, and real metrics; do not treat INCOMPLETE_* as license to invent any of those
- 2026-09-19 | Experiment results start as a dry-run ledger (`tools/experiment_loop.py`). Missing provider_video_id is HOLD_UNPUBLISHED. Empty metrics are HOLD_NO_EVIDENCE. Decision stays pending. No Analytics call lives in this tool. | Run 220: after the feedback collector existed, the next unblocked reusable capability was the compare/keep ledger specified by docs/feedback_loop.md. | After a published video has real metrics and a documented baseline; do not treat pending as keep/discard
- 2026-09-19 | YouTube feedback starts as a dry-run adapter (`tools/youtube_feedback.py`). Missing provider_video_id is HOLD_UNPUBLISHED. Missing OAuth is `YOUTUBE_AUTH_REQUIRED`. Metrics stay empty until a live report is fetched. No Analytics or comment API call lives in this tool. | Run 219: after assemble.py existed, the next unblocked reusable capability was the credential-last collector specified by docs/youtube_integration.md and docs/feedback_loop.md. | After a published video ID exists and OAuth env is supplied out of git; do not treat empty metrics as collected evidence
- 2026-09-19 | YouTube publishing starts as a dry-run adapter (`tools/youtube_upload.py`). Missing or invalid master export is FAIL. Missing OAuth is `YOUTUBE_AUTH_REQUIRED`. No videos.insert call lives in this tool. Secrets are never printed or written. | Run 217: after media QA existed, the next unblocked reusable capability was the credential-last uploader specified by docs/youtube_integration.md. Run 225 added the ftyp requirement. | After a local master exists and OAuth env is supplied out of git; do not treat READY or a named export as published
- 2026-09-19 | Media QA is a fail-closed inspect tool (`tools/media_qa.py`). Missing VO or cards is FAIL, not a reason to invent files. ffmpeg stays gated on timeline ready_to_assemble plus this gate. | Run 216: after the cut list existed, the next reusable capability was a mechanical media check that works without credentials and does not claim a master export. | After Q1 has on-disk VO and cards; loudness/silence and export ftyp landed Runs 223-224; do not treat FAIL as license to commit media
- 2026-09-19 | Assembly starts as a WORDS/card cut list (`tools/timeline.py`). ffmpeg is forbidden until that planner prints ready_to_assemble=yes. | Run 215: editor.md already blocked a recipe before VO+cards exist; a reusable timeline still reduces edit labor on every future packet. | After Q1 has on-disk VO and cards; do not treat timeline.md as a master export
- 2026-09-19 | Cards are generated locally from assets.md at 1920x1080 and stay gitignored. assets.md Status stays planned unless --mark-ready after inspect-only PASS. | Run 214: visual generation was the next unblocked reusable capability after narration adapter; committing PNGs would fake presence. | After Q1 cards exist on the gate machine; do not git add -f; do not treat manifest as render-complete
- 2026-09-18 | Executive trajectory: prioritize first completed video over further architecture expansion. | The repository has substantial safeguards but zero published videos; first end-to-end production yields more decision-relevant evidence than additional governance. | Revisit after first completed video or if a direct production blocker proves the current path cannot work.

Earlier decisions remain in force in prior commits.
