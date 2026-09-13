# Topic queue

Working titles for the next non-fixture packets. Niche lock: `docs/channel.md`.

This file is a list, not a draft. It does not contain spoken WORDS.

Status values:
- queued — available for `tools/new_packet.py`
- used — a packet folder already exists for this slug or title
- parked — keep, but do not scaffold yet

`tools/queue_lib.py` holds slugify, next_id, parse, and folder match. `tools/next_topic.py` is read-only. It prints the first `queued` row that does not already match a `videos/` folder, plus a predicted `videos/NNN-slug` path. It does not create packets and does not invent WORDS.

`tools/queue_status.py` is the read-only board for this table versus `videos/`. Codes: ok-queued, mark-needed, missing-folder, ok-used, parked, fixture-refuse. It does not write this file.

`tools/queue_contract.py` locks those codes, the PACKET column, default exit 0, and `--strict` 2/1 on a tempfile tree. It does not write this file.

`tools/mark_topic.py` is the only writer of this table. Dry-run default. `--write` is required. It refuses to mark a row `used` until a matching non-fixture `videos/` folder exists. It refuses the sample-001 fixture.

`tools/new_packet.py` reprints the matching `mark_topic --id QN` dry-run after scaffold. It also reprints suggested `idea.md` topic + mechanism from this table's `one_line`. It does not write this table and does not write idea.md.

A human (or an agent with an explicit human instruction) scaffolds with the printed `new_packet.py` line. Do not scaffold `sample-001`. Do not mark a row `used` until the packet folder exists.

Numeric ids treat `sample-001-*` as 001, so the next scaffold is `002-...`.

| id | status | working_title | one_line |
|----|--------|---------------|----------|
| Q1 | used | Stop deciding what to work on every morning | Install a written next-action default so the morning does not reopen the whole list. |
| Q2 | queued | Put the start cue on the work itself | Name one physical or file cue that means this is the first two minutes. |
| Q3 | queued | One list, one next action | Collapse competing lists into a single next verb the viewer can do today. |
| Q4 | queued | Close the extra tab before you open the work | A shutdown default that removes the stall of just checking one more thing. |
| Q5 | queued | Keep the checklist where the stall happens | Put the constraint on the desk, file, or app that already absorbs the delay. |
