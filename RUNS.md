# RUNS

## Run 454 — 2026-10-10T21:15:00Z
- Objective: Restore green selftest by compacting RUNS.md that had accumulated a 13th section past the max-12 cap.
- Action: Ran tools/runs_compact.py which moved the oldest entry to docs/runs_archive.md. Verified compact_all --check OK and selftest PASS. Did not poll secrets, dispatch, edit briefs, extend the card, rematerialize, or commit media.
- Result: Videos published stay 0. Selftest green. Upload blocked only on secrets. Log hygiene restored without new tools.
- Verification: runs_compact moved=1. compact_all --check COMPACT ALL OK. selftest SELFTEST PASS. next_action reports materialize-q1 (media absent on clone).
- Discovery: Live logs can drift over the section cap between runs; compacting in the recording path prevents a red selftest on the next push.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and prefers non-verification work.

## Run 453 — 2026-10-10T17:13:00Z
- Objective: Reduce rediscovery cost of the long OAuth stall by making the single remaining human action unmistakable at the top of the existing checklist.
- Action: Added an explicit ONLY ACTION NEEDED banner to the top of docs/human_oauth_checklist.md stating that ~180 verified runs have confirmed readiness and the three secrets + one dispatch are the sole remaining step. Updated the note. Did not poll secrets, dispatch, edit briefs, extend the card, rematerialize, or commit media.
- Result: Videos published stay 0. Checklist now opens with the unambiguous status. Upload blocked only on secrets.
- Verification: Checklist file updated and committed. No provider write. No new tool surface.
- Discovery: The long stall continues; a prominent banner in the document humans are directed to reduces the chance both humans and agents restate readiness instead of completing the one action.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md (now with the banner) or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and prefers non-verification work if any unblocked path exists.

## Run 452 — 2026-10-10T16:20:00Z
- Objective: Reduce the chance of continued low-leverage pure-verification agent runs by adding an explicit human-facing note that the path has been verified ~180 times and only the secrets advance the system.
- Action: Materialized Q1 (checksums matched, ignored truncated r249). Verified media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS. Appended note to docs/human_oauth_checklist.md. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Checklist now explicitly tells the human that further agent verification is low-leverage. Upload blocked only on secrets.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate PASS. next_action upload-blocked. operator_card PASS.
- Discovery: The long stall continues; a human-facing reminder reduces the chance agents keep restating readiness without the human acting.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and prefers non-verification work if any unblocked path exists.

## Run 451 — 2026-10-10T15:30:00Z
- Objective: Confirm Q1 materialize + local gates on a fresh clone and record that the long OAuth stall continues so future agents treat pure verification as low-leverage.
- Action: Ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS, selftest PASS. Used record_run.py. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. Stall duration noted.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate PASS. next_action upload-blocked. operator_card PASS. selftest PASS.
- Discovery: Pre-upload path remains stable. oauth_idle_without_publish stall is unchanged and now ~180 runs. Pure verification has diminishing returns.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and prefers non-verification work if any unblocked path exists.

## Run 450 — 2026-10-10T14:20:00Z
- Objective: Reduce human setup error on the remaining OAuth secret step by adding a human-only confirmation script that reports PRESENT/MISSING without values.
- Action: Materialized Q1 (checksums matched, ignored truncated r249). Verified media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS, selftest PASS. Created tools/human_secret_confirm.py (explicitly for human terminal use only). Linked it as optional step 7c in docs/human_oauth_checklist.md. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Human now has a local script that confirms the three secrets exist without printing values. Upload blocked only on secrets.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate PASS. next_action upload-blocked. operator_card PASS. selftest PASS. New script exits non-zero when secrets absent (expected). Checklist updated.
- Discovery: The long stall continues; a human-only confirm tool reduces one class of "I set them but they are not visible" mistakes.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md (including optional 7c) or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and prefers non-verification work.

## Run 449 — 2026-10-10T13:30:00Z
- Objective: Clarify what success looks like after the human sets the three secrets and dispatches once, reducing post-setup confusion.
- Action: Materialized Q1 (checksums matched, ignored truncated r249). Verified media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS, selftest PASS. Added Expected outcomes section to docs/human_oauth_checklist.md. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Checklist now states where the video id appears and the do-not-re-dispatch rule. Upload blocked only on secrets.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate PASS. next_action upload-blocked. operator_card PASS. selftest PASS. Checklist diff reviewed.
- Discovery: The long stall continues; documenting expected outcomes reduces one class of human uncertainty after the secrets are finally set.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and prefers non-verification work.

