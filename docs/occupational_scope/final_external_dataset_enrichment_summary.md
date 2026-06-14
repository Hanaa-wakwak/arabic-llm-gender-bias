# Final External Dataset Enrichment Summary

## Purpose

This document summarizes the external dataset enrichment phase of the thesis.

The main thesis benchmark remains:

`data/occupational_benchmark/occupational_bias_v2.csv`

External datasets are used as auxiliary robustness and validation resources, not as replacements for the main occupational benchmark.

---

## Main Benchmark

The main benchmark is the internally constructed occupational benchmark v2.

It contains:

| Component                | Count |
| ------------------------ | ----: |
| Occupations              |    60 |
| Fields                   |     6 |
| Templates per occupation |     4 |
| Sentence pairs           |   240 |

This benchmark is used for the main quantitative thesis results.

---

## External Dataset 1 — APGC-Format Pilot

### Role

The APGC-format pilot tests whether the sentence-pair scoring pipeline can be applied to broader Arabic grammatical-gender sentence pairs beyond occupations.

### Dataset Used

`data/external_datasets/apgc/apgc_gender_pairs_sample.csv`

### Size

| Component        | Count |
| ---------------- | ----: |
| Sentence pairs   |    10 |
| Gender contexts  |     4 |
| Models evaluated |     6 |

### Models Evaluated

| Model          | Family              |
| -------------- | ------------------- |
| AraGPT2-base   | Arabic-specific     |
| AraGPT2-medium | Arabic-specific     |
| BLOOM-560m     | Non-Arabic-specific |
| BLOOM-1b1      | Non-Arabic-specific |
| XGLM-564M      | Non-Arabic-specific |
| Qwen2.5-0.5B   | Non-Arabic-specific |

### Pilot Result

| Model          | Masculine Preferred | Feminine Preferred | Equal | Direction          |
| -------------- | ------------------: | -----------------: | ----: | ------------------ |
| AraGPT2-base   |                   6 |                  4 |     0 | Masculine by count |
| AraGPT2-medium |                   6 |                  4 |     0 | Masculine by count |
| BLOOM-560m     |                   5 |                  4 |     1 | Almost balanced    |
| BLOOM-1b1      |                   5 |                  5 |     0 | Balanced           |
| XGLM-564M      |                   2 |                  8 |     0 | Feminine           |
| Qwen2.5-0.5B   |                   4 |                  6 |     0 | Feminine           |

### Interpretation

The APGC-format pilot confirms that the thesis scoring method can be reused for external masculine/feminine Arabic sentence pairs.

However, because the pilot contains only 10 pairs, it should be treated as a pipeline validation step rather than a final statistical result.

---

## External Dataset 2 — ArGAN-Format Pilot

### Role

The ArGAN-format pilot tests whether prompt-based Arabic gender-bias evaluation can be added to the thesis.

Unlike the occupational benchmark and APGC pilot, ArGAN-style evaluation depends on model generation and output annotation.

### Dataset Used

`data/external_datasets/argan/argan_gender_pilot_sample.csv`

### Size

| Component                  |                   Count |
| -------------------------- | ----------------------: |
| Arabic gender prompts      |                      10 |
| Prompt types               | generation / completion |
| Main tested instruct model |   Qwen2.5-0.5B-Instruct |

### Generation Quality Result

The ArGAN-Instruct pilot was evaluated using an automatic quality checker.

| Metric                        | Value |
| ----------------------------- | ----: |
| Total outputs                 |    10 |
| Empty outputs                 |     0 |
| Prompt echo outputs           |     0 |
| Repetition outputs            |     0 |
| Gender mismatch outputs       |     2 |
| Too short outputs             |     0 |
| Outputs needing manual review |     2 |
| Needs manual review percent   |   20% |
| Average output word count     |    23 |

### Interpretation

The ArGAN-Instruct pilot shows that prompt-based Arabic bias evaluation is possible, but it requires stronger instruction-following models and manual output annotation.

The pilot is useful as qualitative external validation, but it is not strong enough to be treated as a final quantitative bias result.

---

## Final Dataset-Enrichment Decision

The final thesis should use the datasets as follows:

| Dataset                   | Role in Thesis                                  |
| ------------------------- | ----------------------------------------------- |
| Occupational benchmark v2 | Main quantitative benchmark                     |
| APGC-format pilot         | External grammatical-gender pipeline validation |
| ArGAN-format pilot        | Qualitative prompt-based external pilot         |
| AraWEAT                   | Related-work / lexical comparison resource      |
| Real APGC                 | Future extension                                |
| Full ArGAN                | Future extension                                |

---

## Recommended Thesis Framing

The main thesis contribution remains the controlled occupational counterfactual benchmark.

The external datasets strengthen the work by showing that the pipeline can be extended beyond the custom benchmark.

Recommended wording:

> The occupational benchmark v2 is used as the main quantitative benchmark. External dataset pilots based on APGC and ArGAN are added to test the extensibility of the evaluation pipeline. APGC demonstrates that the sentence-pair scoring method can generalize to broader Arabic grammatical-gender examples, while ArGAN demonstrates the feasibility and limitations of prompt-based Arabic bias evaluation.

---

## Final Conclusion

External dataset enrichment strengthens the thesis, but the main final result should still be based on the occupational benchmark v2 and the six-model analysis.

The external pilots should be presented as:

1. robustness evidence,
2. pipeline validation,
3. future-work preparation,
4. external-resource alignment.
