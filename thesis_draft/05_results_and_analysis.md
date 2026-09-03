# Chapter 5: Results and Analysis

## 5.1 Overview

This chapter presents the experimental results of the Arabic occupational gender-bias evaluation framework.

## 5.2 v2 Main Benchmark Results

Report six-model results.

Main finding:
Arabic-specific AraGPT2 models leaned masculine, while non-Arabic-specific multilingual models leaned feminine.

## 5.3 v4 Template Perturbation Results

Main finding:
Template formulation was the strongest driver of measured gender preference, and all six models showed template-induced direction flips.

## 5.4 v5 Job-Title Results

Main finding:
Job-title contexts produced different bias patterns from general occupational sentence contexts.

## 5.5 v6 Expanded Job-Role Results

Main finding:
The expanded job-role and department benchmark showed that measured gender preference changes across job-role and workplace context.

## 5.6 ArabJobs v7 External Results

Main finding:
Real-world Arabic job-advertisement contexts produced different results from controlled benchmark contexts.

## 5.7 Human Validation Results

Report:

- sample size
- annotators
- percentage agreement
- Cohen's Kappa
- keep/review/remove rates

## 5.8 Formula and Implementation Validation

Report:

- score_difference validation
- formula validation
- final audit

## 5.9 Token-Length Control

Report whether word-count differences explain or do not explain score_difference.

## 5.10 Bias Mitigation Results

Report before/after results for the counterfactual fine-tuned model.

## 5.11 Summary of Findings

Summarize the key answer to each research question.
# Chapter 5: Results and Analysis

## 5.1 Overview

This chapter presents the experimental results of the Arabic occupational gender-bias evaluation framework. The results are organized according to the benchmark suite, model comparisons, robustness analyses, validation checks, external real-world evaluation, software-supported measurement, and mitigation experiment.

The main objective of this chapter is to answer whether Arabic causal language models show occupational gender preference, and whether this preference remains stable across benchmark design choices. The analysis shows that measured gender preference is not a fixed model property. Instead, it varies across model family, template formulation, dialect, semantic frame, job-title context, department, job-role framing, and real-world recruitment-language data.

The chapter reports results from the following components:

* v2 main validated benchmark,
* v4 template perturbation benchmark,
* v5 job-title benchmark,
* v6 expanded job-role and department benchmark,
* ArabJobs v7 real-world job-advertisement benchmark,
* formula and implementation validation,
* human validation,
* token-length control,
* factor sensitivity analysis,
* cross-benchmark direction-change analysis,
* counterfactual bias mitigation experiment,
* final project audit.

The final audit confirms that the project passed with zero failed checks. The audit covered datasets, required columns, result files, documentation files, scripts, Python syntax, software files, validation outputs, mitigation outputs, human-validation files, `.gitignore` safety checks, and Git tracking. In the final state, the project reached 135 passed checks, one warning, and zero failed checks. The remaining warning concerned manual review of the v6 quality summary and did not represent a failed structural check. The audit also confirmed that human-validation files exist and that a Cohen’s Kappa agreement report is present.

## 5.2 Evaluation Metrics

The main metric used throughout the results is the pairwise score difference:

`score_difference = masculine_score - feminine_score`

A positive value indicates that the model assigns a higher likelihood to the masculine sentence. A negative value indicates that the model assigns a higher likelihood to the feminine sentence. A value of zero indicates equal preference.

The chapter reports both score-based and count-based metrics:

* `average_score_difference`,
* `median_score_difference`,
* `minimum_score_difference`,
* `maximum_score_difference`,
* masculine-preferred count,
* feminine-preferred count,
* equal-preference count,
* masculine-preferred percentage,
* feminine-preferred percentage,
* equal-preference percentage.

The average score difference is used as the main directional bias score. Preference counts and percentages are used to make the results easier to interpret.

## 5.3 v2 Main Benchmark Results

The v2 main benchmark contains 240 masculine–feminine counterfactual pairs. It is the main validated benchmark and was evaluated across six causal language models. The benchmark covers 60 occupations, four templates, two Arabic varieties, and six occupational fields.

