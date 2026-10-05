# Channel (working lock)

Status: **temporary default**. A human may replace this. Do not reopen the debate in agent runs until DECISIONS.md changes.

## Niche
Systems for doing focused work. Productivity as process design, not motivation.

## Audience
People who already plan their week, then stall when it is time to start.

## Audience designation
audience_designation: not_made_for_kids

category_id: 27

YouTube snippet.categoryId. 27 is Education and matches the previous videos.insert hardcode. An unknown or missing id is METADATA_REJECTED before the token refresh. Do not omit it. Do not change it unless the channel decision changes.

license: youtube

playlist_id: not_set

One series playlist for this channel. not_set means do not call playlistItems.insert and do not invent a PL id. Upload does not wait on this field. After a human creates the playlist in Studio, replace this line with that id. The production job then adds the provider video id. A missing id still does not start videos.insert.

YouTube status.license. youtube is the standard license. creativeCommon is the other accepted value. An unknown or missing license is METADATA_REJECTED before the token refresh. Do not invent creativeCommon.

YouTube `status.selfDeclaredMadeForKids` must be present and false for this channel. Omitting the field uploads a video that stays blocked until Studio sets the audience. Do not change this line to `made_for_kids` unless the channel decision changes. Do not omit it.

## Promise
After each video the viewer can install one small default (cue, constraint, or checklist) the same day.

## Format
- 6–10 minute explainer
- On-screen text + b-roll notes (no requirement for a face)
- Target duration: 8 minutes
- Cadence target: 1 video / week once a production path exists

## Voice
Calm, specific, operational. Name the stall. Name the default. Tell the viewer where it lives.

## Out of scope
Guru motivation, morning-routine flex, income claims, tool-of-the-week reviews unless the tool *is* the constraint.
