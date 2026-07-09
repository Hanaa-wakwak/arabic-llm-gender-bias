# Final Thesis Package Index

## Thesis Title

Measuring Occupational Gender Bias in Arabic Causal Language Models using a Counterfactual Dialect-Aware Benchmark

---

## Main Benchmark

| Item                            | Path                                                                              |
| ------------------------------- | --------------------------------------------------------------------------------- |
| Final occupational benchmark v2 | `data/occupational_benchmark/occupational_bias_v2.csv`                            |
| Occupation-field lexicon v2     | `data/occupational_benchmark/occupations_fields_v2.csv`                           |
| Benchmark quality report        | `results/occupational_benchmark_quality/occupational_bias_v2_quality_summary.csv` |

---

## Main Results

| Item                       | Path                                                                                                                      |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Six-model combined results | `results/occupational_benchmark_v2_all_models/combined_analysis/overall_by_model.csv`                                     |
| Model-family summary       | `results/occupational_benchmark_v2_all_models/combined_analysis/overall_by_model_family.csv`                              |
| Binomial tests             | `results/occupational_benchmark_v2_all_models/combined_analysis/statistical_tests/overall_binomial_by_model.csv`          |
| Wilcoxon tests             | `results/occupational_benchmark_v2_all_models/combined_analysis/statistical_tests/overall_wilcoxon_by_model.csv`          |
| Chi-square family test     | `results/occupational_benchmark_v2_all_models/combined_analysis/statistical_tests/chi_square_model_family_preference.csv` |
| Pairwise model comparisons | `results/occupational_benchmark_v2_all_models/combined_analysis/statistical_tests/pairwise_model_comparisons.csv`         |

---

## Main Scripts

| Script                                           | Purpose                                               |
| ------------------------------------------------ | ----------------------------------------------------- |
| `src/build_occupations_fields_v2.py`             | Builds the final occupation-field list                |
| `src/build_occupational_benchmark_v2.py`         | Builds the final v2 sentence-pair benchmark           |
| `src/check_occupational_benchmark_quality.py`    | Checks benchmark consistency                          |
| `src/score_occupational_single_model_v1.py`      | Scores one model on masculine/feminine sentence pairs |
| `src/analyze_occupational_results_v1.py`         | Produces field/dialect/template summaries             |
| `src/combine_all_v2_models.py`                   | Combines six-model v2 results                         |
| `src/statistical_tests_occupational_reusable.py` | Runs statistical tests                                |

---

## Models Evaluated

| Model                       | Family              |
| --------------------------- | ------------------- |
| `aubmindlab/aragpt2-base`   | Arabic-specific     |
| `aubmindlab/aragpt2-medium` | Arabic-specific     |
| `bigscience/bloom-560m`     | Non-Arabic-specific |
| `bigscience/bloom-1b1`      | Non-Arabic-specific |
| `facebook/xglm-564M`        | Non-Arabic-specific |
| `Qwen/Qwen2.5-0.5B`         | Non-Arabic-specific |

---

## Final Main Finding

Arabic-specific models showed masculine occupational preference.

Non-Arabic-specific multilingual/general models showed feminine occupational preference.

| Model Family        | Total Items | Masculine Preferred | Feminine Preferred | Direction |
| ------------------- | ----------: | ------------------: | -----------------: | --------- |
| Arabic-specific     |         480 |                 320 |                160 | Masculine |
| Non-Arabic-specific |         960 |                 346 |                610 | Feminine  |

The model-family association was statistically significant:

```text
chi-square p-value = 1.64e-27
```

---

## External Dataset Pilots

| Dataset            | Role                                                          |
| ------------------ | ------------------------------------------------------------- |
| APGC-format pilot  | External grammatical-gender sentence-pair pipeline validation |
| ArGAN-format pilot | Qualitative prompt-based external validation                  |

---

## APGC Files

