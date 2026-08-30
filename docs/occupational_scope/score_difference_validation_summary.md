# Score Difference Validation Summary

## Purpose

This validation verifies that score_difference is implemented consistently as masculine_score minus feminine_score.

## Validation Rule

score_difference = masculine_score - feminine_score

## Preference Rule

- positive score_difference = masculine preference
- negative score_difference = feminine preference
- zero score_difference = equal preference

## Summary

- Files checked: 115
- Files passed: 115
- Files needing review: 0

## Output

- Detailed validation report: `results\final_package\score_difference_validation_report.csv`

## Thesis Use

This validation provides implementation-level evidence that the score_difference equation was applied correctly across model scoring outputs.