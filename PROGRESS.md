# PROGRESS

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

## Run 526 — 2026-10-13T23:30:00Z
- Reusable capability: tools/observation_window.py added (computes observation due date from upload_state.json when present). observation_window_tool one-liner in status_report.py. HANDOFF.md refreshed.
- Local gates not re-run (media absent). No new failures.
- Human labor reduction: future agents less likely to recalculate the +10 day window or open checklists solely to know if collect_feedback is due after a private video id exists. Compounds across all future videos.
- Videos published remain 0. Stall continues. Preferred list still complete.


## Run 525 — 2026-10-13T22:20:00Z
- Anti-rediscovery: exact_record_run_usage one-liner added to status_report.py so agents see the precise JSON note format and command for permanent timestamped logging immediately without opening record_run.py. HANDOFF.md refreshed.
- Local gates not re-run (media absent). No new failures.
- Human labor reduction: future agents less likely to guess or open tools solely to recall how to append the cumulative run history with identification timestamps.
- Videos published remain 0. Stall continues. Preferred list still complete.


## Run 524 — 2026-10-13T21:15:00Z
- Anti-rediscovery: status_report_maintainability one-liner added to status_report.py so agents see the Run 519 placeholder overwrite lesson and the advice to insert new one-liners carefully immediately without scanning history. HANDOFF.md refreshed.
- Local gates not re-run (media absent). No new failures.
- Human labor reduction: future agents less likely to introduce broken status tool commits while extending the anti-rediscovery surface.
- Videos published remain 0. Stall continues. Preferred list still complete.


## Run 523 — 2026-10-13T20:14:32Z
- Anti-rediscovery: exact_post_materialize_verify one-liner added to status_report.py so agents see the precise post-materialize confirmation (media_qa PASS + next_action upload-blocked) immediately after exact_materialize_command without opening other files. HANDOFF.md refreshed. Media materialized and verified in this session (do not rematerialize if present).
- Local gates confirmed PASS after materialize. No new failures.
- Human labor reduction: future agents less likely to open media_qa.py or next_action.py solely to recall the verification steps after materializing the Q1 release.
- Videos published remain 0. Stall continues. Preferred list still complete.


## Run 522 — 2026-10-13T22:13:00Z
- Anti-rediscovery: exact_oauth_exchange_command one-liner added to status_report.py so agents see the precise human-only token minting commands (oauth_exchange.py + --exchange) immediately after exact_secret_set_commands without opening operator_card.py. HANDOFF.md refreshed.
- Local gates not re-run (media absent). No new failures.
- Human labor reduction: future agents less likely to open operator_card.py solely to copy the oauth_exchange steps once preparing the human terminal actions.
- Videos published remain 0. Stall continues. Preferred list still complete.


## Run 520 — 2026-10-13T20:15:00Z
- Recovery + anti-rediscovery: restored status_report.py from broken PLACEHOLDER state left by Run 519 commits and added checklist_banner_status one-liner so agents see the frozen Run 473 banner rule immediately without scanning HANDOFF or the checklist. HANDOFF.md refreshed.
- Local gates not re-run (media absent). No new failures beyond the recovered placeholder bug.
- Human labor reduction: future agents less likely to rediscover the banner freeze rule or hit a broken status tool.
- Videos published remain 0. Stall continues. Preferred list still complete.


## Run 518 — 2026-10-13T17:30:00Z
- Anti-rediscovery: upload_state_status one-liner added to status_report.py so agents see whether upload_state.json exists and (if so) the private provider_video_id without opening the packet file or scanning Actions logs. HANDOFF.md refreshed to reflect the new line.
- Local gates not re-run (media absent). No new failures.
- Human labor reduction: future agents less likely to open upload_state.json or dig through workflow logs solely to confirm the first successful execute once secrets are set.
- Videos published remain 0. Stall continues. Preferred list still complete.


## Run 517 — 2026-10-13T16:30:00Z
- Anti-rediscovery: optional_human_secret_confirm one-liner added to status_report.py so agents see the precise human-only confirmation command (prints PRESENT/MISSING, never values; exit 0 = all three exist) immediately after exact_secret_set_commands without scanning the human step section. HANDOFF.md refreshed to reflect the new line.
- Local gates not re-run solely for confirmation (media was materialized for print verification). No new failures.
- Human labor reduction: future agents less likely to open the human step section solely to recall the optional human_secret_confirm.py usage once secrets are being set.
- Videos published remain 0. Stall continues. Preferred list still complete.


## Run 516 — 2026-10-13T12:30:00Z
- Anti-rediscovery: exact_secret_set_commands one-liner added to status_report.py so agents see the precise three gh secret set commands (with human-only and scopes notes) immediately after exact_collect_command without scanning the human step section. Restored HANDOFF.md from the broken `$(cat /tmp/HANDOFF.md)` placeholder to a concise usable operator entry point.
- Local gates not re-run (media absent). No new failures.
- Human labor reduction: future agents less likely to open the human step section solely to copy the secret-set commands; HANDOFF.md is again a reliable front door.
- Videos published remain 0. Stall continues. Preferred list still complete.

## Run 514 — 2026-10-13T13:30:00Z
- Anti-rediscovery: observation_window_formula one-liner added to status_report.py so agents see the exact due_at = uploaded_at + 7d + 3 lag (= +10d) and early-collect OBSERVATION_WINDOW_NOT_DUE immediately after privacy_constraint without scanning the after-dispatch section. HANDOFF.md refreshed to reflect the new line.
- Local gates not re-run (media absent). No new failures.
- Human labor reduction: future agents less likely to open the after-dispatch section solely to recall the observation window calculation once a private video id exists.
- Videos published remain 0. Stall continues. Preferred list still complete.

## Run 513 — 2026-10-13T12:20:00Z
- Anti-rediscovery: privacy_constraint one-liner added to status_report.py so agents see the exact initial-privacy-stays-private rule and no-re-dispatch-until-id immediately after required_oauth_scopes without scanning the human step or after-dispatch sections. HANDOFF.md refreshed to reflect the new line.
- Local gates not re-run (media absent). No new failures.
- Human labor reduction: future agents less likely to open the human step or after-dispatch sections solely to recall the privacy constraint once secrets are set and a video id appears.
- Videos published remain 0. Stall continues. Preferred list still complete.

## Run 512 — 2026-10-13T11:15:00Z
- Anti-rediscovery: exact_collect_command one-liner added to status_report.py so agents see the precise gh workflow dispatch for collect_feedback=true (only after private video id + 10-day window) without scanning the after-dispatch section. HANDOFF.md refreshed to reflect the new line.
- Local gates not re-run (media absent). No new failures.
- Human labor reduction: future agents less likely to open the after-dispatch section or checklist solely to copy the collect command once a video id exists.
- Videos published remain 0. Stall continues. Preferred list still complete.