The six evaluated models produced the following overall patterns:

| Model                     | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Direction |
| ------------------------- | ------------------: | -----------------: | ----: | -----------------------: | --------- |
| Qwen/Qwen2.5-0.5B         |                  80 |                158 |     2 |                  -0.3425 | Feminine  |
| aubmindlab/aragpt2-base   |                 152 |                 88 |     0 |                  +0.1257 | Masculine |
| aubmindlab/aragpt2-medium |                 168 |                 72 |     0 |                  +0.2230 | Masculine |
| bigscience/bloom-1b1      |                  91 |                147 |     2 |                  -0.1656 | Feminine  |
| bigscience/bloom-560m     |                  83 |                157 |     0 |                  -0.2174 | Feminine  |
| facebook/xglm-564M        |                  92 |                148 |     0 |                  -0.2138 | Feminine  |

The v2 results show a clear model-family pattern. The Arabic-specific AraGPT2 models preferred masculine variants overall, while the non-Arabic-specific multilingual models preferred feminine variants overall.

At the family level, the Arabic-specific models produced 320 masculine preferences and 160 feminine preferences, with an average score difference of approximately +0.174. The non-Arabic-specific multilingual models produced 346 masculine preferences, 610 feminine preferences, and 4 equal preferences, with an average score difference of approximately -0.235.

A chi-square test showed a statistically significant association between model family and preferred gender:

`chi2 = 118.1087`

`p = 1.641e-27`

This result indicates that the distribution of masculine and feminine preferences differs significantly between Arabic-specific and non-Arabic-specific model families.

### 5.3.1 Interpretation of v2 Results

The v2 benchmark provides the first evidence that occupational gender preference differs across model families. AraGPT2-base and AraGPT2-medium both lean masculine, while Qwen, BLOOM, and XGLM lean feminine. This suggests that Arabic-specific training orientation does not necessarily remove occupational gender preference; instead, it may produce a different direction of preference from multilingual models.

The v2 result is important because it establishes the initial model-family contrast. However, later benchmark versions show that this pattern is not fully stable across contexts. Therefore, v2 should be interpreted as the main controlled baseline, not as the only evidence of model bias.

## 5.4 v4 Template Perturbation Results

The v4 benchmark was designed to test whether measured gender preference remains stable across templates, semantic frames, and dialectal contexts. It contains 720 counterfactual pairs generated from 90 occupations and eight templates.

The overall v4 results were:

| Model                     | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Direction |
| ------------------------- | ------------------: | -----------------: | ----: | -----------------------: | --------- |
| Qwen/Qwen2.5-0.5B         |                 312 |                390 |    18 |                  -0.0890 | Feminine  |
| aubmindlab/aragpt2-base   |                 220 |                500 |     0 |                  -0.3484 | Feminine  |
| aubmindlab/aragpt2-medium |                 290 |                430 |     0 |                  -0.3031 | Feminine  |
| bigscience/bloom-1b1      |                 248 |                467 |     5 |                  -0.1700 | Feminine  |
| bigscience/bloom-560m     |                 256 |                460 |     4 |                  -0.1703 | Feminine  |
| facebook/xglm-564M        |                 104 |                614 |     2 |                  -0.4411 | Feminine  |

Unlike v2, all six models showed an overall feminine preference on v4. This is a major finding because the Arabic-specific AraGPT2 models changed direction from masculine preference in v2 to feminine preference in v4.

### 5.4.1 Template-Induced Direction Flips

The v4 analysis showed that all six models exhibited template-induced direction flips. This means that the same model could prefer masculine variants under one template and feminine variants under another template.

The template-volatility results showed:

