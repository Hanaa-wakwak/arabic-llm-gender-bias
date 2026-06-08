# Experiment 01 — Pilot Minimal Pair Scoring

## Date
8 June 2026

## Goal
The goal of this experiment is to test whether the scoring pipeline works on a small Arabic gender minimal-pair benchmark.

## Dataset
The pilot dataset contains 50 Arabic minimal pairs.

Each item contains:
- masculine sentence
- feminine sentence
- dialect label
- dimension label
- stereotype direction label

## Dialects
- MSA
- Egyptian Arabic

## Dimensions
- Occupation
- Trait/adjective

## Model
aubmindlab/aragpt2-base

## Scoring Method
For each item, the model scores both the masculine and feminine sentence.

The score difference is computed as:

score_difference = masculine_score - feminine_score

Interpretation:
- Positive score_difference means masculine preference.
- Negative score_difference means feminine preference.
- Near-zero score_difference means weak preference.

## Overall Results

| Metric | Value |
|---|---:|
| Total items | 50 |
| Masculine preferred count | 25 |
| Feminine preferred count | 25 |
| Equal count | 0 |
| Masculine preferred percent | 50.0% |
| Feminine preferred percent | 50.0% |
| Equal percent | 0.0% |
| Average score difference | -0.4021 |
| Median score difference | 0.1239 |

## Initial Interpretation

The model preferred masculine versions in 25 items and feminine versions in 25 items. This means that the preference counts are balanced in the pilot dataset.

However, the average score difference is negative, while the median score difference is positive. This suggests that some items may have large negative score differences, pulling the average toward the feminine side.

Therefore, this pilot result should not be interpreted as strong evidence of gender bias yet.

## Current Conclusion

This experiment confirms that the scoring pipeline works.

The result is useful as a pilot test, but the benchmark is still too small to support a strong bias claim.

## Next Steps

1. Analyze results by dialect.
2. Analyze results by dimension.
3. Analyze results by stereotype direction.
4. Identify outlier items.
5. Improve the pilot benchmark.
6. Increase the dataset size.
