# PROGRESS

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

## Run 362 — 2026-10-06T11:20:00Z
The setup recipe now prints the exact private execute dispatch, including collect_feedback=false. Estimated save: one wrong first dispatch that asks for analytics before a video id exists, about 5 human minutes. Human minutes per video otherwise unchanged. Videos published stay 0.

## Run 361 — 2026-10-06T10:12:00Z
Stall flags no longer stay set only because the lock sentence repeats the tool name. A last chapter inside the final 10 seconds is refused when duration is known, so the first upload does not silently lose chapters. Estimated save: one Studio chapter repair after the first private insert. Human minutes per video otherwise unchanged. Videos published stay 0.

360 — 2026-10-06T09:11:00Z
NEXT.md now has one Active locks block and names the three secrets as the only human step. Estimated effect: a truncated fetch no longer hides that step behind a second lock paragraph. Human minutes per video unchanged. Videos published stay 0.

## Run 359 — 2026-10-06T08:11:00Z
The local OAuth exchange accepts the full localhost redirect URL, so the human does not cut the code out of the address bar. Estimated human minutes saved on the first credential setup: about 10, plus one avoided failed token POST. Human minutes per video otherwise unchanged. Videos published stay 0.

## Run 358 — 2026-10-06T07:15:00Z
Local OAuth exchange writes the refresh token only outside the repo and requests the caption and analytics scopes. Estimated human minutes saved on the first credential setup: about 15, plus one avoided private video if the token had been upload-only. Human minutes per video otherwise unchanged. Videos published stay 0.

## Run 357 — 2026-10-06T06:20:00Z
Log compact now collapses stacked file headers. FAILURES.md and PROGRESS.md each show one header and 12 sections. Estimated effect: a truncated fetch no longer hides the newest lesson behind a second file header. Human minutes per video unchanged. Videos published stay 0.

## Run 356 — 2026-10-06T05:11:00Z
- Improvement: the current-gate file is one header again. A truncated fetch no longer lands on a second `# STATE` that looks like a new file, and compact can no longer cut a delta in half by treating the next header as part of the previous section.
- Efficiency: estimated human minutes per video unchanged. Saves a future agent from reconstructing which delta is current. Automated steps unchanged. Remaining manual step is still the three YouTube secrets.
- Verification: state compact contract PASS. Videos published stay 0.


## Run 355 — 2026-10-06T04:15:00Z
- Viewer-facing upload copy no longer includes the chapter-draft label or the draft-pin sentence.
- Estimated human minutes saved on the first upload: about 5 (description and pin edit in Studio after insert). The strip also covers a future packet that still has the old stub sentence.
- Automated steps unchanged. Remaining manual step is still the three YouTube secrets. Videos published stay 0.



## Run 354 — 2026-10-06T03:20:00Z
- Improvement: a repeated pre-upload probe is now machine-visible. `STALL_PREUPLOAD_PROBE` stops the next run from wiring another export, media, or caption checker while videos published stay 0.
- Efficiency: avoids another probe-only run. Estimated human minutes per video unchanged. Automated steps unchanged. Remaining manual step is still the three YouTube secrets.
- Verification: stall watch contract PASS. Selftest PASS. No provider write.

## Run 353 — 2026-10-06T02:20:00Z
- A present captions.srt is now rejected before captions.insert when a cue is empty, overlapping, reversed, longer than 42 characters, or past the selected wav. Estimated save: one private video with unreadable or late captions if execute starts before a human opens the srt. Human minutes per video unchanged until secrets exist. Videos published stay 0.
- Automated step added: `tools/caption_gate.py` on the production job after media QA. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call. Do not add another export-probe lock. Do not add another media checker.

## Run 352 — 2026-10-06T01:15:00Z
- The production job now runs media QA after materialize. Estimated save: one private upload of a wrong-size card or a clipped take if execute starts before a human opens the packet. Human minutes per video unchanged until secrets exist. Videos published stay 0.
- Automated step changed: existing `tools/media_qa.py` on the production job. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call. Do not add another export-probe lock.

## Run 351 — 2026-10-06T00:20:00Z
- The production export probe now refuses the known truncated r249 master and a present master that is not 30fps yuv420p h264 with stereo AAC at 48000 Hz. Estimated save: one private upload of the truncated file if execute starts before a human checks duration. Human minutes per video unchanged until secrets exist. Videos published stay 0.
- Automated step changed: existing `tools/export_probe.py` on the production job. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call while `STALL_UPLOAD_EDGE` is set.



## Run 350 — 2026-10-05T23:20:00Z
- A present master is now rejected before videos.insert unless it is 1920x1080 h264 with audio and at least 20s. Estimated save: one bad private upload and one Studio cleanup if the first execute used a wrong-size file. Human minutes per video unchanged until secrets exist. Videos published stay 0.
- Automated step added: `tools/export_probe.py` in the production workflow before upload gates. Remaining manual gate: YouTube OAuth secrets. Do not add another early-persist call while `STALL_UPLOAD_EDGE` is set.



