# Chapter 4 — Experiments and Results

## 4.1 Introduction

This chapter presents the experimental results of measuring occupational gender bias in Arabic causal language models.

The experiments use the final benchmark version:

`occupational_bias_v2.csv`

This benchmark contains 60 occupations, six professional fields, four templates per occupation, and 240 masculine/feminine counterfactual sentence pairs.

The chapter first reports the original four-model experiment, then presents the enriched six-model robustness experiment.

---

## 4.2 Experimental Setup

The benchmark was evaluated using causal language models. For each masculine/feminine sentence pair, the model assigned a score to both sentence versions.

The score difference was computed as:

```text
score_difference = masculine_score - feminine_score
```

A positive value indicates masculine preference, while a negative value indicates feminine preference.

The final benchmark includes:

| Component                | Count |
| ------------------------ | ----: |
| Occupations              |    60 |
| Occupational fields      |     6 |
| Templates per occupation |     4 |
| Sentence pairs           |   240 |

---

## 4.3 Original Four-Model Experiment

The original experiment evaluated four causal language models:

| Model          | Model Family    |
| -------------- | --------------- |
| AraGPT2-base   | Arabic-specific |
| AraGPT2-medium | Arabic-specific |
| BLOOM-560m     | Multilingual    |
| BLOOM-1b1      | Multilingual    |

The purpose of this experiment was to compare Arabic-specific causal language models against multilingual causal language models.

---

## 4.4 Original Four-Model Overall Results

| Model          | Family          | Masculine Preferred | Feminine Preferred | Equal | Direction |
| -------------- | --------------- | ------------------: | -----------------: | ----: | --------- |
| AraGPT2-base   | Arabic-specific |                 152 |                 88 |     0 | Masculine |
| AraGPT2-medium | Arabic-specific |                 168 |                 72 |     0 | Masculine |
| BLOOM-1b1      | Multilingual    |                  91 |                147 |     2 | Feminine  |
| BLOOM-560m     | Multilingual    |                  83 |                157 |     0 | Feminine  |

The results show a clear model-family pattern. The two Arabic-specific AraGPT2 models prefer masculine occupational sentences, while the two multilingual BLOOM models prefer feminine occupational sentences.

---

## 4.5 Original Four-Model Percentages

| Model          | Masculine % | Feminine % | Equal % | Direction |
| -------------- | ----------: | ---------: | ------: | --------- |
| AraGPT2-base   |      63.33% |     36.67% |   0.00% | Masculine |
| AraGPT2-medium |      70.00% |     30.00% |   0.00% | Masculine |
| BLOOM-1b1      |      37.92% |     61.25% |   0.83% | Feminine  |
| BLOOM-560m     |      34.58% |     65.42% |   0.00% | Feminine  |

AraGPT2-medium shows the strongest masculine preference among the original models. BLOOM-560m shows the strongest feminine preference among the original four models.

---

## 4.6 Average Score Differences

| Model          | Average Score Difference | Median Score Difference | Direction |
| -------------- | -----------------------: | ----------------------: | --------- |
| AraGPT2-base   |                  +0.1257 |                 +0.2537 | Masculine |
| AraGPT2-medium |                  +0.2230 |                 +0.3249 | Masculine |
| BLOOM-1b1      |                  -0.1656 |                 -0.1934 | Feminine  |
| BLOOM-560m     |                  -0.2174 |                 -0.2168 | Feminine  |

The score-difference analysis supports the preference-count results. Positive average score differences appear for the AraGPT2 models, while negative average score differences appear for the BLOOM models.

---

## 4.7 Statistical Significance of the Original Experiment

### 4.7.1 Binomial Test

| Model          | Direction | Binomial p-value | Significant |
| -------------- | --------- | ---------------: | ----------- |
| AraGPT2-base   | Masculine |         4.33e-05 | Yes         |
| AraGPT2-medium | Masculine |         5.13e-10 | Yes         |
| BLOOM-1b1      | Feminine  |         3.44e-04 | Yes         |
| BLOOM-560m     | Feminine  |         2.05e-06 | Yes         |

The binomial test shows that all four models have statistically significant gender-preference counts.

### 4.7.2 Wilcoxon Signed-Rank Test

| Model          | Direction | Wilcoxon p-value | Significant |
| -------------- | --------- | ---------------: | ----------- |
| AraGPT2-base   | Masculine |         2.79e-04 | Yes         |
| AraGPT2-medium | Masculine |         3.29e-08 | Yes         |
| BLOOM-1b1      | Feminine  |         8.51e-05 | Yes         |
| BLOOM-560m     | Feminine  |         5.76e-07 | Yes         |

The Wilcoxon test shows that the score differences are significantly different from zero for all four models.

---

## 4.8 Original Model-Family Analysis

The chi-square test was used to examine whether model family is associated with gender-preference direction.

For the original four-model experiment, the model-family chi-square result was:

```text
chi-square p-value = 1.31e-20
```

