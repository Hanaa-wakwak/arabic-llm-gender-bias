# Final Contribution Map

## Main Contribution

This thesis contributes a robustness-oriented Arabic occupational gender-bias evaluation framework for causal language models.

The contribution is organized into five layers:

1. Benchmark construction,
2. Model evaluation,
3. Robustness and sensitivity analysis,
4. Statistical and uncertainty analysis,
5. Documentation, traceability, and defense readiness.

---

## Layer 1 — Benchmark Construction

| Contribution | Description |
|---|---|
| v2 main benchmark | Main validated Arabic occupational gender-bias benchmark. |
| v3 benchmark | Expanded occupation and template sensitivity benchmark. |
| v3 controlled | Diagnostic benchmark separating occupation expansion from template expansion. |
| v3 balanced | Stereotype-balanced benchmark. |
| v4 template perturbation | Benchmark for template, semantic-frame, and dialect sensitivity. |
| v5 job-title benchmark | Explicit professional job-title context benchmark. |

---

## Layer 2 — Model Evaluation

| Contribution | Description |
|---|---|
| Six-model evaluation | Evaluation of Arabic-specific and non-Arabic-specific causal language models. |
| Model-family comparison | Comparison between Arabic-specific and multilingual/general model families. |
| External pilots | APGC and ArGAN pilot extensions. |

---

## Layer 3 — Robustness and Sensitivity Analysis

| Contribution | Description |
|---|---|
| v3 sensitivity analysis | Tests whether benchmark expansion changes measured bias. |
| v4 template volatility | Detects template-induced bias direction flips. |
| Dialect sensitivity | Compares MSA and Egyptian Arabic contexts. |
| Semantic-frame sensitivity | Tests whether meaning frame affects measured preference. |
| v4-v5 context comparison | Compares broader occupational sentence contexts with explicit job-title contexts. |
| Context Sensitivity Index | Summarizes template, dialect, and job-title context sensitivity. |
| Cross-benchmark stability map | Tracks whether model direction remains stable across benchmark versions. |

---

## Layer 4 — Statistical and Uncertainty Analysis

| Contribution | Description |
|---|---|
| Chi-square tests | Tests significance of model, family, template, semantic frame, dialect, field, and stereotype label. |
| Cramér’s V effect sizes | Measures practical effect size. |
| Bootstrap confidence intervals | Estimates uncertainty around average score differences. |
| Extreme bias case analysis | Extracts strongest masculine, strongest feminine, and near-neutral examples. |

---

## Layer 5 — Quality Control, Documentation, and Traceability

| Contribution | Description |
|---|---|
| Counterfactual pair integrity audit | Checks structural comparability of masculine-feminine sentence pairs. |
| Benchmark design taxonomy | Documents the design dimensions tested across versions. |
| Reporting checklist | Recommends what Arabic bias evaluations should report. |
| Benchmark datasheet | Documents intended use, limitations, scoring, and ethical considerations. |
| Threats to validity map | Links limitations to mitigation strategies. |
| Claim-to-evidence matrix | Maps major thesis claims to supporting files and outputs. |
| Final artifact registry | Tracks benchmark, result, and documentation files. |
| Final implementation report | Consolidates final technical outputs. |

---

## Final Technical Claim

The thesis contribution is not only a benchmark or a set of model results.

It is a benchmark-design-sensitive evaluation framework for Arabic occupational gender bias in causal language models.

It shows that measured Arabic occupational gender bias is:

- model-dependent,
- template-dependent,
- semantic-frame-dependent,
- dialect-sensitive,
- context-sensitive,
- and not fully captured by one overall score.

---

## Final Defense Sentence

My contribution is a robustness-oriented Arabic occupational gender-bias evaluation framework. It includes benchmark construction, likelihood-based scoring, multi-model evaluation, sensitivity analysis, template perturbation, dialect analysis, job-title context analysis, statistical testing, uncertainty estimation, quality-control audits, and claim-to-evidence traceability.