# Threats to Validity and Mitigation Map

## Purpose

This document summarizes the main threats to validity in the Arabic occupational gender-bias evaluation suite and explains how the thesis mitigates or reports each threat.

This strengthens the research by making the limitations explicit and showing that the benchmark design was evaluated critically.

---

## Threats to Validity

| Threat Type | Threat | Possible Impact | Mitigation in This Thesis |
|---|---|---|---|
| Construct validity | Gender bias is measured through likelihood preference, not direct real-world discrimination. | The score may reflect language likelihood rather than social bias alone. | The thesis clearly defines score_difference as relative model preference, not as a direct social discrimination measure. |
| Construct validity | Masculine and feminine forms may differ in tokenization length. | Tokenization differences may affect likelihood scores. | The thesis reports likelihood-based scoring limitations and uses controlled paired comparisons. |
| Internal validity | Sentence templates may influence measured bias direction. | Results may depend on wording rather than only occupation gender. | v4 template perturbation benchmark explicitly tests template sensitivity. |
| Internal validity | Occupation wording may change model behavior. | Different lexical choices may produce different score directions. | v3, v3 controlled, and v3 balanced test occupation-set and wording sensitivity. |
| Internal validity | Masculine and feminine pairs may not be perfectly equivalent. | Uncontrolled sentence differences may affect scores. | Counterfactual pair integrity audit checks sentence length, word count, identical-pair errors, and occupation-form presence. |
| External validity | Dialect coverage is limited to MSA and Egyptian Arabic. | Findings may not generalize to all Arabic dialects. | The thesis reports dialect limitation and includes dialect sensitivity analysis as a first step. |
| External validity | Only selected causal language models are tested. | Findings may not generalize to all Arabic or multilingual models. | Six models from Arabic-specific and non-Arabic-specific families are evaluated, and future work recommends more models. |
| External validity | External datasets are used only as pilots. | External validation is not yet full-scale. | APGC and ArGAN pilots are reported as enrichment and future-work directions, not as final validation. |
| Statistical conclusion validity | Statistical significance alone may overstate practical importance. | Very small effects can be statistically significant. | The thesis adds Cramér’s V effect-size analysis to report practical effect size. |
| Statistical conclusion validity | Overall averages may hide subgroup behavior. | A model may look stable overall but flip across templates or dialects. | The thesis reports template, dialect, semantic-frame, field, and stereotype-label subgroup analyses. |
| Reliability | Manual benchmark construction can introduce human errors. | Errors may affect benchmark consistency. | Automated quality checks, artifact registry, completeness checks, and counterfactual integrity audit are added. |
| Reproducibility | Results may be difficult to trace across many benchmark versions. | Reviewers may not know which file supports each claim. | Final artifact registry and technical contribution matrix map claims to files and outputs. |

---

## Key Mitigation Layers

The thesis includes the following mitigation layers:

1. benchmark quality checks,
2. stereotype-balance checks,
3. counterfactual pair integrity audit,
4. v3 sensitivity analysis,
5. v4 template perturbation analysis,
6. dialect sensitivity analysis,
7. v5 job-title context analysis,
8. chi-square statistical testing,
9. Cramér’s V effect-size analysis,
10. final artifact registry,
11. benchmark datasheet,
12. reporting checklist.

---

## Final Validity Statement

The thesis does not claim that one benchmark version provides a universal measurement of Arabic gender bias.

Instead, it argues that Arabic occupational gender-bias evaluation must report benchmark-design sensitivity.

This makes the contribution stronger because the thesis explicitly studies how measurement changes under different benchmark design choices.