This indicates a highly significant association between model family and preference direction.

The result suggests that Arabic-specific models and multilingual models behave differently on the occupational gender-bias benchmark.

---

## 4.9 Field-Level Results

The field-level analysis shows that gender preference is not uniform across all professional domains.

### 4.9.1 Arabic-Specific Models

The AraGPT2 models show stronger masculine preference in:

* Business,
* Legal/Government,
* STEM,
* Media/Creative.

Healthcare is weaker and less stable, which suggests that the strength and direction of bias can vary by field.

### 4.9.2 Multilingual Models

The BLOOM models show stronger feminine preference in:

* Education,
* Healthcare,
* Media/Creative.

Business and Legal/Government are weaker or closer to balanced.

This field-level variation shows that occupational bias should be analyzed by professional domain rather than only by overall model score.

---

## 4.10 Enriched Six-Model Robustness Experiment

To test whether the original pattern was limited to the BLOOM model family, two additional non-Arabic-specific causal language models were evaluated:

| Model        | Category                       |
| ------------ | ------------------------------ |
| XGLM-564M    | Multilingual causal LM         |
| Qwen2.5-0.5B | General/multilingual causal LM |

Both models were evaluated on the same final benchmark, `occupational_bias_v2.csv`.

This produced a total of six evaluated models:

| Model          | Family              | Category                  |
| -------------- | ------------------- | ------------------------- |
| AraGPT2-base   | Arabic-specific     | Arabic-specific           |
| AraGPT2-medium | Arabic-specific     | Arabic-specific           |
| BLOOM-560m     | Non-Arabic-specific | Multilingual-BLOOM        |
| BLOOM-1b1      | Non-Arabic-specific | Multilingual-BLOOM        |
| XGLM-564M      | Non-Arabic-specific | Multilingual-XGLM         |
| Qwen2.5-0.5B   | Non-Arabic-specific | General-multilingual-Qwen |

---

## 4.11 Enriched Six-Model Overall Results

| Model          | Family              | Masculine Preferred | Feminine Preferred | Equal | Direction | Average Score Difference |
| -------------- | ------------------- | ------------------: | -----------------: | ----: | --------- | -----------------------: |
| AraGPT2-base   | Arabic-specific     |                 152 |                 88 |     0 | Masculine |                  +0.1257 |
| AraGPT2-medium | Arabic-specific     |                 168 |                 72 |     0 | Masculine |                  +0.2230 |
| BLOOM-1b1      | Non-Arabic-specific |                  91 |                147 |     2 | Feminine  |                  -0.1656 |
| BLOOM-560m     | Non-Arabic-specific |                  83 |                157 |     0 | Feminine  |                  -0.2174 |
| XGLM-564M      | Non-Arabic-specific |                  92 |                148 |     0 | Feminine  |                  -0.2138 |
| Qwen2.5-0.5B   | Non-Arabic-specific |                  80 |                158 |     2 | Feminine  |                  -0.3425 |

The two additional models also show overall feminine occupational preference. This strengthens the original finding because the feminine preference pattern is not limited to BLOOM models only.

---

## 4.12 Enriched Model-Family Aggregation

| Model Family        | Total Items | Masculine Preferred | Feminine Preferred | Equal | Direction |
| ------------------- | ----------: | ------------------: | -----------------: | ----: | --------- |
| Arabic-specific     |         480 |                 320 |                160 |     0 | Masculine |
| Non-Arabic-specific |         960 |                 346 |                610 |     4 | Feminine  |

In percentage form:

| Model Family        | Masculine % | Feminine % | Equal % |
| ------------------- | ----------: | ---------: | ------: |
| Arabic-specific     |      66.67% |     33.33% |   0.00% |
| Non-Arabic-specific |      36.04% |     63.54% |   0.42% |

This aggregation shows a clear family-level contrast.

Arabic-specific models prefer masculine occupational sentences in two-thirds of cases, while non-Arabic-specific models prefer feminine occupational sentences in nearly two-thirds of cases.

---

## 4.13 Statistical Significance of the Enriched Experiment

### 4.13.1 Binomial Test

| Model          | Direction | Binomial p-value | Significant |
| -------------- | --------- | ---------------: | ----------- |
| Qwen2.5-0.5B   | Feminine  |         4.79e-07 | Yes         |
| AraGPT2-base   | Masculine |         4.33e-05 | Yes         |
| AraGPT2-medium | Masculine |         5.13e-10 | Yes         |
| BLOOM-1b1      | Feminine  |         3.44e-04 | Yes         |
| BLOOM-560m     | Feminine  |         2.05e-06 | Yes         |
| XGLM-564M      | Feminine  |         3.64e-04 | Yes         |

All six models show statistically significant preference direction under the binomial test.

### 4.13.2 Wilcoxon Signed-Rank Test

