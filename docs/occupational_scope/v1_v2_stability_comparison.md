# v1 vs v2 Occupational Benchmark Stability Comparison

## Purpose

This document compares the occupational benchmark v1 and v2 to decide which version should be used as the main thesis benchmark.

## Benchmark Sizes

| Version | Occupations | Fields | Templates | Sentence Pairs |
|---|---:|---:|---:|---:|
| v1 | 36 | 6 | 4 | 144 |
| v2 | 60 | 6 | 4 | 240 |

v2 expands the benchmark by adding 24 occupations while preserving the same six professional fields and the same four controlled sentence templates.

## Overall Model-Level Results

### v1 Overall Direction

| Model | Model Family | Direction |
|---|---|---|
| AraGPT2-base | Arabic-specific | Masculine |
| AraGPT2-medium | Arabic-specific | Masculine |
| BLOOM-1b1 | Multilingual | Feminine |
| BLOOM-560m | Multilingual | Feminine |

### v2 Overall Direction

| Model | Model Family | Masculine Count | Feminine Count | Direction | Binomial p-value |
|---|---|---:|---:|---|---:|
| AraGPT2-base | Arabic-specific | 152 | 88 | Masculine | 4.33e-05 |
| AraGPT2-medium | Arabic-specific | 168 | 72 | Masculine | 5.13e-10 |
| BLOOM-1b1 | Multilingual | 91 | 147 | Feminine | 3.44e-04 |
| BLOOM-560m | Multilingual | 83 | 157 | Feminine | 2.05e-06 |

## Stability of Main Finding

The central finding is stable across v1 and v2:

> Arabic-specific AraGPT2 models prefer masculine occupational sentences more often, while multilingual BLOOM models prefer feminine occupational sentences more often.

This means the thesis result is not dependent on the smaller v1 benchmark.

## Score-Difference Stability

In v2, average score differences are:

| Model | Average Score Difference | Median Score Difference | Direction |
|---|---:|---:|---|
| AraGPT2-base | +0.1257 | +0.2537 | Masculine |
| AraGPT2-medium | +0.2230 | +0.3249 | Masculine |
| BLOOM-1b1 | -0.1656 | -0.1934 | Feminine |
| BLOOM-560m | -0.2174 | -0.2168 | Feminine |

Positive values indicate masculine preference. Negative values indicate feminine preference.

## Statistical Stability

All four models show statistically significant overall gender preference in v2.

| Model | Binomial Significant | Wilcoxon Significant |
|---|---|---|
| AraGPT2-base | Yes | Yes |
| AraGPT2-medium | Yes | Yes |
| BLOOM-1b1 | Yes | Yes |
| BLOOM-560m | Yes | Yes |

The model-family association remains highly significant:

| Version | Chi-square p-value |
|---|---:|
| v1 | 5.74e-22 |
| v2 | 1.31e-20 |

Both versions show a strong association between model family and gender-preference direction.

## Field-Level Pattern in v2

The v2 benchmark gives more detailed field-level behavior.

### Arabic-specific Models

AraGPT2 models show strongest masculine preference in:

- Business,
- Legal/Government,
- STEM,
- Media/Creative.

Healthcare is weaker and less stable, which suggests that occupational bias is field-dependent rather than uniform.

### Multilingual Models

BLOOM models show strongest feminine preference in:

- Education,
- Healthcare,
- Media/Creative.

Business and Legal/Government are weaker or closer to balanced.

## Pairwise Model Comparison in v2

The pairwise Wilcoxon tests show that:

1. AraGPT2-base and AraGPT2-medium differ significantly in v2.
2. Each AraGPT2 model differs significantly from each BLOOM model.
3. BLOOM-1b1 and BLOOM-560m do not significantly differ from each other in v2.

This supports the conclusion that the largest difference is between Arabic-specific and multilingual model families.

## Interpretation

v2 is preferable because it:

1. has broader occupational coverage,
2. preserves the original controlled counterfactual design,
3. passes benchmark quality checks,
4. keeps the same overall model-family finding as v1,
5. provides stronger field-level analysis,
6. supports more reliable statistical testing due to larger sample size.

## Final Decision

v2 should be used as the main thesis benchmark.

v1 should be reported as an earlier controlled pilot or sanity-check experiment.

Recommended wording:

> After validating the smaller v1 benchmark, we expanded the occupational benchmark to v2 by increasing the number of occupations from 36 to 60 while preserving the same counterfactual template design. The main model-family pattern remained stable: Arabic-specific AraGPT2 models showed masculine occupational preference, while multilingual BLOOM models showed feminine occupational preference. Therefore, v2 is used as the main benchmark in the thesis, and v1 is treated as a pilot benchmark.