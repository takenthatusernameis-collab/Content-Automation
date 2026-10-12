# RUNS

## Run 494 — 2026-10-12T14:20:00Z
- Objective: Reduce rediscovery of the exact observation window timing by embedding the precise calculation (uploaded_at + 7 calendar days + 3 days Analytics lag = due at +10 days) in the primary status_report.py after-dispatch section.
- Action: Updated tools/status_report.py to print the exact due_at formula and OBSERVATION_WINDOW_NOT_DUE note. Updated preferred-list note. Prepended logs. Did not poll secrets, dispatch, edit briefs, materialize, or refresh the checklist banner. Local gates not re-run (media absent).
- Result: Videos published stay 0. Primary status command now surfaces the precise window timing without opening youtube_feedback.py. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: File update committed. status_report.py contains the new timing line. No gate re-run claimed.
- Discovery: Explicit 7+3 lag formula in the primary status printer reduces the chance future agents open youtube_feedback.py or workflow comments solely to learn the observation due date.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, prioritizes the human step or a truly new small anti-rediscovery item that introduces reusable capability, does not invent data or expand locked surfaces, and does not refresh the banner solely for its timestamp.

## Run 493 — 2026-10-12T10:45:00Z
- Objective: Reduce rediscovery of the secret confirmation method by embedding the forbidden `gh secret list` reminder and the optional human_secret_confirm.py command in the primary status_report.py human step section.
- Action: Materialized Q1 media locally (not committed). Re-ran media_qa (PASS), next_action (upload-blocked), confirmed master SHA MATCH, closed_brief_gate (PASS), selftest (PASS). Updated tools/status_report.py to print the confirmation notes and refreshed last_gates_confirmed to Run 493. Updated preferred-list note. Prepended logs via record_run.py. Did not poll secrets, dispatch, edit briefs, or refresh the checklist banner.
- Result: Videos published stay 0. Primary status command now surfaces the exact confirmation method without opening the checklist or operator_card. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: python3 tools/status_report.py shows the new confirmation lines in the human step section after materialize. media_qa PASS. next_action upload-blocked. SHA MATCH. selftest PASS. next_compact_contract PASS.
- Discovery: Explicit confirmation method in the primary status printer reduces the chance future agents open docs/human_oauth_checklist.md or operator_card solely to learn how to confirm secrets or avoid forbidden commands.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, prioritizes the human step or a truly new small anti-rediscovery item that introduces reusable capability, does not invent data or expand locked surfaces, and does not refresh the banner solely for its timestamp.
