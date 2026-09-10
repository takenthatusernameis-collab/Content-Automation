# NEXT_RUN_PROMPT

Use the original master prompt unchanged, plus these targeted additions:

## Bootstrap rule
If STATE.md exists, trust it over memory. If the repo only has a README, create the memory files and one reusable production artifact before anything else.
Clone-less agents print `python3 tools/needed.py --bootstrap` for the first-fetch set and `python3 tools/needed.py --plan` for the next wave command. Do not rebuild those lists from memory. Do not treat --bootstrap or --plan as a contract. Keep BOOTSTRAP short. Keep WAVE 2 as a command, not a file dump. Keep WAVE 3 as two commands (reconstruct `queue_status.py` then run it), not a file dump.

## Scope cap
Ship at most one new reusable capability per run after foundation exists. Prefer extending `tools/` and `videos/_template/` over new top-level concepts.
Do not add a start.py that only reprints doctor.
Do not add a sixth contract whose only job is to lock needed.py.
Do not add WAVE 4 unless a human still has to guess a command after WAVE 3 READY.
Do not edit needed.py unless a new clone-less guess is observed after WAVE 3 READY. The 037-042 reconstruct-loop is flagged in FAILURES.md.
Prefer completing `docs/human_session.md` or a human-owned Q1 packet over another reconstruct printer.
Do not auto-write idea.md from new_packet.

## Evidence rule
If you add a script, run it against a copy of `videos/sample-001-*` fields (dry-run is enough if write would mutate the fixture) and paste the command output into RUNS.md.
Do not claim `git clone` or `validate_packet.py --all` succeeded unless you actually have a local checkout.
HTTPS clone of this private repo fails in the agent sandbox. Do not retry after the first failure in a run. Push via GitHub file APIs.
Reconstruct the selftest tree per `docs/agent_session.md` using `python3 tools/needed.py selftest.py` then download_url tokens. After Run 026, fixture selftest runtime is PASS unless a later run prints SELFTEST FAIL.
After apply_script or set_status edits, run `tools/write_path_contract.py` on a reconstructed tools tree.
After new_packet or after_scaffold edits, run `tools/scaffold_contract.py`.

## Reconstruct-list rule
`needed.py` is read-only. It prints paths. It does not download and does not write videos/.
Keep it unmapped in which_contract (same class as doctor.py).
If EXTRA paths drift from agent_session, fix needed.py EXTRA, not by inventing a new lock.
`--missing`, `--bootstrap`, and `--plan` always exit 0.

## Niche rule
Do not reopen niche debate unless a human changed DECISIONS.md. Specialize prompts toward `docs/channel.md`.

## Topic-queue rule
`docs/topic_queue.md` holds working titles only. `tools/next_topic.py` and `tools/queue_status.py` are read-only and must not call `new_packet.py`.
`tools/mark_topic.py` is the only writer of queue status. Dry-run default. Refuse `used` without a matching non-fixture `videos/` folder. Refuse sample-001.
Do not auto-scaffold a queued title without an explicit human instruction.
Do not treat a queue row as spoken WORDS.
Numeric ids treat `sample-001-*` as 001, so the next scaffold is `002-...`.
Default `queue_status.py` exit is 0. `--strict` may exit 2 on missing-folder and 1 on mark-needed. Do not make default exit non-zero.
`new_packet.py` reprints mark_topic dry-run and idea.md suggestions only. It must not call mark_topic --write and must not write idea.md.

## Duration rule
Spoken WORDS for `explainer-6-10min` belong in 900-1500 at 150 wpm. Default validate prints WARN. `--duration` may FAIL. Do not pad sample-001. Do not make WARN the default FAIL.

## Expand rule
`expand_brief.py` writes a beat budget. It must not rewrite `script.md` or invent spoken lines.
Do not overwrite a filled `expand.md` without `--force`.
A Status `short` budget is not a draft.

## Expand-prompt rule
`expand_prompt.py` prints a paste pack. It must not write `script.md`.
Refuse `--out` when the destination is `script.md`.
On `sample-001-*` print the fixture lock banner. Do not paste the output back onto the fixture.
Do not expand while idea.md still uses the scaffold template-default or blank mechanism.

## Apply-script rule
`apply_script.py` dry-runs by default. `--write` is required.
Refuse `sample-001-*`.
Refuse text that looks like expand_prompt stdout.
Do not bump packet status.
`--refresh` may rewrite expand/vo_session/captions only after a successful write on a non-fixture packet.

## Status-write rule
`set_status.py` dry-runs by default. `--write` is required.
Refuse promoting `sample-001-*`.
Refuse skip-ahead.
Refuse `ready_for_vo` / `ready_for_edit` while duration WARN is present.
Refuse later statuses without Selected VO / Master export on disk.
Do not create media.
`pipeline_status.py`, `next_action.py`, `hint.py`, `doctor.py`, `selftest.py`, `next_topic.py`, `queue_status.py`, `queue_contract.py`, `write_path_contract.py`, `scaffold_contract.py`, `which_contract.py`, `router_contract.py`, and `needed.py` stay read-only versus videos/ and must not write the queue.

## Hint rule
`hint.py` is read-only. Map next_action codes to copy-paste CLI.
Never print `--write` as the first command.
On `sample-001-*` print a fixture lock instead of apply_script --write.

## Doctor rule
`doctor.py` is read-only. One health block per packet.
Reuse `hint.commands_for` so CLI text cannot drift.
`--strict` may fail on FAIL gate or drift only. Duration WARN is not a strict failure.
Never print `--write` as the first command.

## Human-session rule
`docs/human_session.md` is the operator path. Keep it short. Do not turn it into a second prompt or a wrapper tool. Keep the first-video expand/apply/status commands on that page; do not defer them to prior commits. Keep the current Q1 working title and predicted folder on that page while Q1 is still queued. Require the idea.md mechanism edit before expand_prompt. Note that new_packet reprints topic + mechanism and still does not write idea.md.

## Agent-session rule
`docs/agent_session.md` is the clone-less reconstruct path. Update Last verified runtime only after a real selftest run. Do not invent PASS.

## Board rule
`pipeline_status.py` is read-only. It must not rewrite `packet.md` status, render.md, or qa.md.
Duration WARN is not FAIL and not drift.
`queue_status.py` is read-only. It must not rewrite `docs/topic_queue.md`.
`queue_status.py --strict` may exit non-zero on queue drift only.

## Next-action rule
`next_action.py` is read-only. One recommended step per packet. Prefer gate FAIL, then drift, then duration WARN (`expand-script`), then the first real production file the human can add.

## Scaffold rule
Reuse `after_scaffold.py` and `write_empty_*`; never pass `--force` from scaffold.
`new_packet.py` must print mark_topic dry-run then a commented `--write`. It must not mark the queue.
`new_packet.py` may reprint idea.md suggestions. It must not write idea.md.

## Fixture freeze
Do not overwrite `videos/sample-001-*` titles, thumbnail, or script WORDS unless the packet schema itself changed.
Do not expand sample-001 WORDS to clear duration WARN.

## Private repo
Push via GitHub file APIs. Do not retry HTTPS clone after it fails once in the run.
