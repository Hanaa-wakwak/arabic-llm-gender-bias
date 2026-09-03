# Chapter 4: Implementation

## 4.1 Project Structure

Describe repository folders:

- data
- src
- results
- docs
- software_bias_measurement
- software_dashboard
- thesis_draft

## 4.2 Benchmark Construction Scripts

Describe scripts for v2, v4, v5, v6, and ArabJobs v7.

## 4.3 Scoring Pipeline

Describe:

- input CSV
- model loading
- sentence scoring
- score_difference calculation
- output CSV

## 4.4 Analysis Pipeline

Describe:

- overall summaries
- field summaries
- dialect summaries
- template summaries
- cross-benchmark summaries

## 4.5 Validation Pipeline

Describe:

- score validation
- formula validation
- token-length control
- human validation
- final audit

## 4.6 Software Tools

Describe:

- Arabic Bias Measurement App
- Arabic Bias Dashboard App
- run scripts
- GitHub reproducibility

## 4.7 Mitigation Pipeline

Describe:

- balanced training data creation
- counterfactual fine-tuning
- before/after comparison



# Chapter 3: Methodology

## 3.1 Overview

This chapter presents the methodology used to measure occupational gender bias in Arabic causal language models. The proposed framework is based on counterfactual evaluation, where each benchmark item consists of two Arabic sentences that preserve the same occupational meaning while differing only in gendered linguistic form. One sentence uses a masculine occupational form, and the other uses the corresponding feminine form. The central objective is to determine whether a causal language model assigns higher likelihood to the masculine or feminine variant.

The methodology is designed as a robustness-oriented evaluation framework rather than a single static benchmark. It includes controlled benchmark construction, dialect-aware template design, likelihood-based scoring, model-level comparison, template and dialect sensitivity analysis, job-title and job-role evaluation, real-world job-advertisement evaluation, validation procedures, software implementation, and a bias-mitigation experiment.

The framework evaluates open-weight causal language models using average token log-probability. For each masculine–feminine counterfactual pair, the score difference is computed as:

`score_difference = masculine_score - feminine_score`

A positive score difference indicates masculine preference, a negative score difference indicates feminine preference, and zero indicates equal preference. This formulation adapts the logic of paired-sentence and likelihood-based bias evaluation from prior NLP bias research and applies it to Arabic occupational gender morphology.

## 3.2 Research Design

This thesis follows an experimental computational research design. The study constructs Arabic occupational counterfactual benchmarks and evaluates multiple causal language models under controlled and external conditions. The methodology is organized around four main layers:

1. **Benchmark construction layer:** creates masculine–feminine occupational sentence pairs across templates, dialects, job titles, departments, and real-world job-ad contexts.

2. **Model scoring layer:** computes average token log-probability for each sentence and derives directional gender-preference scores.

3. **Analysis and validation layer:** evaluates model behavior using descriptive statistics, statistical tests, robustness checks, human validation, formula validation, and implementation validation.

4. **Software and mitigation layer:** provides an interactive software tool for bias measurement and tests whether counterfactual data augmentation can reduce measured bias.

This design allows the thesis to answer not only whether Arabic causal language models exhibit occupational gender preference, but also whether the measured preference remains stable across benchmark design choices and linguistic contexts.

## 3.3 Research Questions

The methodology is guided by the following research questions:

**RQ1:** How can occupational gender bias be measured in Arabic causal language models using masculine–feminine counterfactual sentence pairs?

**RQ2:** Do Arabic-specific and multilingual causal language models show different occupational gender-preference patterns?

**RQ3:** Is measured gender preference stable across templates, dialects, semantic frames, job-title contexts, departments, and job-role contexts?

**RQ4:** Do real-world Arabic job-advertisement contexts produce different measured gender-preference patterns from controlled benchmark contexts?

**RQ5:** Can counterfactual data augmentation reduce measured occupational gender preference in Arabic causal language models?

## 3.4 Benchmark Suite Design

