# PROGRESS

- Run 961 enhancement: tools/card_generator.py updated so CTA / install-related text-cards prefer ranked End screen text extracted from local recommended_publish_fill.md when present (before idea.md mechanism fallback). Reduces future manual copy of the aligned CTA phrase into the card generator and lowers mismatch risk between metadata selection and on-card text. No writes to publish.md, no invented text, no secrets polled. Compounds the selector and fill work into the card step.
- Small reusable visual-asset alignment improvement. Card source for CTA now sits after ranking/fill.
- Human labor reduction: lower chance of manually transferring the recommended end-screen text; one command after fill produces aligned CTA cards.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

- Run 960 enhancement: tools/end_screen_preview.py updated to prefer ranked End screen text extracted from local recommended_publish_fill.md when present (before script.md CTA fallback). Reduces future manual copy of the aligned CTA phrase into the end-screen preview and lowers mismatch risk between metadata selection and on-screen text. No writes to publish.md, no invented text, no secrets polled. Compounds the selector and fill work into the end-screen step.
- Small reusable visual-asset alignment improvement. End-screen source now sits after ranking/fill.
- Human labor reduction: lower chance of manually transferring the recommended end-screen text; one command after fill produces an aligned preview PNG.
- Videos published remain 0. Stall continues. Preferred list still complete. Next high-value action is the human OAuth step or another truly new production capability.

(Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.)
