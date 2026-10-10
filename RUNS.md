# RUNS

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

## Run 434 — 2026-10-09T21:13:00Z
- Objective: Restore the green selftest after Run 433 left STATE.md over the 12-section cap.
- Action: Confirmed Actions run 37986179006 failed on `compact_all --check` and `state_compact_contract` (STATE=13). Ran `state_compact.py`, then recorded this note with `record_run.py` so compact happens in the same process. Did not poll secrets. Did not dispatch execute. Did not add a scanner, recovery edge, card extension, freeze module, or compact check. Did not rewrite Q1. Did not edit brief generators. Did not rematerialize media.
- Result: Videos published stay 0. STATE.md is back at the cap. The human OAuth step is unchanged.
- Verification: failed log names `STATE.md has 13 sections, max 12`. After compact, `compact_all.py --check` must print COMPACT ALL OK. No provider write.
- Discovery: Run 433 verified media locally and still shipped a red selftest by skipping `record_run.py`. Suspicious: oauth_idle_without_publish is unchanged since before Run 270. Log-cap misses are the second repeating no-progress pattern.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent materializes only if packet media is missing, and prepends logs only through `record_run.py`.

## Run 433 — 2026-10-09T20:20:00Z
- Objective: Advance the live Q1 packet past the ignored-media gap instead of another brief edit.
- Action: Ran `python3 tools/materialize_q1_release.py`. Then `media_qa.py`, `assemble.py` dry-run, and `youtube_upload.py` dry-run. Closed brief gate still passed. Pointed `next_action.py` and `hint.py` at materialize when packet media is missing, and at operator_card only when it is present. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, freeze module, or compact check. Did not rewrite Q1 markdown. Did not commit media.
- Result: Videos published stay 0. Local Q1 media QA is PASS. Assemble sees the r253 master. Upload remains YOUTUBE_AUTH_REQUIRED.
- Verification: materialize printed ignored truncated r249 master, 7 cards, and r253 master path. media_qa gate PASS. assemble EXPORT_EXISTS. upload dry-run exit 3 with only oauth_complete failing. closed_brief_gate CLOSED BRIEF GATE PASS. next_action returned materialize-q1 when vo/ was moved aside, then upload-blocked after restore. No provider write.
- Discovery: Fresh clones look like missing Selected VO even though releases are complete. Agents that only read the old upload-blocked sentence skip materialize and reopen closed brief stubs. Suspicious: oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`, stores the three secrets, then dispatches execute=true. Next agent materializes only if packet media is missing.

## Run 432 — 2026-10-09T18:12:00Z
- Objective: Stop the next agent from re-hand-rolling the Run 431 verification and inventing another brief edit.
- Action: Added `tools/closed_brief_gate.py` and a selftest hook. The gate runs publish, chapter, caption, asset, and title contracts, then title dry-runs for charger-before, phone-where, and notebook-and. Did not edit those generators. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, freeze module, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Closed brief rules stayed closed. No packet file changed.
- Verification: `python3 tools/closed_brief_gate.py` printed CLOSED BRIEF GATE PASS. `check_closed_brief_gate()` returned no failures. No provider write.
- Discovery: The Run 431 checks were still a manual sequence. One command now fails only if a named rule fails. Suspicious: oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/closed_brief_gate.py` and stop if it passes.

## Run 431 — 2026-10-09T16:14:00Z
- Objective: Verify the Run 430 publish contract and the closed chapter, caption, and asset rules before any brief edit.
- Action: `publish_brief_contract.py`, `chapter_draft_contract.py`, `caption_brief_contract.py`, and `asset_brief_contract.py` passed. Title dry-runs for a charger-before packet, a phone-where packet, and a notebook-and packet printed SELF_CHECK PASS. Did not edit those generators. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, freeze module, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Closed brief rules stayed closed. No packet file changed.
- Verification: four brief contracts PASS. Three later-packet title dry-runs SELF_CHECK PASS. `record_run.py` compact path used. No provider write.
- Discovery: A when-clause problem still becomes one If, which is readable and not the double-If leak. Unfinished trailing and/because in a title was already clipped. Suspicious: oauth_idle_without_publish is unchanged since before Run 270. Brief-stub microfixes 420-430 have no new failed dry-run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should not edit a brief generator unless a dry-run fails the rule named in NEXT.md.

## Run 430 — 2026-10-09T15:20:00Z
- Objective: Verify the Run 429 chapter contract, then fix only a real later-packet dry-run failure outside the closed chapter rules.
- Action: `chapter_draft_contract.py` passed. Later-packet chapter lines kept not and did not end on so or without. Did not edit chapter_draft. Asset and caption contracts passed. Those stubs were not edited. Publish contract passed, then a later-packet problem `The inbox reopens if the lid stays up` still printed `If the inbox reopens if the lid stays up`. A problem that already contains if is no longer wrapped. Contract covers that packet. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Nested if problems stay one clause. Q1 publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS after the edit. `python3 tools/chapter_draft_contract.py` PASS. No provider write.
- Discovery: Keeping a so-clause did not cover a problem that already said if. Suspicious: oauth_idle_without_publish is unchanged since before Run 270. Publish-stub work resumes only on that named machine sentence.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/publish_brief_contract.py` before any new publish edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit chapter_draft, asset_brief, or caption_brief again unless a dry-run still fails the rule named in NEXT.md.

## Run 429 — 2026-10-09T14:20:00Z
- Objective: Verify Run 428 chapter contract, then fix only a real later-packet dry-run failure outside the closed negation and on-screen rules.
- Action: `chapter_draft_contract.py` passed. Asset, caption, and publish contracts passed. Those stubs were not edited. Title dry-run passed SELF_CHECK. Chapter dry-run still ended `Notebook stays bag so` and `Next block starts without`. Unfinished so/without/before/after/until/because are now dropped. Contract covers that packet. NEXT.md was 12644 bytes; older notes moved to the archive so the 12000 cap holds. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Later-packet chapter lines no longer end on so or without. Q1 chapters.md unchanged.
- Verification: `python3 tools/chapter_draft_contract.py` PASS after the edit. Later-packet chapter line is `0:00 Do not reopen inbox`. No provider write.
- Discovery: Keeping not did not stop a title from ending on the next glue word. Suspicious: oauth_idle_without_publish is unchanged since before Run 270. Chapter-stub microfixes now span runs 428-429.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/chapter_draft_contract.py` before any new chapter edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit asset_brief, caption_brief, or publish_brief again unless a dry-run still fails the rule named in NEXT.md.

Permanent log. Newest first. Do not paste the archive back into this file.

Older run notes live in `docs/runs_archive.md`. Do not paste the archive back.