The benchmark suite consists of multiple benchmark versions, each designed to test a different aspect of Arabic occupational gender-bias measurement. The purpose of using multiple versions is to avoid relying on a single benchmark design and to evaluate the robustness of measured bias across different linguistic and occupational contexts.

### 3.4.1 v2 Main Validated Benchmark

The v2 benchmark is the main controlled benchmark. It contains 240 masculine–feminine counterfactual pairs generated from 60 occupations and four templates. The occupations are distributed across six occupational fields:

* STEM
* Healthcare
* Education
* Business
* Legal and Government
* Media and Creative

The v2 benchmark includes both Modern Standard Arabic and Egyptian Arabic templates. It serves as the primary baseline benchmark for six-model evaluation.

### 3.4.2 v4 Template Perturbation Benchmark

The v4 benchmark tests whether measured bias is stable across different templates and semantic frames. It expands the evaluation to 720 counterfactual pairs generated from 90 occupations and eight templates. These templates represent different semantic frames, including workplace presence, professional experience, leadership, competence, promotion, responsibility, and team dependency.

The purpose of v4 is to examine whether model preference changes when the occupation appears in different linguistic and professional contexts. This is important because a bias score may depend not only on the occupation, but also on how the occupation is framed.

### 3.4.3 v5 Job-Title Benchmark

The v5 benchmark isolates explicit job-title contexts. It contains 540 pairs generated from 90 occupations and six templates. The templates represent contexts such as CVs, job advertisements, HR records, and professional profiles.

This benchmark tests whether gender preference changes when the occupation appears as a formal job title rather than as part of a general sentence. This distinction is important for applications related to recruitment, employment platforms, and professional profiling.

### 3.4.4 v6 Expanded Job-Role and Department Benchmark

The v6 benchmark expands the framework beyond simple occupational titles. It contains 2,880 counterfactual pairs generated from 120 structured job roles and 24 templates. These roles are distributed across 10 departments and include metadata such as job family, seniority level, job-role type, workplace context, semantic frame, and dialect.

The v6 benchmark strengthens the framework by introducing a more realistic labor-market structure. Instead of evaluating only isolated occupations, it evaluates gender preference across job roles, departments, professional responsibilities, workplace settings, and role seniority.

### 3.4.5 ArabJobs v7 External Real-World Benchmark

The ArabJobs v7 benchmark extends the evaluation to real-world Arabic job-advertisement contexts. It is derived from the ArabJobs corpus by matching real job-ad data to the project’s occupational and job-role lexicon, then generating controlled masculine–feminine counterfactual pairs from matched contexts.

The purpose of this benchmark is external validation. While the controlled benchmarks test model behavior under designed experimental conditions, ArabJobs v7 tests whether the framework can be applied to real-world recruitment-language data. This allows the thesis to compare controlled benchmark results with results derived from naturally occurring Arabic job advertisements.

## 3.5 Counterfactual Pair Construction

Each benchmark item consists of a masculine sentence and a feminine sentence:

`(x_i^m, x_i^f)`

where `x_i^m` is the masculine Arabic sentence and `x_i^f` is the feminine Arabic counterfactual sentence.

The pair construction follows three principles:

First, the two sentences must preserve the same meaning. The occupational context, template, semantic frame, and professional situation should remain constant.

Second, the gendered occupational form must change. For example, a masculine form such as `طبيب` is paired with the feminine form `طبيبة`.

Third, the surrounding sentence must be grammatically adjusted where necessary. Arabic grammatical gender may affect demonstratives, verbs, adjectives, or agreement markers. Therefore, counterfactual construction must account for Arabic morphology and syntax rather than simply replacing one word.

An example pair is:

Masculine sentence:

`هذا الطبيب يعمل في المستشفى.`

Feminine sentence:

`هذه الطبيبة تعمل في المستشفى.`

The meaning is preserved, while the gendered occupational form and agreement markers are changed.

## 3.6 Dialect-Aware Design

Arabic presents a methodological challenge because bias measurement may differ across Modern Standard Arabic and dialectal Arabic. This thesis includes both Modern Standard Arabic and Egyptian Arabic templates to test dialect sensitivity.

