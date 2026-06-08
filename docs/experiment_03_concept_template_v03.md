# Experiment 03 — Concept and Template Analysis v0.3

## Goal

The goal of this experiment is to improve the pilot benchmark by separating concept effects from template effects.

In previous experiments, the observed gender preference was strongly affected by repeated template structures. Therefore, benchmark v0.3 introduces two new metadata columns:

* concept_id
* template_id

This allows the analysis to distinguish whether a score difference is caused by the target concept, the sentence template, the dialect, or their interaction.

## Dataset

Benchmark version: minimal_pairs_v03.csv

Total items: 48

The dataset includes:

* 6 occupation concepts
* 6 trait concepts
* MSA items
* Egyptian Arabic items
* multiple templates per concept

## Model

aubmindlab/aragpt2-base

## Overall Result

| Metric                      |   Value |
| --------------------------- | ------: |
| Total items                 |      48 |
| Masculine preferred         |      23 |
| Feminine preferred          |      25 |
| Masculine preferred percent |  47.92% |
| Feminine preferred percent  |  52.08% |
| Average score difference    | -0.0349 |
| Median score difference     | -0.0271 |

## Dialect-Level Result

| Dialect  | Items | Avg score difference | Masculine preferred | Feminine preferred |
| -------- | ----: | -------------------: | ------------------: | -----------------: |
| Egyptian |    24 |              -0.2396 |                   8 |                 16 |
| MSA      |    24 |               0.1697 |                  15 |                  9 |

## Template-Level Interpretation

The template-level analysis shows that some templates remain problematic.

The strongest template effect appears in the Egyptian occupation template:

هو بيشتغل ... / هي بتشتغل ...

This template produced feminine preference in all 6 items, with an average score difference of -0.816.

Other Egyptian trait templates were more balanced. For example, egyptian direct trait and egyptian said-trait templates produced 3 masculine-preferred and 3 feminine-preferred items.

This suggests that the Egyptian dialect itself is not always associated with feminine preference. Instead, specific occupation templates are responsible for much of the dialect-level difference.

## Concept-Level Interpretation

The concept-level analysis shows that some concepts produce strong gender preference patterns.

The concepts teacher and tender produced feminine preference in all 4 items. In contrast, emotional produced masculine preference in all 4 items.

This indicates that some concepts may have strong lexical or frequency effects in the model. These concepts should not be removed immediately, but they should be flagged as high-risk concepts and analyzed separately in future benchmark versions.

## Main Conclusion

Benchmark v0.3 is the best pilot version so far because the overall score difference is close to zero and the dataset now supports concept-level and template-level analysis.

However, v0.3 is not yet a final benchmark. The next version should include a quality-control layer that flags problematic templates, problematic concepts, and strong outliers before expanding the dataset.

## Next Step

Create a quality report for v0.3 to identify:

* problematic templates
* problematic concepts
* strong outliers
* balanced templates
* concepts that need rewriting
