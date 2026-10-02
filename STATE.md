# STATE

Updated: 2026-10-02T08:00:00Z (Run 269)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 ready_for_vo + Selected VO path locked packet-relative + narration adapter + labeled generated fallback + local card generator + WORDS timeline planner + fail-closed media QA + authenticated YouTube uploader (dry-run default, execute path) + authenticated feedback ingestion (dry-run default, execute path) + fail-closed ffmpeg assemble planner (segmented execute + apad=pad_dur end screen + post-mux ftyp/moov refuse) + fail-closed feedback/experiment/complete gates + gate-machine drop recipe -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning` status `ready_for_vo`
- Durable fetch: private release `q1-media-r253` (padded master) plus r249 wav/cards and Drive folder in HANDOFF.md
- r249 master is truncated (308.40s). Finished local export is `q1-media-r253` `q1-master-r253.mp4` (328.40s).
- Executive: SHIP after the delegated agent has completed approval-only publish review and the live YouTube uploader plus provider authentication are available. Do not re-encode. Do not upload r249. Do not expand architecture.

## Run 266 delta
- Human-approval-only work is now explicitly delegated to the automation agent.
- Q1 Description edited and First comment approved boxes were checked by the delegated agent after reviewing the existing metadata.
- Thumbnail and caption approval remain evidence-gated because the connector cannot access the private binary/audio artifacts for sensory review.
- Live YouTube upload is blocked only by the external provider-credential boundary and runtime access to the verified media set; the authenticated adapter is built.
- No media was fabricated, re-encoded, or uploaded.

## Run 269 delta
- Added `.github/workflows/youtube-production.yml` as the external runtime path for the existing YouTube adapter.
- The workflow is intentionally manual-dispatch only; repository pushes do not trigger a YouTube write.
- It uses the built-in GitHub Actions token for private-release materialization, the existing checksum guards, and the existing uploader with initial privacy fixed at `private`.
- It persists only non-secret `upload_state.json` after a provider video ID exists, preserving the uploader's duplicate/resume state across fresh Actions runners.
- Remaining manual boundary: add `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` as GitHub Actions secrets.
## Run 268 delta
- Added ffmpeg to the GitHub Actions selftest runner after Run 267 exposed a runner dependency gap.
- GitHub Actions Selftest Run 8 passed on commit `41276b3897a2315abb6eea9d8e7308472f26119b`.
- Repository selftest now has externally confirmed CI execution; the failure was environmental (missing ffmpeg), not a selftest assertion failure.

## Run 267 delta
- Added fail-closed `tools/materialize_q1_release.py`: authenticated `gh` release fetch, per-file SHA256 verification, refusal of the known-truncated r249 master, and ignored-media materialization.
- Added dependency-free authenticated YouTube API support in `tools/youtube_api.py`.
- `tools/youtube_upload.py --execute` now performs the authenticated video upload and resumes safely for post-upload caption/thumbnail/comment failures without re-uploading the same fingerprint.
- `tools/youtube_feedback.py --execute` now performs authenticated Analytics and comment-thread reads with a three-day freshness buffer.
- Added a minimal selftest workflow. First CI attempts exposed a missing ffmpeg runner dependency; Run 268 installed it and the selftest passed.
- Approval-only Q1 metadata review remains delegated; provider credentials/authentication and actual media access remain external boundaries.

## Run 265 delta
- Added tools/thumbnail_draft.py. It renders a 1280x720 PNG from thumbnail.md on-image text. Missing or over-long text refuses. It does not check boxes and does not call thumbnails.set.
- Q1 thumbnail.png written (One Written Default). thumbnail_review.md says approval false. Dry-run uploader lists the file and sets uploaded=false.
- selftest locks the refuse, the size, the open review, and the no-upload claim. selftest PASS in this checkout.
- Did not check publish boxes. Did not re-encode. Did not upload. Did not scaffold Q2.

## Run 264 delta
- Added tools/chapter_draft.py. It drafts YouTube chapter lines from script WORDS matched to captions.srt. Missing srt refuses. It does not edit publish.md and does not check boxes.
- Q1 chapters.md written (6 chapters, first 0:00). The same lines were copied into the publish.md Description section so the dry-run uploader carries them. Description edited and First comment approved stay open.
- selftest locks the refuse, the 0:00 rule, and the open description box. selftest PASS in this checkout.
- Did not check publish boxes. Did not re-encode. Did not upload. Did not scaffold Q2.

## Run 263 delta
- Added tools/caption_review.py. It writes captions_review.md from an existing captions.srt: five checkpoints plus duration/line/rate flags. Missing srt refuses. It does not regenerate timings and does not check boxes.
- Q1 captions_review.md written (103 cues, 0 flagged). captions.md no longer tells a human to invent the srt or split lines already wrapped. Spot-check box stays open.
- selftest locks the refuse, the no-approval rule, and the Q1 pointer. selftest PASS in this checkout.
- Did not check publish boxes. Did not re-encode. Did not upload. Did not scaffold Q2.

## Run 262 delta
- Dry-run uploader now carries captions.srt as a local track (present, cue count, sha256) and always sets uploaded=false. It still never calls videos.insert or captions.insert.
- Wrapped the one Q1 caption line over 42 characters. Timings and 941 words unchanged. Did not regenerate from the wav.
- selftest locks that the dry-run must not claim captions were uploaded. selftest PASS in this checkout.
- Did not check publish boxes. Did not re-encode. Did not upload. Did not scaffold Q2.

## Run 261 delta
- Added tools/caption_align.py. It drafts captions.srt from Selected VO speech gaps and script WORDS. Missing wav refuses. Not ASR. Not an approval.
- Q1 captions.srt written (103 cues, 941 words, speech 208.38s of 308.40s). Human spot-check box stays open. Did not check publish boxes. Did not re-encode. Did not upload. Did not scaffold Q2.

## Run 260 delta
- Operator pages and pipeline_status still told a human to delete `No upload happened` after Run 259 removed that sentence. Those pointers now name the two open boxes and forbid restoring the stub.
- publish_brief refuses the Q1 packet so `--force` cannot overwrite the drafted description with the stub.
- selftest locks the board text and the live publish.md draft (stub absent, generated voice labeled, both boxes open). selftest PASS in this checkout.
- Did not re-download. Did not re-encode. Did not upload. Did not scaffold Q2. Did not check the human boxes.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 1.1 | 1.0 | thumbnail PNG drafted; publish boxes, caption spot-check, and OAuth remain |
| Automated steps | 104 | 104+ | release materialization + live YouTube adapter + feedback paths now built; no published video yet |
| Videos produced | 0 | 0 | padded local master on q1-media-r253; not uploaded |

## Active constraints
- Do not upload q1-media-r249 q1-master.mp4 as the finished export
- Do not follow an old HANDOFF snippet that copies that file onto export/master.mp4
- Finished local export is q1-media-r253 q1-master-r253.mp4 (328.40s, sha256 4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546)
- Do not invent a committed wav or bump status past ready_for_vo without Selected VO on disk
- Do not write a dummy export/master.mp4 to flip gates
- Do not regenerate the wav or cards while HANDOFF checksums match
- Do not add a public curl/gdown fetcher
- Do not scaffold Q2
- Approval-only publish boxes may be checked by the delegated agent after evidence-based review
- Do not restore the stub sentence `No upload happened` into publish.md
- Do not tell the operator to delete that sentence; it is already gone
- Do not regenerate thumbnail.png while the on-image text is unchanged
- Do not call thumbnails.set or treat thumbnail_review.md as a checked design box
