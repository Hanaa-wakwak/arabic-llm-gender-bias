# Experiment 06 — Expanded Benchmark v0.7

## Goal

The goal of v0.7 is to improve the expanded benchmark v0.6 by reducing Egyptian template-driven effects while keeping the dataset size fixed at 144 items.

## Dataset

Benchmark version: minimal_pairs_v07.csv

Total items: 144

The dataset includes:
- 18 occupation concepts
- 18 trait concepts
- MSA and Egyptian Arabic
- 8 template types
- concept_id and template_id metadata

## Overall Result

| Metric | Value |
|---|---:|
| Total items | 144 |
| Masculine preferred | 84 |
| Feminine preferred | 60 |
| Masculine preferred percent | 58.33% |
| Feminine preferred percent | 41.67% |
| Average score difference | -0.0139 |
| Median score difference | 0.0711 |
| Outlier percent | 17.36% |

## Dialect-Level Result

| Dialect | Items | Avg score difference | Masculine preferred | Feminine preferred |
|---|---:|---:|---:|---:|
| Egyptian | 72 | -0.0348 | 42 | 30 |
| MSA | 72 | 0.0071 | 42 | 30 |

## Interpretation

Compared with v0.6, benchmark v0.7 is more stable. The overall average score difference is closer to zero, the outlier rate is lower, and both dialects show the same preference count distribution.

This suggests that the revised Egyptian templates reduced some of the template-driven masculine preference observed in v0.6.

## Remaining Problems

Two template-level problems remain:

1. egyptian occupation known-role template:
   - masculine preference dominance

2. egyptian trait people-say template:
   - feminine preference dominance

Therefore, v0.7 is a strong expanded pilot candidate, but one more template revision is needed before selecting a stable expanded benchmark.

## Decision

Treat v0.7 as the best expanded benchmark so far.

The next version, v0.8, should revise only the two problematic Egyptian templates while preserving the same lexicon and dataset size.