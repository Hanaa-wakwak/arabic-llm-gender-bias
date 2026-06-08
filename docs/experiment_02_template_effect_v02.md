# Experiment 02 — Template Effect Analysis v0.2

## Goal

The goal of this experiment is to test whether the dialect-level difference observed in v0.1 is caused by dialect variation or by repeated template structures.

## Dataset

Benchmark version: minimal_pairs_v02.csv

Total items: 36

The dataset includes:
- MSA items
- Egyptian Arabic items
- Occupation templates
- Trait templates
- Template type labels

## Model

aubmindlab/aragpt2-base

## Overall Result

| Metric | Value |
|---|---:|
| Total items | 36 |
| Masculine preferred | 17 |
| Feminine preferred | 19 |
| Masculine preferred percent | 47.22% |
| Feminine preferred percent | 52.78% |
| Average score difference | -0.264 |
| Median score difference | -0.039 |

## Dialect-Level Result

| Dialect | Items | Avg score difference | Masculine preferred | Feminine preferred |
|---|---:|---:|---:|---:|
| Egyptian | 18 | -0.733 | 5 | 13 |
| MSA | 18 | 0.204 | 12 | 6 |

## Template-Level Result

| Template | Items | Avg score difference | Masculine preferred | Feminine preferred |
|---|---:|---:|---:|---:|
| egyptian_byeshtaghal_role | 6 | -0.667 | 0 | 6 |
| egyptian_direct_trait | 6 | 0.082 | 5 | 1 |
| egyptian_shaghal_role | 6 | -1.613 | 0 | 6 |
| msa_direct_trait | 6 | 0.005 | 4 | 2 |
| msa_named_role | 6 | 0.259 | 4 | 2 |
| msa_work_role | 6 | 0.349 | 4 | 2 |

## Interpretation

The results show that the observed Egyptian feminine preference is strongly affected by template type.

The strongest effect appears in the Egyptian occupation template "هو شغال / هي شغالة", which produced feminine preference in all 6 items and had the strongest negative average score difference.

The Egyptian "بيشتغل / بتشتغل" template also produced feminine preference in all 6 items, but the effect was weaker.

However, Egyptian direct trait templates preferred masculine forms in 5 out of 6 items. This means that the Egyptian dialect itself does not always produce feminine preference. Instead, occupation templates appear to be the main driver.

## Conclusion

This experiment confirms that template effects must be controlled before making gender-bias claims.

The scoring pipeline works, but the benchmark needs a more carefully balanced template design.

## Next Step

Create benchmark v0.3 with:
- more balanced templates
- fewer repeated structures
- template_id column
- concept_id column
- matched MSA/Egyptian pairs for each concept
