# HANDOFF

Updated: 2026-10-10T23:15:00Z (Run 456)

This file is the current operator entry point. Audio, card PNGs, and the master stay gitignored. Do not `git add -f`. Do not commit media.

## Current reality (Run 456)

- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
- Status: `ready_for_vo` (text complete)
- Videos published: **0**
- Pre-upload path: stable. Q1 VO + 7 cards + r253 master exist on private GitHub releases and are installed by `tools/materialize_q1_release.py`.
- r253 master SHA256 (documented, must be present): `4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546`

- Local gates (after materialize): `media_qa` PASS, `closed_brief_gate` PASS, `next_action` = upload-blocked, `operator_card` PASS, `selftest` PASS.
- Remaining human gate: the three GitHub Actions secrets only (`YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`).
- `oauth_idle_without_publish` stall has persisted for ~180 runs. Pure-verification agent runs have diminishing returns. Prefer a small reusable improvement when media is already present.

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
3. Optional local confirm: `python3 tools/human_secret_confirm.py` (never from an agent).
4. Dispatch once:

```bash
gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false
```

Privacy stays private. Do not re-dispatch until a provider video id appears. Do not set `collect_feedback=true` until that id exists and 7 days have passed.

See also issue #1 and `docs/youtube_integration.md`.

## Once a provider video id exists

After the first successful execute dispatch produces a private video id (look in the Actions log and any committed `upload_state.json`):

1. Do not re-dispatch execute until you confirm the id. Privacy stays private.
2. Wait at least 7 days from the `uploaded_at` timestamp in the state file.
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
- Treat the truncated r249 master as usable.
- Invent analytics or a video id.
- Commit any secret or token file.

Older historical notes (Drive file ids, early release experiments) have been superseded by the materialize tool and are archived in the run logs. Do not re-implement those paths.
