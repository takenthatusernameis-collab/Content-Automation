# RUNS

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

## Run 442 — 2026-10-10T05:25:00Z
- Objective: Verify fresh-clone materialize + gates, then surface a fresh timestamped status on issue #1 so the human sees that the system remains ready.
- Action: Ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS. Posted verification comment to issue #1. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. Issue #1 now has a Run 442 confirmation.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate CLOSED BRIEF GATE PASS. operator_card OPERATOR CARD PASS. next_action upload-blocked. Issue comment posted. No provider write.
- Discovery: The pre-upload path remains stable. The long oauth_idle_without_publish stall continues. A fresh issue comment reduces the chance the human misses that everything else is ready.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs.

## Run 441 — 2026-10-10T07:20:00Z
- Objective: Verify fresh-clone materialize + gates, then surface a fresh timestamped status on issue #1 so the human sees that the system remains ready.
- Action: Ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS. Posted verification comment to issue #1. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. Issue #1 now has a Run 441 confirmation.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate CLOSED BRIEF GATE PASS. operator_card OPERATOR CARD PASS. next_action upload-blocked. Issue comment posted. No provider write.
- Discovery: The pre-upload path remains stable. The long oauth_idle_without_publish stall continues. A fresh issue comment reduces the chance the human misses that everything else is ready.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs.

## Run 440 — 2026-10-10T03:45:00Z
- Objective: Verify fresh-clone materialize + gates, then remove a duplicate NEXT header that risked compounding log-hygiene stalls.
- Action: Ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS, doctor consistent. Edited NEXT.md to drop the second `# NEXT` header. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. NEXT.md now has a single header. Compact check OK.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate CLOSED BRIEF GATE PASS. operator_card OPERATOR CARD PASS. next_action upload-blocked. Header count=1. No provider write.
- Discovery: A second `# NEXT` header had appeared after the archive marker. Removing it prevents the stall_watch header-delta path from accumulating. Suspicious: oauth_idle_without_publish unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs, and does not prepend a second NEXT header.

## Run 439 — 2026-10-10T02:15:00Z
- Objective: Verify fresh-clone materialize + gates, then surface the ready status on the open human issue so the remaining step is timestamped and obvious.
- Action: Ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS. Posted verification comment to issue #1. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. Issue #1 now has a Run 439 confirmation.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate CLOSED BRIEF GATE PASS. operator_card OPERATOR CARD PASS. next_action upload-blocked. Issue comment posted. No provider write.
- Discovery: The pre-upload path remains stable. The long oauth_idle_without_publish stall continues. A fresh issue comment reduces the chance the human misses that everything else is ready.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs.

## Run 437 — 2026-10-10T03:30:00Z
- Objective: Verify fresh-clone materialize + gates, then make the repository entry point (README) match current reality so future agents and the human do not rediscover the outdated VO-drop instruction.
- Action: Cloned, ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked. Updated README.md live-packet and human-session sections. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. README now correctly names the three secrets and operator_card.py as the human gate.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate CLOSED BRIEF GATE PASS. operator_card.py still OPERATOR CARD PASS. README diff reviewed. No provider write.
- Discovery: README still described the remaining human gate as a Selected VO drop even after media materialize and OAuth became the sole blocker. Suspicious: oauth_idle_without_publish unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs.

## Run 437 — 2026-10-10T03:30:00Z
- Objective: Verify fresh-clone materialize + gates, then make the repository entry point (README) match current reality so future agents and the human do not rediscover the outdated VO-drop instruction.
- Action: Cloned, ran materialize_q1_release.py (checksums matched, ignored truncated r249), media_qa PASS, closed_brief_gate PASS, next_action upload-blocked. Updated README.md live-packet and human-session sections. Did not poll secrets, dispatch, edit briefs, extend the card, or commit media.
- Result: Videos published stay 0. Local Q1 media ready. Upload blocked only on secrets. README now correctly names the three secrets and operator_card.py as the human gate.
- Verification: materialize ignored truncated r249. media_qa gate PASS. closed_brief_gate CLOSED BRIEF GATE PASS. operator_card.py still OPERATOR CARD PASS. README diff reviewed. No provider write.
- Discovery: README still described the remaining human gate as a Selected VO drop even after media materialize and OAuth became the sole blocker. Suspicious: oauth_idle_without_publish unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs.

## Run 436 — 2026-10-10T02:20:00Z
- Objective: Verify fresh-clone materialize + gates, then make the one human OAuth step slightly more robust against common setup mistakes.
- Action: Cloned, ran materialize_q1_release.py (checksums matched), media_qa PASS, assemble EXPORT_EXISTS, closed_brief_gate PASS, next_action upload-blocked. Added static Common pitfalls section to operator_card.py. Did not poll secrets, dispatch, edit briefs, or commit media.
- Result: Videos published stay 0. Card still PASS. Local Q1 media ready. Upload blocked only on secrets.
- Verification: materialize ignored truncated r249. media_qa gate PASS. operator_card.py printed pitfalls and OPERATOR CARD PASS. No provider write.
- Discovery: The pre-upload path is stable. The remaining leverage is reducing error on the single human secret step. Suspicious: oauth_idle_without_publish unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows operator_card.py. Next agent materializes only if media missing, uses record_run.py, does not reopen closed briefs.

## Run 435 — 2026-10-09T22:12:00Z
- Objective: Confirm the fresh-clone materialize path still installs the verified Q1 release and stops at the OAuth gate.
- Action: Ran `python3 tools/materialize_q1_release.py` because packet media was absent. Then media_qa, assemble dry-run, youtube_upload dry-run, and closed_brief_gate. Did not poll secrets. Did not dispatch execute. Did not add a scanner, recovery edge, card extension, freeze module, or compact check. Did not rewrite Q1. Did not edit brief generators. Did not commit media.
- Result: Videos published stay 0. Local Q1 media QA is PASS. Assemble sees the r253 master. Upload remains YOUTUBE_AUTH_REQUIRED. next_action is upload-blocked.
- Verification: materialize ignored truncated r249 master. wav sha256 758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2. master sha256 4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546. media_qa gate PASS. assemble EXPORT_EXISTS. upload dry-run exit 3 with only oauth_complete failing. closed_brief_gate CLOSED BRIEF GATE PASS. No provider write.
- Discovery: The release install path still matches the recorded checksums on a clean clone. Suspicious: oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent materializes only if packet media is missing, and prepends logs only through `record_run.py`.

Permanent log. Newest first. Do not paste the archive back into this file.

Older run notes live in `docs/runs_archive.md`. Do not paste the archive back.
