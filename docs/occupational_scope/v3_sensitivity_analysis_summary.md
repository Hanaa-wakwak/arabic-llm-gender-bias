# v3 Sensitivity Analysis Summary

## Purpose

This document summarizes the diagnostic analysis of the enhanced occupational benchmark v3.

Benchmark v3 was created to increase benchmark coverage by expanding the occupation list from 60 to 90 occupations and increasing the templates from 4 to 6.

The purpose of the diagnostic analysis was to check whether the v3 expansion preserves the main v2 model-family pattern.

---

## v3 Quality Check

The v3 benchmark passed automatic quality checks.

| Metric | Value |
|---|---:|
| Total sentence pairs | 540 |
| Unique occupations | 90 |
| Unique fields | 6 |
| Unique templates | 6 |
| Quality issues | 0 |

---

## Quick v3 Model Test

Two models were tested first:

| Model | Family |
|---|---|
| AraGPT2-base | Arabic-specific |
| BLOOM-560m | Non-Arabic-specific |

The quick test showed:

| Model | Total Items | Masculine Preferred | Feminine Preferred | Direction |
|---|---:|---:|---:|---|
| AraGPT2-base | 540 | 188 | 352 | Feminine |
| BLOOM-560m | 540 | 240 | 300 | Feminine |

This differs from v2 because AraGPT2-base showed masculine preference in v2 but feminine preference in v3.

---

## Template Group Diagnostic

To determine whether the new v3 templates caused the change, v3 templates were divided into:

| Group | Meaning |
|---|---|
| old_v2_template | original four templates |
| new_v3_template | two newly added templates |

The result showed that the new v3 templates were almost balanced for AraGPT2-base.

| Template Group | Total | Masculine | Feminine | Direction |
|---|---:|---:|---:|---|
| old_v2_template | 360 | 97 | 263 | Feminine |
| new_v3_template | 180 | 91 | 89 | Almost balanced |

This means the reversal was not mainly caused by the newly added templates.

---

## v3 Controlled Diagnostic

A controlled v3 benchmark was created using:

- 90 occupations,
- original four v2-style templates only,
- 360 sentence pairs.

AraGPT2-base still showed strong feminine preference:

| Model | Total | Masculine | Feminine | Direction |
|---|---:|---:|---:|---|
| AraGPT2-base | 360 | 97 | 263 | Feminine |

This indicates that the change is related to occupation coverage and/or lexical/contextual formulation rather than only the new templates.

---

## Original-v2 vs Added-v3 Occupation Diagnostic

The v3 controlled benchmark was divided into occupations that matched v2 and occupations newly added in v3.

The diagnostic found:

| Occupation Origin | Total Items | Masculine | Feminine | Direction |
|---|---:|---:|---:|---|
| original_v2_occupation | 160 | 35 | 125 | Feminine |
| added_v3_occupation | 200 | 62 | 138 | Feminine |

Only 40 of the 60 v2 occupation pairs matched exactly in v3 using the masculine/feminine occupation pair comparison.

This suggests that v3 differs from v2 not only by adding new occupations, but also by changing lexical/contextual formulation for some occupations.

---

## Interpretation

The v3 experiment reveals an important sensitivity issue.

The direction of model preference can change when the benchmark is expanded or reformulated.

Therefore, v3 should not replace v2 as the main benchmark at this stage.

Instead, v3 should be reported as an experimental sensitivity benchmark.

---

## Final Decision

The thesis should use:

| Benchmark | Role |
|---|---|
| v2 | Main validated benchmark |
| v3 | Experimental sensitivity analysis |
| v3_controlled | Diagnostic benchmark |
| future v3_balanced | Future improved benchmark |

---

## Recommended Thesis Wording

The v3 expansion passed automatic quality checks, but a quick model test showed that AraGPT2-base changed from masculine preference in v2 to feminine preference in v3. Diagnostic analysis showed that this reversal was not mainly caused by the newly added templates, since the new templates were nearly balanced. Instead, the results suggest that model preference is sensitive to occupation coverage and lexical/contextual formulation. Therefore, v2 remains the main validated benchmark, while v3 is reported as an experimental sensitivity analysis and a basis for future benchmark balancing and human validation.

---

## Research Value

This result is scientifically useful because it shows that Arabic occupational gender-bias evaluation is sensitive to benchmark design.

It strengthens the thesis by demonstrating that benchmark expansion should be validated carefully rather than assumed to preserve earlier results.