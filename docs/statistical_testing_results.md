# Statistical Testing Results

## Goal

The goal of this step is to test whether the observed masculine/feminine preference patterns are statistically meaningful rather than only descriptive count differences.

The statistical tests were applied to the multi-model evaluation results on the selected expanded benchmark:

minimal_pairs_v07.csv

## Tests Used

Three statistical tests were used:

1. Binomial test
   Used to test whether masculine/feminine preference counts differ significantly from a 50/50 distribution.

2. Wilcoxon signed-rank test vs zero
   Used to test whether score differences are significantly different from zero for each model.

3. Pairwise Wilcoxon signed-rank test between models
   Used to test whether two models differ significantly in their score-difference distributions on the same benchmark items.

## Overall Binomial Test Results

| Model                     | Direction |  p-value | Significant at 0.05 |
| ------------------------- | --------- | -------: | ------------------- |
| aubmindlab/aragpt2-base   | masculine |   0.0549 | No                  |
| aubmindlab/aragpt2-medium | masculine |   0.5598 | No                  |
| bigscience/bloom-1b1      | feminine  |   0.0003 | Yes                 |
| bigscience/bloom-560m     | feminine  | 1.49e-06 | Yes                 |

## Interpretation of Binomial Tests

The binomial test shows that the AraGPT2 models do not significantly deviate from a 50/50 masculine/feminine preference distribution.

In contrast, both BLOOM models show statistically significant feminine preference. This indicates that the feminine preference observed in BLOOM models is unlikely to be due to random variation alone.

## Wilcoxon Test vs Zero

| Model                     | Average Score Difference |  p-value | Significant at 0.05 |
| ------------------------- | -----------------------: | -------: | ------------------- |
| aubmindlab/aragpt2-base   |                  -0.0139 |   0.3455 | No                  |
| aubmindlab/aragpt2-medium |                  -0.0524 |   0.5958 | No                  |
| bigscience/bloom-1b1      |                  -0.2519 | 1.43e-06 | Yes                 |
| bigscience/bloom-560m     |                  -0.3909 | 4.67e-11 | Yes                 |

## Interpretation of Wilcoxon Tests

The Wilcoxon signed-rank test confirms the same overall pattern.

AraGPT2-base and AraGPT2-medium do not show statistically significant score-difference shifts away from zero.

BLOOM-1b1 and BLOOM-560m show statistically significant negative score differences, indicating stronger preference for feminine sentence variants.

## Pairwise Model Comparison

Pairwise Wilcoxon tests show that all model pairs differ significantly at the 0.05 level.

This suggests that model family and model size affect measured Arabic gender preference patterns.

The largest differences appear between AraGPT2 models and BLOOM models, supporting the earlier descriptive finding that Arabic-specific and multilingual models behave differently on the benchmark.

## Dialect-Level Statistical Results

At the dialect level, BLOOM-560m shows statistically significant feminine preference in both Egyptian Arabic and MSA.

BLOOM-1b1 shows significant feminine preference in Egyptian Arabic, but not in MSA under the binomial test.

AraGPT2-base and AraGPT2-medium do not show statistically significant preference at the dialect level.

## Main Statistical Findings

1. AraGPT2 models do not significantly deviate from balanced masculine/feminine preference overall.

2. BLOOM models show statistically significant feminine-form preference.

3. BLOOM-560m shows the strongest statistically significant feminine preference.

4. Pairwise model comparisons show significant differences between model score-difference distributions.

5. The statistical tests support the claim that Arabic-specific and multilingual models behave differently on the proposed benchmark.

## Note on Multiple Comparisons

The pairwise Wilcoxon tests are reported at the 0.05 significance level. Since multiple pairwise tests are performed, later analysis should also report corrected p-values, such as Bonferroni or false discovery rate correction.
