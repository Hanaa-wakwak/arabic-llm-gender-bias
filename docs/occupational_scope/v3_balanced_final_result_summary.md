# v3 Balanced Final Result Summary

## Purpose

The v3 balanced benchmark was created after the experimental v3 benchmark showed sensitivity to occupation coverage and lexical/contextual formulation.

The goal was to test whether a more controlled and stereotype-balanced version of v3 would restore the main v2 pattern.

---

## Benchmark Design

The v3 balanced benchmark contains:

| Item | Value |
|---|---:|
| Occupations | 90 |
| Templates | 4 |
| Sentence pairs | 360 |
| Fields | 6 |
| Stereotype labels | 3 |

The benchmark uses the original four v2-style templates.

---

## Stereotype Balance

The final v3 balanced benchmark is balanced across stereotype labels.

| Stereotype Label | Sentence Pairs | Occupations |
|---|---:|---:|
| male_stereotyped | 120 | 30 |
| female_stereotyped | 120 | 30 |
| neutral | 120 | 30 |

---

## Quality Check

The benchmark passed quality checks.

| Issue Type | Details | Count |
|---|---|---:|
| no_issues_found | v3 balanced benchmark passed quality checks | 0 |

---

## Quick Model Sanity Test

Two models were tested:

| Model | Family |
|---|---|
| AraGPT2-base | Arabic-specific |
| BLOOM-560m | Non-Arabic-specific |

### Overall Results

| Model | Total | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Direction |
|---|---:|---:|---:|---:|---:|---|
| AraGPT2-base | 360 | 98 | 262 | 0 | -0.4394 | Feminine |
| BLOOM-560m | 360 | 140 | 217 | 3 | -0.1462 | Feminine |

---

## Interpretation

Even after balancing stereotype labels and using only the original four v2-style templates, AraGPT2-base still preferred feminine occupational sentences.

This means that the v3-balanced expansion did not restore the v2 model-family pattern.

The result confirms that Arabic occupational gender-bias measurement is sensitive to benchmark design, especially occupation selection, lexical formulation, and contextual wording.

---

## Final Technical Decision

The v3 balanced benchmark should not replace v2.

The final benchmark roles are:

| Benchmark | Final Role |
|---|---|
| v1 | Pilot benchmark |
| v2 | Main validated benchmark |
| v3 | Experimental sensitivity analysis |
| v3 controlled | Diagnostic sensitivity benchmark |
| v3 balanced | Balanced sensitivity benchmark |
| APGC pilot | External dataset pipeline validation |
| ArGAN pilot | Qualitative generation pilot |

---

## Recommended Thesis Wording

The v3 balanced benchmark was constructed to test whether the v3 sensitivity issue could be reduced through controlled template use and balanced stereotype-label distribution. Although the benchmark passed quality checks and achieved equal male-stereotyped, female-stereotyped, and neutral occupation groups, the quick model test still showed feminine preference for both AraGPT2-base and BLOOM-560m. Therefore, v3 balanced is not used as a replacement for v2. Instead, it supports the methodological finding that Arabic occupational gender-bias measurement is sensitive to benchmark design. The v2 benchmark remains the main validated benchmark because it was evaluated across six models and produced a statistically significant model-family pattern.