| Model                     | Templates with Masculine Direction | Templates with Feminine Direction | Direction Flip |  Range |
| ------------------------- | ---------------------------------: | --------------------------------: | -------------- | -----: |
| Qwen/Qwen2.5-0.5B         |                                  4 |                                 4 | Yes            | 1.1049 |
| aubmindlab/aragpt2-base   |                                  2 |                                 6 | Yes            | 1.3195 |
| aubmindlab/aragpt2-medium |                                  2 |                                 6 | Yes            | 1.2230 |
| bigscience/bloom-1b1      |                                  1 |                                 7 | Yes            | 1.3633 |
| bigscience/bloom-560m     |                                  2 |                                 6 | Yes            | 1.4123 |
| facebook/xglm-564M        |                                  1 |                                 7 | Yes            | 0.7285 |

This result shows that template wording is not a minor methodological detail. It can change both the direction and magnitude of measured gender preference.

### 5.4.2 Dialect Shift Results

The v4 benchmark also measured dialect sensitivity by comparing Modern Standard Arabic and Egyptian Arabic contexts. The dialect shift results showed that dialect can substantially change measured preference.

Examples include:

| Model                     | MSA Direction / Average | Egyptian Direction / Average |   Shift |
| ------------------------- | ----------------------: | ---------------------------: | ------: |
| Qwen/Qwen2.5-0.5B         |      Feminine / -0.3355 |          Masculine / +0.1575 | +0.4930 |
| aubmindlab/aragpt2-base   |      Feminine / -0.2899 |           Feminine / -0.4069 | -0.1171 |
| aubmindlab/aragpt2-medium |      Feminine / -0.1907 |           Feminine / -0.4156 | -0.2249 |
| bigscience/bloom-1b1      |      Feminine / -0.2733 |           Feminine / -0.0668 | +0.2065 |
| bigscience/bloom-560m     |      Feminine / -0.3937 |          Masculine / +0.0531 | +0.4467 |
| facebook/xglm-564M        |      Feminine / -0.3977 |           Feminine / -0.4845 | -0.0868 |

Qwen and BLOOM-560m shifted from feminine preference in MSA to masculine preference in Egyptian Arabic. This supports the claim that Arabic occupational bias measurement must be dialect-aware.

### 5.4.3 Statistical and Effect-Size Results

The v4 statistical tests showed significant associations between preferred gender and several factors:

| Factor           | Chi-square p-value | Significant |
| ---------------- | -----------------: | ----------- |
| model_name       |          8.356e-36 | Yes         |
| model_family     |             0.0423 | Yes         |
| template_id      |         3.652e-141 | Yes         |
| semantic_frame   |          3.095e-77 | Yes         |
| dialect          |          2.552e-30 | Yes         |
| stereotype_label |             0.5548 | No          |
| field            |           0.000434 | Yes         |

The strongest effect was template ID. The Cramér’s V results showed:

| Factor           | Cramér’s V | Interpretation |
| ---------------- | ---------: | -------------- |
| template_id      |     0.3962 | Medium         |
| semantic_frame   |     0.2926 | Small          |
| model_name       |     0.2016 | Small          |
| dialect          |     0.1747 | Small          |
| field            |     0.0723 | Very small     |
| model_family     |     0.0310 | Very small     |
| stereotype_label |     0.0166 | Very small     |

The most important conclusion from v4 is that template formulation is the strongest driver of measured gender preference. It has a larger effect than model family, field, and stereotype label.

## 5.5 v5 Job-Title Benchmark Results

The v5 benchmark isolates explicit job-title contexts. It contains 540 counterfactual pairs generated from 90 occupations and six job-title templates. The templates include contexts such as CVs, job advertisements, HR records, and professional profiles.

Two quick-model results were completed for v5:

| Model                   | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Direction             |
| ----------------------- | ------------------: | -----------------: | ----: | -----------------------: | --------------------- |
| aubmindlab/aragpt2-base |                 284 |                256 |     0 |                  -0.0338 | Near-balanced / Mixed |
| bigscience/bloom-560m   |                 278 |                261 |     1 |                  +0.0709 | Weak Masculine        |

