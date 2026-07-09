# Final Slides Prompt

Create a professional academic thesis defense presentation about the following project:

**Title:** Detecting and Analyzing Occupational Gender Bias in Arabic Causal Language Models

The presentation should be clear, academic, visually modern, and suitable for a master's thesis defense.

Use a clean university-style design with:
- white or dark navy background,
- blue/gold accent colors,
- clear section dividers,
- tables for results,
- simple diagrams for methodology,
- Arabic NLP / AI visual theme,
- minimal text per slide,
- speaker notes under each slide.

---

## Slide 1 — Title Slide

**Title:** Detecting and Analyzing Occupational Gender Bias in Arabic Causal Language Models

Include:
- student name placeholder
- supervisor name placeholder
- university placeholder
- date placeholder

Visual:
Arabic text + AI model/network illustration.

Speaker note:
“This thesis studies occupational gender bias in Arabic causal language models using controlled masculine-feminine sentence pairs.”

---

## Slide 2 — Motivation

Main points:
- Arabic is morphologically gendered.
- Occupations often have masculine and feminine forms.
- Bias can appear in model preference between gendered sentence variants.
- Most bias benchmarks focus on English or general multilingual settings.

Visual:
Arabic masculine/feminine occupational word examples.

Speaker note:
“In Arabic, gender is often encoded directly in occupational words, so Arabic needs targeted bias evaluation.”

---

## Slide 3 — Research Problem

Main question:
Do Arabic causal language models prefer masculine or feminine occupational sentences?

Add:
The thesis also asks whether measured bias is stable under benchmark-design changes.

Visual:
Question mark + model scoring two sentence variants.

Speaker note:
“The goal is not only to detect bias, but also to test whether bias measurement is stable across templates, dialects, and benchmark versions.”

---

## Slide 4 — Core Method

Show formula:

score_difference = masculine_score - feminine_score

Interpretation:
- positive = masculine preference
- negative = feminine preference
- zero = equal preference

Visual:
Two sentence cards:
1. masculine Arabic sentence
2. feminine Arabic sentence
then arrow to model likelihood comparison.

Speaker note:
“For each pair, I compute the model likelihood for the masculine and feminine sentence and subtract the feminine score from the masculine score.”

---

## Slide 5 — Example Sentence Pair

Example:
Masculine: هذا الطبيب يعمل في المستشفى.
Feminine: هذه الطبيبة تعمل في المستشفى.

Show:
Same occupation, same context, only gender changes.

Speaker note:
“This controlled design helps isolate gendered occupational formulation.”

---

## Slide 6 — Models Tested

Table:

| Model | Family |
|---|---|
| AraGPT2-base | Arabic-specific |
| AraGPT2-medium | Arabic-specific |
| BLOOM-560m | Non-Arabic-specific |
| BLOOM-1b1 | Non-Arabic-specific |
| XGLM-564M | Non-Arabic-specific |
| Qwen2.5-0.5B | Non-Arabic-specific |

Visual:
Model family grouping.

Speaker note:
“I compared Arabic-specific models against multilingual or general non-Arabic-specific models.”

---

## Slide 7 — Benchmark Suite Overview

Table:

| Benchmark | Role |
|---|---|
| v1 | Pilot |
| v2 | Main validated benchmark |
| v3 | Expansion sensitivity |
| v3 controlled | Occupation-vs-template diagnostic |
| v3 balanced | Stereotype-balanced sensitivity |
| v4 | Template, semantic-frame, and dialect sensitivity |

Visual:
Timeline from v1 to v4.

Speaker note:
“The project evolved from a main benchmark into a robustness-oriented evaluation suite.”

---

## Slide 8 — v2 Main Benchmark

Include:
- 60 occupations
- 4 templates
- 240 sentence pairs
- 6 fields
- 6 models

Visual:
Benchmark card.

Speaker note:
“v2 is the main validated benchmark and the basis for the core empirical result.”

---

## Slide 9 — v2 Main Result

Main result:
Arabic-specific models showed masculine preference.
Non-Arabic-specific models showed feminine preference.

Add:
Chi-square model-family test:
p = 1.64e-27

Visual:
Two grouped bars:
Arabic-specific → masculine
Non-Arabic-specific → feminine

Speaker note:
“The v2 result showed a statistically significant model-family pattern.”

---

## Slide 10 — Why Robustness Analysis?

Main points:
- A single benchmark may hide design sensitivity.
- Templates, occupation wording, dialect, and semantic frame may affect measured bias.
- Therefore, additional benchmark versions were created.

Visual:
Benchmark design factors diagram.

Speaker note:
“After the main result, I tested whether the measurement remains stable when benchmark design changes.”

---

## Slide 11 — v3 Sensitivity Benchmark

Include:
- v3 expanded occupations from 60 to 90.
- v3 expanded templates from 4 to 6.
- v3 showed direction changes.
- Therefore, v3 is sensitivity analysis, not replacement.

Visual:
Expansion diagram.

Speaker note:
“v3 showed that expanding the benchmark can change measured bias direction.”

---

## Slide 12 — v3 Controlled Diagnostic

Include:
- 90 occupations
- original 4 v2-style templates
- 360 sentence pairs
- AraGPT2-base still shifted direction

Main interpretation:
The change was not only caused by new templates.

Speaker note:
“v3 controlled separated occupation expansion from template expansion.”

---

## Slide 13 — v3 Balanced Benchmark

Include:
- 90 occupations
- 30 male-stereotyped
- 30 female-stereotyped
- 30 neutral
- 360 sentence pairs
- quality check passed

Result:
AraGPT2-base: feminine
BLOOM-560m: feminine

Speaker note:
“Even stereotype balancing did not restore the v2 pattern, showing that wording and formulation still matter.”

