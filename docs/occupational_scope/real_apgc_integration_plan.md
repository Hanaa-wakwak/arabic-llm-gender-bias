# Real APGC Integration Plan

## Purpose

The APGC-format pilot sample confirmed that the thesis scoring pipeline can be applied to external Arabic grammatical-gender sentence pairs.

The next step is to replace the small manual pilot sample with real APGC data.

## Current Pilot

Current pilot file:

`data/external_datasets/apgc/apgc_gender_pairs_sample.csv`

This file contains only 10 manually created APGC-format sentence pairs.

It is useful for testing the pipeline, but it is not large enough for final statistical claims.

## Target Real Dataset

The real APGC dataset should be converted into the thesis pairwise format:

| Column             | Description                |
| ------------------ | -------------------------- |
| id                 | unique pair ID             |
| source_dataset     | APGC                       |
| masculine_sentence | masculine sentence variant |
| feminine_sentence  | feminine sentence variant  |
| gender_context     | grammatical gender context |
| notes              | processing notes           |

## Why APGC Is Useful

The main benchmark measures occupational gender bias.

APGC can measure broader Arabic grammatical-gender preference beyond occupations.

This helps answer:

> Do the same models show masculine/feminine preference in general Arabic gendered sentences, not only occupational sentences?

## Integration Strategy

The real APGC integration should be done in three stages:

1. Inspect the original APGC file columns.
2. Convert masculine/feminine sentence variants into the thesis pairwise format.
3. Score the converted APGC pairs using the same model scoring script.

## Important Rule

APGC should not replace the occupational benchmark.

It should be used as an auxiliary external validation dataset.

## Recommended Thesis Wording

> The occupational benchmark remains the main thesis contribution. APGC is used as an external grammatical-gender validation dataset to test whether the sentence-pair scoring method generalizes beyond occupation-specific examples.

## Expected Output Files

The converted APGC files should be stored as:

`data/external_datasets/apgc/apgc_gender_pairs_real.csv`

The scored outputs should be stored in:

`results/external_datasets/apgc_real/`

## Analysis

The same scoring formula will be used:

```text
score_difference = masculine_score - feminine_score
```

Positive values indicate masculine preference.

Negative values indicate feminine preference.

Near-zero values indicate no clear preference.
