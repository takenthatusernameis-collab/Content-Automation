# RUNS

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

## Run 428 — 2026-10-09T13:30:00Z
- Objective: Verify Run 427 asset contract, then fix only a real later-packet dry-run failure outside the closed asset, caption, and publish loops.
- Action: `asset_brief_contract.py`, `caption_brief_contract.py`, and `publish_brief_contract.py` passed. Those stubs were not edited. Title dry-run passed SELF_CHECK. Chapter dry-run inverted `Do not *reopen*` into `Do reopen inbox after` because TITLE_DROP removed `not`. Chapter titles now keep not/no/never. Added `tools/chapter_draft_contract.py` and a selftest hook. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Hook chapter is `0:00 Do not reopen inbox`. Q1 chapters.md unchanged.
- Verification: `python3 tools/chapter_draft_contract.py` PASS. `python3 tools/asset_brief_contract.py` PASS. `python3 tools/selftest.py` PASS. Later-packet chapter line keeps not. No provider write.
- Discovery: Caption emphasis unwrap did not cover chapter titles. Dropping `not` inverted the beat. Suspicious: oauth_idle_without_publish is unchanged since before Run 270. Brief-stub microfixes moved to a new file after the asset loop closed.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/chapter_draft_contract.py` before any new chapter edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit asset_brief, caption_brief, or publish_brief again unless a dry-run still fails the rule named in NEXT.md.

## Run 427 — 2026-10-09T12:25:00Z
- Objective: Verify Run 426 caption contract, then fix only a real later-packet dry-run failure outside the closed caption and publish loops.
- Action: `caption_brief_contract.py` passed. Caption and publish later-packet dry-runs did not reprint the closed leaks. Did not edit caption_brief or publish_brief. Asset dry-run still put `ON SCREEN: FACE DOWN` into the need and `cards/hook-phone-face-up-on-screen-face-down.png`. VISUAL now stops before ON SCREEN. Added `tools/asset_brief_contract.py` and a selftest hook. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. On-screen labels no longer need a human card rename of that shape. Q1 assets.md unchanged.
- Verification: `python3 tools/asset_brief_contract.py` PASS. `python3 tools/caption_brief_contract.py` PASS. `python3 tools/publish_brief_contract.py` PASS. `python3 tools/selftest.py` PASS. Phone asset dry-run need is `phone face up` and file is `cards/hook-phone-face-up.png`. No provider write.
- Discovery: Run 426 stopped caption cues before ON SCREEN and left the same label on the asset row. Suspicious: oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/asset_brief_contract.py` before any new asset edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit publish_brief or caption_brief again unless a dry-run still fails the rule named in NEXT.md.

## Run 426 — 2026-10-09T11:20:00Z
- Objective: Verify Run 425 caption contract, then fix only a real later-packet caption dry-run failure.
- Action: `caption_brief_contract.py` passed. Later-packet dry-runs still deleted `*reopen*`, kept bullet dashes, and appended `ON SCREEN: STOP`. Spoken body now unwraps inline emphasis, drops italic-only visual lines and list markers, and stops before ON SCREEN. Contract covers those three leaks. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not edit publish_brief. Did not open a title phrase edit.
- Result: Videos published stay 0. Emphasis, lists, and on-screen labels no longer need a human cue rewrite of that shape. Q1 captions.md unchanged.
- Verification: `python3 tools/caption_brief_contract.py` PASS after the edit. `python3 tools/selftest.py` PASS. Q1 caption dry-run still prints spoken cues. No provider write.
- Discovery: Run 425 filled empty plain beats and still stripped every `*...*` span, which deleted spoken words. Suspicious: oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/caption_brief_contract.py` before any new caption edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit publish_brief again unless a dry-run still emits a machine sentence or a lone tag the title/mechanism rule does not drop. Do not edit caption_brief again unless a dry-run still deletes a spoken word or prints a visual or on-screen label.

## Run 425 — 2026-10-09T10:20:00Z
- Objective: Verify Run 424 publish contract, stop the publish-stub loop if the dry-run is clean, and fix one other later-packet leak.
- Action: `publish_brief_contract.py` passed. Keys, mug, and window publish dry-runs did not emit a machine stall sentence or a lone tag the title/mechanism rule missed. Did not edit publish_brief. Caption dry-run on a plain beat counted words and printed an empty cue. `spoken_text` now uses the same body as the word count. Visual notes stay out. Added `tools/caption_brief_contract.py`. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Plain-beat cues now carry the spoken line. Q1 captions.md and publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS. `python3 tools/caption_brief_contract.py` PASS. Sample caption dry-run still prints WORDS lines. `python3 tools/selftest.py` PASS. No provider write.
- Discovery: Run 424 closed the tag-source leak. The next human rewrite was caption stubs that counted a plain sentence and left the dash empty. Suspicious: oauth_idle_without_publish is unchanged since before Run 270. Publish-stub microfixes 420-424 had no new failure this run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/caption_brief_contract.py` before any new caption edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit publish_brief again unless a dry-run still emits a machine sentence or a lone tag the title/mechanism rule does not drop.

