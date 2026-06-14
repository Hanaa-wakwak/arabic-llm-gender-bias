# Final Enriched Model Results

## Purpose

This document summarizes the enriched model experiment for the Arabic occupational gender-bias thesis.

The original main experiment evaluated four causal language models:

* AraGPT2-base,
* AraGPT2-medium,
* BLOOM-560m,
* BLOOM-1b1.

To strengthen the robustness of the findings, two additional non-Arabic-specific causal language models were evaluated:

* XGLM-564M,
* Qwen2.5-0.5B.

All six models were evaluated on the same final benchmark:

`data/occupational_benchmark/occupational_bias_v2.csv`

## Final Benchmark

The benchmark contains:

| Component                | Count |
| ------------------------ | ----: |
| Occupations              |    60 |
| Fields                   |     6 |
| Templates per occupation |     4 |
| Sentence pairs           |   240 |

## All Six Models

| Model          | Family              | Category                  |
| -------------- | ------------------- | ------------------------- |
| AraGPT2-base   | Arabic-specific     | Arabic-specific           |
| AraGPT2-medium | Arabic-specific     | Arabic-specific           |
| BLOOM-560m     | Non-Arabic-specific | Multilingual-BLOOM        |
| BLOOM-1b1      | Non-Arabic-specific | Multilingual-BLOOM        |
| XGLM-564M      | Non-Arabic-specific | Multilingual-XGLM         |
| Qwen2.5-0.5B   | Non-Arabic-specific | General-multilingual-Qwen |

## Overall Results by Model

| Model          | Masculine | Feminine | Equal | Direction | Average Score Difference |
| -------------- | --------: | -------: | ----: | --------- | -----------------------: |
| AraGPT2-base   |       152 |       88 |     0 | Masculine |                  +0.1257 |
| AraGPT2-medium |       168 |       72 |     0 | Masculine |                  +0.2230 |
| BLOOM-1b1      |        91 |      147 |     2 | Feminine  |                  -0.1656 |
| BLOOM-560m     |        83 |      157 |     0 | Feminine  |                  -0.2174 |
| XGLM-564M      |        92 |      148 |     0 | Feminine  |                  -0.2138 |
| Qwen2.5-0.5B   |        80 |      158 |     2 | Feminine  |                  -0.3425 |

## Overall Results by Model Family

| Model Family        | Total Items | Masculine | Feminine | Equal | Main Direction |
| ------------------- | ----------: | --------: | -------: | ----: | -------------- |
| Arabic-specific     |         480 |       320 |      160 |     0 | Masculine      |
| Non-Arabic-specific |         960 |       346 |      610 |     4 | Feminine       |

## Percentages by Model Family

| Model Family        | Masculine % | Feminine % | Equal % |
| ------------------- | ----------: | ---------: | ------: |
| Arabic-specific     |      66.67% |     33.33% |   0.00% |
| Non-Arabic-specific |      36.04% |     63.54% |   0.42% |

## Statistical Significance by Model

All six models show statistically significant overall gender preference.

| Model          | Direction | Binomial p-value | Wilcoxon p-value |
| -------------- | --------- | ---------------: | ---------------: |
| AraGPT2-base   | Masculine |         4.33e-05 |         2.79e-04 |
| AraGPT2-medium | Masculine |         5.13e-10 |         3.29e-08 |
| BLOOM-1b1      | Feminine  |         3.44e-04 |         8.51e-05 |
| BLOOM-560m     | Feminine  |         2.05e-06 |         5.76e-07 |
| XGLM-564M      | Feminine  |         3.64e-04 |         7.93e-07 |
| Qwen2.5-0.5B   | Feminine  |         4.79e-07 |         7.33e-13 |

## Model-Family Association

The chi-square test shows a highly significant association between model family and gender-preference direction:

```text
chi-square p-value = 1.64e-27
```

This means that the difference between Arabic-specific and non-Arabic-specific models is highly unlikely to be random.

## Pairwise Model Comparison

Pairwise Wilcoxon comparisons show that:

1. AraGPT2-base significantly differs from BLOOM-1b1, BLOOM-560m, XGLM-564M, and Qwen2.5-0.5B.
2. AraGPT2-medium significantly differs from BLOOM-1b1, BLOOM-560m, XGLM-564M, and Qwen2.5-0.5B.
3. BLOOM-1b1, BLOOM-560m, and XGLM-564M do not significantly differ from each other after correction.
4. Qwen2.5-0.5B is more strongly feminine than some other non-Arabic-specific models, but it still follows the same overall feminine-preference direction.

## Main Enriched Finding

The enriched six-model experiment supports the main thesis finding:

> Arabic-specific AraGPT2 causal language models show statistically significant masculine occupational preference, while non-Arabic-specific multilingual/general causal language models show statistically significant feminine occupational preference.

## Why This Strengthens the Thesis

The enriched experiment strengthens the thesis because the original pattern is no longer limited to BLOOM models.

The feminine preference pattern appears in:

* BLOOM-560m,
* BLOOM-1b1,
* XGLM-564M,
* Qwen2.5-0.5B.

This suggests that the contrast is more generally related to model family and pretraining background, not only to one specific model architecture.

## Recommended Thesis Framing

The main thesis experiment remains the controlled occupational benchmark v2.

The enriched model experiment should be presented as a robustness experiment.

Recommended wording:

> After the initial four-model experiment, two additional non-Arabic-specific causal language models were evaluated on the same benchmark. Both XGLM-564M and Qwen2.5-0.5B showed overall feminine occupational preference, reinforcing the model-family pattern observed in the original experiment. Therefore, the expanded six-model analysis strengthens the conclusion that occupational gender-preference direction differs between Arabic-specific and non-Arabic-specific causal language models.

## Final Note

The labels should be used carefully:

* AraGPT2 models should be called Arabic-specific models.
* BLOOM and XGLM should be called multilingual models.
* Qwen should be called a general/multilingual causal model.
* The combined group can be called non-Arabic-specific models.