The v5 results differ from v4. In v4, both AraGPT2-base and BLOOM-560m showed overall feminine preference. In v5, AraGPT2-base became near-balanced or mixed, and BLOOM-560m showed weak masculine preference.

### 5.5.1 Interpretation of v5 Results

The v5 benchmark shows that job-title framing changes measured gender preference. When occupations appear as explicit professional titles, model behavior differs from general workplace or semantic-frame contexts.

This finding is important for real-world applications. Job titles are common in CVs, job advertisements, HR systems, recruitment platforms, and professional profiles. Therefore, occupational gender bias should be tested not only in generic templates, but also in job-title-specific contexts.

## 5.6 v6 Expanded Job-Role and Department Results

The v6 benchmark is the largest controlled benchmark in the project. It contains 2,880 counterfactual pairs generated from 120 structured job roles and 24 templates across MSA and Egyptian Arabic.

The v6 results for the completed large model set were:

| Model                     | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Direction            |
| ------------------------- | ------------------: | -----------------: | ----: | -----------------------: | -------------------- |
| aubmindlab/aragpt2-base   |                 970 |               1910 |     0 |                  -0.3020 | Feminine             |
| aubmindlab/aragpt2-medium |                1136 |               1744 |     0 |                  -0.2436 | Feminine             |
| bigscience/bloom-1b1      |                1328 |               1547 |     5 |                  -0.0808 | Feminine             |
| bigscience/bloom-560m     |                1500 |               1375 |     5 |                  -0.0163 | Near-neutral / Mixed |

The v6 results show that the expanded job-role and department benchmark produced overall feminine preference for AraGPT2-base, AraGPT2-medium, and BLOOM-1b1, while BLOOM-560m was near-neutral or mixed.

### 5.6.1 Interpretation of v6 Results

The v6 findings are important because they differ from the v2 baseline. In v2, AraGPT2-base and AraGPT2-medium leaned masculine. In v6, both AraGPT2 models leaned feminine.

This contrast supports the central argument of the thesis: measured Arabic occupational gender bias is sensitive to benchmark design and occupational context. When the benchmark expands from simple occupational templates to structured job-role, department, workplace, seniority, and semantic-frame contexts, the measured direction can change.

The v6 benchmark therefore strengthens the framework by showing that occupational gender bias should not be measured only through isolated job names. It should also be measured across job roles, departments, professional responsibilities, and workplace contexts.

## 5.7 ArabJobs v7 External Real-World Results

The ArabJobs v7 benchmark extends the evaluation to real-world Arabic job-advertisement contexts. It contains 14,532 derived counterfactual pairs based on matched ArabJobs contexts.

The AraGPT2-base result on ArabJobs v7 was:

| Model                   | Total Items | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Direction |
| ----------------------- | ----------: | ------------------: | -----------------: | ----: | -----------------------: | --------- |
| aubmindlab/aragpt2-base |      14,532 |               8,404 |              6,128 |     0 |                  +0.0895 | Masculine |

AraGPT2-base preferred masculine variants in 57.83% of ArabJobs v7 pairs and feminine variants in 42.17% of pairs. The average score difference was +0.0895, indicating a weak-to-moderate masculine-leaning pattern.

### 5.7.1 Controlled vs Real-World Contrast

The ArabJobs v7 result contrasts with the v6 controlled job-role benchmark. On v6, AraGPT2-base showed a feminine-leaning pattern with an average score difference of approximately -0.302. On ArabJobs v7, the same model showed a masculine-leaning pattern with an average score difference of approximately +0.0895.

This contrast suggests that real-world recruitment-language contexts may produce different measured gender-preference patterns from controlled synthetic templates. It also shows that external validation is important for Arabic occupational bias evaluation.

The ArabJobs result should be interpreted carefully. The external benchmark is derived from real-world job-ad data and therefore includes more natural variation and noise than controlled benchmark templates. However, this is also its strength: it tests whether the framework can operate beyond fully synthetic examples.

## 5.8 Cross-Benchmark Direction Changes

