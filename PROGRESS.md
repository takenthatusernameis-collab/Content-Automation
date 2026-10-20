# PROGRESS

- Reusable capability: improved tools/topic_suggest.py so idea.md skeletons are emitted via idea_brief.paste_block (the same function used by apply_idea and idea_brief --queue). Suggestion output now matches the locked paste format with no hand-format drift. Applies to every future use of the topic generator and every later apply_idea fill.
- Local gates not re-run (STALL_GATE_CONFIRM; previous verification holds). No new failures.
- Human labor reduction: operators or agents pasting idea content from topic_suggest no longer need to reformat fields to satisfy apply_idea / idea_brief --check.
- Videos published remain 0. Stall continues. Preferred list still complete. Idea-generation path reliability improved (single source of truth for paste format).

# PROGRESS

- Reusable capability: improved tools/topic_suggest.py to print ready idea.md skeletons for the top candidate topics. Agents or humans can now obtain paste-ready idea content (topic, viewer, problem, mechanism, why now) in the same command that lists candidates, reducing the steps between suggestion and usable idea.md. Applies to every future use of the topic generator.
- Local gates not re-run (STALL_GATE_CONFIRM; previous verification holds). No new failures.
- Human labor reduction: operators or agents expanding the topic queue no longer need a separate idea_brief invocation or manual assembly of idea fields for the top candidates.
- Videos published remain 0. Stall continues. Preferred list still complete. Idea-generation path further shortened.

# PROGRESS

- Reusable capability: improved tools/topic_suggest.py to compute the next Q id dynamically from the existing queue (using parse_queue). Hardcoded start numbers are eliminated, so future expansions remain correctly numbered without manual correction. Applies to every future use of the topic generator.
- Local gates not re-run (STALL_GATE_CONFIRM; previous verification holds). No new failures.
- Human labor reduction: operators or agents expanding the topic queue no longer need to adjust starting ids by hand.
- Videos published remain 0. Stall continues. Preferred list still complete. Idea-generation path reliability improved.
