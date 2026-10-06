# FAILURES

Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.

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

## Run 363 — 2026-10-06T12:20:00Z
- Failed approach not retried: another exchange parser, scanner, or pre-upload checker while videos published stay 0.
- Lesson: a progress line that omits the Run heading is invisible to log compact and can be cut with the previous section. Promote that shape. Do not poll secrets.

## Run 362 — 2026-10-06T11:20:00Z
- Failed approach not retried: another exchange parser, scanner, or pre-upload checker while videos published stay 0. Dispatch was not run.
- Lesson: naming execute=true is not the command. Print the `gh workflow dispatch` line and keep collect_feedback false on the first dispatch. Do not poll secrets.

## Run 361 — 2026-10-06T10:12:00Z
- Failed approach not retried: another exchange parser, scanner, or pre-upload checker while videos published stay 0.
- Lesson: a do-not-add sentence is not a wired probe. Scrub it before the stall token check. A last chapter inside the final 10 seconds is ignored by YouTube. Refuse that shape when duration is known. Do not invent duration.

## Run 360 — 2026-10-06T09:11:00Z
- Failed approach not retried: another OAuth exchange parser, export probe, media checker, or caption cue gate while videos published stay 0.
- Lesson: Runs 358-359 scripted the token exchange and published nothing. A second Active locks block hid the same human step. Collapse the copy. Do not add another exchange parser.

## Run 359 — 2026-10-06T08:11:00Z
- Failed approach not retried: another export probe, media checker, or caption cue gate while `STALL_PREUPLOAD_PROBE` is set. Polling secrets was not the run.
- Lesson: a pasted localhost redirect is the normal Desktop consent result. Extract the code. Do not print it. Do not treat a raw-code-only exchange as finished.

## Run 358 — 2026-10-06T07:15:00Z
- Failed approach not retried: another export probe, media checker, or caption cue gate while `STALL_PREUPLOAD_PROBE` is set. Polling secrets was not the run.
- Lesson: the remaining human step was an unscripted token exchange. Script the exchange and refuse a repo path. Do not print the token.

## Run 357 — 2026-10-06T06:20:00Z
- Failed approach not retried: another export probe, media checker, or caption cue gate while `STALL_PREUPLOAD_PROBE` is set.
- Lesson: a second `# FAILURES` or `# PROGRESS` header is the same cut-fetch bug as a second STATE header. Collapse it in log compact. Do not finish a STATE bullet with the header token the contract counts.

## Run 356 — 2026-10-06T05:11:00Z
- Failed approach not retried: another export probe, media checker, or caption cue gate while `STALL_PREUPLOAD_PROBE` is set.
- Lesson: prepending a whole `# STATE` file looked like a log update and left a dangling header. Compact must collapse headers. Do not treat a second header as a new gate.

