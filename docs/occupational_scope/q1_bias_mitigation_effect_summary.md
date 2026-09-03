# Q1 Bias Mitigation Effect Summary

## Purpose

This analysis compares AraGPT2-base before and after counterfactual data augmentation fine-tuning.

## Mitigation Formula

Mitigation_Gain = |Bias_before| - |Bias_after|

A positive mitigation gain means the absolute directional bias decreased after fine-tuning.

## Output

- CSV: `results\q1_bias_mitigation\q1_bias_mitigation_effect_summary.csv`

## Results

### v2_main

- Status: compared
- Before average score_difference: 0.1257066498200098
- After average score_difference: -0.0508336658279101
- Before direction: masculine
- After direction: feminine
- Mitigation gain: 0.07487298399209971
- Bias reduced: True
- Before file: `results\occupational_benchmark_v2_all_models\combined_analysis\overall_by_model.csv`
- After file: `results\q1_bias_mitigation\analysis_mitigated_aragpt2_base_v2\summary_overall.csv`

### v5_job_titles

- Status: compared
- Before average score_difference: -0.0338489797380235
- After average score_difference: 0.0347361726893319
- Before direction: near-neutral_or_mixed
- After direction: near-neutral_or_mixed
- Mitigation gain: -0.000887192951308402
- Bias reduced: False
- Before file: `results\occupational_benchmark_v5_job_titles_quick_models\analysis_aragpt2_base\summary_overall.csv`
- After file: `results\q1_bias_mitigation\analysis_mitigated_aragpt2_base_v5\summary_overall.csv`

### v6_job_roles_departments

- Status: compared
- Before average score_difference: -0.3019826209379567
- After average score_difference: -0.0529510714217192
- Before direction: feminine
- After direction: feminine
- Mitigation gain: 0.2490315495162375
- Bias reduced: True
- Before file: `results\occupational_benchmark_v6_job_roles_large_all_models\combined_analysis\v6_overall_by_model.csv`
- After file: `results\q1_bias_mitigation\analysis_mitigated_aragpt2_base_v6\summary_overall.csv`

### arabjobs_v7_external

- Status: compared
- Before average score_difference: 0.0894636630749459
- After average score_difference: -0.192275839241746
- Before direction: masculine
- After direction: feminine
- Mitigation gain: -0.10281217616680009
- Bias reduced: False
- Before file: `results\external_datasets\arabjobs\combined_analysis\arabjobs_v7_overall_by_model.csv`
- After file: `results\q1_bias_mitigation\analysis_mitigated_aragpt2_base_arabjobs_v7\summary_overall.csv`

## Publication Claim

This experiment extends the framework from bias measurement to bias mitigation by testing whether balanced Arabic masculine-feminine counterfactual fine-tuning reduces measured occupational gender preference.

## Limitation

This experiment does not claim to remove gender bias completely. It evaluates whether one controlled counterfactual fine-tuning intervention reduces measured bias under the proposed paired-likelihood metric.