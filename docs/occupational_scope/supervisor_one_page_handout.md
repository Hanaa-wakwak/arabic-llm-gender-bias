# Thesis Progress Summary

## Updated Thesis Topic

**Counterfactual Evaluation of Occupational Gender Bias in Arabic Causal Language Models**

## Scope Refinement

Based on supervisor feedback, the thesis scope was narrowed from general Arabic gender bias to **occupational gender bias**.

The previous benchmark included occupations and traits. It is now treated as a pilot experiment. The main thesis benchmark now focuses only on **jobs and professional fields**.

## Research Goal

The goal is to measure whether Arabic causal language models prefer masculine or feminine forms when scoring Arabic job-role sentences.

The benchmark is:

* counterfactual,
* occupation-focused,
* field-aware,
* dialect-aware,
* template-controlled.

## Benchmark Design

Current benchmark file:

`data/occupational_benchmark/occupational_bias_v1.csv`

The benchmark contains:

| Component           | Count |
| ------------------- | ----: |
| Sentence pairs      |   144 |
| Occupations         |    36 |
| Occupational fields |     6 |
| Arabic varieties    |     2 |
| Sentence templates  |     4 |

## Occupational Fields

The benchmark covers six fields:

1. STEM
2. Healthcare
3. Education
4. Business
5. Legal/Government
6. Media/Creative

Each field contains six occupations.

## Example Counterfactual Pair

Masculine:

`هذا طبيب يعمل في المستشفى`

Feminine:

`هذه طبيبة تعمل في المستشفى`

The meaning and context are preserved. Only the gender-marked Arabic forms change.

## Bias Measurement

For each pair:

`score_difference = masculine_score - feminine_score`

Interpretation:

* positive value → masculine preference,
* negative value → feminine preference,
* near zero → balanced preference.

The results are aggregated by model, model family, occupational field, dialect, template, and occupation.

## Evaluated Models

| Model          | Family          |
| -------------- | --------------- |
| AraGPT2-base   | Arabic-specific |
| AraGPT2-medium | Arabic-specific |
| BLOOM-560m     | Multilingual    |
| BLOOM-1b1      | Multilingual    |

The purpose is to compare Arabic-specific pretraining against multilingual pretraining.

## Main Preliminary Result

| Model          | Family          | Masculine Preferred | Feminine Preferred | Avg Score Difference | Direction |
| -------------- | --------------- | ------------------: | -----------------: | -------------------: | --------- |
| AraGPT2-base   | Arabic-specific |                  96 |                 48 |              +0.2021 | Masculine |
| AraGPT2-medium | Arabic-specific |                 105 |                 39 |              +0.2590 | Masculine |
| BLOOM-1b1      | Multilingual    |                  45 |                 98 |              -0.2400 | Feminine  |
| BLOOM-560m     | Multilingual    |                  39 |                105 |              -0.3239 | Feminine  |

## Statistical Findings

All four models show statistically significant occupational gender preference.

* AraGPT2 models show significant masculine occupational preference.
* BLOOM models show significant feminine occupational preference.

The chi-square test between model family and preference direction was significant:

`p = 5.74e-22`

This suggests that model family is strongly associated with measured occupational gender preference.

## Current Main Claim

Arabic-specific causal language models and multilingual causal language models show opposite occupational gender-preference patterns on the same Arabic counterfactual benchmark.

## Next Steps

1. Human validation of sentence naturalness and gender-pair equivalence.
2. Expand the benchmark with more occupations per field.
3. Add more Arabic and multilingual causal language models.
4. Add dialect-level and template-level robustness analysis.
5. Add token-level explainability.
6. Add mitigation experiments.