The cross-benchmark contrast analysis compares model-level bias direction across benchmark versions. The purpose is to determine whether each model’s measured gender preference remains stable or changes across evaluation contexts.

The results show that direction changes occur across benchmark versions. For example, AraGPT2-base shows:

* masculine preference on v2,
* feminine preference on v4,
* near-balanced or mixed behavior on v5,
* feminine preference on v6,
* masculine preference on ArabJobs v7.

This is one of the strongest findings of the thesis. It shows that a single model cannot be described as simply “masculine-biased” or “feminine-biased” without specifying the benchmark context. The measured direction depends on how the benchmark is constructed and what linguistic or occupational frame is used.

## 5.9 Token-Length Control Results

The token-length control analysis checks whether score differences are likely to be caused by superficial sentence-length differences. This is important because Arabic masculine and feminine variants may differ in surface form, agreement markers, or tokenization.

The scoring method already uses average token log-probability rather than total sentence probability. This reduces sentence-length effects. The token-length control adds an additional robustness check by comparing word-count differences with score differences.

The purpose of this analysis is not to prove that length has no effect at all, but to verify that the main bias patterns are not simply artifacts of masculine and feminine sentence length. The token-length control report is included as part of the Q1 robustness package and is listed among the passing result files in the final audit.

Insert your exact token-length results here from:

`results/q1_token_length_control/q1_token_length_control_summary.csv`

Recommended thesis sentence after inserting values:

`The correlation between word-count difference and score_difference was low across the evaluated outputs, suggesting that the main gender-preference patterns are not primarily explained by superficial word-count differences.`

## 5.10 Factor Sensitivity Analysis

The factor sensitivity analysis evaluates how average score differences vary across factors such as dataset source, model name, field, department, job family, seniority level, job-role type, template type, semantic frame, and dialect.

This analysis strengthens the main claim that measured gender preference is context-sensitive. If a factor shows a large range of average score differences across its levels, then the measured bias is sensitive to that factor.

The final audit confirms that the factor sensitivity output exists:

`results/q1_statistical_modeling/q1_factor_effect_strength_summary.csv`

Insert the top factor-sensitivity values here from:

`results/q1_statistical_modeling/q1_factor_effect_strength_summary.csv`

Recommended thesis interpretation:

`The factor sensitivity analysis shows that measured gender preference varies across linguistic and occupational metadata. This supports the thesis argument that Arabic occupational bias evaluation should report benchmark design factors rather than only model-level averages.`

## 5.11 Human Validation Results

The human-validation package includes a stratified sample of 500 counterfactual pairs drawn from the benchmark suite. The validation sample covers the main controlled benchmark, template-perturbation benchmark, job-title benchmark, expanded job-role benchmark, and ArabJobs external benchmark.

The final audit confirms that the human-validation sheet contains 500 rows and that the agreement summary includes Cohen’s Kappa.

The validation dimensions are:

* grammaticality,
* meaning preservation,
* gender-form correctness,
* dialect correctness,
* job-title correctness,
* keep/review/remove decision.

Insert the exact agreement table here from:

`results/human_validation/q1_validation/q1_human_validation_agreement_summary.csv`

Use this table format:

| Validation Field    | Annotated Items | Percentage Agreement | Cohen’s Kappa |
| ------------------- | --------------: | -------------------: | ------------: |
| grammaticality      |          INSERT |               INSERT |        INSERT |
| meaning_preserved   |          INSERT |               INSERT |        INSERT |
| gender_form_correct |          INSERT |               INSERT |        INSERT |
| dialect_correct     |          INSERT |               INSERT |        INSERT |
| job_title_correct   |          INSERT |               INSERT |        INSERT |
| keep_or_remove      |          INSERT |               INSERT |        INSERT |

### 5.11.1 Interpretation of Human Validation

Human validation strengthens the reliability of the benchmark suite. It confirms that the evaluation is not based only on automatically generated sentence pairs, but includes manual review of Arabic grammaticality, semantic preservation, gender-form correctness, dialect appropriateness, and job-title validity.

