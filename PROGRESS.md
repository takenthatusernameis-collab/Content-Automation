# PROGRESS

- Run 965 enhancement: Added tools/ranked_fill_qa.py. After recommended_publish_fill.py, one command extracts ranked fields via shared phrase_utils extractors, reports presence and word-count against the fill writer's windows, and aggregates the existing no-write publish-surface scanners. Compounds ranking into a single post-fill QA step.
- Real production-path capability. Reduces sequential scanner invocations and manual length checks on every future packet.
- Human labor reduction: one command after fill produces a complete ranked-metadata review brief instead of five separate scanner runs plus manual presence checks.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 964 enhancement: Fixed extract_recommended_thumbnail to match `## Thumbnail text` (the label written by recommended_publish_fill.py). Previously only `## Thumbnail` matched, so ranked thumbnail text was silently skipped and thumbnail_generator fell through to mechanism/title. Added extract_recommended_first_comment, extract_recommended_title, extract_recommended_description. Added tools/first_comment_preview.py preferring ranked First comment. Compounds ranking into first-comment review and restores ranked thumbnail preference on every future packet.
- Real production-path bugfix + small reusable capability. Ranked thumbnail text now reaches the visual tool; first-comment has a glanceable preview parallel to cta_preview.
- Human labor reduction: one fewer silent mismatch between ranked metadata and thumbnail PNG; one command after fill produces an aligned first-comment preview without opening publish.md.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

(Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.)