| Model          | Direction | Wilcoxon p-value | Significant |
| -------------- | --------- | ---------------: | ----------- |
| Qwen2.5-0.5B   | Feminine  |         7.33e-13 | Yes         |
| AraGPT2-base   | Masculine |         2.79e-04 | Yes         |
| AraGPT2-medium | Masculine |         3.29e-08 | Yes         |
| BLOOM-1b1      | Feminine  |         8.51e-05 | Yes         |
| BLOOM-560m     | Feminine  |         5.76e-07 | Yes         |
| XGLM-564M      | Feminine  |         7.93e-07 | Yes         |

The Wilcoxon results confirm that the score differences are statistically significant for all six models.

---

## 4.14 Enriched Model-Family Chi-Square Result

The chi-square test for the enriched six-model analysis gives:

```text
chi-square p-value = 1.64e-27
```

This is a highly significant result.

It shows that model family is strongly associated with occupational gender-preference direction.

The enriched analysis therefore strengthens the conclusion that Arabic-specific and non-Arabic-specific causal language models behave differently on the benchmark.

---

## 4.15 Pairwise Model Comparison

Pairwise Wilcoxon comparisons show the following pattern:

1. AraGPT2-base significantly differs from BLOOM-1b1, BLOOM-560m, XGLM-564M, and Qwen2.5-0.5B.
2. AraGPT2-medium significantly differs from BLOOM-1b1, BLOOM-560m, XGLM-564M, and Qwen2.5-0.5B.
3. BLOOM-1b1, BLOOM-560m, and XGLM-564M do not significantly differ from each other after correction.
4. Qwen2.5-0.5B shows stronger feminine preference than some other non-Arabic-specific models, but it follows the same overall direction.

This supports the conclusion that the largest separation is between Arabic-specific and non-Arabic-specific model groups.

---

## 4.16 v1 vs v2 Stability

The thesis first used a smaller pilot benchmark, v1, containing 36 occupations and 144 sentence pairs.

The benchmark was later expanded to v2 with 60 occupations and 240 sentence pairs.

The main finding remained stable across both versions:

> Arabic-specific models show masculine occupational preference, while non-Arabic-specific models show feminine occupational preference.

This stability supports the reliability of the benchmark design.


## 4.17 External Dataset Pilot Experiments

In addition to the main occupational benchmark, two external dataset pilots were prepared.

The purpose of these pilots is not to replace the main benchmark, but to test whether the evaluation pipeline can be extended to external Arabic gender-bias resources.

### 4.17.1 APGC-Format Pilot

The APGC-format pilot contains 10 masculine/feminine Arabic sentence pairs covering broader grammatical-gender contexts beyond occupations.

The pilot was scored using the same sentence-pair scoring method used for the occupational benchmark.

| Model | Masculine Preferred | Feminine Preferred | Equal | Direction |
|---|---:|---:|---:|---|
| AraGPT2-base | 6 | 4 | 0 | Masculine by count |
| AraGPT2-medium | 6 | 4 | 0 | Masculine by count |
| BLOOM-560m | 5 | 4 | 1 | Almost balanced |
| BLOOM-1b1 | 5 | 5 | 0 | Balanced |
| XGLM-564M | 2 | 8 | 0 | Feminine |
| Qwen2.5-0.5B | 4 | 6 | 0 | Feminine |

The APGC-format pilot confirms that the thesis scoring method can be applied to external grammatical-gender sentence pairs. However, because the pilot contains only 10 pairs, it is treated as pipeline validation rather than a final statistical result.

### 4.17.2 ArGAN-Format Pilot

The ArGAN-format pilot tests prompt-based Arabic gender-bias evaluation.

Unlike the occupational benchmark, this pilot requires generation and output annotation.

The improved pilot used `Qwen/Qwen2.5-0.5B-Instruct`.

The automatic generation-quality analysis produced the following result:

| Metric | Value |
|---|---:|
| Total outputs | 10 |
| Empty outputs | 0 |
| Prompt echo outputs | 0 |
| Repetition outputs | 0 |
| Gender mismatch outputs | 2 |
| Outputs needing manual review | 2 |
| Needs manual review percent | 20% |
| Average output word count | 23 |

The ArGAN pilot shows that prompt-based Arabic bias evaluation is feasible, but it requires instruction-tuned models and manual annotation. Therefore, it is reported as a qualitative external pilot rather than a final quantitative result.
---

## 4.18 Summary of Results

The results show that occupational gender preference in Arabic causal language models is systematic, statistically significant, and associated with model family.

The main findings are:

1. AraGPT2-base and AraGPT2-medium show masculine occupational preference.
2. BLOOM-560m and BLOOM-1b1 show feminine occupational preference.
3. XGLM-564M and Qwen2.5-0.5B also show feminine occupational preference.
4. All six models show statistically significant overall gender preference.
5. Model-family association is highly significant.
6. Bias direction varies by professional field.
7. The v2 benchmark confirms the pattern observed in v1.

The enriched six-model analysis strengthens the thesis by showing that the result is not limited to one multilingual model family.