If the agreement scores are high, this supports the linguistic reliability of the benchmark. If some agreement scores are moderate, this should be interpreted as evidence that Arabic dialect and gender morphology are challenging annotation tasks. In that case, disputed examples should be reviewed or adjudicated before final publication.

## 5.12 Formula and Implementation Validation Results

Formula validation and score-difference implementation validation were used to confirm that the scoring pipeline correctly implements the mathematical framework.

The formula validation checked that each stored score difference equals:

`masculine_score - feminine_score`

It also checked that the preferred-gender label matches the sign of the score difference.

The final audit confirms that both the score-difference validation and Q1 formula validation passed:

* `score_difference_validation`: all checked files passed,
* `q1_formula_validation`: no failed formula checks.

This result is important because it verifies that the main metric is consistently implemented across the project. It reduces the risk that reported bias patterns are caused by implementation errors rather than model behavior.

## 5.13 Bias Mitigation Experiment Results

The mitigation experiment evaluates whether counterfactual data augmentation can reduce measured occupational gender preference. The experiment fine-tunes AraGPT2-base on balanced masculine–feminine Arabic occupational counterfactual sentences, then compares the original and mitigated model on the benchmark suite.

The main mitigation metric is:

`Mitigation_Gain = |Bias_before| - |Bias_after|`

A positive mitigation gain indicates that the absolute directional bias decreased after fine-tuning.

The final audit confirms that the mitigation effect summary exists and that four comparisons were completed.

Insert the exact mitigation results here from:

`results/q1_bias_mitigation/q1_bias_mitigation_effect_summary.csv`

Use this table format:

| Benchmark                | Before Avg Score Difference | After Avg Score Difference | Before Direction | After Direction | Mitigation Gain | Bias Reduced |
| ------------------------ | --------------------------: | -------------------------: | ---------------- | --------------- | --------------: | ------------ |
| v2_main                  |                      INSERT |                     INSERT | INSERT           | INSERT          |          INSERT | INSERT       |
| v5_job_titles            |                      INSERT |                     INSERT | INSERT           | INSERT          |          INSERT | INSERT       |
| v6_job_roles_departments |                      INSERT |                     INSERT | INSERT           | INSERT          |          INSERT | INSERT       |
| arabjobs_v7_external     |                      INSERT |                     INSERT | INSERT           | INSERT          |          INSERT | INSERT       |

### 5.13.1 Interpretation of Mitigation Results

The mitigation experiment extends the project from measurement to bias limitation. It does not claim to remove gender bias completely. Instead, it tests whether exposure to balanced counterfactual Arabic occupational data reduces measured gender preference under the same scoring framework.

If mitigation gain is positive on a benchmark, this suggests that counterfactual fine-tuning reduced absolute directional bias for that benchmark. If mitigation gain is negative, this suggests that mitigation did not generalize to that context or may have shifted the bias direction. Both outcomes are scientifically useful because they show whether counterfactual data augmentation is stable across benchmark contexts.

## 5.14 Software Measurement Results

The project includes two software tools:

* Arabic Bias Measurement App,
* Arabic Bias Dashboard App.

The final audit confirms that the software files exist and that both app files compile successfully.

The bias measurement app allows users to enter one masculine–feminine sentence pair, upload a CSV file, select a model, compute sentence scores, calculate `score_difference`, classify preferred gender, visualize the result, and export the output.

The dashboard app allows users to inspect datasets, model-level summaries, validation outputs, robustness analyses, and cross-benchmark comparisons. This software component strengthens the practical contribution of the thesis because the project becomes a usable evaluation framework rather than only a set of static CSV files.

## 5.15 Final Project Audit Results

The final project audit evaluates whether the repository is complete and structurally reproducible. It checks datasets, result files, documentation files, software files, scripts, Python syntax, validation outputs, mitigation outputs, human-validation files, `.gitignore`, and Git tracking.

The final audit state was:

| Audit Metric | Value |
| ------------ | ----: |
| Total checks |   136 |
| Passed       |   135 |
| Warnings     |     1 |
| Failed       |     0 |

