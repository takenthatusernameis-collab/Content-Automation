## Run 274 — 2026-10-02T12:25:00Z
- Experiment ledger now computes one primary-metric delta from a documented baseline and collected rows. Decision stays pending. A delta cannot mark a video complete. Videos published stay 0.

## Run 273 — 2026-10-02T11:17:00Z
- Experiment ledger now accepts a documented baseline file and refuses an invented one. Comparison can start after a real fetch without a human designing the schema. Decision stays pending. Videos published stay 0.

## Run 272 — 2026-10-02T10:15:00Z
- Execute dispatch now refuses missing OAuth secrets before ffmpeg and media materialize. Dry-run path unchanged. Videos published stay 0.

## Run 271 — 2026-10-02T09:15:00Z
- Experiment and completion gates now read collected feedback metrics instead of the always-empty dry-run field. A real fetch will no longer look like HOLD_NO_EVIDENCE forever.
- Local selftest passed. Videos published stay 0. OAuth secrets remain the publish boundary.

## Run 270 — 2026-10-02T08:22:00Z
- Production workflow dry-run is now externally verified after the truncated-master skip. Actions run 36983196381 succeeded. Videos published stay 0.
- Automated materialize is no longer blocked by the expected r249 asset. Remaining publish gate is OAuth secrets only.

Updated: 2026-10-02T07:50:00Z

## Run 268
Selftest runner dependency fixed: GitHub Actions now installs ffmpeg, and Selftest Run 8 passed. Repository-side validation is green. No video published; provider authorization and runtime media access remain external.

Updated: 2026-10-02T07:55:00Z

## Run 267
Repository-side bottlenecks removed: durable Q1 release materialization, authenticated YouTube upload execution, resumable post-upload artifacts, authenticated Analytics/comment feedback reads, delegated approval policy, and a minimal selftest workflow. No video published; provider credentials and runtime media access remain external.

Updated: 2026-10-02T07:45:00Z

## Run 266
Approval-only human gates delegated to the automation agent. Q1 description and first-comment approvals completed. Thumbnail/caption sensory review remains evidence-gated because private binary/audio artifacts are inaccessible here. YouTube OAuth remains the external publish bottleneck. No video published.

## Run 265
Q1 thumbnail.png drafted from the locked on-image line (1280x720). Review stays unapproved. Uploader names it and sets uploaded=false. Automated steps 104. Videos published 0.

## Run 264
Q1 chapter lines drafted from script + captions.srt (6 chapters) and copied into publish.md. Boxes stay open. Automated steps 103. Videos published 0.

## Run 263
Q1 caption spot-check sheet written (5 checkpoints, 0 flagged). captions.md no longer assigns inventing the srt. Spot-check and publish boxes stay open. OAuth unchanged. Automated steps 102. Videos published 0.

## Run 261
Q1 captions.srt drafted from wav speech gaps (103 cues). Human still spot-checks. Publish boxes and OAuth unchanged. Automated steps 101. Videos published 0.

## Run 260
Stale "delete No upload happened" instructions removed from pipeline_status, gate_machine, human_session, agent_session, and HANDOFF. publish_brief cannot overwrite the Q1 draft. Human minutes stay 1.5. Videos published 0.

# PROGRESS

## Efficiency ledger

| When | Human min / video | Automated steps | Notes |
|------|-------------------|-----------------|-------|
| 2026-10-02 Run 274 | ~0.5 estimate | 109 | numeric delta is automatic; keep/discard still pending; OAuth still blocks publish |
| 2026-10-02 Run 273 | ~0.5 estimate | 108 | baseline file is loaded fail-closed; OAuth still blocks publish |
| 2026-10-02 Run 271 | ~0.5 estimate | 106 | collected feedback visible to experiment/complete; OAuth still blocks publish |
| 2026-10-02 Run 265 | ~1.0 estimate | 104 | thumbnail PNG drafted; two publish boxes, caption spot-check, and OAuth remain |
| 2026-10-02 Run 264 | ~1.1 estimate | 103 | chapter lines drafted into the description; two publish boxes and OAuth remain |
| 2026-10-02 Run 263 | ~1.2 estimate | 102 | caption review is five checkpoints; two publish boxes and OAuth remain |
| 2026-10-02 Run 261 | ~1.5 estimate | 101 | caption draft from Selected VO; two publish boxes and OAuth remain |
| 2026-10-02 Run 260 | ~1.5 estimate | 100 | operator pages match the drafted description; two boxes and OAuth remain |
| 2026-10-02 Run 259 | ~1.5 estimate | 100 | description drafted; human checks two boxes; OAuth remains |
| 2026-10-02 Run 258 | ~2.0 estimate | 99 | pipeline_status and gate_machine stop the record loop; publish edit and OAuth remain |
| 2026-10-01 Run 253 | ~2.5 estimate | 96 | Padded master 328.40s on q1-media-r253; r249 truncated master must not be uploaded; OAuth still blocks publish |

These numbers are **estimates**, not stopwatch data. Earlier rows remain in prior commits.

## Capability additions
- Run 265: thumbnail_draft.py writes a non-approving 1280x720 PNG from thumbnail.md. Q1 file committed. Dry-run never calls thumbnails.set.
- Run 264: chapter_draft.py writes a non-approving YouTube chapter list from script WORDS and captions.srt. Q1 lines committed into chapters.md and the description draft.
- Run 263: caption_review.py writes a non-approving spot-check sheet from an existing srt. Q1 sheet committed. Human listens to checkpoints instead of all cues.
- Run 261: caption_align.py drafts captions.srt from packet DROP wav speech gaps and script WORDS. Refuses a missing wav. Not ASR. Q1 draft committed; spot-check stays open.
- Run 260: remaining operator surfaces no longer assign a compose step that is already done. Q1 publish.md cannot be force-stubbed.
- Run 259: publish.md no longer needs a human to compose the description. The human still must check Description edited and First comment approved. Agent must not check those boxes.
- Run 253: Live Q1 padded master exists. Duration 328.40s, sha256 `4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546`, private release `q1-media-r253`. Videos published stay 0.

- Run 262 (2026-10-02): uploader dry-run names captions.srt and refuses to claim captions.insert. One overlong Q1 caption line wrapped. Human caption edit is wording spot-check only. Estimated human minutes 1.5 -> 1.4. Videos published stay 0.
