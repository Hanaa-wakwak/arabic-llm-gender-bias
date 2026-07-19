# Benchmark Design Taxonomy

## Purpose

This taxonomy summarizes how each benchmark version contributes a different design dimension to the Arabic occupational gender-bias evaluation suite.

## Taxonomy Table

| benchmark | role | occupation_count | template_count | sentence_pair_count | dialects | semantic_frames | stereotype_balance | main_context | main_question | technical_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v2 | main_validated_benchmark | 60 | 4 | 240 | MSA, Egyptian | workplace_presence, professional_statement | not_fully_balanced | general occupational workplace sentences | Do models prefer masculine or feminine occupational sentence variants? | core validated benchmark and six-model model-family comparison |
| v3 | expansion_sensitivity | 90 | 6 | 540 | MSA, Egyptian | expanded occupational sentence frames | partially controlled | expanded occupation and template coverage | Does expanding the benchmark change measured bias direction? | tests sensitivity to occupation coverage and template expansion |
| v3_controlled | occupation_vs_template_diagnostic | 90 | 4 | 360 | MSA, Egyptian | original v2-style frames | partially controlled | expanded occupations with original templates | Is the direction shift caused only by new templates? | separates occupation-set effects from template-set effects |
| v3_balanced | stereotype_balanced_sensitivity | 90 | 4 | 360 | MSA, Egyptian | original v2-style frames | 30 male-stereotyped, 30 female-stereotyped, 30 neutral | balanced occupation stereotype labels | Does stereotype balancing stabilize measured bias direction? | tests robustness after stereotype-label balancing |
| v4 | template_semantic_frame_dialect_sensitivity | 90 | 8 | 720 | MSA, Egyptian | occupation_presence, professional_experience, leadership, competence, achievement_reward, responsibility_trust | 30 male-stereotyped, 30 female-stereotyped, 30 neutral | template perturbation and semantic-frame variation | Does measured bias flip across templates, semantic frames, and dialects? | introduces template-induced direction volatility and effect-size analysis |
| v5 | explicit_job_title_context_sensitivity | 90 | 6 | 540 | MSA, Egyptian | CV profile, job advertisement, HR record, professional profile | 30 male-stereotyped, 30 female-stereotyped, 30 neutral | explicit professional job-title contexts | Do models prefer masculine or feminine job-title forms when occupations appear as direct titles? | separates job-title preference from broader sentence-context preference |

## Interpretation

The benchmark suite is intentionally multi-version. Each version tests a different source of measurement sensitivity: occupation coverage, template design, stereotype balance, semantic frame, dialect, and job-title context.

## Contribution

This taxonomy widens the contribution by presenting the thesis as a benchmark-design framework rather than a single Arabic bias dataset.

The thesis therefore contributes both empirical results and a methodology for testing whether Arabic occupational gender-bias measurements are robust to benchmark-design choices.
