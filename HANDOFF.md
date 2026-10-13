# HANDOFF

Updated: 2026-10-13T07:20:00Z (Run 508)

This file is the current operator entry point. Audio, card PNGs, and the master stay gitignored. Do not `git add -f`. Do not commit media.

## Current reality

- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- Status: `ready_for_vo` (text complete)
- Videos published: **0**
- Pre-upload path: stable. Q1 VO + 7 cards + r253 master exist on private GitHub releases and are installed by `tools/materialize_q1_release.py`.
- r253 master SHA256 (documented, must be present): `4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546`
- packet.md remaining human work checks off generated VO / cards / edit steps, publish-lock, and captions review (delegated structural approval in captions_review.md). Open box: upload only.
- status_report.py prints remaining_open_boxes, captions_review_ready, captions_review_checkpoints, thumbnail_review_status, and captions_review_status so agents see the exact unchecked items, readiness, the 5 silence-proportional spot-check times, thumbnail and captions approval states without opening packet.md, captions_review.md, or thumbnail_review.md.

- Local gates (after materialize): `media_qa` PASS, `closed_brief_gate` PASS, `next_action` = upload-blocked, `operator_card` PASS, `selftest` PASS.
- Remaining human gate: the three GitHub Actions secrets only (`YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`).
- `oauth_idle_without_publish` stall has persisted for ~186+ historical runs (live idle_streak dynamic in status_report.py). Preferred unblocked preparation list in status_report.py is complete. Pure-verification agent runs have diminishing returns. Prefer the human step or one newly identified small reusable improvement that reduces rediscovery or post-secret friction without inventing data or expanding locked surfaces.

## Quick status

```bash
python3 tools/status_report.py
```

Self-contained printer. Shows videos published, media_status (with target SHA prefix and MATCH/MISMATCH when present), master_sha_target (full r253 checksum for easy copy), recommended_next (materialize if missing else human_step), active_stall_flags, remaining_open_boxes, captions_review_ready, captions_review_checkpoints (5 silence-proportional spots and method), thumbnail_review_status (approved under delegated review; PNG committed and inspected), next_action_code, optional_playlist (not_set, does not block), last_gates_confirmed, full stall flags (including dynamic idle_streak), next_action, complete human step (exact three secret names + gh secret set commands + required scopes + forbidden gh secret list + optional human_secret_confirm.py + exact execute dispatch + initial privacy stays private), after-dispatch confirmation (private video id look-up + precise observation window: uploaded_at + 7 calendar days + 3 days Analytics lag = due at +10 days; early collect = OBSERVATION_WINDOW_NOT_DUE + exact collect_feedback dispatch), and stall-length suspicion. Does not write files, poll secrets, or dispatch.

## While the OAuth stall continues

The oauth_idle_without_publish pattern has persisted for ~186+ runs. Pure verification has diminishing returns. The preferred unblocked improvements list is complete. Next agents should prioritize the single human step (three secrets + one dispatch) or identify a truly new small anti-rediscovery item that introduces reusable capability and does not violate locks. See the "Agent behavior during external stalls" section in `docs/production_rules.md`. Do not rematerialize if media is present. Do not reopen closed briefs. Do not scaffold Q2, poll secrets, or extend locked surfaces. Do not refresh the human_oauth_checklist banner solely to update its timestamp (STALL_BANNER_REFRESH). The single remaining human step remains the highest-leverage action.

## First commands on a fresh clone

```bash
python3 tools/materialize_q1_release.py   # verifies checksums, installs r253 master, ignores truncated r249, does not commit media
python3 tools/media_qa.py videos/002-stop-deciding-what-to-work-on-every-morning
python3 tools/next_action.py videos/002-stop-deciding-what-to-work-on-every-morning
python3 tools/operator_card.py            # prints the one human step
```

If `vo/`, `cards/`, and `export/master.mp4` are already present, do not rematerialize. Do not edit the closed brief generators unless `python3 tools/closed_brief_gate.py` fails. Prepend logs only through `python3 tools/record_run.py`.

## The single remaining human step

Follow the printable checklist:

```bash
cat docs/human_oauth_checklist.md
# or
python3 tools/operator_card.py
```

Then (human terminal only):

1. Mint the refresh token with the required scopes (`youtube.upload`, `youtube.force-ssl`, `yt-analytics.readonly`).
2. Store the three secrets with `gh secret set` (paste into the prompt; never on the command line).
3. Optional local confirm: `python3 tools/human_secret_confirm.py` (never from an agent; prints PRESENT/MISSING, never values).
4. Dispatch once:

```bash
gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false
```

Privacy stays private. Do not re-dispatch until a provider video id appears. Do not set `collect_feedback=true` until that id exists and uploaded_at + 7 calendar days + 3 days Analytics lag have passed (due at +10 days). Early collect is OBSERVATION_WINDOW_NOT_DUE.

See also issue #1 and `docs/youtube_integration.md`.

## Once a provider video id exists

After the first successful execute dispatch produces a private video id (look in the Actions log and any committed `upload_state.json`):

1. Do not re-dispatch execute until you confirm the id. Privacy stays private.
2. Wait until uploaded_at + 7 calendar days + 3 days Analytics lag (due_at = uploaded_at + 10 days).
3. Then dispatch once with collect_feedback:
   ```bash
   gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=false -f collect_feedback=true
   ```
4. The job will run `youtube_feedback.py --execute` and `experiment_loop.py --write-state` only if the window is due. It commits redacted `feedback_state.json` only on COLLECTED.
5. Do not invent metrics, a baseline, or a keep/discard decision. The observation window and experiment ledger are already built; the next agent can compare once real data lands.
6. After feedback is collected, the system can advance to COMPLETE only when `tools/complete.py` sees real evidence (VO + cards + master + id + metrics + experiment result).

This path is already implemented and dry-run validated. No new tools are required. The stall ends only when the three secrets are set and the first execute succeeds.

## Do not

- Scaffold Q2.
- Poll secrets from an agent run.
- Add a scanner, extend the operator card, or add another OAuth parser while videos published stay 0.
- Refresh the human_oauth_checklist banner solely for its timestamp.
- Treat the truncated r249 master as usable.
- Invent analytics or a video id.
- Commit any secret or token file.

Older historical notes (Drive file ids, early release experiments) have been superseded by the materialize tool and are archived in the run logs. Do not re-implement those paths.
