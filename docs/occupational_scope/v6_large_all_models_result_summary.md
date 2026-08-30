# v6 Large Job Roles Benchmark — All Models Result Summary

## Dataset

- Benchmark: v6 expanded job roles and departments
- Total pairs per completed model: 2,880
- Structure: 120 job roles × 24 templates
- Dialects: MSA and Egyptian Arabic

## Overall Results

### aubmindlab/aragpt2-base

- Total items: 2880
- Masculine preferred: 970 (33.68055555555556%)
- Feminine preferred: 1910 (66.31944444444444%)
- Equal: 0 (0.0%)
- Average score difference: -0.3019826209379567
- Median score difference: -0.2294025421142578
- Direction: feminine

### aubmindlab/aragpt2-medium

- Total items: 2880
- Masculine preferred: 1136 (39.44444444444444%)
- Feminine preferred: 1744 (60.55555555555555%)
- Equal: 0 (0.0%)
- Average score difference: -0.2435836901267369
- Median score difference: -0.1814496517181396
- Direction: feminine

### bigscience/bloom-1b1

- Total items: 2880
- Masculine preferred: 1328 (46.11111111111112%)
- Feminine preferred: 1547 (53.71527777777778%)
- Equal: 5 (0.1736111111111111%)
- Average score difference: -0.0808241102430555
- Median score difference: -0.0546875
- Direction: feminine

### bigscience/bloom-560m

- Total items: 2880
- Masculine preferred: 1500 (52.083333333333336%)
- Feminine preferred: 1375 (47.74305555555556%)
- Equal: 5 (0.1736111111111111%)
- Average score difference: -0.0163350423177083
- Median score difference: 0.03125
- Direction: near_neutral_or_mixed

## Interpretation

The v6 benchmark evaluates Arabic occupational gender preference across expanded job-role, department, workplace, seniority, and job-title contexts. Negative average score differences indicate higher likelihood for feminine variants, while positive values indicate higher likelihood for masculine variants.

## Note

Only models with completed analysis folders are included in this combined summary. If a model did not generate a scoring CSV, it is skipped automatically.