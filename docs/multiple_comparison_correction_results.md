# Multiple-Comparison Correction Results

## Goal

The goal of this step is to correct the pairwise model comparison p-values because multiple Wilcoxon signed-rank tests were performed.

Without correction, repeated pairwise testing can increase the chance of false positive significance results.

## Correction Methods

Three correction methods were applied:

1. Bonferroni correction
   A conservative correction that multiplies each p-value by the number of comparisons.

2. Holm-Bonferroni correction
   A stepwise correction that is usually less conservative than Bonferroni.

3. Benjamini-Hochberg False Discovery Rate correction
   A correction that controls the expected false discovery rate.

## Interpretation Plan

The corrected p-values will be used to determine whether model-pair differences remain significant after accounting for multiple comparisons.

If the difference between AraGPT2 and BLOOM models remains significant after correction, this strengthens the claim that Arabic-specific and multilingual models behave differently on the benchmark.

## Expected Use in Thesis

The corrected pairwise test table should be reported alongside the uncorrected pairwise Wilcoxon test results.

The thesis should state whether significance remains after correction, especially for comparisons between:

* AraGPT2-base and BLOOM models
* AraGPT2-medium and BLOOM models
* BLOOM-1b1 and BLOOM-560m
## Actual Correction Results

After applying multiple-comparison correction, most pairwise model differences remained statistically significant.

The comparison between AraGPT2-base and AraGPT2-medium was significant before correction, and remained significant under Holm and Benjamini-Hochberg FDR correction. However, it was not significant under the more conservative Bonferroni correction.

In contrast, all comparisons between AraGPT2 models and BLOOM models remained significant even after Bonferroni correction. This strengthens the claim that Arabic-specific AraGPT2 models and multilingual BLOOM models behave differently on the proposed Arabic gender counterfactual benchmark.

The comparison between BLOOM-1b1 and BLOOM-560m also remained significant after all correction methods, indicating that model size or training dynamics within the BLOOM family may affect measured gender-preference patterns.

## Main Corrected Statistical Finding

The strongest corrected statistical finding is that Arabic-specific AraGPT2 models differ significantly from multilingual BLOOM models in their score-difference distributions.

This supports the thesis claim that model family strongly affects measured Arabic gender preference.