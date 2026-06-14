# APGC-Format External Dataset Pilot Summary

## Purpose

This pilot tests whether the thesis scoring pipeline can be applied to external Arabic grammatical-gender sentence pairs.

The current sample is not the full APGC dataset. It is a small APGC-format pilot sample used to validate the external dataset pipeline.

## Dataset

The pilot file is:

`data/external_datasets/apgc/apgc_gender_pairs_sample.csv`

It contains 10 masculine/feminine Arabic sentence pairs.

The sentence pairs cover several grammatical-gender contexts, including:

* first-person adjective agreement,
* second-person adjective agreement,
* third-person pronoun and adjective agreement,
* demonstrative noun adjective agreement.

## Why This Pilot Matters

The main benchmark of the thesis focuses on occupational gender bias.

The APGC-format pilot checks whether the same scoring method can also be applied to broader Arabic grammatical-gender contexts beyond occupations.

## Models Evaluated

The pilot was scored using six causal language models:

| Model          | Family              |
| -------------- | ------------------- |
| AraGPT2-base   | Arabic-specific     |
| AraGPT2-medium | Arabic-specific     |
| BLOOM-560m     | Non-Arabic-specific |
| BLOOM-1b1      | Non-Arabic-specific |
| XGLM-564M      | Non-Arabic-specific |
| Qwen2.5-0.5B   | Non-Arabic-specific |

## Pilot Results

| Model          | Masculine Preferred | Feminine Preferred | Equal | Direction by Count |
| -------------- | ------------------: | -----------------: | ----: | ------------------ |
| AraGPT2-base   |                   6 |                  4 |     0 | Masculine          |
| AraGPT2-medium |                   6 |                  4 |     0 | Masculine          |
| BLOOM-560m     |                   5 |                  4 |     1 | Almost balanced    |
| BLOOM-1b1      |                   5 |                  5 |     0 | Balanced           |
| XGLM-564M      |                   2 |                  8 |     0 | Feminine           |
| Qwen2.5-0.5B   |                   4 |                  6 |     0 | Feminine           |

## Interpretation

The APGC-format pilot confirms that the external grammatical-gender scoring pipeline works.

Because the pilot contains only 10 sentence pairs, it should not be treated as a final statistical result.

However, the pilot is useful because it shows that the same sentence-pair scoring method can be reused for external Arabic gender-pair datasets.

## Relation to Main Benchmark

The main thesis benchmark remains:

`occupational_bias_v2.csv`

The APGC-format pilot is an auxiliary external validation step.

Recommended thesis wording:

> To test the extensibility of the scoring pipeline beyond occupations, a small APGC-format grammatical-gender pilot sample was constructed and scored using the same sentence-likelihood method. The pilot confirms that the method can be applied to external gender-pair data, but the sample is too small for final statistical claims.

## Next Step

The next step is to replace the manual APGC-format pilot with real APGC data, then convert a larger subset into the same pairwise scoring format.
