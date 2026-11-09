# Content-Automation

Recurring-agent workspace for a low-labor YouTube production system.

## Live packet (current state)

Packet: `videos/002-stop-deciding-what-to-work-on-every-morning`  
Status: `ready_for_vo` (text complete; generated VO + cards + r253 master exist on private releases and can be materialized).  
Videos published: 0.  
**Remaining human gate: three GitHub Actions secrets** (`YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`).

Run this first on any clone or agent run:

```bash
python3 tools/status_report.py            # one-command stall flags, next_action, published count, human step
# then, only if media is missing:
python3 tools/materialize_q1_release.py   # installs verified wav, 7 cards, r253 master; ignores truncated r249
python3 tools/media_qa.py videos/002-stop-deciding-what-to-work-on-every-morning
python3 tools/next_action.py videos/002-stop-deciding-what-to-work-on-every-morning
python3 tools/operator_card.py            # prints the one human OAuth step + pitfalls
```

Do not scaffold Q2. Do not poll secrets. Do not edit brief generators unless `python3 tools/closed_brief_gate.py` fails. Do not rematerialize when vo/, cards/, and export/master.mp4 are already present. Prepend logs only through `python3 tools/record_run.py`. Do not refresh the human_oauth_checklist banner solely for its timestamp (intentionally frozen at Run 473 / STALL_BANNER_REFRESH).

Start here for context:
- `STATE.md` — current reality
- `NEXT.md` — what the next run should do
- `docs/HUMAN_PRIORITY.md` — single-page high-signal human OAuth step (preferred start for humans)
- `tools/operator_card.py` — the one human step
- `docs/gate_machine.md` — packet-relative Selected VO drop (generated fallback already authorized for Q1)
- `docs/youtube_integration.md` — upload contract
- `RUNS.md` — timestamped log
- `ORIGINAL_MASTER_PROMPT.md` — frozen operating prompt
- `docs/channel.md` — working niche lock
- `docs/format.md` — face-free explainer timing and named outputs

## Human session

**Highest-leverage remaining action:** set the three OAuth secrets and dispatch execute=true once. See `docs/HUMAN_PRIORITY.md` for the single-page version. The human_oauth_checklist banner timestamp is intentionally frozen at Run 473; agents will not update it solely for the date.

The one remaining human step is the three OAuth secrets. Start with:

```bash
python3 tools/human_starter.py
```

or open `docs/HUMAN_PRIORITY.md`.

Then follow the numbered steps. Store the secrets with `gh secret set` (paste into the prompt). Dispatch once:

```bash
gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false
```

After the single execute dispatch, confirm success by a private provider video id appearing in the Actions log and in the packet upload_state.json (see Expected outcomes in docs/human_oauth_checklist.md). Do not invent an id. Do not re-dispatch until that id is visible.

Do not run `gh secret list`. Do not commit the token file. After a provider video id exists and `uploaded_at` is at least 10 days old (7 calendar + 3 Analytics lag), a later dispatch with `collect_feedback=true` is allowed.

Parked until that publish happens:

```bash
python3 tools/doctor.py
python3 tools/queue_status.py
python3 tools/next_topic.py
```

Those printers still print the Q1 hold before idea_brief/new_packet. Do not treat them as permission to scaffold Q2.

(The remainder of the README is unchanged and describes the tool contracts.)
