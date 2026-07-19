# Arabic Occupational Bias Evaluation Reporting Checklist

## Purpose

This checklist summarizes what should be reported when evaluating occupational gender bias in Arabic causal language models.

It is derived from the benchmark-design sensitivity findings of this thesis.

## Checklist

| Item | Why It Matters |
|---|---|
| Model name and model family | Bias direction differs across models and model families. |
| Arabic variety or dialect | MSA and Egyptian Arabic can produce different measured preferences. |
| Occupation list and field distribution | Occupation coverage affects measured bias. |
| Masculine and feminine occupational forms | Arabic occupations often have gendered morphology. |
| Template wording | Template formulation can change measured direction. |
| Semantic frame | Workplace, competence, leadership, achievement, and responsibility frames can behave differently. |
| Stereotype-label distribution | Bias results should not rely on an unbalanced occupation stereotype set. |
| Score definition | The meaning of positive and negative score differences must be explicit. |
| Tokenization and scoring method | Likelihood scores depend on tokenization and causal LM scoring. |
| Overall result and subgroup results | Reporting only an overall score may hide template or dialect flips. |
| Statistical tests | Significance should be reported when comparing factors. |
| Effect sizes | Practical impact should be reported, not only p-values. |
| Direction-flip analysis | Models may change direction across templates or contexts. |
| External validation or pilots | External datasets help test extensibility. |
| Limitations | Manual construction, dialect coverage, and scoring assumptions should be stated. |

## Recommended Reporting Format

A complete Arabic occupational bias evaluation should report:

1. overall model-level preference,
2. preference by dialect,
3. preference by template,
4. preference by semantic frame,
5. preference by occupation field,
6. preference by stereotype label,
7. statistical significance,
8. effect size,
9. direction flips,
10. benchmark-design limitations.

## Final Recommendation

Arabic occupational gender-bias evaluation should not rely on one template, one dialect, or one overall score.

It should report benchmark-design sensitivity as part of the final bias result.
