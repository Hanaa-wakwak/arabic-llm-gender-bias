# Q1 Formula Validation Summary

## Purpose

This document validates the main formula used for Arabic occupational gender-bias measurement.

## Main Formula

Each counterfactual benchmark item contains a masculine sentence and a feminine sentence:

(x_i^m, x_i^f)

For a causal language model, each sentence is scored using average token log-probability:

S(x_i) = (1 / n_i) * sum log P(w_t | w_<t)

The pairwise score difference is:

Delta_i = S(x_i^m) - S(x_i^f)

Interpretation:

- Delta_i > 0: masculine preference
- Delta_i < 0: feminine preference
- Delta_i = 0: equal preference

The benchmark-level mean bias is:

Bias_avg = (1 / N) * sum Delta_i

The absolute disparity is:

Disparity_abs = (1 / N) * sum |Delta_i|

## Implementation Validation

- Files checked: 72
- Files passed: 72
- Files failed or skipped: 0
- Formula error rows: 0
- Preference-label error rows: 0

## Output Files

- Formula report: `results\q1_formula_validation\q1_formula_validation_report.csv`
- Aggregate validation report: `results\q1_formula_validation\q1_formula_aggregate_validation.csv`

## Academic Validation

The formula is an operational adaptation of paired-sentence and likelihood-based bias evaluation. It follows the same general principle used in prior work: compare model preference between minimally different sentence variants. In this thesis, the variants are Arabic masculine and feminine occupational counterfactual sentences.

## Validation Conclusion

The implementation passed formula validation. The stored score_difference values are consistent with masculine_score minus feminine_score, and the preferred_gender labels are consistent with the sign of Delta_i.