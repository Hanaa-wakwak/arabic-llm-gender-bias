# Context Sensitivity Index Summary

## Purpose

This diagnostic summarizes how sensitive each model is to benchmark-context changes in Arabic occupational gender-bias evaluation.

The diagnostic combines:

1. v4 template volatility range,
2. v4 dialect shift magnitude,
3. v4-to-v5 job-title context shift.

## Important Note

This is a thesis-specific diagnostic index, not a universal standard metric. Its purpose is to summarize robustness and context sensitivity within this benchmark suite.

## Results

| model_name | v4_average_score_difference | v4_direction | v5_average_score_difference | v5_direction | v4_to_v5_direction_changed | job_title_context_shift | abs_job_title_context_shift | v4_template_volatility_range | v4_dialect_shift | abs_v4_dialect_shift | context_sensitivity_score | context_sensitivity_label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| aubmindlab/aragpt2-base | -0.3484 | feminine | -0.0338 | feminine | False | 0.3145 | 0.3145 | 1.3195 | -0.1171 | 0.1171 | 1.7512 | high_context_sensitivity |
| bigscience/bloom-560m | -0.1703 | feminine | 0.0709 | masculine | True | 0.2412 | 0.2412 | 1.4123 | 0.4467 | 0.4467 | 2.1003 | high_context_sensitivity |

## Interpretation

A higher context-sensitivity score means that the model's measured gender preference changes more strongly across templates, dialects, and explicit job-title contexts.

The v4-to-v5 direction-change flag indicates whether the model's average preference direction changed when moving from broader occupational sentence contexts to explicit job-title contexts.

## Thesis Contribution

This diagnostic enriches the thesis contribution by converting the robustness finding into a measurable model-level sensitivity summary.

It supports the final claim that Arabic occupational gender-bias evaluation is not only model-dependent, but also benchmark-design-dependent and context-sensitive.