Modern Standard Arabic templates represent formal contexts such as written professional records, official descriptions, and standard workplace statements. Egyptian Arabic templates represent more colloquial or locally natural forms of occupational expression.

By including both dialect types, the framework tests whether gender preference is stable across Arabic varieties. This is important because Arabic language models may be trained on mixtures of formal, dialectal, and web-based Arabic data, and their behavior may differ depending on dialectal context.

## 3.7 Scoring Method

The project evaluates open-weight causal language models. A causal language model estimates the probability of a token given the previous tokens. For a sentence:

`x = (w_1, w_2, ..., w_n)`

the sentence score is defined as the average token log-probability:

`S(x) = (1 / n) * sum log P(w_t | w_<t)`

where `n` is the number of tokens in the sentence, and `P(w_t | w_<t)` is the probability assigned by the model to token `w_t` given the preceding context.

Average token log-probability is used instead of total sentence probability to reduce the effect of sentence length. This is important because Arabic masculine and feminine variants may differ slightly in tokenization or surface form. Normalizing by token count makes the sentence-level score more comparable across paired variants.

## 3.8 Pairwise Score Difference

For each counterfactual pair, the score difference is computed as:

`Delta_i = S(x_i^m) - S(x_i^f)`

This is implemented in the project as:

`score_difference = masculine_score - feminine_score`

The interpretation is:

* `Delta_i > 0`: the model assigns higher likelihood to the masculine sentence.
* `Delta_i < 0`: the model assigns higher likelihood to the feminine sentence.
* `Delta_i = 0`: the model assigns equal likelihood to both variants.

This directional score is the main metric used throughout the thesis.

## 3.9 Benchmark-Level Bias Metrics

For a benchmark with `N` counterfactual pairs, the average directional bias is computed as:

`Bias_avg = (1 / N) * sum Delta_i`

This metric indicates the overall direction of model preference across the benchmark. A positive value indicates an overall masculine preference, while a negative value indicates an overall feminine preference.

The framework also computes absolute disparity:

`Disparity_abs = (1 / N) * sum |Delta_i|`

This metric measures the magnitude of preference regardless of direction. It is useful because a model may have near-zero average bias if masculine and feminine preferences cancel each other out, while still showing strong pair-level disparities.

The framework also reports preference rates:

`R_m = number of masculine-preferred pairs / N`

`R_f = number of feminine-preferred pairs / N`

`R_e = number of equal-preference pairs / N`

These rates provide an interpretable count-based summary of how often each model prefers masculine, feminine, or equal variants.

## 3.10 Model Selection

The evaluation uses open-weight causal language models that allow access to token-level likelihood or loss values. The model set includes Arabic-specific and multilingual causal language models. The Arabic-specific models include AraGPT2 variants, while the multilingual models include BLOOM, XGLM, and Qwen variants.

The purpose of including both Arabic-specific and multilingual models is to compare whether model family and training orientation affect measured occupational gender preference. Arabic-specific models may encode Arabic morphology more directly, while multilingual models may reflect broader multilingual training distributions.

The main model categories are:

* Arabic-specific causal language models
* Multilingual causal language models
* General multilingual models with Arabic coverage

This model selection supports model-level and model-family-level comparison.

## 3.11 Experimental Procedure

The experimental procedure consists of the following steps:

1. Load a benchmark CSV file containing masculine and feminine sentence pairs.

2. Load the selected causal language model and tokenizer.

3. Score each masculine sentence using average token log-probability.

4. Score each feminine sentence using average token log-probability.

5. Compute `score_difference` as `masculine_score - feminine_score`.

6. Assign the preferred gender label based on the sign of `score_difference`.

7. Save row-level scoring outputs.

8. Aggregate results by model, benchmark, field, dialect, template, semantic frame, department, job family, and other available metadata.

9. Apply statistical, robustness, and validation analyses.

This procedure is repeated across benchmark versions and models.

## 3.12 Validation Procedures

The framework includes several validation procedures to strengthen reliability and reproducibility.

### 3.12.1 Benchmark Quality Validation

