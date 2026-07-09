# v4 Effect-Size Analysis Summary

## Purpose

After running chi-square tests on the v4 template perturbation benchmark, effect-size analysis was added using Cramér's V.

The goal was to determine not only whether each factor was statistically significant, but also how strong its association was with preferred gender.

---

## Effect-Size Results

| Variable | Levels | p-value | Cramér's V | Effect Size |
|---|---:|---:|---:|---|
| template_id | 8 | 3.65e-141 | 0.3962 | Medium |
| semantic_frame | 6 | 3.10e-77 | 0.2926 | Small |
| model_name | 6 | 8.36e-36 | 0.2016 | Small |
| dialect | 2 | 2.55e-30 | 0.1747 | Small |
| field | 6 | 0.000434 | 0.0723 | Very small |
| model_family | 2 | 0.0423 | 0.0310 | Very small |
| stereotype_label | 3 | 0.5548 | 0.0166 | Very small |

---

## Key Finding

The strongest practical effect came from template ID.

This means that sentence formulation had the strongest association with preferred gender in the v4 benchmark.

Although model name, semantic frame, dialect, model family, and field were statistically significant, their effect sizes were smaller than template ID.

Stereotype label was not statistically significant and had a very small effect size.

---

## Interpretation

The v4 effect-size results show that measured Arabic occupational gender bias is strongly affected by benchmark design.

In particular, template formulation can influence measured gender preference more strongly than model family or stereotype-label category.

This supports the thesis claim that Arabic bias evaluation should not rely on a single prompt or template.

---

## Methodological Contribution

The effect-size analysis strengthens the proposed contribution:

**Template-Induced Bias Direction Volatility**

This contribution means that the same model can show different gender-preference directions under different templates, and template choice has a measurable association with preferred gender.

---

## Final Thesis Wording

The v4 benchmark showed that template ID was the strongest factor associated with preferred gender, with a medium Cramér's V effect size. Semantic frame, model name, and dialect were also significant, but with smaller effect sizes. In contrast, stereotype label was not statistically significant after balancing. These results suggest that Arabic occupational gender-bias evaluation is highly sensitive to benchmark formulation, and that template-level reporting is necessary for reliable bias analysis.