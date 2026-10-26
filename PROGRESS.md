# PROGRESS

- Reusable capability: tools/script_visual_plan.py extracts key sentences from spoken WORDS and prints a structured Markdown visual plan section mapping each signal to a suggested short card text (via shared shorten) with blank slots for broll_or_visual_note and card_file. Agents or humans run one command instead of manually scanning the script and drafting visual/asset plans from scratch for every future packet. No invented visuals or content. Reduces assets-stage planning friction before every future packet.
- Small new production tool only. No packet writes, no secrets polled.
- Human labor reduction: lower time and cognitive load when planning on-screen text cards and b-roll notes from the current script; one command replaces manual visual plan drafting.
- Videos published remain 0. Stall continues. Preferred list still complete. Pre-upload path stable. Next high-value action is the human OAuth step or another truly new production capability.

- Reusable capability: tools/script_experiment_candidates.py extracts potential questions/objections and long sentences (retention risks) from spoken WORDS and prints a structured Markdown section mapping each signal to a suggested ALLOWED_CHANGES type with blank slots for hypothesis, primary_metric, and notes. Agents or humans run one command instead of manually scanning the script and mapping risks to single-variable test candidates for the next packet on every future video. No invented hypotheses, metrics, or decisions. Reduces next-packet experiment-selection friction before every future packet.
- Small new production tool only. No packet writes, no secrets polled.
- Human labor reduction: lower time and cognitive load when choosing the next single variable to test from the current content; one command replaces manual candidate drafting.
- Videos published remain 0. Stall continues. Preferred list still complete. Pre-upload path stable. Next high-value action is the human OAuth step or another truly new production capability.

- Reusable capability: tools/feedback_to_experiment_bridge.py extracts potential viewer questions/objections from spoken WORDS and prints a structured Markdown bridge section mapping each baseline question to blank slots for possible_change, hypothesized_effect, target_metric, and next_test_idea. Agents or humans run one command instead of manually drafting the connection from anticipated questions to candidate experiments after the observation window on every future packet. No invented comments, changes, or metrics. Reduces post-observation experiment-preparation friction before every future packet.
- Small new production tool only. No packet writes, no secrets polled.
- Human labor reduction: lower time and cognitive load when turning anticipated questions into explicit test ideas; one command replaces manual bridge drafting.
- Videos published remain 0. Stall continues. Preferred list still complete. Pre-upload path stable. Next high-value action is the human OAuth step or another truly new production capability.
