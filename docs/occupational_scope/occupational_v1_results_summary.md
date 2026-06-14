# Occupational Benchmark v1 Results Summary

## Scope Refinement

Based on supervisor feedback, the thesis scope was narrowed from general Arabic gender bias to occupational gender bias.

The new scope focuses on measuring gender preference in Arabic job-role sentences across different professional fields.

The updated benchmark is:

`occupational_bias_v1.csv`

It contains 144 masculine/feminine counterfactual sentence pairs.

## Benchmark Design

The benchmark covers six occupational fields:

1. STEM
2. Healthcare
3. Education
4. Business
5. Legal/Government
6. Media/Creative

Each occupation is represented using masculine and feminine Arabic forms.

Each pair preserves the same meaning and context, while only the gender-marked forms change.

The benchmark includes both Modern Standard Arabic and Egyptian Arabic templates.

## Bias Measurement

Bias is measured using sentence-level score differences.

The score is computed as:

`score_difference = masculine_score - feminine_score`

Interpretation:

* Positive score difference means the model prefers the masculine version.
* Negative score difference means the model prefers the feminine version.
* Values close to zero suggest a more balanced preference.

The results are aggregated by model, model family, occupational field, dialect, and template.

## Evaluated Models

Four causal language models were evaluated:

| Model                     | Model Family    |
| ------------------------- | --------------- |
| aubmindlab/aragpt2-base   | Arabic-specific |
| aubmindlab/aragpt2-medium | Arabic-specific |
| bigscience/bloom-560m     | Multilingual    |
| bigscience/bloom-1b1      | Multilingual    |

The purpose of this model selection is to compare Arabic-specific causal language models with multilingual causal language models.

## Overall Results

| Model                     | Model Family    | Masculine Preferred | Feminine Preferred | Average Score Difference | Direction |
| ------------------------- | --------------- | ------------------: | -----------------: | -----------------------: | --------- |
| aubmindlab/aragpt2-base   | Arabic-specific |                  96 |                 48 |                   0.2021 | Masculine |
| aubmindlab/aragpt2-medium | Arabic-specific |                 105 |                 39 |                   0.2590 | Masculine |
| bigscience/bloom-1b1      | Multilingual    |                  45 |                 98 |                  -0.2400 | Feminine  |
| bigscience/bloom-560m     | Multilingual    |                  39 |                105 |                  -0.3239 | Feminine  |

## Main Finding

The Arabic-specific AraGPT2 models show statistically significant masculine occupational preference.

The multilingual BLOOM models show statistically significant feminine occupational preference.

This indicates that model family is strongly associated with the measured direction of occupational gender preference.

## Statistical Testing

Binomial tests showed that all four models significantly deviate from a balanced 50/50 masculine/feminine preference distribution.

Wilcoxon signed-rank tests also showed that the score-difference distributions for all four models significantly deviate from zero.

The chi-square test between model family and gender preference was significant:

`p = 5.74e-22`

This supports the conclusion that Arabic-specific and multilingual models behave differently on the occupational benchmark.

## Field-Level Findings

For AraGPT2-base, the strongest significant masculine preferences appeared in:

* Business
* Media/Creative

For AraGPT2-medium, significant masculine preferences appeared in:

* Business
* Education
* Legal/Government
* Media/Creative

For BLOOM-1b1, significant feminine preferences appeared in:

* Education
* Healthcare
* STEM

For BLOOM-560m, significant feminine preferences appeared in:

* Education
* Healthcare

## Corrected Pairwise Model Comparison

Pairwise Wilcoxon tests with multiple-comparison correction showed that comparisons between AraGPT2 models and BLOOM models remained statistically significant.

The comparison between AraGPT2-base and AraGPT2-medium was not significant after correction, suggesting that the two Arabic-specific models behave similarly.

The comparison between BLOOM-1b1 and BLOOM-560m was weaker and did not remain significant under the most conservative correction methods.

Therefore, the strongest distinction is between model families rather than only model size.

## Thesis Interpretation

The occupation-only benchmark provides a clearer and more defensible research scope than the earlier mixed occupation-and-trait benchmark.

The results suggest that Arabic occupational gender-bias evaluation should consider:

1. model family,
2. occupational field,
3. dialect,
4. sentence template design,
5. statistical significance.

The current findings support the thesis direction of building a counterfactual, dialect-aware occupational gender-bias benchmark for Arabic causal language models.