| Item                   | Path                                                                               |
| ---------------------- | ---------------------------------------------------------------------------------- |
| APGC pilot sample      | `data/external_datasets/apgc/apgc_gender_pairs_sample.csv`                         |
| APGC combined analysis | `results/external_datasets/apgc/combined_analysis/apgc_pilot_overall_by_model.csv` |
| APGC converter         | `src/convert_apgc_to_pair_format.py`                                               |
| APGC analyzer          | `src/analyze_apgc_gender_results.py`                                               |
| APGC combine script    | `src/combine_apgc_pilot_results.py`                                                |

---

## ArGAN Files

| Item                                | Path                                                                                                                                                       |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ArGAN pilot sample                  | `data/external_datasets/argan/argan_gender_pilot_sample.csv`                                                                                               |
| Base generation script              | `src/generate_argan_outputs.py`                                                                                                                            |
| Improved instruct generation script | `src/generate_argan_outputs_instruct.py`                                                                                                                   |
| Annotation sheet creator            | `src/create_argan_annotation_sheet.py`                                                                                                                     |
| Quality analyzer                    | `src/analyze_argan_generation_quality.py`                                                                                                                  |
| Qwen-Instruct generation results    | `results/external_datasets/argan_instruct/argan_instruct_generation_results_Qwen_Qwen2_5_0_5B_Instruct.csv`                                                |
| Quality summary                     | `results/external_datasets/argan_instruct/quality_analysis_qwen_instruct/argan_instruct_generation_results_Qwen_Qwen2_5_0_5B_Instruct_quality_summary.csv` |

---

## Thesis Chapter Drafts

| Chapter                                | Path                                                                |
| -------------------------------------- | ------------------------------------------------------------------- |
| Chapter 3 — Methodology                | `docs/occupational_scope/chapter_3_methodology_draft.md`            |
| Chapter 4 — Results                    | `docs/occupational_scope/chapter_4_results_draft.md`                |
| Chapter 5 — Discussion                 | `docs/occupational_scope/chapter_5_discussion_draft.md`             |
| Chapter 6 — Conclusion and Future Work | `docs/occupational_scope/chapter_6_conclusion_future_work_draft.md` |

---

## Supervisor / Presentation Documents

| Document                             | Path                                                              |
| ------------------------------------ | ----------------------------------------------------------------- |
| Supervisor comments response         | `docs/occupational_scope/supervisor_comments_response.md`         |
| Final supervisor meeting summary     | `docs/occupational_scope/final_supervisor_meeting_summary.md`     |
| Final thesis results summary         | `docs/occupational_scope/final_thesis_results_summary.md`         |
| Final presentation discussion script | `docs/occupational_scope/final_presentation_discussion_script.md` |
| Final thesis report structure        | `docs/occupational_scope/final_thesis_report_structure.md`        |

---

## Final Repository Explanation

This repository contains a complete pipeline for measuring occupational gender bias in Arabic causal language models.

The pipeline includes:

1. benchmark construction,
2. benchmark quality checking,
3. model likelihood scoring,
4. result aggregation,
5. statistical testing,
6. external dataset pilots,
7. thesis chapter drafts,
8. supervisor-facing summaries.

The main quantitative contribution is the occupational benchmark v2 and the six-model statistical analysis.

The APGC and ArGAN pilots are auxiliary validation experiments showing that the evaluation framework can be extended to broader Arabic gender-bias datasets.
## v3 Sensitivity Analysis Files

| Item | Path |
|---|---|
| v3 occupation lexicon | `data/occupational_benchmark/occupations_fields_v3.csv` |
| v3 benchmark | `data/occupational_benchmark/occupational_bias_v3.csv` |
| v3 controlled benchmark | `data/occupational_benchmark/occupational_bias_v3_controlled.csv` |
| v3 quality summary | `results/occupational_benchmark_v3_quality/occupational_bias_v3_quality_summary.csv` |
| v3 quick model results | `results/occupational_benchmark_v3_quick_models/` |
| v3 controlled diagnostics | `results/occupational_benchmark_v3_controlled_quick_models/` |
| v3 sensitivity summary | `docs/occupational_scope/v3_sensitivity_analysis_summary.md` |
| v3 balanced plan | `docs/occupational_scope/v3_balanced_benchmark_plan.md` |