---

## Slide 14 — v4 Template Perturbation Benchmark

Include:
- 90 balanced occupations
- 8 templates
- 6 semantic frames
- 2 dialects
- 720 sentence pairs
- 6 models

Semantic frames:
- occupation presence
- professional experience
- leadership
- competence
- achievement/reward
- responsibility/trust

Visual:
Matrix: occupations × templates × dialects.

Speaker note:
“v4 is the strongest methodological extension because it tests template, semantic-frame, and dialect sensitivity.”

---

## Slide 15 — v4 Overall Results

Table:

| Model | Masculine | Feminine | Equal | Direction |
|---|---:|---:|---:|---|
| Qwen2.5-0.5B | 312 | 390 | 18 | Feminine |
| AraGPT2-base | 220 | 500 | 0 | Feminine |
| AraGPT2-medium | 290 | 430 | 0 | Feminine |
| BLOOM-1b1 | 248 | 467 | 5 | Feminine |
| BLOOM-560m | 256 | 460 | 4 | Feminine |
| XGLM-564M | 104 | 614 | 2 | Feminine |

Speaker note:
“All six models showed an overall feminine direction on v4.”

---

## Slide 16 — Template-Induced Direction Flips

Main point:
All six models showed direction flips across templates.

Table:

| Model | Masculine Templates | Feminine Templates | Direction Flip |
|---|---:|---:|---|
| Qwen2.5-0.5B | 4 | 4 | True |
| AraGPT2-base | 2 | 6 | True |
| AraGPT2-medium | 2 | 6 | True |
| BLOOM-1b1 | 1 | 7 | True |
| BLOOM-560m | 2 | 6 | True |
| XGLM-564M | 1 | 7 | True |

Speaker note:
“This is one of the strongest findings: the same model can prefer masculine sentences in one template and feminine sentences in another.”

---

## Slide 17 — Examples of Direction Flips

Show examples:

AraGPT2-base:
- egy_experience_statement → masculine
- egy_workplace_original → feminine

BLOOM-560m:
- egy_promotion_frame → masculine
- msa_experience_statement → feminine

Visual:
Split arrows showing flip.

Speaker note:
“These examples show that bias direction depends strongly on sentence framing.”

---

## Slide 18 — Dialect Sensitivity

Table:

| Model | MSA Direction | Egyptian Direction |
|---|---|---|
| Qwen2.5-0.5B | Feminine | Masculine |
| AraGPT2-base | Feminine | Feminine |
| AraGPT2-medium | Feminine | Feminine |
| BLOOM-1b1 | Feminine | Feminine |
| BLOOM-560m | Feminine | Masculine |
| XGLM-564M | Feminine | Feminine |

Speaker note:
“Some models changed direction between MSA and Egyptian Arabic, showing dialect sensitivity.”

---

## Slide 19 — Statistical Tests

Table:

| Factor | p-value | Significant |
|---|---:|---|
| model_name | 8.36e-36 | Yes |
| model_family | 0.0423 | Yes |
| template_id | 3.65e-141 | Yes |
| semantic_frame | 3.10e-77 | Yes |
| dialect | 2.55e-30 | Yes |
| stereotype_label | 0.5548 | No |
| field | 0.000434 | Yes |

Speaker note:
“Template, semantic frame, and dialect were highly significant, while stereotype label was not significant after balancing.”

---

## Slide 20 — Effect Size Analysis

Table:

| Variable | Cramér’s V | Effect Size |
|---|---:|---|
| template_id | 0.3962 | Medium |
| semantic_frame | 0.2926 | Small |
| model_name | 0.2016 | Small |
| dialect | 0.1747 | Small |
| field | 0.0723 | Very small |
| model_family | 0.0310 | Very small |
| stereotype_label | 0.0166 | Very small |

Highlight:
Template ID had the strongest practical effect.

Speaker note:
“Effect-size analysis showed that template formulation had the strongest practical effect on measured gender preference.”

---

## Slide 21 — External Dataset Pilots

Include:
- APGC pilot for Arabic gender-pair pipeline validation
- ArGAN pilot for qualitative Arabic bias-generation analysis

Speaker note:
“These pilots show how the project can be extended beyond the manually constructed benchmark.”

---

## Slide 22 — Final Contributions

List:

1. Arabic occupational gender-bias benchmark.
2. Six-model causal LM evaluation.
3. Benchmark expansion sensitivity analysis.
4. Stereotype-balanced sensitivity benchmark.
5. Template perturbation benchmark.
6. Dialect and semantic-frame sensitivity analysis.
7. Template-Induced Bias Direction Volatility.
8. External dataset pilots.

Speaker note:
“The contribution is a complete Arabic occupational gender-bias evaluation suite, not a single dataset.”

---

## Slide 23 — Final Claim

Big text:

Arabic occupational gender-bias evaluation is both model-dependent and benchmark-design-dependent.

Add:
Template formulation had the strongest practical effect in v4.

Speaker note:
“The thesis shows that model-level bias should be reported together with benchmark-design sensitivity.”

---

## Slide 24 — Limitations

Include:
- manual benchmark construction
- limited dialect coverage
- likelihood scoring depends on tokenization
- external datasets used as pilots only
- need human validation

Speaker note:
“These limitations guide future work.”

---

## Slide 25 — Future Work

Include:
- human validation and inter-annotator agreement
- more Arabic dialects
- more model families
- full APGC integration
- generation-based evaluation
- mitigation experiments
- public benchmark release

Speaker note:
“Future work can transform this into a larger public Arabic bias benchmark suite.”

---

## Slide 26 — Thank You

Include:
Thank you.
Questions?

Visual:
Arabic NLP + AI theme.