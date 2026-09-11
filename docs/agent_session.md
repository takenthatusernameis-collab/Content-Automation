# Agent session

One page for recurring agents when there is no local git checkout.

Humans follow `docs/human_session.md`. This page is not a second start command for humans.

## Clone

HTTPS clone of this private repo fails in the agent sandbox. Do not retry after the first failure in a run. Push via GitHub file APIs.

## First fetch

Do not rebuild the first-fetch set from memory. Print it:

```bash
python3 tools/needed.py --bootstrap
python3 tools/needed.py --bootstrap --missing
python3 tools/needed.py --plan
python3 tools/needed.py --plan --missing
```

`--bootstrap` is read-only. It prints the six session-start paths. Combined with `--missing` it labels PRESENT or MISSING and prints READY or NOT READY. Exit is always 0. It is not a contract.

`--plan` is read-only. WAVE 1 reprints those six paths. WAVE 2 prints the next reconstruct command (`python3 tools/needed.py selftest.py --missing`) and does not dump that file list. WAVE 3 prints the reconstruct command for the operator (`python3 tools/needed.py queue_status.py --missing`) then the operator command (`python3 tools/queue_status.py`) and does not dump queue files or scaffold. Combined with `--missing` it labels WAVE 1 only. Exit is always 0. It is not a contract.

Then fetch WAVE 1 and continue below.

## Which files

Do not rebuild the reconstruct list from memory. Print it:

```bash
python3 tools/needed.py selftest.py
python3 tools/needed.py new_packet.py
python3 tools/needed.py queue_status.py
python3 tools/needed.py --all
python3 tools/needed.py new_packet.py --missing
```

`needed.py` is read-only. It prints repo-relative paths plus the contract command. `--missing` labels each path PRESENT or MISSING and prints READY or NOT READY. Exit is always 0. It does not download files and does not write `videos/`.

Without `which_contract.py` on disk, FALLBACK_ALIAS still resolves edited-tool names such as `new_packet.py` → scaffold_contract and `queue_status.py` → queue_contract. Unmapped tools (`doctor.py`, `expand_prompt.py`, `needed.py`, `idea_gate_contract.py`, `operator_pin_contract.py`, `idea_brief_contract.py`) print Unknown and exit 0.

## Which contract

After editing a tool, do not scan NEXT for the lock name. Run:

```bash
python3 tools/needed.py EDITED_FILE.py --missing
python3 tools/which_contract.py --after EDITED_FILE.py
```

Then run the printed command if the reconstructed tree is READY. `--run` SKIP means deps were missing, not that the lock passed.

After editing `which_contract.py` itself, run:

```bash
python3 tools/router_contract.py
```

Expected: `ROUTER CONTRACT PASS`, exit 0, no writes to `docs/` or `videos/`.

After reconstructing or editing write-path tools (`write_path_contract.py`, `apply_script.py`, `set_status.py`, `contract_shape.py`), run:

```bash
python3 tools/verify_write_path.py
```

Expected when siblings are on disk: `CONTRACT SHAPE PASS` then `WRITE PATH CONTRACT PASS` then `VERIFY WRITE PATH PASS`, exit 0, no writes. If `contract_shape.py` or `write_path_contract.py` is missing, expect `VERIFY WRITE PATH FAIL` and a non-zero exit. Do not treat this wrapper as a replacement for those two files. Do not map it in `needed.py`.

## Unmapped locks

These are not reconstruct waves and are not in which_contract. Run them directly after the matching edit:

```bash
python3 tools/idea_gate_contract.py
python3 tools/operator_pin_contract.py
python3 tools/idea_brief_contract.py
```

- After fill-idea / expand refuse edits: idea_gate_contract
- After human_session or Q1 queue pin edits (title, slug, one_line, problem sentence): operator_pin_contract
- After idea_brief reprint-recover or `--block` edits: idea_brief_contract
- After new_packet idea reprint edits: scaffold_contract (mapped; not this list)

`idea_brief.py` is also unmapped as a printer. It is a reprint recover tool, not a lock. `--block` prints a paste-ready idea.md body and still does not write. PASS/print does not mean Q1 is scaffolded. Do not write idea.md because they passed.

PASS does not mean Q1 is scaffolded. Do not write idea.md because they passed.

## Reconstruct and prove the fixture

`tools/selftest.py` is the packet contract. Reconstruct only what `python3 tools/needed.py selftest.py` prints. Confirm with `--missing` until READY.

