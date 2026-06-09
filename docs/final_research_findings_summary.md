# Final Research Findings Summary

## Project Title

Counterfactual and Dialect-Aware Gender Bias Evaluation in Arabic Causal Language Models

## Current Research Status

This project developed and evaluated a controlled Arabic gender-bias benchmark for causal language models.

The selected expanded benchmark is:

minimal_pairs_v07.csv

It contains 144 masculine/feminine counterfactual sentence pairs covering:

* Modern Standard Arabic
* Egyptian Arabic
* occupation concepts
* trait concepts
* male-stereotype concepts
* female-stereotype concepts
* neutral concepts
* controlled sentence templates

The benchmark also includes metadata for concept, dialect, dimension, stereotype direction, and template type.

---

## Finding 1 — AraGPT2 models are more balanced than BLOOM models

The Arabic-specific AraGPT2 models produced more balanced masculine/feminine preference counts than the multilingual BLOOM models.

Overall preference counts:

| Model          | Masculine Preferred | Feminine Preferred | Direction                       |
| -------------- | ------------------: | -----------------: | ------------------------------- |
| AraGPT2-base   |                  84 |                 60 | weak masculine count preference |
| AraGPT2-medium |                  76 |                 68 | near balanced                   |
| BLOOM-1b1      |                  50 |                 94 | strong feminine preference      |
| BLOOM-560m     |                  43 |                101 | strongest feminine preference   |

The statistical tests confirmed that BLOOM models significantly deviate from a balanced masculine/feminine distribution, while AraGPT2 models do not.

---

## Finding 2 — BLOOM models show statistically significant feminine-form preference

Both descriptive and statistical analyses show that BLOOM models prefer feminine variants more often.

Binomial test results:

| Model      | Direction |  p-value | Significant |
| ---------- | --------- | -------: | ----------- |
| BLOOM-1b1  | feminine  |   0.0003 | Yes         |
| BLOOM-560m | feminine  | 1.49e-06 | Yes         |

Wilcoxon signed-rank tests also confirmed significant negative score differences for BLOOM models.

This means that BLOOM models assign systematically higher probability to feminine sentence variants on this benchmark.

---

## Finding 3 — AraGPT2-medium is the most balanced model overall

Among the evaluated models, AraGPT2-medium is the most balanced by preference counts:

* Masculine preferred: 76
* Feminine preferred: 68
* Masculine percentage: 52.78%
* Feminine percentage: 47.22%

The binomial test for AraGPT2-medium was not significant, suggesting that its preference distribution does not significantly deviate from a balanced 50/50 distribution.

---

## Finding 4 — Model family significantly affects measured gender preference

Pairwise Wilcoxon tests showed significant differences between model score-difference distributions.

After multiple-comparison correction, the differences between AraGPT2 models and BLOOM models remained statistically significant.

This supports the conclusion that Arabic-specific and multilingual model families behave differently on the proposed Arabic gender counterfactual benchmark.

---

## Finding 5 — Occupation items reveal stronger model divergence than trait items

The occupation dimension produced clearer differences between Arabic-specific and multilingual models.

For occupation items:

| Model          | Masculine Preferred | Feminine Preferred |
| -------------- | ------------------: | -----------------: |
| AraGPT2-base   |                  47 |                 25 |
| AraGPT2-medium |                  45 |                 27 |
| BLOOM-1b1      |                  20 |                 52 |
| BLOOM-560m     |                  18 |                 54 |

AraGPT2 models preferred masculine variants more often in occupation items, while BLOOM models strongly preferred feminine variants.

Trait items were less divergent, especially for AraGPT2-base.

---

## Finding 6 — Dialect matters, but model family matters more

The benchmark includes both MSA and Egyptian Arabic.

AraGPT2-base showed identical preference-count distribution across both dialects:

* Egyptian: 42 masculine, 30 feminine
* MSA: 42 masculine, 30 feminine

AraGPT2-medium showed dialect-sensitive behavior:

* Egyptian: more feminine preference
* MSA: more masculine preference

BLOOM models showed feminine preference across both dialects, especially BLOOM-560m.

This suggests that dialect can affect model behavior, but the strongest overall difference appears between model families.

---

## Finding 7 — Template construction strongly affects measured bias

During benchmark development, several versions were tested.

The experiments showed that small changes in Arabic templates can change the measured direction and strength of gender preference.

For example, some Egyptian templates introduced masculine or feminine dominance even when the underlying concept remained the same.

Therefore, template-level metadata and quality-control analysis are essential for Arabic gender-bias evaluation.

---

## Finding 8 — v0.7 is the selected expanded pilot benchmark

Several benchmark versions were constructed and compared.

v0.7 was selected as the expanded pilot benchmark because it provided the best balance between:

* dataset size
* dialect-level stability
* overall score stability
* acceptable outlier rate
* template quality

v0.8 slightly reduced the outlier rate but introduced a stronger Egyptian feminine shift, so it was treated as a template ablation rather than the selected benchmark.

---

## Main Thesis Claim

The results show that Arabic gender-bias evaluation must be counterfactual, dialect-aware, and template-controlled.

The proposed benchmark reveals differences between Arabic-specific and multilingual causal language models that would not be visible from a simple MSA-only or template-uncontrolled evaluation.

---

## Current Contribution

This project currently contributes:

1. A controlled Arabic gender counterfactual benchmark with MSA and Egyptian Arabic.

2. A benchmark versioning and quality-control process for detecting template artifacts.

3. A scoring pipeline based on sentence log-probability for causal language models.

4. A multi-model comparison between Arabic-specific and multilingual models.

5. Statistical testing showing significant differences between model families.

6. Thesis-ready figures, tables, methodology draft, results draft, and literature review draft.

---

## Next Research Steps

Recommended next steps:

1. Add more Arabic and multilingual models.

2. Add human validation for sentence naturalness and gender-pair equivalence.

3. Add statistical tests by dimension and stereotype direction.

4. Add token-level explainability to identify which words drive preference scores.

5. Add mitigation experiments, such as prompt-based rewriting or fairness-aware fine-tuning.

6. Expand beyond Egyptian Arabic to additional dialects.