Benchmark quality scripts check whether required columns exist, whether sentence fields are empty, whether template and dialect distributions are present, and whether benchmark sizes match expected values. These checks ensure that each benchmark version is structurally valid before model scoring.

### 3.12.2 Formula Validation

The formula validation procedure confirms that the mathematical definition of the score is consistently applied. It verifies that each row-level `score_difference` equals `masculine_score - feminine_score`.

It also verifies that the preferred gender label matches the sign of the score difference. This ensures alignment between the theoretical formula, implementation, and interpretation.

### 3.12.3 Score-Difference Implementation Validation

The implementation validation script recomputes score differences across scoring output files and checks for formula errors or preference-label errors. This prevents accidental inconsistencies in output files and confirms that the scoring pipeline implements the metric correctly.

### 3.12.4 Token-Length Control

The token-length control analysis examines whether score differences are likely to be driven by surface-level sentence-length differences. The analysis compares masculine and feminine sentence lengths and estimates the relationship between length differences and score differences.

This control is important because Arabic gendered forms can differ in length or tokenization. Since the main score uses average token log-probability, the method already reduces length effects, but the token-length control adds an additional robustness check.

### 3.12.5 Human Validation

The project includes a human-validation package. A stratified sample of 500 counterfactual pairs is drawn from the main benchmark, template-perturbation benchmark, job-title benchmark, expanded job-role benchmark, and ArabJobs external benchmark.

Two annotators evaluate each pair using the following dimensions:

* grammaticality
* meaning preservation
* gender-form correctness
* dialect correctness
* job-title correctness
* keep/review/remove decision

The analysis reports percentage agreement and Cohen’s Kappa. Human validation strengthens the reliability of the benchmark by showing that the counterfactual pairs are linguistically and semantically acceptable.

### 3.12.6 Final Project Audit

A final audit script checks the presence and validity of datasets, scripts, result files, documentation files, software files, validation reports, mitigation outputs, and Git tracking status. This ensures that the project is reproducible and complete before thesis submission and paper preparation.

## 3.13 Statistical Analysis

The analysis includes descriptive and inferential components.

Descriptive analysis reports:

* total benchmark items
* masculine-preferred count
* feminine-preferred count
* equal-preference count
* masculine-preferred percentage
* feminine-preferred percentage
* equal-preference percentage
* average score difference
* median score difference
* minimum and maximum score difference

Statistical testing is used to examine associations between preferred gender and factors such as model name, model family, template, semantic frame, dialect, field, and stereotype label. Chi-square tests are used where appropriate to evaluate whether preference distributions differ significantly across categorical variables.

Effect-size analysis is also used to interpret the practical strength of associations. Cramér’s V is used to summarize the strength of categorical associations. This is important because statistical significance alone may be influenced by large sample size; effect sizes help interpret how strong the observed association is.

The Q1-oriented robustness analysis also includes factor sensitivity analysis. This analysis compares the range of average score differences across factor levels, such as template type, semantic frame, dialect, department, job family, and dataset source. Larger ranges indicate stronger sensitivity of measured bias to that factor.

## 3.14 Cross-Benchmark Robustness Analysis

A central methodological aim is to determine whether occupational gender bias is a stable property of a model or a context-dependent measurement outcome. To test this, the framework compares results across benchmark versions.

The cross-benchmark analysis examines whether each model’s direction of preference changes across:

* v2 main benchmark
* v4 template perturbation benchmark
* v5 job-title benchmark
* v6 expanded job-role benchmark
* ArabJobs v7 external benchmark

If a model shows masculine preference in one benchmark and feminine preference in another, this indicates that measured bias is sensitive to benchmark design and context. This analysis supports the thesis argument that Arabic occupational gender-bias evaluation should not rely on a single template or dataset.

## 3.15 External Real-World Evaluation

The ArabJobs v7 evaluation extends the framework beyond controlled synthetic templates. Real-world job-advertisement data is matched to the project’s occupational and job-role lexicon. Matched rows are converted into masculine–feminine counterfactual pairs while preserving relevant metadata such as country, job category, subcategory, profession, and original job-title context.

