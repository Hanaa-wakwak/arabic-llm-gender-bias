# Experiment 07 — Template Ablation v0.8

## Goal

The goal of v0.8 is to test whether revising the remaining problematic Egyptian templates from v0.7 can further improve the expanded benchmark.

## Dataset

Benchmark version: minimal_pairs_v08.csv

Total items: 144

The dataset uses the same occupation and trait lexicons as v0.7, but revises selected Egyptian templates.

## Overall Result

| Metric                      |   Value |
| --------------------------- | ------: |
| Total items                 |     144 |
| Masculine preferred         |      81 |
| Feminine preferred          |      63 |
| Masculine preferred percent |  56.25% |
| Feminine preferred percent  |  43.75% |
| Average score difference    | -0.0577 |
| Median score difference     |  0.0599 |
| Outlier percent             |  16.67% |

## Dialect-Level Result

| Dialect  | Items | Avg score difference | Masculine preferred | Feminine preferred |
| -------- | ----: | -------------------: | ------------------: | -----------------: |
| Egyptian |    72 |              -0.1225 |                  39 |                 33 |
| MSA      |    72 |               0.0071 |                  42 |                 30 |

## Template-Level Finding

v0.8 reduced the number of problematic templates, but introduced a strong feminine preference in the Egyptian occupation context-said template.

Problematic template:

egy_occ_context_said_role

* Average score difference: -0.3529
* Feminine preference: 77.78%
* Warning: high average score difference and feminine preference dominance

## Comparison with v0.7

Compared with v0.7, v0.8 slightly improves the outlier rate and gender preference count balance.

However, v0.8 performs worse on dialect-level balance. The Egyptian subset shifts more strongly toward feminine preference, while the MSA subset remains close to the previous result.

## Decision

v0.8 is useful as a template ablation experiment, but it should not replace v0.7 as the expanded pilot benchmark.

The selected expanded pilot benchmark remains:

minimal_pairs_v07.csv
