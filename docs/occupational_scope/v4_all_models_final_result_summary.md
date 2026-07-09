# v4 All-Model Template Perturbation Final Result Summary

## Purpose

The v4 template perturbation benchmark was created to test whether Arabic occupational gender-bias measurement remains stable across templates, semantic frames, and dialects.

Unlike v2, which is the main validated benchmark, v4 is designed as a methodological sensitivity benchmark.

---

## Benchmark Design

| Item | Value |
|---|---:|
| Occupations | 90 |
| Sentence pairs | 720 |
| Templates | 8 |
| Semantic frames | 6 |
| Dialects | 2 |
| Stereotype labels | 3 |
| Models tested | 6 |

The benchmark uses a balanced occupation lexicon:

| Stereotype Label | Occupations |
|---|---:|
| male_stereotyped | 30 |
| female_stereotyped | 30 |
| neutral | 30 |

---

## Overall Model Results

| Model | Masculine | Feminine | Equal | Average Score | Overall Direction |
|---|---:|---:|---:|---:|---|
| Qwen/Qwen2.5-0.5B | 312 | 390 | 18 | -0.0890 | Feminine |
| AraGPT2-base | 220 | 500 | 0 | -0.3484 | Feminine |
| AraGPT2-medium | 290 | 430 | 0 | -0.3031 | Feminine |
| BLOOM-1b1 | 248 | 467 | 5 | -0.1700 | Feminine |
| BLOOM-560m | 256 | 460 | 4 | -0.1703 | Feminine |
| XGLM-564M | 104 | 614 | 2 | -0.4411 | Feminine |

All six models showed an overall feminine direction on v4.

---

## Template Volatility

All six models showed template-induced direction flips.

| Model | Masculine Templates | Feminine Templates | Direction Flip | Volatility Range |
|---|---:|---:|---|---:|
| Qwen/Qwen2.5-0.5B | 4 | 4 | True | 1.1049 |
| AraGPT2-base | 2 | 6 | True | 1.3195 |
| AraGPT2-medium | 2 | 6 | True | 1.2230 |
| BLOOM-1b1 | 1 | 7 | True | 1.3633 |
| BLOOM-560m | 2 | 6 | True | 1.4123 |
| XGLM-564M | 1 | 7 | True | 0.7285 |

This means that the same model can prefer masculine completions under one template and feminine completions under another template.

---

## Dialect Shift

Some models changed direction between MSA and Egyptian templates.

| Model | MSA Direction | Egyptian Direction | Egyptian - MSA |
|---|---|---|---:|
| Qwen/Qwen2.5-0.5B | Feminine | Masculine | 0.4930 |
| AraGPT2-base | Feminine | Feminine | -0.1171 |
| AraGPT2-medium | Feminine | Feminine | -0.2249 |
| BLOOM-1b1 | Feminine | Feminine | 0.2065 |
| BLOOM-560m | Feminine | Masculine | 0.4467 |
| XGLM-564M | Feminine | Feminine | -0.0868 |

Qwen and BLOOM-560m changed from feminine preference in MSA to masculine preference in Egyptian.

---

## Statistical Tests

Chi-square tests showed that several factors significantly affect preferred gender.

| Factor | p-value | Significant |
|---|---:|---|
| model_name | 8.36e-36 | Yes |
| model_family | 0.0423 | Yes |
| template_id | 3.65e-141 | Yes |
| semantic_frame | 3.10e-77 | Yes |
| dialect | 2.55e-30 | Yes |
| stereotype_label | 0.5548 | No |
| field | 0.000434 | Yes |

The most important finding is that template, semantic frame, and dialect are statistically significant, while stereotype label is not significant after balancing.

---

## Key Methodological Finding

The v4 results show that Arabic occupational gender-bias measurement is highly sensitive to benchmark design.

In particular, measured bias direction can change depending on:

1. sentence template,
2. semantic frame,
3. dialect,
4. occupation field,
5. model family.

This means that Arabic gender-bias evaluation should not rely on a single template or a single benchmark formulation.

---

## Final Contribution

This thesis contributes not only a benchmark, but a robustness evaluation suite.

The final contribution includes:

| Component | Role |
|---|---|
| v2 | Main validated benchmark |
| v3 | Expansion sensitivity benchmark |
| v3 controlled | Occupation-vs-template diagnostic |
| v3 balanced | Stereotype-balanced sensitivity benchmark |
| v4 | Template, semantic-frame, and dialect sensitivity benchmark |
| APGC pilot | External gender-pair pipeline validation |
| ArGAN pilot | Qualitative Arabic bias-generation pilot |

---

## Final Thesis Wording

The v4 template perturbation benchmark demonstrates that measured Arabic occupational gender bias is highly sensitive to template design, semantic frame, and dialect. Although all six models showed an overall feminine direction on v4, every model also showed template-induced direction flips. Chi-square tests confirmed that template ID, semantic frame, dialect, model name, model family, and field significantly affect preferred gender, while stereotype label was not significant after balancing. This supports the methodological contribution of the thesis: Arabic gender-bias evaluation should report not only model-level bias, but also benchmark-design sensitivity.