# Experiment 04 — Stable Pilot Benchmark v0.4

## Goal

The goal of this experiment is to create a more stable pilot benchmark by reducing template-driven effects observed in earlier versions.

Previous benchmark versions showed that some dialect-level differences were caused by repeated template structures, especially Egyptian occupation templates such as:

هو بيشتغل ... / هي بتشتغل ...

Therefore, v0.4 removes the most problematic Egyptian occupation template and replaces it with more balanced role-description templates.

## Dataset

Benchmark version: minimal_pairs_v04.csv

Total items: 48

The dataset includes:

* 6 occupation concepts
* 6 trait concepts
* MSA items
* Egyptian Arabic items
* multiple controlled templates
* concept_id and template_id metadata

## Model

aubmindlab/aragpt2-base

## Overall Result

| Metric                      |  Value |
| --------------------------- | -----: |
| Total items                 |     48 |
| Masculine preferred         |     26 |
| Feminine preferred          |     22 |
| Masculine preferred percent | 54.17% |
| Feminine preferred percent  | 45.83% |
| Average score difference    | 0.0599 |
| Median score difference     | 0.0615 |

## Dialect-Level Result

| Dialect  | Items | Avg score difference | Masculine preferred | Feminine preferred |
| -------- | ----: | -------------------: | ------------------: | -----------------: |
| Egyptian |    24 |               0.0602 |                  13 |                 11 |
| MSA      |    24 |               0.0597 |                  13 |                 11 |

## Template-Level Interpretation

The v0.4 template-level analysis shows that template effects were substantially reduced.

Unlike v0.3, no template produced a 100% feminine or masculine dominance pattern. The Egyptian and MSA templates became more balanced after removing the earlier problematic Egyptian occupation template.

This suggests that the earlier dialect-level gap was largely caused by template construction rather than dialect alone.

## Concept-Level Interpretation

Although template-level stability improved, several concept-level effects remain.

Examples:

* emotional showed strong masculine preference.
* engineer showed strong feminine average score difference.
* manager showed strong masculine preference.
* tender showed strong feminine preference.

These effects may reflect lexical frequency, stereotype association, or sentence-specific artifacts. They should be reviewed manually before expanding the benchmark.

## Main Conclusion

Benchmark v0.4 is the first stable pilot benchmark.

Compared with v0.3, v0.4 shows much better dialect balance. Egyptian and MSA subsets have almost identical average score differences, which indicates that the benchmark is less affected by uncontrolled template bias.

However, v0.4 is still a pilot benchmark. It should be used as the starting point for expansion, not as a final benchmark.

## Next Step

The next step is to create a manual review sheet for concept-level problematic items and decide which concepts should be rewritten, retained, or expanded.
