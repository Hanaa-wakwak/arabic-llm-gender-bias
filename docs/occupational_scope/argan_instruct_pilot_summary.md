# ArGAN Instruct Pilot Summary

## Purpose

This pilot tested whether ArGAN-style Arabic gender-bias prompts can be evaluated using instruction-based generation.

The main thesis benchmark remains the controlled occupational benchmark:

`occupational_bias_v2.csv`

The ArGAN pilot is used as an external qualitative validation experiment.

## Model Tested

The improved pilot used:

`Qwen/Qwen2.5-0.5B-Instruct`

This model was selected because instruction-tuned models are more suitable for prompt-based evaluation than base causal language models.

## Prompting Strategy

Each Arabic prompt was wrapped with an instruction asking the model to:

* answer in one Arabic sentence,
* avoid repetition,
* avoid stereotypes,
* produce a professional and neutral response.

## Observed Output Behavior

The model produced more direct responses than base models, but several issues remained:

1. gender mismatch,
2. incomplete responses,
3. mixed-language tokens,
4. weak instruction following,
5. output longer than requested,
6. occasional prompt instability.

## Interpretation

The ArGAN instruct pilot confirms that the generation pipeline works, but the outputs are not reliable enough for final quantitative bias measurement.

Therefore, the ArGAN pilot should be treated as a qualitative external validation step and a limitation/future-work direction.

## Relation to Main Thesis Benchmark

The occupational benchmark remains stronger for the main thesis because it uses controlled masculine/feminine sentence pairs and sentence-likelihood scoring.

ArGAN-style prompt evaluation depends heavily on generation quality and instruction following.

## Recommended Thesis Wording

> The ArGAN-format pilot demonstrated that prompt-based Arabic bias evaluation requires instruction-tuned models and careful output annotation. Although the generation pipeline worked, the pilot outputs showed issues such as gender mismatch and weak instruction following. Therefore, ArGAN is reported as an external qualitative pilot rather than a final quantitative result.

## Next Step

A future version should use stronger Arabic-capable instruction models and human annotation before drawing final conclusions from ArGAN-style prompt outputs.