## Run 424 — 2026-10-09T09:12:00Z
- Objective: Verify Run 423 publish contract, then fix only a real later-packet publish dry-run failure.
- Action: `publish_brief_contract.py` passed. Later-packet dry-runs still emitted lone tags from problem prose and title imperatives (`under`, `while`, `already`, `hang`, `set`, `down`). Tag source is now title and mechanism only. Command-first words and short mechanism-only words are skipped. Contract covers the keys packet and the mug packet. Did not grow TAG_GLUE. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Those leaks are gone on the later-packet dry-run. Q1 publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS after the edit. `python3 tools/selftest.py` PASS. No provider write.
- Discovery: Run 423 skipped listed function words and still tokenized the problem sentence. A source rule beats another skip-list append. Suspicious: publish-stub microfixes now span runs 420-424 while oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/publish_brief_contract.py` before any new publish edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit publish_brief again unless a dry-run still emits a machine sentence or a lone tag the title/mechanism rule does not drop.

## Run 423 — 2026-10-09T08:14:00Z
- Objective: Verify Run 422 publish contract, then fix only a real later-packet publish dry-run failure.
- Action: `publish_brief_contract.py` passed. Later-packet dry-runs still printed `If the stall named in this packet` with no problem, and lone tags don't/until/ends/onto/has/where/does. Description now omits that machine sentence. Those function words are skipped. Contract covers the empty-problem packet, inbox tags, bag tags, and phone tags. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Those leaks are gone on the later-packet dry-run. Q1 publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS after the edit. No provider write.
- Discovery: Run 422 fixed period, imperative, and bare so-clause only. Incomplete packets still needed a human delete of the stall sentence, and function words still became tags. Suspicious: publish-stub microfixes now span runs 420-423 while oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/publish_brief_contract.py` before any new publish edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit publish_brief again unless a dry-run still emits a machine sentence or a lone tag a human would delete.

## Run 422 — 2026-10-09T07:14:00Z
- Objective: Verify Run 421 publish contract, then fix only a real later-packet publish dry-run failure.
- Action: `publish_brief_contract.py` passed. Later-packet dry-runs still printed `Shut the lid..`, `If don't reopen the inbox until the block ends`, and `If the notebook stays in the bag so the block has no page`. Description now keeps a finished period, keeps an imperative problem, and keeps a bare so-clause. Contract covers lid, inbox, and notebook packets. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Those three description leaks are gone on the later-packet dry-run. Q1 publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS after the edit. No provider write.
- Discovery: Run 421 skipped lone verbs only. The description still needed a human rewrite on punctuated titles, imperative problems, and so-clauses without a comma. Suspicious: publish-stub microfixes now span runs 420-422 while oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/publish_brief_contract.py` before any new publish edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not open a phrase edit unless a later-packet title dry-run fails. Do not add another lone-verb skip unless a dry-run still emits one.

Permanent log. Newest first. Do not paste the archive back into this file.

Older run notes live in `docs/runs_archive.md`. Do not paste the archive back.
