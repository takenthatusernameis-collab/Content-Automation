# BLOCKED

External work is parked here so runs do not retry it blindly.

| Dependency            | Why needed                         | Simplest human setup                                      | Status   |
|-----------------------|------------------------------------|-----------------------------------------------------------|----------|
| Channel niche/brand   | Every template depends on it       | Confirm or replace `docs/channel.md`                      | temporary default set |
| YouTube Data API OAuth| Upload, titles, analytics          | Cloud project + OAuth client + token file documented      | not started |
| TTS or microphone VO  | Narration audio                    | Record to `vo/NNN-slug-take-selected.wav` or document a local TTS CLI | path convention exists; no vendor |
| Stock / original media| B-roll and thumbs                  | Decide “text-card + public-domain” vs licensed stock      | not started |
| ffmpeg render profile | Repeatable export                  | Add after first format lock                               | not started |

Do not poll APIs hoping credentials appear.
