# PROGRESS

- Run 958 enhancement: tools/recommended_publish_fill.py added. Reuses metadata_selector ranking logic to write a local recommended_publish_fill.md containing the highest-scoring candidate per field, formatted as ready-to-review sections. Reduces remaining manual comparison and reformatting labor when filling publish.md from the options files. No writes to publish.md, no invented options, no secrets polled. Compounds the selector into a structured local artifact.
- Small reusable textual-asset selection improvement. Fill file sits after ranking.
- Human labor reduction: lower chance of manually reformatting ranked prints into publish sections; one command produces a reviewable block.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 957 enhancement: tools/metadata_selector.py added. Ranks candidates from the six local options files by key-term overlap with the assignment primary (via assignment_utils.read_primary) plus length fitness. Prints the highest-scoring recommendation and runner-up per field. Reduces future manual comparison labor when filling publish.md. No writes, no invented options, no secrets polled. Compounds the recent assignment-source and alignment work into an actionable ranking step.
- Small reusable textual-asset selection improvement. Ranking sits after generation and scanning.
- Human labor reduction: lower chance of comparing every candidate by hand; one command surfaces the best-aligned options for each publish field.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

(Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.)
