# Q1 Token-Length Control Summary

## Purpose

This analysis checks whether score_difference is likely to be driven by superficial word-count differences between masculine and feminine sentence variants.

## Method

- Count words in masculine and feminine sentence variants.
- Compute word_count_difference = masculine_word_count - feminine_word_count.
- Estimate correlation between word_count_difference and score_difference.

## Output Files

- Row-level file: `results\q1_token_length_control\q1_token_length_control_all_rows.csv`
- Summary file: `results\q1_token_length_control\q1_token_length_control_summary.csv`

## Summary

### arabjobs_v7 | aubmindlab/aragpt2-base

- Total items: 14532
- Mean masculine word count: 8.668731076245527
- Mean feminine word count: 8.668731076245527
- Mean word-count difference: 0.0
- Mean absolute word-count difference: 0.0
- Same word-count percent: 100.0
- Correlation with score_difference: nan

### arabjobs_v7 | bigscience/bloom-560m

- Total items: 14532
- Mean masculine word count: 8.668731076245527
- Mean feminine word count: 8.668731076245527
- Mean word-count difference: 0.0
- Mean absolute word-count difference: 0.0
- Same word-count percent: 100.0
- Correlation with score_difference: nan

### v6_job_roles | aubmindlab/aragpt2-base

- Total items: 2880
- Mean masculine word count: 8.625
- Mean feminine word count: 8.625
- Mean word-count difference: 0.0
- Mean absolute word-count difference: 0.0
- Same word-count percent: 100.0
- Correlation with score_difference: nan

### v6_job_roles | aubmindlab/aragpt2-medium

- Total items: 2880
- Mean masculine word count: 8.625
- Mean feminine word count: 8.625
- Mean word-count difference: 0.0
- Mean absolute word-count difference: 0.0
- Same word-count percent: 100.0
- Correlation with score_difference: nan

### v6_job_roles | bigscience/bloom-1b1

- Total items: 2880
- Mean masculine word count: 8.625
- Mean feminine word count: 8.625
- Mean word-count difference: 0.0
- Mean absolute word-count difference: 0.0
- Same word-count percent: 100.0
- Correlation with score_difference: nan

### v6_job_roles | bigscience/bloom-560m

- Total items: 2880
- Mean masculine word count: 8.625
- Mean feminine word count: 8.625
- Mean word-count difference: 0.0
- Mean absolute word-count difference: 0.0
- Same word-count percent: 100.0
- Correlation with score_difference: nan

## Publication Claim

This analysis provides a control check showing whether measured gender-preference scores are plausibly explained by sentence-length differences. Since the main scoring method uses average token log probability, this check adds an additional surface-form validation layer.