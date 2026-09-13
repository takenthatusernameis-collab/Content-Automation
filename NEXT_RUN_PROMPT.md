# NEXT RUN PROMPT

Keep the original master prompt unchanged.

Targeted addition from Run 109:

- `docs/human_session.md` step 3 must keep the empty-script Target column: hook 28 / payoff 60 / beats 220×4 / CTA 50 / land ~1010.
- Do not strip that paragraph. Do not change Q1 title, slug, one_line, or problem when editing that page.

Targeted addition from Run 108:

- `videos/_template/expand.md` must keep the empty-WORDS Band-landing table. Status stays `placeholder` so expand_is_filled does not treat it as finished.
- `tools/expand_prompt.py` must paste `expand_brief.render()` when expand.md is missing or not expand_is_filled. It must not write expand.md.
- Do not revert that fallback to the stub line "budgets will appear here".

Targeted addition from Run 107:

- `tools/expand_brief.py` must print a budget table from script.md headings even when spoken WORDS are 0.
- Empty hook want is 28 (band 20-35). Payoff want 60 (40-70). CTA want 50 (40-80). Beat want clamped to 140-220.
- Four empty template beats target 220. Do not hide this table. Do not add a CLI that only reprints Band landing.
- Status stays `placeholder` when total WORDS are 0 so expand_is_filled does not treat the empty table as a finished brief.

Targeted addition from Run 106:

- `new_packet.draft_followup()` must reprint PATH/draft.md as the overwrite target and that it is not script.md.
- Do not add a fourth new_packet followup unless that reprint regresses.

Targeted addition from Run 105:

- `videos/_template/draft.md` must stay the packet save target.
- Do not treat an empty copied draft.md as script.md or as apply --write.

Targeted addition from Run 104:

- Do not touch needed.py reconstruct / WAVE 3 / doctor mapping unless a new READY lie is proven with an isolated tree.
- `prompts/script_writer.md` must keep the Band landing table.
- Do not rewrite those prompts again unless a real non-fixture draft misses the band.
- Remaining high-value work is still human-owned: scaffold Q1, paste idea fields, overwrite PATH/draft.md, land WORDS in band, apply --write --refresh, set_status ready_for_vo.

Targeted addition from Run 081:

- After a GitHub write of a high-risk tool, run `python3 tools/prove_locks.py` first.
- Do not map words.py, words_contract.py, placeholder_guard.py, or prove_locks.py.
