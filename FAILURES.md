# FAILURES

Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.

## Run 375 — 2026-10-07T03:11:00Z
- Failed approach not retried: treating a green persist step as proof the video id is on main, or another exchange parser, scanner, or pre-upload checker while videos published stay 0.
- Lesson: `PERSIST_PUSH_NOT_INSERT_FAILURE` keeps the job green and can still drop the id. The artifact `provider-upload-state` is the recovery copy. Do not dispatch execute again until that file is on main. Do not poll secrets.



## Run 374 — 2026-10-07T02:13:00Z
- Failed approach not retried: exiting 0 on a classify miss before `git add`, or another exchange parser, scanner, or pre-upload checker while videos published stay 0.
- Lesson: a green persist step that skips the commit leaves the video id on the runner. Print `PERSIST_CLASSIFY_MISS_STILL_COMMIT` and commit. Status 2 still skips. Do not poll secrets.

## Run 373 — 2026-10-07T01:15:00Z
- Failed approach not retried: another exchange parser, scanner, or pre-upload checker while videos published stay 0. A spaced `PY` heredoc was not left in the workflow.
- Lesson: swallowing a persist miss is not a push. `<<'PY'` closed by an indented `PY` never runs `push_with_retry`. Call `persist_provider_state.py push`. Do not poll secrets.

## Run 372 — 2026-10-07T00:15:00Z
- Failed approach not retried: another exchange parser, scanner, pre-upload checker, or early-persist call while videos published stay 0. Execute was not dispatched.
- Lesson: swallowing only a rejected commit or push still leaves a classify miss as a red job. Print `PERSIST_PUSH_NOT_INSERT_FAILURE` and exit 0 when a provider video id exists. A miss without that id still fails. Do not dispatch execute again. Do not poll secrets.

## Run 371 — 2026-10-06T23:13:00Z
- Failed approach not retried: another exchange parser, scanner, pre-upload checker, or early-persist call while videos published stay 0. Execute was not dispatched.
- Lesson: swallowing only playlist exit 2 still leaves a crash as a red job. Print `PLAYLIST_INSERT_NOT_UPLOAD_FAILURE` and exit 0 on any non-zero membership exit after upload state exists. Do not leave the summary saying a caption miss exits non-zero after the video id is written. Do not dispatch execute again. Do not poll secrets.

## Run 370 — 2026-10-06T21:16:00Z
- Failed approach not retried: another exchange parser, scanner, pre-upload checker, or early-persist call while videos published stay 0. Execute was not dispatched.
- Lesson: a Studio pin miss or a rejected provider-state push after the video id is written must not fail the job. Print `STUDIO_PIN_NOT_INSERT_FAILURE` or `PERSIST_PUSH_NOT_INSERT_FAILURE` and exit 0. Do not dispatch execute again to retry videos.insert. Do not poll secrets.

## Run 369 — 2026-10-06T19:12:00Z
- Failed approach not retried: another exchange parser, scanner, pre-upload checker, or early-persist call while videos published stay 0. Execute was not dispatched.
- Lesson: a caption, thumbnail, or comment miss after the video id is written must not fail the job. Print `POST_UPLOAD_NOT_INSERT_FAILURE` and exit 0. Do not dispatch execute again to retry videos.insert. Do not poll secrets.

## Run 368 — 2026-10-06T18:12:00Z
- Failed approach not retried: another exchange parser, scanner, or pre-upload checker while videos published stay 0. Execute was not dispatched.
- Lesson: a workflow comment that says exit 2 is not an upload failure does not change the job result. The step must exit 0 after printing `PLAYLIST_INSERT_NOT_UPLOAD_FAILURE`. Do not poll secrets.

## Run 367 — 2026-10-06T17:11:00Z
- Failed approach not retried: another exchange parser, scanner, or pre-upload checker while videos published stay 0. A playlist end-screen element was not requested.
- Lesson: playlist_id not_set must not become a Studio instruction to add a playlist element. Ask for one video element (best for viewer). A failed playlistItems.insert does not mean videos.insert did not run. Do not poll secrets.

## Run 366 — 2026-10-06T16:20:00Z
- Failed approach not retried: another exchange parser, scanner, or pre-upload checker while videos published stay 0.
- Lesson: a second `check_stall_watch` later in selftest replaces the contract call. Keep one definition. Do not poll secrets.

## Run 365 — 2026-10-06T15:20:00Z
- Failed approach not retried: treating `idle_streak: 0` as a stall flag, or leaving STATE.md and NEXT.md over the compact cap.
- Lesson: a count of zero must stay quiet. Print the streak only when it is positive. Compact before the live file exceeds 12 sections. Do not poll secrets.

## Run 364 — 2026-10-06T13:22:00Z
- Failed approach not retried: another exchange parser, scanner, or pre-upload checker while videos published stay 0.
- Lesson: an idle flag without a count still looks like a fresh note. Print `idle_streak`. At 8 or more, print `suspicious: oauth_idle_without_publish`. Do not poll secrets.