## Run 448 — 2026-10-10T15:20:00Z
- Objective: Slightly harden the one-time human OAuth step against a common omission (not confirming secrets in the UI) and record that local gates still pass.
- Action: Materialized Q1 (checksums matched, ignored truncated r249). Verified media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS. Added UI confirmation step and one pitfall to docs/human_oauth_checklist.md. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Checklist is marginally clearer. Upload blocked only on secrets.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate PASS. next_action upload-blocked. operator_card PASS. Checklist diff reviewed.
- Discovery: The long stall continues; a small checklist clarification reduces one class of human setup mistake.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and prefers non-verification work.

## Run 447 — 2026-10-10T14:16:00Z
- Objective: Codify the lesson from the ~175-run OAuth idle stall so future agents treat pure verification as low-leverage and prefer small tool or clarity improvements.
- Action: Materialized Q1 (checksums matched). Verified media_qa PASS, closed_brief_gate PASS, next_action upload-blocked. Appended evidence lesson to PROMPT_EVOLUTION.md. Prepended targeted note to NEXT_RUN_PROMPT.md. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. Future operating prompts now explicitly deprioritize pure-verification runs.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate PASS. next_action upload-blocked. Files updated without media commit.
- Discovery: The long stall continues; documenting diminishing returns of verification reduces the chance of another 10 identical runs.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and prefers non-verification work.

## Run 446 — 2026-10-10T10:20:00Z
- Objective: Add a printable human OAuth checklist so the remaining one-time secret step is harder to mis-execute.
- Action: Created docs/human_oauth_checklist.md with numbered steps, exact commands, pitfalls, and success criteria. Pointed operator_card.py at it. Did not poll secrets, dispatch, edit briefs, or commit media.
- Result: Videos published stay 0. Local gates still PASS. Human now has a single checklist document in addition to the operator card.
- Verification: operator_card still prints OPERATOR CARD PASS and includes the checklist pointer. selftest PASS.
- Discovery: The long oauth_idle_without_publish stall continues; a consolidated checklist reduces the chance of a setup mistake when the human finally acts.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and prefers non-verification work.

## Run 445 — 2026-10-10T09:14:00Z
- Objective: Confirm Q1 materialize + all local gates on a clean clone, then record that the long OAuth stall continues so future agents treat pure verification as low-leverage.
- Action: Ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS, selftest PASS. Used record_run.py. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. Stall duration noted.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate PASS. operator_card PASS. next_action upload-blocked. selftest PASS. No provider write.
- Discovery: Pre-upload path remains stable. oauth_idle_without_publish stall is unchanged and now ~175 runs. Pure verification has diminishing returns.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and prefers non-verification work if any unblocked path exists.

## Run 444 — 2026-10-10T07:30:00Z
- Objective: Restore green selftest by compacting oversized NEXT.md that had accumulated near-identical run notes past the 12000-byte cap.
- Action: Materialized Q1 (checksums matched, ignored truncated r249). Verified media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS. Rewrote NEXT.md to keep only essential Active locks, human step, and two newest run notes; moved prior content to docs/next_archive.md. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Selftest now PASS. Upload blocked only on secrets.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate PASS. operator_card PASS. next_action upload-blocked. next_compact_contract PASS. compact_all --check OK. selftest PASS. No provider write.
- Discovery: NEXT.md item parser only treats digit-starting blocks as archivable items; Run NNN: paragraphs accumulate in preamble and can exceed the byte cap. Cleaning restores the truncated-fetch guarantee.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and keeps NEXT under the size cap.

## Run 443 — 2026-10-10T06:17:00Z
- Objective: Verify fresh-clone materialize + gates, then surface a fresh timestamped status on issue #1 so the human sees that the system remains ready.
- Action: Ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS. Posted verification comment to issue #1. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. Issue #1 now has a Run 443 confirmation.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate CLOSED BRIEF GATE PASS. operator_card OPERATOR CARD PASS. next_action upload-blocked. Issue comment posted. No provider write.
- Discovery: The pre-upload path remains stable. The long oauth_idle_without_publish stall continues. A fresh issue comment reduces the chance the human misses that everything else is ready.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs.

Permanent log. Newest first. Do not paste the archive back into this file.

Older run notes live in `docs/runs_archive.md`. Do not paste the archive back.
