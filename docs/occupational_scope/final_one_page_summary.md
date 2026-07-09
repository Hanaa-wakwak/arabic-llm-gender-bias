# Final One-Page Thesis Summary

## Title

Detecting and Analyzing Occupational Gender Bias in Arabic Causal Language Models

## Problem

Arabic occupational terms are often gendered. This makes Arabic an important language for evaluating gender bias in language models.

Most existing bias evaluations focus on English or general multilingual benchmarks. This thesis focuses on Arabic causal language models and occupational gender bias.

## Method

The thesis uses controlled masculine-feminine sentence pairs.

For each pair:

score_difference = masculine_score - feminine_score

Positive score means masculine preference. Negative score means feminine preference.

## Main Benchmark

The v2 benchmark is the main validated benchmark.

It contains:

- 60 occupations,
- 4 templates,
- 240 sentence pairs.

It was tested on six causal language models.

## Main Result

The v2 benchmark showed a statistically significant model-family pattern:

- Arabic-specific AraGPT2 models preferred masculine occupational sentences.
- Non-Arabic-specific models preferred feminine occupational sentences.

## Robustness Analysis

The thesis then tested whether measured bias remains stable under benchmark-design changes.

Additional benchmarks were created:

| Benchmark | Purpose |
|---|---|
| v3 | Expansion sensitivity |
| v3 controlled | Occupation-vs-template diagnostic |
| v3 balanced | Stereotype-balanced sensitivity |
| v4 | Template, semantic-frame, and dialect sensitivity |

## Strongest Methodological Finding

The v4 benchmark showed that all six models had template-induced direction flips.

This means the same model can prefer masculine occupational sentences under one template and feminine occupational sentences under another.

Chi-square tests showed that template ID, semantic frame, and dialect significantly affect preferred gender.

Cramér’s V effect-size analysis showed that template ID had the strongest practical effect.

## Contribution

The thesis contributes an Arabic occupational gender-bias evaluation suite.

The contribution is not only detecting bias. It also shows that bias measurement in Arabic is sensitive to benchmark design.

## Final Claim

Arabic occupational gender-bias evaluation is both model-dependent and benchmark-design-dependent.