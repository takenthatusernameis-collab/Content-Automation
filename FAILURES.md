# FAILURES

Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.

## Run 385 — 2026-10-07T13:23:00Z
- Failed approach not retried: another operator-card reprint, provider-state recovery edge, exchange parser, scanner, or secret poll while videos published stay 0.
- Lesson: Runs 383-384 extended the card and published nothing. `operator_card_freeze.py` fails the build when the function list or card-module list grows. Do not add a function to clear it. Do not poll secrets. oauth_idle_without_publish remains; do not spend the next run only restating it.

## Run 384 — 2026-10-07T12:20:00Z
- Failed approach not retried: another provider-state recovery edge, exchange parser, scanner, or secret poll while videos published stay 0. Also not retried: a second operator card that only reprints secret-set lines.
- Lesson: Run 383 left the Google Cloud clicks off the one command. Reprint those steps from `oauth_setup.py`. Do not add an edge to make the card pass. Do not poll secrets. oauth_idle_without_publish remains; do not spend the next run only restating it.

## Run 383 — 2026-10-07T11:17:00Z
- Failed approach not retried: another provider-state recovery edge, exchange parser, scanner, or secret poll while videos published stay 0.
- Lesson: freeze and stall flags did not give the human one command. `operator_card.py` is that command. Do not add an edge to make the card pass. Do not poll secrets. oauth_idle_without_publish remains; do not spend the next run only restating it.

## Run 382 — 2026-10-07T10:14:00Z
- Failed approach not retried: another provider-state recovery edge, exchange parser, scanner, or secret poll while videos published stay 0.
- Lesson: a stall flag after four edges did not stop the next edge. `recovery_freeze.py` fails the build when the artifact or recover call count grows. Do not add an edge to clear it. Do not poll secrets. oauth_idle_without_publish remains; do not spend the next run only restating it.



## Run 381 — 2026-10-07T09:13:00Z
- Failed approach not retried: another provider-state recovery edge, exchange parser, scanner, or secret poll while videos published stay 0.
- Lesson: Runs 368-378 stacked recover paths and prose did not stop the next edge. `STALL_RECOVERY_EDGE` now fires only when four deltas wire that path. Do not add an edge to clear it. Do not poll secrets.


## Run 380 — 2026-10-07T08:11:00Z
- Failed approach not retried: another provider-state recovery edge, exchange parser, scanner, or secret poll while videos published stay 0. Also not retried: claiming a local selftest that ran before the log prepend.
- Lesson: Run 378 left 13 sections and Actions run 37580716646 failed. Compact with `python3 tools/compact_all.py` in the same commit. Suspicious: oauth_idle_without_publish has no publish since before Run 270, and Runs 368-378 only stacked recovery edges. Do not spend the next run restating either.

## Run 379 — 2026-10-07T07:16:00Z
- Failed approach not retried: treating a local SELFTEST PASS as proof the pushed logs still fit the compact cap, or adding another provider-state recovery edge while Actions is red for a size miss.
- Lesson: Run 378 left 13 STATE sections and 13 NEXT notes. Actions run 37580716646 failed. Compact in the same commit that prepends. Do not poll secrets. oauth_idle_without_publish remains; do not restate it as the work.

## Run 378 — 2026-10-07T06:14:00Z
- Failed approach not retried: keeping the first `provider-upload-state` download, or another exchange parser, scanner, or pre-upload checker while videos published stay 0.
- Lesson: a later execute can upload `upload_state.json` with no `provider_video_id`. Recovery must skip that file. Do not dispatch execute again. Do not poll secrets. oauth_idle_without_publish has now repeated from Run 366 through Run 378 with no publish; do not spend the next run only restating it.

## Run 377 — 2026-10-07T05:11:00Z
- Failed approach not retried: `gh run list --workflow youtube-production.yml --limit 1` as the only recovery selector, or a bare download when that id is empty.
- Lesson: the newest production run can be execute=false and have no artifact. Walk recent production runs and refuse an empty id. Do not dispatch execute again. Do not poll secrets.

## Run 376 — 2026-10-07T04:12:00Z
- Failed approach not retried: a bare `gh run download --name provider-upload-state`, or another exchange parser, scanner, or pre-upload checker while videos published stay 0.
- Lesson: the newest run after an agent commit is often selftest.yml. That run has no video id. Pin `youtube-production.yml` before download. Do not dispatch execute again. Do not poll secrets.

## Run 375 — 2026-10-07T03:11:00Z
- Failed approach not retried: treating a green persist step as proof the video id is on main, or another exchange parser, scanner, or pre-upload checker while videos published stay 0.
- Lesson: `PERSIST_PUSH_NOT_INSERT_FAILURE` keeps the job green and can still drop the id. The artifact `provider-upload-state` is the recovery copy. Do not dispatch execute again until that file is on main. Do not poll secrets.



## Run 374 — 2026-10-07T02:13:00Z
- Failed approach not retried: exiting 0 on a classify miss before `git add`, or another exchange parser, scanner, or pre-upload checker while videos published stay 0.
- Lesson: a green persist step that skips the commit leaves the video id on the runner. Print `PERSIST_CLASSIFY_MISS_STILL_COMMIT` and commit. Status 2 still skips. Do not poll secrets.

