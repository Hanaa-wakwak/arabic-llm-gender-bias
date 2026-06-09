# Experiment 05 — Expanded Benchmark v0.6

## Goal

The goal of v0.6 is to expand the stable pilot benchmark from 48 items to 144 controlled minimal pairs using separate lexicon files for occupations and traits.

## Dataset

Benchmark version: minimal_pairs_v06.csv

Total items: 144

The dataset includes:
- 18 occupation concepts
- 18 trait concepts
- MSA and Egyptian Arabic
- 8 controlled template types
- concept_id and template_id metadata

## Overall Result

| Metric | Value |
|---|---:|
| Total items | 144 |
| Masculine preferred | 93 |
| Feminine preferred | 51 |
| Masculine preferred percent | 64.58% |
| Feminine preferred percent | 35.42% |
| Average score difference | 0.0297 |
| Median score difference | 0.2047 |
| Outlier percent | 25.69% |

## Dialect-Level Result

| Dialect | Items | Avg score difference | Masculine preferred | Feminine preferred |
|---|---:|---:|---:|---:|
| Egyptian | 72 | 0.0524 | 51 | 21 |
| MSA | 72 | 0.0071 | 42 | 30 |

## Template-Level Findings

The expanded benchmark revealed new template-level effects.

The strongest problematic templates are:

1. egyptian occupation direct-role template:
   - masculine preferred: 14 / 18
   - warning: masculine preference dominance

2. egyptian trait said template:
   - masculine preferred: 14 / 18
   - warning: masculine preference dominance

This indicates that expansion introduced template-driven masculine preference, especially in Egyptian Arabic templates.

## Main Conclusion

v0.6 successfully expands the benchmark to 144 items, but it is not yet a stable expanded benchmark.

Although the overall average score difference is close to zero, the preference counts are skewed toward masculine forms and the outlier rate is high.

## Decision

Treat v0.6 as an expanded benchmark attempt, not the selected expanded baseline.

The next version, v0.7, should revise the problematic Egyptian templates while keeping the same concept lexicon and dataset size.