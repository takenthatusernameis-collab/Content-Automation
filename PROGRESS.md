# PROGRESS

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

## Run 369 — 2026-10-06T19:12:00Z
- Improvement: a post-upload caption, thumbnail, or comment miss no longer fails the production job when the video id is already written. Estimated save: one extra execute dispatch after the first private insert, which could start another videos.insert, about 15 human minutes plus a duplicate private video.
- Efficiency: human minutes per video otherwise unchanged. Automated steps unchanged. Remaining manual step is still the three YouTube secrets.
- Verification: selftest PASS. No provider write. Videos published stay 0.

## Run 368 — 2026-10-06T18:12:00Z
- Improvement: a failed playlist insert no longer fails the production job. Estimated save: one extra execute dispatch after the first private insert, which could start another videos.insert, about 15 human minutes plus a duplicate private video.
- Efficiency: human minutes per video otherwise unchanged. Automated steps unchanged. Remaining manual step is still the three YouTube secrets.
- Verification: selftest PASS. No provider write. Videos published stay 0.

## Run 367 — 2026-10-06T17:11:00Z
- Improvement: the first Studio end-screen note no longer asks for a playlist element while playlist_id is not_set. Estimated save: one failed end-screen setup after the first private insert, about 5 human minutes.
- Efficiency: human minutes per video otherwise unchanged. Automated steps unchanged. Remaining manual step is still the three YouTube secrets.
- Verification: selftest PASS. No provider write. Videos published stay 0.

## Run 366 — 2026-10-06T16:20:00Z
- Improvement: selftest now executes `stall_watch_contract.py` again. A later duplicate function had shadowed that call since the inline checks were added.
- Efficiency: a broken stall contract fails here instead of on a later run that happens to invoke the contract alone. Estimated human minutes per video unchanged. Automated steps unchanged. Remaining manual step is still the three YouTube secrets.
- Verification: selftest PASS. No provider write. Videos published stay 0.

## Run 365 — 2026-10-06T15:20:00Z
Selftest can see a clear stall watch again. A zero idle streak is not a flag, so a quiet file no longer looks like a stall. STATE.md and NEXT.md are back at the 12-section cap. Estimated effect: the next run does not reconstruct a red gate that was only a count of zero. Human minutes per video unchanged. Videos published stay 0.

## Run 364 — 2026-10-06T13:22:00Z
The production stall printer now counts consecutive unpublished OAuth-idle deltas. Estimated effect: a later run can see `idle_streak` and `suspicious: oauth_idle_without_publish` without reconstructing STATE. Human minutes per video unchanged. Videos published stay 0. Live streak after this delta: 13.

## Run 363 — 2026-10-06T12:20:00Z
A bare `360 — timestamp` progress line is now a real section. Log compact promotes that shape before the size cap, and the live Run 360 heading is restored. Estimated effect: a truncated fetch no longer drops the Run 360 lesson into the previous section. Human minutes per video unchanged. Videos published stay 0.

## Run 362 — 2026-10-06T11:20:00Z
The setup recipe now prints the exact private execute dispatch, including collect_feedback=false. Estimated save: one wrong first dispatch that asks for analytics before a video id exists, about 5 human minutes. Human minutes per video otherwise unchanged. Videos published stay 0.

## Run 361 — 2026-10-06T10:12:00Z
Stall flags no longer stay set only because the lock sentence repeats the tool name. A last chapter inside the final 10 seconds is refused when duration is known, so the first upload does not silently lose chapters. Estimated save: one Studio chapter repair after the first private insert. Human minutes per video otherwise unchanged. Videos published stay 0.

## Run 360 — 2026-10-06T09:11:00Z
NEXT.md now has one Active locks block and names the three secrets as the only human step. Estimated effect: a truncated fetch no longer hides that step behind a second lock paragraph. Human minutes per video unchanged. Videos published stay 0.

## Run 359 — 2026-10-06T08:11:00Z
The local OAuth exchange accepts the full localhost redirect URL, so the human does not cut the code out of the address bar. Estimated human minutes saved on the first credential setup: about 10, plus one avoided failed token POST. Human minutes per video otherwise unchanged. Videos published stay 0.

## Run 358 — 2026-10-06T07:15:00Z
Local OAuth exchange writes the refresh token only outside the repo and requests the caption and analytics scopes. Estimated human minutes saved on the first credential setup: about 15, plus one avoided private video if the token had been upload-only. Human minutes per video otherwise unchanged. Videos published stay 0.

