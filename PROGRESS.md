# PROGRESS

- Run 964 enhancement: Fixed extract_recommended_thumbnail to match `## Thumbnail text` (the label written by recommended_publish_fill.py). Previously only `## Thumbnail` matched, so ranked thumbnail text was silently skipped and thumbnail_generator fell through to mechanism/title. Added extract_recommended_first_comment, extract_recommended_title, extract_recommended_description. Added tools/first_comment_preview.py preferring ranked First comment. Compounds ranking into first-comment review and restores ranked thumbnail preference on every future packet.
- Real production-path bugfix + small reusable capability. Ranked thumbnail text now reaches the visual tool; first-comment has a glanceable preview parallel to cta_preview.
- Human labor reduction: one fewer silent mismatch between ranked metadata and thumbnail PNG; one command after fill produces an aligned first-comment preview without opening publish.md.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 963 enhancement: phrase_utils.py now provides extract_recommended_end_screen and extract_recommended_thumbnail. card_generator, cta_preview, end_screen_preview, and thumbnail_generator import them instead of maintaining local copies. Reduces future maintenance and mismatch risk on ranked metadata preference. No writes to publish.md, no invented text, no secrets polled. Compounds the selector and fill work into a shared helper.
- Small reusable consistency improvement. Visual tools share one extraction implementation.
- Human labor reduction: lower chance of one tool using a slightly different length or parsing rule than another.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

(Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.)
