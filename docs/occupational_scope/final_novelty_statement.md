# Final Novelty Statement

## Main Novelty

The novelty of this thesis is that it does not treat Arabic occupational gender-bias evaluation as a single static benchmark problem.

Instead, it builds a robustness-oriented evaluation suite that tests whether measured bias remains stable under benchmark-design changes.

## What Is New?

The thesis contributes the following:

1. A controlled Arabic occupational gender-bias benchmark for causal language models.
2. A likelihood-based masculine-feminine paired-sentence scoring pipeline.
3. A six-model comparison between Arabic-specific and non-Arabic-specific causal language models.
4. A benchmark expansion sensitivity study.
5. A stereotype-balanced benchmark design.
6. A template perturbation benchmark with semantic-frame and dialect variation.
7. A template-induced bias direction volatility analysis.
8. A dialect sensitivity analysis between MSA and Egyptian Arabic.
9. A statistical and effect-size analysis showing that template ID has the strongest practical effect.
10. A job-title-specific benchmark that isolates explicit occupational titles.
11. A v4-v5 comparison showing that explicit job-title contexts can behave differently from broader occupational sentence contexts.
12. External dataset pilots showing future extensibility.

## Why This Matters

Many bias evaluations report one overall bias score.

This thesis shows that, for Arabic occupational gender bias, the measured direction can change depending on how the benchmark is formulated.

Therefore, Arabic bias evaluation should not report only a single model-level score. It should also report:

- template sensitivity,
- semantic-frame sensitivity,
- dialect sensitivity,
- occupation-set sensitivity,
- stereotype-balance sensitivity,
- job-title-context sensitivity.

## Final Novelty Claim

The thesis introduces a benchmark-design-sensitive methodology for Arabic occupational gender-bias evaluation.

It shows that Arabic occupational bias measurement is not only model-dependent, but also context-dependent and benchmark-design-dependent.
## Added Novelty: Context Sensitivity Index

An additional novelty is the proposed context-sensitivity diagnostic.

This diagnostic summarizes how sensitive a model's measured occupational gender preference is to changes in template, dialect, and job-title context.

It is thesis-specific and is used as a robustness summary, not as a universal bias metric.

This strengthens the methodological contribution because the thesis does not only observe benchmark-design sensitivity; it also operationalizes it as a measurable diagnostic.
## Widened Contribution

The thesis contribution was widened beyond benchmark construction and model evaluation.

It now includes three additional methodological layers:

1. a cross-benchmark stability map,
2. a benchmark design taxonomy,
3. an Arabic occupational bias evaluation reporting checklist.

These additions strengthen the thesis because they transform the work from a set of experiments into a structured evaluation framework.

The final contribution is therefore not only an Arabic occupational gender-bias benchmark, but a methodology for testing and reporting benchmark-design sensitivity in Arabic bias evaluation.
## Widened Contribution

The thesis contribution was widened beyond benchmark construction and model evaluation.

It now includes three additional methodological layers:

1. a cross-benchmark stability map,
2. a benchmark design taxonomy,
3. an Arabic occupational bias evaluation reporting checklist.

These additions strengthen the thesis because they transform the work from a set of experiments into a structured evaluation framework.

The final contribution is therefore not only an Arabic occupational gender-bias benchmark, but a methodology for testing and reporting benchmark-design sensitivity in Arabic bias evaluation.

## Additional Contribution: Counterfactual Pair Integrity Audit

An additional contribution is the counterfactual pair integrity audit.

This audit checks whether masculine and feminine sentence pairs are structurally comparable across the benchmark suite.

It verifies character-length differences, word-count differences, identical-pair errors, and occupation-form presence.

This strengthens the benchmark validity because the evaluation depends on comparing near-counterfactual masculine and feminine sentence variants.

## Additional Contribution: Benchmark Datasheet

An additional contribution is the benchmark datasheet.

The datasheet documents the benchmark purpose, construction process, intended use, limitations, scoring method, quality-control checks, and ethical considerations.

This improves transparency and makes the benchmark suite easier to understand, reproduce, and evaluate.

## Additional Contribution: Threats to Validity and Mitigation Map

An additional contribution is the threats-to-validity and mitigation map.

This document identifies construct, internal, external, statistical, reliability, and reproducibility threats.

It also explains how each threat is addressed or reported in the thesis.

This strengthens the work because the thesis does not only present results; it critically evaluates the reliability and boundaries of those results.