How: list `tools/` and the sample folder with GitHub get_file_contents, then curl each `download_url` into that tree. Do not invent file bodies from memory.

Then:

```bash
python3 tools/selftest.py
```

Expected on current sample-001 (do not pad WORDS to change this):

- Gate PASS
- Status draft
- Code expand-script
- Duration WARN: spoken 153 words (~01:01 at 150 wpm) below explainer-6-10min band 900–1500
- First live command is expand_prompt with no `--write`
- SELFTEST PASS
- Exit 0
- No writes

## Queue / write-path / scaffold / router contracts

Same as prior page: reconstruct what `needed.py CONTRACT` prints, confirm `--missing` READY, then run the named contract. Expected PASS, exit 0, no writes to `docs/` or `videos/`.

After WAVE 2 READY, print WAVE 3 reconstruct, fetch until READY, then run the operator command and stop at the board. Do not treat WAVE 3 as scaffold permission.

For write-path after reconstruct, prefer `python3 tools/verify_write_path.py` over running the two locks out of order.

## Last verified runtime

verify_write_path missing-sibling:

- When: 2026-09-11T11:10:00Z (Run 070)
- How: sandbox file only; no sibling tools tree
- Result: VERIFY WRITE PATH FAIL, missing contract_shape.py, exit 1; no videos/ writes

idea_brief --block:

- When: 2026-09-10T19:10:00Z (Run 054)
- How: `/tmp/ca` with idea_brief.py --block + idea_brief_contract.py + new_packet.idea_followup + queue_lib.py + operator_pin Q1_PROBLEM + docs/topic_queue.md + docs/human_session.md
- Result: IDEA BRIEF CONTRACT PASS, exit 0; idea.md hash unchanged under default and --block; Q1 remains queued; no videos/ writes in the repo

idea_brief contract:

- When: 2026-09-10T17:05:00Z (Run 053)
- How: `/tmp/ca` with idea_brief_contract.py + idea_brief.py + new_packet.idea_followup + queue_lib.py + operator_pin Q1_PROBLEM + docs/topic_queue.md + docs/human_session.md
- Result: IDEA BRIEF CONTRACT PASS, exit 0; idea.md hash unchanged; Q1 remains queued; no videos/ writes in the repo

idea_brief reprint recover:

- When: 2026-09-10T16:15:00Z (Run 052)
- How: `/tmp/ca` with idea_brief.py + new_packet.idea_followup + queue_lib.py + docs/topic_queue.md + a blank 002 packet
- Result: exit 0; printed blank current fields + Q1 topic/problem/mechanism; idea.md hash unchanged; Q1 remains queued; no videos/ writes in the repo

Scaffold problem reprint:

- When: 2026-09-10T15:05:00Z (Run 051)
- How: `/tmp/ca` with new_packet.py + scaffold_contract.py + queue_lib.py + operator_pin Q1_PROBLEM + docs/topic_queue.md
- Result: SCAFFOLD CONTRACT PASS, exit 0; idea_followup printed topic + problem + mechanism; Q1 remains queued; no videos/ writes

Operator pin problem-line lock:

- When: 2026-09-10T14:20:00Z (Run 050)
- How: `/tmp/ca` with operator_pin_contract.py + queue_lib.py + docs/topic_queue.md + docs/human_session.md
- Result: OPERATOR PIN CONTRACT PASS, exit 0; Q1 remains queued; no videos/ writes

Prior bootstrap / presence / reconstruct times remain those recorded in Run 037–042. Prior contract PASS times remain those recorded in Run 026–050. If a later run cannot reconstruct, record FAIL with the missing file.

## Stop

- Do not retry clone after one failure.
- Do not write reconstructed files back onto sample-001.
- Do not invent WORDS, wav, cards, or ffmpeg recipes.
- Do not wrap doctor in start.py.
- Do not make needed.py --missing, --bootstrap, or --plan exit 1.
- Do not treat --bootstrap or --plan as a contract.
- Do not list WAVE 2 reconstruct files inside --plan.
- Do not list WAVE 3 queue files inside --plan.
- Do not treat WAVE 3 as auto-scaffold.
- Do not map idea_gate_contract, operator_pin_contract, or idea_brief_contract.
- Do not write idea.md from idea_brief.py or idea_brief.py --block.
- Do not treat verify_write_path.py as a replacement for contract_shape.py or write_path_contract.py.
