# Expanded Benchmark Decision

## Selected Expanded Pilot Benchmark

The selected expanded pilot benchmark is:

minimal_pairs_v07.csv

## Reason

v0.7 provides the best balance between benchmark size, overall score stability, dialect-level balance, and acceptable outlier rate.

## Version Comparison

| Version | Items | Overall Avg | Egyptian Avg | MSA Avg | Outlier Rate | Decision                |
| ------- | ----: | ----------: | -----------: | ------: | -----------: | ----------------------- |
| v0.6    |   144 |      0.0297 |       0.0524 |  0.0071 |       25.69% | Expanded attempt        |
| v0.7    |   144 |     -0.0139 |      -0.0348 |  0.0071 |       17.36% | Selected expanded pilot |
| v0.8    |   144 |     -0.0577 |      -0.1225 |  0.0071 |       16.67% | Template ablation       |

## Final Decision

v0.7 is selected because it has the best dialect-level balance.

The Egyptian and MSA subsets in v0.7 have the same preference count distribution:

* Egyptian: 42 masculine preferred, 30 feminine preferred
* MSA: 42 masculine preferred, 30 feminine preferred

The overall average score difference is also close to zero:

* Overall average score difference: -0.0139

Although v0.8 slightly reduces the outlier rate, it introduces a stronger Egyptian feminine shift and therefore is not selected as the main expanded pilot benchmark.

## Research Interpretation

The experiments show that Arabic gender-bias evaluation is highly sensitive to template construction. Small changes in Egyptian Arabic templates can change the direction and strength of measured gender preference.

Therefore, template-level metadata and quality-control analysis are necessary for any reliable Arabic gender-bias benchmark.

## Next Stage

The next stage is model comparison.

The selected benchmark version, minimal_pairs_v07.csv, will be used to evaluate multiple Arabic and multilingual language models.
