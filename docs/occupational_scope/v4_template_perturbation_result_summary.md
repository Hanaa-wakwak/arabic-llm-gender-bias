# v4 Template Perturbation Result Summary

## Purpose

The v4 template perturbation benchmark was created to test whether measured occupational gender bias remains stable across different sentence templates, dialects, and semantic frames.

The benchmark uses the balanced v3 occupation lexicon:

- 90 occupations
- 30 male-stereotyped occupations
- 30 female-stereotyped occupations
- 30 neutral occupations

Each occupation is tested across 8 templates.

---

## Benchmark Size

| Item | Value |
|---|---:|
| Occupations | 90 |
| Templates | 8 |
| Sentence pairs | 720 |
| Fields | 6 |
| Semantic frames | 6 |
| Dialects | 2 |
| Stereotype labels | 3 |

---

## Quality Check

The v4 benchmark passed automatic quality checks.

| Issue Type | Details | Count |
|---|---|---:|
| no_issues_found | v4 template perturbation benchmark passed quality checks | 0 |

---

## Quick Model Test

Two models were tested:

| Model | Family |
|---|---|
| AraGPT2-base | Arabic-specific |
| BLOOM-560m | Non-Arabic-specific |

### Overall Results

| Model | Total | Masculine | Feminine | Equal | Average Score Difference | Direction |
|---|---:|---:|---:|---:|---:|---|
| AraGPT2-base | 720 | 220 | 500 | 0 | -0.3484 | Feminine |
| BLOOM-560m | 720 | 256 | 460 | 4 | -0.1703 | Feminine |

---

## Key Template-Sensitivity Finding

The v4 benchmark revealed strong template-induced bias direction changes.

The same model can prefer masculine occupational sentences in one template and feminine occupational sentences in another template.

### AraGPT2-base Examples

| Template | Masculine % | Feminine % | Average Score | Direction |
|---|---:|---:|---:|---|
| egy_experience_statement | 75.56 | 24.44 | 0.3830 | Masculine |
| msa_workplace_original | 65.56 | 34.44 | 0.1603 | Masculine |
| egy_workplace_original | 4.44 | 95.56 | -0.9366 | Feminine |
| msa_competence_frame | 11.11 | 88.89 | -0.4889 | Feminine |

### BLOOM-560m Examples

| Template | Masculine % | Feminine % | Average Score | Direction |
|---|---:|---:|---:|---|
| egy_promotion_frame | 97.78 | 2.22 | 0.8178 | Masculine |
| egy_experience_statement | 57.78 | 41.11 | 0.0144 | Slight Masculine |
| msa_competence_frame | 4.44 | 95.56 | -0.4785 | Feminine |
| msa_experience_statement | 5.56 | 94.44 | -0.5944 | Feminine |

---

## Interpretation

The v4 results show that measured Arabic occupational gender bias is highly sensitive to template and semantic frame.

This means that bias evaluation should not rely on a single sentence structure.

Instead, Arabic bias benchmarks should test multiple controlled templates and report template-level sensitivity.

---

## Technical Contribution

This benchmark adds a new methodological contribution:

**Template-Induced Bias Direction Volatility**

This contribution measures whether model bias direction changes across templates, dialects, and semantic frames.

The result strengthens the thesis because it shows that Arabic gender-bias evaluation is not only model-dependent, but also benchmark-design-dependent.

---

## Final Role

v4 is not used as the main benchmark.

Its role is:

| Benchmark | Role |
|---|---|
| v2 | Main validated benchmark |
| v4 | Template and semantic-frame sensitivity benchmark |

v4 supports the conclusion that v2 findings should be interpreted with awareness of benchmark-design sensitivity.