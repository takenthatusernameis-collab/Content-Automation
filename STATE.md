# STATE

Updated: 2026-10-01T18:25:00Z (Run 252)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 ready_for_vo + Selected VO path locked packet-relative + narration adapter + labeled generated fallback + local card generator + WORDS timeline planner + fail-closed media QA + credential-ready dry-run uploader + fail-closed ffmpeg assemble planner (segmented execute + apad=pad_dur end screen + post-mux ftyp/moov refuse) + fail-closed feedback/experiment/complete gates + gate-machine drop recipe -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning` status `ready_for_vo`
- Durable fetch: private release `q1-media-r249` plus Drive folder in HANDOFF.md
- r249 master is truncated (308.40s VO, no 20s end screen). Do not upload it.
- Executive: HOLD for on-disk Selected VO on the publish machine; SHIP after a padded re-encode + OAuth. Do not expand architecture.

## Run 252 delta
- assemble --execute refuses a muxed file without ftyp/moov and leaves export/.segments.
- Evidence: sandbox mux with bare apad was Killed; ffprobe reported moov atom not found.
- Do not re-download. Do not regenerate. Next action is re-encode on a checkout that already has DROP + cards.

## Run 251 delta
- assemble recipe and mux use apad=pad_dur=20 then -shortest. Bare apad hangs.
- r249 master sha256 `abec4eb94199d0cbbf00659891d4e79c0040a6b1bb5450fa6e1db0e54c4b4d53` is truncated.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 3.2 | 3.2 | remaining human gate is YouTube OAuth + re-encode |
| Automated steps | 96 | 96 | header refuse after mux |
| Videos produced | 0 | 0 | local truncated master exists; not uploaded |

## Active constraints
- Do not upload q1-media-r249 q1-master.mp4 as the finished export
- Do not invent a committed wav or bump status past ready_for_vo without Selected VO on disk
- Do not write a dummy export/master.mp4 to flip gates
- Do not regenerate the wav or cards while HANDOFF checksums match
- Do not add a public curl/gdown fetcher
- Do not scaffold Q2
