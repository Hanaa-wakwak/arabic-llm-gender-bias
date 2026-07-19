# Final Contribution Statement

## Main Contribution

This thesis contributes an Arabic occupational gender-bias evaluation suite for causal language models.

The contribution is not limited to measuring bias on one dataset. It also evaluates whether measured bias remains stable under controlled benchmark-design changes.

---

## Contribution 1: Main Validated Benchmark

The v2 benchmark is the main validated benchmark.

It contains 60 occupations, 4 templates, and 240 sentence pairs.

It was evaluated on six causal language models and showed a statistically significant model-family pattern.

---

## Contribution 2: Benchmark Expansion Sensitivity

The v3 benchmark expanded the occupation set and template set.

The results showed that benchmark expansion can change measured bias direction.

This motivated further diagnostic analysis.

---

## Contribution 3: Controlled Diagnostic Benchmark

The v3 controlled benchmark used the expanded occupation list but only the original v2-style templates.

This helped separate occupation-expansion effects from template-expansion effects.

---

## Contribution 4: Stereotype-Balanced Sensitivity Benchmark

The v3 balanced benchmark used 90 occupations balanced across:

- 30 male-stereotyped occupations,
- 30 female-stereotyped occupations,
- 30 neutral occupations.

The benchmark passed quality checks but still showed sensitivity, confirming that stereotype balance alone does not stabilize measured bias.

---

## Contribution 5: Template Perturbation Benchmark

The v4 template perturbation benchmark tested 90 balanced occupations across 8 templates, 6 semantic frames, and 2 dialects.

All six models showed template-induced direction flips.

Chi-square tests showed that template ID, semantic frame, and dialect significantly affect preferred gender.

This introduces a methodological contribution:

**Template-Induced Bias Direction Volatility**

---

## Contribution 6: External Dataset Pilots

The thesis also includes APGC and ArGAN pilot experiments to test external-dataset enrichment and qualitative prompt-based evaluation.

---

## Final Claim

The thesis shows that Arabic occupational gender-bias evaluation is both model-dependent and benchmark-design-dependent.

Therefore, Arabic bias evaluation should report:

1. model-level bias,
2. model-family differences,
3. dialect sensitivity,
4. template sensitivity,
5. semantic-frame sensitivity,
6. benchmark robustness.
## Final Strengthened Contribution

The strongest methodological contribution is the finding that template formulation is the strongest practical driver of measured gender preference in the v4 benchmark.

Cramér's V effect-size analysis showed:

| Factor | Effect Size |
|---|---|
| template_id | Medium |
| semantic_frame | Small |
| model_name | Small |
| dialect | Small |
| model_family | Very small |
| stereotype_label | Very small |

This means that Arabic occupational gender-bias evaluation should not report only one overall score.

It should report:

1. overall model-level bias,
2. template-level sensitivity,
3. semantic-frame sensitivity,
4. dialect sensitivity,
5. robustness across benchmark versions.

## Additional Extension: v5 Job-Title Benchmark

An additional v5 benchmark was created to isolate occupational gender preference at the level of explicit job titles.

This benchmark tests CV, job advertisement, HR record, and professional profile contexts.

The v5 results showed that explicit job-title contexts can behave differently from broader occupational sentence templates. AraGPT2-base was near-balanced, while BLOOM-560m showed weak masculine preference.

This further supports the thesis claim that Arabic occupational gender-bias measurement is benchmark-design-dependent.