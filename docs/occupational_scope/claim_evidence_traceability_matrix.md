# Claim-to-Evidence Traceability Matrix

## Purpose

This matrix maps the main thesis claims to the files and outputs that support them.

It improves defense readiness by making each major claim traceable to benchmark data, result files, statistical outputs, or documentation.

## Matrix

| claim_id | claim | evidence | evidence_file | supporting_result | claim_type | evidence_file_exists | supporting_result_exists |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CL1 | v2 is the main validated benchmark. | v2 contains 60 occupations, 4 templates, and 240 sentence pairs with quality checks passed. | data/occupational_benchmark/occupational_bias_v2.csv | results/occupational_benchmark_quality/occupational_bias_v2_quality_summary.csv | benchmark_design | True | True |
| CL2 | Arabic-specific and non-Arabic-specific models show different preference patterns in v2. | v2 six-model combined analysis and model-family summary. | results/occupational_benchmark_v2_all_models/combined_analysis/overall_by_model.csv | results/occupational_benchmark_v2_all_models/combined_analysis/family_summary.csv | empirical_result | True | False |
| CL3 | The v2 model-family pattern is statistically significant. | Chi-square test on model family versus preferred gender. | results/occupational_benchmark_v2_all_models/combined_analysis/chi_square_model_family.csv | results/occupational_benchmark_v2_all_models/combined_analysis/chi_square_model_family.csv | statistical_result | False | False |
| CL4 | Benchmark expansion can change measured bias direction. | v3 and v3 controlled sensitivity results show direction changes compared with v2. | data/occupational_benchmark/occupational_bias_v3.csv | docs/occupational_scope/v3_sensitivity_analysis_summary.md | sensitivity_result | True | True |
| CL5 | Stereotype balancing alone does not guarantee stable bias direction. | v3 balanced benchmark results remain different from the v2 direction for quick models. | data/occupational_benchmark/occupational_bias_v3_balanced.csv | docs/occupational_scope/v3_balanced_final_result_summary.md | robustness_result | True | True |
| CL6 | Template formulation can cause direction flips. | v4 template volatility analysis shows direction_flip_present=True for all six models. | results/occupational_benchmark_v4_template_perturbation_all_models/combined_sensitivity_analysis/template_volatility_by_model.csv | docs/occupational_scope/v4_all_models_final_result_summary.md | robustness_result | True | True |
| CL7 | Dialect affects measured gender preference. | v4 dialect-shift analysis compares MSA and Egyptian Arabic directions. | results/occupational_benchmark_v4_template_perturbation_all_models/combined_sensitivity_analysis/dialect_shift_by_model.csv | docs/occupational_scope/v4_all_models_final_result_summary.md | dialect_result | True | True |
| CL8 | Template ID has the strongest practical effect in v4. | Cramér’s V effect-size analysis ranks template_id as the strongest effect. | results/occupational_benchmark_v4_template_perturbation_all_models/effect_sizes/v4_cramers_v_effect_sizes.csv | docs/occupational_scope/v4_effect_size_analysis_summary.md | effect_size_result | True | True |
| CL9 | Stereotype label is not significant after balancing in v4. | v4 chi-square tests show stereotype_label is not statistically significant. | results/occupational_benchmark_v4_template_perturbation_all_models/statistical_tests/v4_overall_chi_square_tests.csv | results/occupational_benchmark_v4_template_perturbation_all_models/effect_sizes/v4_cramers_v_effect_sizes.csv | statistical_result | True | True |
| CL10 | Explicit job-title contexts behave differently from broader occupational templates. | v5 job-title benchmark and v4-v5 comparison show near-balanced or weak masculine results for quick models. | data/occupational_benchmark/occupational_bias_v5_job_titles.csv | docs/occupational_scope/v4_v5_job_title_context_comparison.md | context_result | True | True |
| CL11 | Arabic occupational bias measurement is context-sensitive. | Context Sensitivity Index combines template volatility, dialect shift, and v4-to-v5 job-title context shift. | results/final_package/context_sensitivity_index_quick_models.csv | docs/occupational_scope/context_sensitivity_index_summary.md | methodological_result | True | True |
| CL12 | The benchmark suite includes quality-control layers. | Counterfactual pair integrity audit, benchmark quality checks, artifact registry, and completeness checks. | results/final_package/counterfactual_pair_integrity_summary.csv | docs/occupational_scope/counterfactual_pair_integrity_audit.md | quality_control | True | True |
| CL13 | The thesis contribution is a framework, not only a dataset. | Benchmark design taxonomy, reporting checklist, technical contribution matrix, and datasheet. | docs/occupational_scope/benchmark_design_taxonomy.md | docs/occupational_scope/final_technical_contribution_matrix.md | contribution_claim | True | True |

## Contribution

This traceability matrix strengthens the thesis package because it links claims, implementation artifacts, and empirical evidence in a transparent way.
