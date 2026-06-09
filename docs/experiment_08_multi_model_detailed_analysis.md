# Experiment 08 — Detailed Multi-Model Analysis

## Goal

This experiment evaluates multiple Arabic and multilingual causal language models on the selected expanded pilot benchmark:

minimal_pairs_v07.csv

The goal is to compare model-level gender preference patterns across:

* dialect
* dimension
* stereotype direction

## Evaluated Models

The evaluated models are:

1. aubmindlab/aragpt2-base
2. aubmindlab/aragpt2-medium
3. bigscience/bloom-560m
4. bigscience/bloom-1b1

## Overall Results

| Model                     | Masculine Preferred | Feminine Preferred | Masculine % | Feminine % | Avg Score Difference |
| ------------------------- | ------------------: | -----------------: | ----------: | ---------: | -------------------: |
| aubmindlab/aragpt2-base   |                  84 |                 60 |      58.33% |     41.67% |              -0.0139 |
| aubmindlab/aragpt2-medium |                  76 |                 68 |      52.78% |     47.22% |              -0.0524 |
| bigscience/bloom-1b1      |                  50 |                 94 |      34.72% |     65.28% |              -0.2519 |
| bigscience/bloom-560m     |                  43 |                101 |      29.86% |     70.14% |              -0.3909 |

## Overall Interpretation

The Arabic-specific AraGPT2 models are more balanced than the multilingual BLOOM models.

AraGPT2-medium is the most balanced model by preference counts, with 52.78% masculine preference and 47.22% feminine preference.

The BLOOM models show a clear feminine-form preference, especially BLOOM-560m, which prefers feminine variants in 70.14% of the benchmark items.

## Dialect-Level Analysis

AraGPT2-base shows identical preference-count distribution across Egyptian and MSA subsets:

* Egyptian: 42 masculine, 30 feminine
* MSA: 42 masculine, 30 feminine

This suggests that AraGPT2-base is relatively stable across the two dialect subsets in this benchmark.

AraGPT2-medium behaves differently across dialects. It shows feminine preference in Egyptian Arabic but masculine preference in MSA:

* Egyptian: 32 masculine, 40 feminine
* MSA: 44 masculine, 28 feminine

The BLOOM models show feminine preference in both dialects. BLOOM-560m shows the strongest feminine preference in both Egyptian and MSA Arabic.

## Dimension-Level Analysis

Occupation items reveal stronger divergence between Arabic-specific and multilingual models.

AraGPT2-base and AraGPT2-medium both prefer masculine variants in occupation items:

* AraGPT2-base: 47 masculine, 25 feminine
* AraGPT2-medium: 45 masculine, 27 feminine

In contrast, BLOOM models strongly prefer feminine variants in occupation items:

* BLOOM-1b1: 20 masculine, 52 feminine
* BLOOM-560m: 18 masculine, 54 feminine

Trait items show weaker masculine preference for AraGPT2-base and stronger feminine preference for AraGPT2-medium and BLOOM models.

## Stereotype-Direction Analysis

AraGPT2 models show behavior that partially follows stereotype direction.

For female-stereotype items, both AraGPT2 models prefer feminine variants more often.

For male-stereotype items, both AraGPT2 models show higher masculine preference, especially AraGPT2-base.

For neutral items, AraGPT2 models still show masculine preference, suggesting that neutral items may require further template and lexical review.

The BLOOM models show feminine preference across female-stereotype, male-stereotype, and neutral categories. This suggests a more general feminine-form preference rather than a stereotype-direction-specific pattern.

## Main Findings

1. Arabic-specific AraGPT2 models are more balanced than multilingual BLOOM models on the proposed Arabic counterfactual gender benchmark.

2. AraGPT2-medium is the most balanced model overall by preference counts.

3. BLOOM models show consistent feminine-form preference across dialects, dimensions, and stereotype categories.

4. Occupation items reveal stronger divergence between Arabic-specific and multilingual models than trait items.

5. AraGPT2-base shows the most stable dialect-level count distribution across MSA and Egyptian Arabic.

## Preliminary Research Conclusion

The proposed benchmark can reveal meaningful differences between Arabic-specific and multilingual causal language models.

The results show that Arabic gender-bias evaluation is sensitive not only to sentence templates and dialect, but also to the model family being evaluated.

This supports the need for counterfactual, dialect-aware, and template-controlled Arabic gender-bias benchmarks.
