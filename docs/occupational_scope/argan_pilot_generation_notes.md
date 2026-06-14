# ArGAN Pilot Generation Notes

## Purpose

The ArGAN-format pilot was used to test prompt-based Arabic gender-bias evaluation.

Unlike the occupational benchmark and APGC-format pilot, ArGAN-style evaluation is not based on masculine/feminine sentence-pair likelihood scoring. It requires model generation and output annotation.

## Observed Behavior

Two models were tested in the pilot:

- `Qwen/Qwen2.5-0.5B`
- `facebook/xglm-564M`

The generation pipeline worked, but the outputs showed quality limitations.

Observed issues included:

1. prompt echoing,
2. repetitive output,
3. incomplete generation,
4. weak instruction following.

## Interpretation

These issues are expected because the tested models are base causal language models rather than instruction-tuned chat models.

Therefore, the ArGAN-format pilot should be treated as a generation-pipeline validation step, not as a final bias result.

## Recommended Next Step

For proper ArGAN-style prompt evaluation, instruction-tuned models should be used, such as Arabic-capable chat/instruct models.

The occupational benchmark remains the main thesis benchmark because it uses controlled sentence-pair scoring and does not depend on open-ended generation quality.