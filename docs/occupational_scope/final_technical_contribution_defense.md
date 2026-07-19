# Final Technical Contribution Defense

## If the examiner asks: What is technically new in your thesis?

Technically, my thesis contributes an Arabic occupational gender-bias evaluation suite for causal language models.

The work is not only a dataset and not only a model comparison.

It includes a full benchmark-design sensitivity framework.

## Technical Components

First, I built v2 as the main validated benchmark. It contains controlled masculine-feminine occupational sentence pairs and was tested on six causal language models.

Second, I created v3, v3 controlled, and v3 balanced to test whether the measured bias remains stable after occupation expansion, template changes, and stereotype balancing.

Third, I created v4 as a template perturbation benchmark. This benchmark tests different templates, semantic frames, and dialects. The v4 results showed that all six models had template-induced direction flips.

Fourth, I added statistical tests and Cramér’s V effect-size analysis. The results showed that template ID had the strongest practical effect on measured gender preference.

Fifth, I added v5 as a job-title-specific benchmark. This benchmark isolates the occupation as an explicit professional title in CV, job advertisement, HR, and profile contexts.

## Why this is a technical contribution

The technical contribution is the evaluation framework itself.

The thesis shows that Arabic gender-bias evaluation should not depend on a single sentence template or one overall score.

Instead, bias evaluation should test whether the result is robust across:

- benchmark version,
- occupation set,
- stereotype balance,
- template wording,
- semantic frame,
- dialect,
- explicit job-title context.

## Strong Answer

My technical contribution is a robustness-oriented benchmark suite for Arabic occupational gender-bias evaluation. It includes validated benchmark construction, likelihood-based scoring, model-family comparison, benchmark sensitivity analysis, template perturbation, dialect analysis, effect-size testing, and a job-title-specific extension.

## One-Sentence Answer

The technical contribution is a benchmark-design-sensitive evaluation framework for Arabic occupational gender bias in causal language models.
## Additional Enrichment: Context Sensitivity Index

To further enrich the technical contribution, I added a context-sensitivity diagnostic.

This diagnostic summarizes how much each model's measured gender preference changes across:

- template perturbation,
- dialect variation,
- explicit job-title contexts.

The index combines v4 template volatility, v4 dialect shift, and v4-to-v5 job-title context shift.

This converts the qualitative robustness finding into a measurable model-level diagnostic.

It strengthens the thesis because the contribution becomes not only benchmark construction, but also benchmark-sensitivity measurement.
## Additional Validation Layer: Counterfactual Pair Integrity Audit

I also added a counterfactual pair integrity audit.

This audit checks whether masculine and feminine sentence pairs are structurally comparable.

It examines sentence length, word count, identical-pair errors, and whether the intended masculine and feminine occupation forms are present in the correct sentence.

This strengthens the technical contribution because the benchmark is not only constructed manually; it is also validated through an implementation-level quality-control process.

## Additional Validation Layer: Counterfactual Pair Integrity Audit

I also added a counterfactual pair integrity audit.

This audit checks whether masculine and feminine sentence pairs are structurally comparable.

It examines sentence length, word count, identical-pair errors, and whether the intended masculine and feminine occupation forms are present in the correct sentence.

This strengthens the technical contribution because the benchmark is not only constructed manually; it is also validated through an implementation-level quality-control process.

## Additional Documentation Layer: Benchmark Datasheet

I also added a benchmark datasheet.

This datasheet documents the purpose of the benchmark, how it was constructed, how it should be used, what its limitations are, and what ethical considerations should be kept in mind.

This strengthens the technical contribution because the benchmark is not only implemented, but also documented in a transparent and reproducible way.

## Additional Rigor Layer: Threats to Validity and Mitigation Map

I also added a threats-to-validity and mitigation map.

This map identifies the main risks in the evaluation, such as template sensitivity, dialect limitation, tokenization effects, manual benchmark construction, and external validation limits.

For each threat, I documented how the thesis mitigates it or reports it transparently.

This improves the methodological rigor of the contribution.

## Additional Interpretability Layer: Extreme Bias Case Analysis

I also added an extreme bias case analysis.

This analysis extracts concrete examples of the strongest masculine preferences, strongest feminine preferences, and near-neutral sentence pairs.

This improves interpretability because the thesis does not only report aggregate numbers; it also shows which sentence pairs produced the strongest model preferences.

## Additional Defense Layer: Claim-to-Evidence Traceability Matrix

I also added a claim-to-evidence traceability matrix.

This matrix maps each major thesis claim to the exact data file, result file, statistical output, or documentation that supports it.

This improves defense readiness because if an examiner asks where a claim comes from, the evidence is already traceable.