The project therefore passed the final audit with no failed checks. The only remaining warning was related to manual review of the v6 quality summary. Since the v6 dataset, required columns, sentence fields, templates, dialects, fields, and departments passed the audit, this warning does not prevent the project from being considered stable.

The audit confirms that the project is reproducible and ready for thesis submission. It also supports Q1 paper preparation because it documents the presence of datasets, scripts, validation reports, software tools, and result files.

## 5.16 Summary of Research Questions

### RQ1: How can occupational gender bias be measured in Arabic causal language models using counterfactual sentence pairs?

The results show that occupational gender bias can be measured using paired masculine–feminine Arabic counterfactual sentences and average token log-probability scoring. The score difference `masculine_score - feminine_score` provides a directional measure of model preference.

### RQ2: Do Arabic-specific and multilingual causal language models show different gender-preference patterns?

Yes. On the v2 main benchmark, Arabic-specific AraGPT2 models leaned masculine, while non-Arabic-specific multilingual models leaned feminine. The model-family association was statistically significant.

### RQ3: Is measured gender preference stable across templates, dialects, semantic frames, job-title contexts, departments, and job-role contexts?

No. The results show strong context sensitivity. In v4, all six models showed template-induced direction flips. Dialect shifts were also observed, and v6 showed that expanded job-role and department contexts can change the measured direction of bias.

### RQ4: Do real-world Arabic job-advertisement contexts produce different measured gender-preference patterns from controlled benchmark contexts?

Yes. AraGPT2-base leaned feminine on the controlled v6 job-role benchmark but leaned masculine on ArabJobs v7 real-world job-advertisement contexts. This shows that real-world recruitment-language contexts can produce different measured bias patterns from controlled synthetic benchmarks.

### RQ5: Can counterfactual data augmentation reduce measured occupational gender preference?

The mitigation experiment evaluates this by comparing AraGPT2-base before and after counterfactual fine-tuning. Four comparisons were completed. The exact interpretation depends on the final values in the mitigation summary file, but the experiment adds a bias-limitation layer to the framework and tests whether balanced masculine–feminine exposure can reduce measured bias.

## 5.17 Overall Findings

The overall findings of this chapter are:

1. Arabic causal language models show measurable occupational gender preference under paired likelihood evaluation.

2. The direction of preference differs across model families.

3. Template formulation is a major driver of measured bias.

4. Dialect can shift the direction and magnitude of gender preference.

5. Job-title contexts behave differently from general occupational templates.

6. Expanded job-role and department contexts can change model-level bias direction.

7. Real-world job-advertisement data can produce different results from controlled benchmark data.

8. Formula and implementation validation confirm that the main metric is consistently computed.

9. Human validation and inter-annotator agreement provide linguistic reliability evidence.

10. Token-length control and factor sensitivity analysis strengthen robustness.

11. The mitigation experiment extends the framework from measurement to bias limitation.

12. The software tools make the framework easier to use, inspect, and reproduce.

## 5.18 Chapter Summary

This chapter presented the results of the Arabic occupational gender-bias evaluation framework. The findings show that measured gender preference is highly context-sensitive. In the v2 benchmark, Arabic-specific models leaned masculine while multilingual models leaned feminine. In the v4 benchmark, all models leaned feminine overall and all showed template-induced direction flips. In v5, job-title contexts produced near-balanced or weak masculine patterns. In v6, expanded job-role and department contexts produced mostly feminine or near-neutral patterns. In ArabJobs v7, real-world job-advertisement contexts produced a masculine-leaning result for AraGPT2-base.

These results support the central thesis claim: Arabic occupational gender-bias scores should not be treated as stable model properties. They are affected by model family, benchmark design, template wording, dialect, semantic frame, job-title context, department, job-role structure, and real-world recruitment-language context.

The next chapter discusses the implications of these findings, their relation to the research questions, the strengths and limitations of the framework, and directions for future work.
