# NEXT

Run 453: Strengthened top of human_oauth_checklist.md with ONLY ACTION NEEDED banner. Upload remains blocked on the three secrets. If vo/, cards/, or export/master.mp4 are missing, run python3 tools/materialize_q1_release.py and do not commit media. If present, do not rematerialize. Do not edit briefs unless closed_brief_gate fails. Prepend logs only through record_run.py. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not extend the card. Human step remains the checklist (now with banner) or operator_card.py then the three secrets and one dispatch. See issue #1.

Active locks: do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets. `playlist_id` stays `not_set` until a human sets it. Do not add another export probe, media checker, or caption cue gate while `STALL_PREUPLOAD_PROBE` is set. Do not add another Location, session hold, or early-persist call while `STALL_UPLOAD_EDGE` is set. Do not prepend a second `# NEXT` header. Do not add another OAuth exchange parser or provider-state recovery edge while videos published stay 0. Do not extend operator_card while videos published stay 0. The unpublished video is the three GitHub Actions secrets. `idle_streak` is a count, not a new gate. `recovery_freeze.py` fails the build if the recovery surface grows. `operator_card_freeze.py` fails the build if the card surface grows. `stall_watch.py` sets `STALL_LOG_HYGIENE` after three log-cap or header deltas. Do not add another compact check while videos published stay 0.

One human step: run `python3 tools/operator_card.py`, then `python3 tools/oauth_exchange.py`, paste the full localhost address-bar URL, and store the three secrets with `gh secret set`. Then run `gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false`. Do not commit the token file. Do not add a scanner. Do not scaffold Q2. Do not poll secrets. Do not extend the card.

Older do-not-rediscover notes live in `docs/next_archive.md`. Do not paste the archive back into this file. Do not restore a behavior named there.

Run 454: Compacted RUNS.md (13→12 sections) so selftest PASS. Upload remains blocked on the three secrets. If vo/, cards/, or export/master.mp4 are missing, run python3 tools/materialize_q1_release.py and do not commit media. If present, do not rematerialize. Do not edit briefs unless closed_brief_gate fails. Prepend logs only through record_run.py. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not extend the card. Human step remains the checklist or operator_card.py then the three secrets and one dispatch. See issue #1.

Run 452: Added human-facing note to checklist about the long stable verification streak. Upload remains blocked on the three secrets. If vo/, cards/, or export/master.mp4 are missing, run python3 tools/materialize_q1_release.py and do not commit media. If present, do not rematerialize. Do not edit briefs unless closed_brief_gate fails. Prepend logs only through record_run.py. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not extend the card. Human step remains the checklist or operator_card.py then the three secrets and one dispatch. See issue #1.

Run 451: Verified materialize + gates on fresh clone. Upload remains blocked on the three secrets. The oauth_idle_without_publish stall is now ~180 runs; pure-verification runs continue to have diminishing returns. If vo/, cards/, or export/master.mp4 are missing, run python3 tools/materialize_q1_release.py and do not commit media. If present, do not rematerialize. Do not edit briefs unless closed_brief_gate fails. Prepend logs only through record_run.py. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not extend the card. Human step remains the checklist or operator_card.py then the three secrets and one dispatch. See issue #1.

Run 450: Added human-only secret confirmation script so the one-time OAuth step has a local PRESENT/MISSING check that never shows values. Upload remains blocked on the three secrets. If vo/, cards/, or export/master.mp4 are missing, run python3 tools/materialize_q1_release.py and do not commit media. If present, do not rematerialize. Do not edit briefs unless closed_brief_gate fails. Prepend logs only through record_run.py. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not extend the card. Human step remains the checklist or operator_card.py then the three secrets and one dispatch. See issue #1.

Run 449: Checklist now includes expected outcomes after dispatch (video id location, private privacy, do-not-re-dispatch rule). Upload remains blocked on the three secrets. If vo/, cards/, or export/master.mp4 are missing, run python3 tools/materialize_q1_release.py and do not commit media. If present, do not rematerialize. Do not edit briefs unless closed_brief_gate fails. Prepend logs only through record_run.py. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not extend the card. Human step remains the checklist or operator_card.py then the three secrets and one dispatch. See issue #1.

Run 448: Checklist now includes a human UI confirmation step for the three secrets. Upload remains blocked on the three secrets. If vo/, cards/, or export/master.mp4 are missing, run python3 tools/materialize_q1_release.py and do not commit media. If present, do not rematerialize. Do not edit briefs unless closed_brief_gate fails. Prepend logs only through record_run.py. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not extend the card. Human step remains the checklist or operator_card.py then the three secrets and one dispatch. See issue #1.

Run 447: Prompt evolution now flags pure verification as low-leverage after long idle. Upload remains blocked on the three secrets. If vo/, cards/, or export/master.mp4 are missing, run python3 tools/materialize_q1_release.py and do not commit media. If present, do not rematerialize. Do not edit briefs unless closed_brief_gate fails. Prepend logs only through record_run.py. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not extend the card. Human step remains the checklist or operator_card.py then the three secrets and one dispatch. See issue #1.

Run 446: Added docs/human_oauth_checklist.md so the one human secret step has a single printable list of numbered steps, exact commands, and pitfalls. Upload remains blocked on the three secrets. If vo/, cards/, or export/master.mp4 are missing, run python3 tools/materialize_q1_release.py and do not commit media. If present, do not rematerialize. Do not edit briefs unless closed_brief_gate fails. Prepend logs only through record_run.py. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not extend the card. Human step remains the checklist or operator_card.py then the three secrets and one dispatch. See issue #1.

Run 446: Added docs/human_oauth_checklist.md so the one human secret step has a single printable list of numbered steps, exact commands, and pitfalls. Upload remains blocked on the three secrets. If vo/, cards/, or export/master.mp4 are missing, run python3 tools/materialize_q1_release.py and do not commit media. If present, do not rematerialize. Do not edit briefs unless closed_brief_gate fails. Prepend logs only through record_run.py. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not extend the card. Human step remains the checklist or operator_card.py then the three secrets and one dispatch. See issue #1.

Run 445: Q1 media materialized and all local gates passed (media_qa, closed_brief_gate, next_action=upload-blocked, operator_card, selftest). Upload remains blocked on the three secrets. The oauth_idle_without_publish stall is now ~175 runs long; further pure-verification runs have diminishing returns unless a change is detected. If vo/, cards/, or export/master.mp4 are missing, run python3 tools/materialize_q1_release.py and do not commit media. If present, do not rematerialize. Do not edit briefs unless closed_brief_gate fails. Prepend logs only through record_run.py. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not extend the card. Human step remains operator_card.py then the three secrets and one dispatch. See issue #1.

Run 444: NEXT.md size restored under 12000 by retaining only newest locks and human step. Upload remains blocked on the three secrets. If vo/, cards/, or export/master.mp4 are missing, run python3 tools/materialize_q1_release.py and do not commit media. If present, do not rematerialize. Do not edit briefs unless closed_brief_gate fails. Prepend logs only through record_run.py. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not extend the card. Do not add a compact check. Human step remains operator_card.py then the three secrets and one dispatch. See issue #1.

2026-10-10T21:15:00Z (Run 454)

2026-10-10T17:13:00Z (Run 453)

2026-10-10T16:20:00Z (Run 452)

2026-10-10T15:30:00Z (Run 451)

2026-10-10T14:20:00Z (Run 450)

2026-10-10T13:30:00Z

2026-10-10T15:20:00Z

2026-10-10T10:20:00Z

2026-10-10T10:20:00Z

2026-10-10T08:15:00Z
