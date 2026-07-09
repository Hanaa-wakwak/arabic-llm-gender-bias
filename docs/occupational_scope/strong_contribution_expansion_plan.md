# Strong Contribution Expansion Plan

## Main Contribution

This thesis contributes an Arabic occupational gender-bias evaluation suite for causal language models.

The suite does not only measure bias on one benchmark. It also tests the robustness of the measurement under benchmark expansion, stereotype balancing, template perturbation, dialect variation, and external dataset pilots.

---

## Contribution Components

| Component | Role |
|---|---|
| v2 | Main validated occupational benchmark |
| v3 | Experimental expansion benchmark |
| v3 controlled | Diagnostic benchmark separating occupation expansion from template expansion |
| v3 balanced | Balanced sensitivity benchmark with 30 male-stereotyped, 30 female-stereotyped, and 30 neutral occupations |
| v4 template perturbation | Template and semantic-frame sensitivity benchmark |
| APGC pilot | External Arabic gender-pair pipeline validation |
| ArGAN pilot | Qualitative prompt-based Arabic bias generation pilot |

---

## Why This Is Stronger

The work shows that Arabic gender-bias measurement is not only model-dependent. It is also benchmark-dependent.

The v2 benchmark provides the main validated result.

The v3, v3 balanced, and v4 benchmarks provide methodological evidence that occupation selection, wording, dialect, and semantic framing can change measured bias direction.

This is a stronger contribution than a single benchmark because it evaluates the stability of bias measurement itself.

---

## Final Thesis Position

The final thesis should use v2 as the main benchmark and report v3, v3 balanced, and v4 as robustness and sensitivity analyses.

This makes the contribution both empirical and methodological.