The purpose is not to claim that the external dataset is perfectly controlled. Instead, it provides an additional real-world evaluation layer. Comparing controlled benchmark results with ArabJobs-derived results helps determine whether measured gender preference changes in recruitment-language contexts.

This strengthens ecological validity because occupational bias is especially relevant in job advertisements, recruitment systems, and employment-related language technologies.

## 3.16 Bias Mitigation Experiment

The thesis also includes a counterfactual bias-mitigation experiment. The purpose is to test whether balanced masculine–feminine occupational data can reduce measured gender preference.

The mitigation procedure consists of:

1. Constructing balanced training data from masculine and feminine occupational counterfactual sentences.

2. Fine-tuning AraGPT2-base on the balanced counterfactual data.

3. Re-scoring the same benchmarks using the mitigated model.

4. Comparing bias scores before and after mitigation.

The main mitigation metric is:

`Mitigation_Gain = |Bias_before| - |Bias_after|`

A positive mitigation gain indicates that the absolute directional bias decreased after fine-tuning. A zero value indicates no change, and a negative value indicates that measured bias increased.

The mitigation experiment does not claim to remove bias completely. Instead, it evaluates whether one counterfactual data augmentation intervention reduces measured occupational gender preference under the proposed scoring framework.

## 3.17 Software Implementation Method

The project includes an interactive software tool for measuring Arabic occupational gender bias. The software supports three modes:

1. measuring one masculine–feminine sentence pair,
2. measuring an uploaded CSV file,
3. measuring existing project benchmarks.

The software uses the validated command-line scoring pipeline as its backend. Users can input Arabic sentence pairs, select a causal language model, calculate masculine and feminine scores, compute `score_difference`, classify preferred gender, visualize the result, and export the output as CSV.

The project also includes a dashboard for inspecting datasets, model results, validation reports, robustness analyses, cross-benchmark comparisons, and software outputs. This software layer strengthens reproducibility and makes the evaluation framework easier to demonstrate, audit, and extend.

## 3.18 Ethical Considerations

This thesis evaluates gender bias in language models and therefore requires careful interpretation. The work does not claim that model likelihood scores directly represent social beliefs or real-world discrimination. Instead, they are treated as measurable indicators of model preference under controlled linguistic conditions.

The thesis also avoids claiming that bias can be fully eliminated. The proposed system measures, validates, analyzes, and supports bias limitation. The mitigation experiment is presented as an experimental intervention, not as proof that a model is safe or unbiased.

For external data, the project distinguishes between original raw datasets and derived evaluation artifacts. Raw external datasets should only be redistributed when licensing allows it. Derived benchmark pairs and metadata are used as research artifacts for reproducible evaluation.

Human validation is included to reduce the risk of invalid Arabic sentences, incorrect gender forms, or unnatural dialectal constructions affecting the results.

## 3.19 Reproducibility

The full project is organized as a reproducible software repository. It includes:

* benchmark datasets,
* scoring scripts,
* analysis scripts,
* validation scripts,
* human-validation files,
* mitigation scripts,
* software tools,
* documentation,
* run instructions,
* final audit reports.

The final audit confirms that the project files required for thesis submission and Q1 paper preparation are present and structurally valid. The repository therefore supports replication of the benchmark construction, scoring process, analysis outputs, validation checks, software execution, and mitigation experiment.

## 3.20 Chapter Summary

This chapter presented the methodology of the proposed Arabic occupational gender-bias evaluation framework. The framework uses masculine–feminine counterfactual sentence pairs, average token log-probability scoring, directional score differences, benchmark-level aggregation, statistical analysis, validation checks, external real-world evaluation, software implementation, and a mitigation experiment.

The methodology is designed to show that Arabic occupational gender-bias measurement is not simply a property of a model. Instead, it is affected by model family, template formulation, dialect, semantic frame, job-title context, department, job-role structure, and real-world recruitment-language context. This methodological design provides the foundation for the implementation and results presented in the following chapters.
