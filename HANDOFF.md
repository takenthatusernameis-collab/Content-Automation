# HANDOFF

Updated: 2026-10-01T14:12:00Z (Run 247)

This file is not Selected VO. Audio and card PNGs stay gitignored. Do not `git add -f`.

## Why this file exists
Run 242 synthesized a labeled generated take and called it operator-downloadable. Run 243 found an empty workspace. Run 244 found the same empty workspace and uploaded the wav to Drive. Run 245 confirmed that Drive file still lists 27200958 bytes and the same sha256, then added the seven planned cards. Run 246 matched those checksums again and found that an unauthenticated curl of the wav file id returns a Google sign-in page. Run 247 downloaded the same Drive bytes into the current operator session (`q1-handoff/` and `q1-handoff-verified.zip`) and matched sha256 again. That session folder is the human copy source for this chat. It is not durable for the next agent, and it is not the packet DROP path.

## Current operator file
- Name: `002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`
- Durable copy: Google Drive file id `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl`
- Folder: `Content-Automation-handoff` (`1ftaVyh8BWQeWp45TIyX7Hh1o0MPmGRev`)
- Link: https://drive.google.com/file/d/1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl/view
- Bytes: 27200958
- Duration: 308.40 s
- Format: 44.1 kHz, mono, s16 wav
- Voice: edge-tts `en-US-AndrewNeural` (espeak-ng still cannot be installed in this sandbox)
- SHA256: `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2`
- Drive listing size_bytes: 27200958 (re-listed Run 245; local re-download sha256 matched again Runs 246 and 247). Level constants measured on the Run 244 decode: peak=0.7713, rms=0.1012, silence_frac=0.5089, clip_frac=0.0000. Those four would PASS if the same file were at the DROP path. Cards and export would still FAIL until the PNGs below are copied and a master exists.
- kind: generated. Not a human recording. Not gate-machine Selected VO.
- Anonymous fetch: not available. Run 246 `curl -L` of the uc export URL saved an HTML sign-in page, not this wav.
- Run 247 session copy: operator artifacts `q1-handoff/` plus zip `q1-handoff-verified.zip` (19908838 bytes). Next agent workspace may be empty. Use the Drive file id, not the zip path.

## Cards (not packet-ready until copied)
Same Drive folder. Generator rules match `tools/card_generator.py` (1920x1080). `cards.sha256` file id `1Exe7TolCKO8f7-vZ6HCSseGEmrVLyU2x` (846 bytes). Do not regenerate while those file ids list the sizes below. Do not mark `assets.md` ready in git until the PNGs exist under the packet `cards/` directory. Runs 246 and 247 matched these sha256 values on download.

| Packet path | Drive file id | Bytes | SHA256 |
|-------------|---------------|------:|--------|
| `cards/hook-card-on-a-closed-laptop-one-handwritte.png` | `1y21dpFuelq-IP2chdd-eg4qmLJRPlPkJ` | 42073 | `820cb09df9806151ed43336deab9dac656cae2dc8d9f6b6c38dee64c02d51982` |
| `cards/payoff-same-card-stop-rule-under-the-sentenc.png` | `1iN3N2BRsy2Ka4xZKbrRIsFBnRY_Flj0n` | 27644 | `a8e6660f152afac65981b2eee6ec34efc9eacc151b19aa1af0ba23fa7aafaf9a` |
| `cards/beat1-split-open-task-board-vs-one-index-car.png` | `1Hqmxzcl6_UoK6ZdlLSiK6_7GtjFURogf` | 27977 | `6fb7611f515ceee6682e140f9e14c637238143555b542851cfbb7fc031a8e20d` |
| `cards/beat2-hand-writing-verb-object-place-on-a-ca.png` | `1N1mU8QWq7RfqaAwu8BDu3iXT59w6bqNm` | 35279 | `e0f306a8c5d41dde81edbab5e2fa70544be075ebcad98dd5a38dc50e69f3af3d` |
| `cards/beat3-four-crossed-out-themes-replaced-by-on.png` | `1mtfPsr06AwxTXvnqnHFBQPxaEzJ-TuRG` | 34701 | `96e2ff34fe8f84b9f99f4094ed443a4606cb979758e084451d0fc1e3b5cc6b33` |
| `cards/beat4-night-card-morning-start-shutdown-rewr.png` | `1ug0ax6vynDtWsaTDamXyeV02BHwikN0r` | 35053 | `0510c7d67b550a6c87fff801238fd5da1430db8c06a417f404bacba8522a74cc` |
| `cards/cta-cta-card-write-tomorrow-s-next-action-on.png` | `1Tne_yISXFwl8_5HA_aJjWnC_4j53xnIp` | 39935 | `b0f67d7c5ad085f5e2882fdcda67a2e363a171d544d854b8c43d3b5d492e56e9` |

## Fetch without regenerating
If the artifacts file is missing, download Drive file id `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl` with the connected Drive account and check sha256. Do not synthesize again while that Drive file lists 27200958 bytes. Download the seven card ids above instead of re-running the card renderer while those sizes match. Regeneration is allowed only if both the Drive file and this checksum are gone. Do not use an unauthenticated curl; it returns a Google sign-in page. Do not treat a session zip as Selected VO.

## Copy (gate machine only)
The gate machine must receive these files from a signed-in session. A public link is not enough. Run 247 left a zip in the operator chat for that copy.

```bash
PACKET=videos/002-stop-deciding-what-to-work-on-every-morning
DROP="$PACKET/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav"
mkdir -p "$PACKET/vo" "$PACKET/cards"
cp -n /path/to/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav "$DROP"
cp -n /path/to/cards/*.png "$PACKET/cards/"
sha256sum "$DROP"
# expect 758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2
python3 tools/narration_adapter.py "$PACKET"
python3 tools/card_generator.py "$PACKET" --inspect-only
```
Keep `vo_origin.md` kind=generated. Do not commit the wav or the PNGs.
