# Q1 Human Validation Protocol

## Purpose

This protocol validates a stratified sample of Arabic masculine-feminine occupational counterfactual pairs from controlled benchmarks and external real-world job-ad data.

## Validation Sources

- v2 main occupational benchmark
- v4 template perturbation benchmark
- v5 job-title benchmark
- v6 expanded job-role and department benchmark
- ArabJobs v7 external real-world job-ad benchmark

## Target Sample

- Total validation pairs: 500
- Annotators: 2

## Annotation Labels

### grammaticality
- valid
- minor_issue
- invalid

### meaning_preserved
- yes
- mostly
- no

### gender_form_correct
- yes
- no

### dialect_correct
- yes
- no
- uncertain

### job_title_correct
- yes
- no
- uncertain

### keep_or_remove
- keep
- review
- remove

## Agreement Metrics

After annotation, the project reports:

- percentage agreement
- Cohen's Kappa
- valid-pair rate
- keep/review/remove distribution

## Q1 Publication Value

This validation layer strengthens benchmark reliability by showing that Arabic counterfactual pairs were manually reviewed for grammaticality, meaning preservation, gender-form correctness, dialect appropriateness, and job-title validity.