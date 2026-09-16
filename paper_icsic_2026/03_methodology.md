# 3. Methodology

## 3.1 Overview

This section presents the methodology used to measure occupational gender bias in Arabic causal language models. The proposed method is based on masculine–feminine counterfactual sentence pairs. Each pair preserves the same occupational meaning while changing the gendered linguistic form and the required Arabic grammatical agreement.

The methodology has four main components:

1. constructing Arabic occupational counterfactual benchmarks,
2. scoring sentence pairs using causal language models,
3. computing directional gender preference using a score-difference metric,
4. analyzing robustness across models, templates, dialects, and occupational contexts.

The goal is not only to determine whether a model prefers masculine or feminine occupational forms, but also to test whether this preference remains stable across different benchmark settings.

## 3.2 Counterfactual Benchmark Design

Each benchmark item contains two Arabic sentences:

```text id="v40lrp"
masculine_sentence
feminine_sentence
```

The masculine sentence uses a masculine occupational form, and the feminine sentence uses the corresponding feminine occupational form. The two sentences are designed to preserve the same semantic meaning.

For example:

```text id="cdq9ka"
Masculine: هذا الطبيب يعمل في المستشفى.
Feminine: هذه الطبيبة تعمل في المستشفى.
```

The pair changes the occupational noun from `الطبيب` to `الطبيبة` and changes the demonstrative from `هذا` to `هذه`. This is necessary because Arabic grammatical gender affects agreement. A valid Arabic counterfactual pair must therefore modify all required gendered elements, not only the occupation word.

Each pair is constructed according to three criteria:

```text id="e00ueu"
1. The masculine and feminine variants preserve the same occupational meaning.
2. The gendered occupational form is changed correctly.
3. The surrounding sentence is grammatically adjusted where required.
```

## 3.3 Benchmark Versions

The study uses multiple benchmark versions to test robustness across linguistic and occupational contexts.

### 3.3.1 v2 Main Controlled Benchmark

The v2 benchmark is the main controlled benchmark. It contains 240 masculine–feminine counterfactual pairs generated from 60 occupations and four templates. The occupations cover six occupational fields, including STEM, healthcare, education, business, legal and government, and media/creative fields.

This benchmark provides the baseline controlled evaluation across Arabic-specific and multilingual causal language models.

### 3.3.2 v4 Template Perturbation Benchmark

The v4 benchmark tests template sensitivity. It contains 720 pairs generated from 90 occupations and eight templates. The templates cover different semantic frames, including workplace presence, professional experience, leadership, competence, promotion, responsibility, and team dependency.

The purpose of this benchmark is to test whether measured gender preference changes when the same occupation appears in different sentence formulations.

### 3.3.3 v5 Job-Title Benchmark

The v5 benchmark evaluates explicit job-title contexts. It contains 540 pairs generated from 90 occupations and six templates. The templates represent contexts such as CVs, job advertisements, HR records, and professional profiles.

This benchmark is included because job-title contexts are common in recruitment and employment-related NLP applications.

### 3.3.4 v6 Expanded Job-Role Benchmark

The v6 benchmark expands the evaluation beyond simple occupation names. It contains 2,880 pairs generated from 120 structured job roles and 24 templates. The benchmark includes metadata such as department, field, job family, seniority level, job-role type, workplace context, template type, semantic frame, and dialect.

This benchmark tests whether occupational gender preference changes across more detailed professional and organizational contexts.

### 3.3.5 ArabJobs v7 External Benchmark

The ArabJobs v7 benchmark extends the evaluation to real-world recruitment-language contexts. It is derived from matched ArabJobs job-advertisement data and converted into controlled masculine–feminine counterfactual pairs. The benchmark contains 14,532 pairs and preserves metadata such as country, original gender label, job category, subcategory, profession, and original job-title context.

This benchmark is used as an external validation layer to compare controlled benchmark results with real-world job-advertisement contexts.

## 3.4 Dialect-Aware Design

The benchmark includes both Modern Standard Arabic and Egyptian Arabic templates. Modern Standard Arabic is used for formal and professional contexts, while Egyptian Arabic is used to represent a common dialectal variety.

This dialect-aware design is necessary because Arabic language models may behave differently across Arabic varieties. A model trained on mixed Arabic data may assign different likelihoods to MSA and dialectal sentence forms. Therefore, the evaluation reports dialect-level results rather than assuming that Arabic is a single homogeneous input variety.

## 3.5 Model Scoring

The evaluation uses open-weight causal language models. A causal language model estimates the probability of each token given the preceding tokens. For a sentence:

```text id="24jmz2"
x = (w_1, w_2, ..., w_n)
```

the sentence score is defined as the average token log-probability:

```text id="8tk81c"
S(x) = (1 / n) * Σ log P(w_t | w_<t)
```

where `n` is the number of tokens in the sentence and `P(w_t | w_<t)` is the probability assigned to token `w_t` given the previous tokens.

Average token log-probability is used instead of total sentence probability to reduce the effect of sentence length. This is important because Arabic masculine and feminine variants may differ in surface form or tokenization.

## 3.6 Score-Difference Metric

For each masculine–feminine pair, the score difference is computed as:

```text id="81i9y0"
score_difference = masculine_score - feminine_score
```

The interpretation is:

```text id="025dy2"
score_difference > 0  → masculine preference
score_difference < 0  → feminine preference
score_difference = 0  → equal preference
```

This score provides a directional measure of model preference. It is computed for each benchmark item and then aggregated across models, templates, dialects, fields, departments, semantic frames, and benchmark versions.

## 3.7 Aggregation Metrics

For each model and benchmark, the following metrics are reported:

```text id="u75e0q"
total_items
masculine_preferred_count
feminine_preferred_count
equal_count
masculine_preferred_percent
feminine_preferred_percent
equal_percent
average_score_difference
median_score_difference
minimum_score_difference
maximum_score_difference
```

The average score difference is used as the main directional benchmark-level bias score. Preference counts and percentages are also reported to make the results easier to interpret.

## 3.8 Experimental Procedure

The experimental procedure follows these steps:

```text id="qhh4kc"
1. Load the benchmark CSV file.
2. Load the selected causal language model and tokenizer.
3. Score each masculine sentence using average token log-probability.
4. Score each feminine sentence using average token log-probability.
5. Compute score_difference as masculine_score - feminine_score.
6. Assign the preferred-gender label based on the sign of score_difference.
7. Save row-level scoring outputs.
8. Aggregate results by model, benchmark, field, dialect, template, semantic frame, department, and job-role metadata.
9. Compare results across benchmark versions to identify robustness and direction changes.
```

## 3.9 Validation and Quality Control

The project includes validation and quality-control checks to reduce the risk of implementation errors.

First, benchmark quality checks verify required columns, row counts, sentence completeness, dialect labels, template distributions, and metadata fields.

Second, score-difference validation checks that the stored score difference is correctly computed as:

```text id="khe0ss"
masculine_score - feminine_score
```

Third, preference-label validation checks that the preferred-gender label matches the sign of the score difference.

Fourth, token-length control checks whether masculine and feminine sentence variants have balanced word counts. This helps determine whether measured preferences are caused by linguistic context rather than simple word-count imbalance.

The wider project also includes a human-validation package and a bias-mitigation experiment. For the conference paper, these are treated as supplementary components supporting the reproducibility and extensibility of the framework.

## 3.10 Software Pipeline

The methodology is implemented as a reproducible Python pipeline. The scoring script takes an input benchmark file, model name, and output directory, then produces sentence-level and aggregate results. The analysis scripts generate summaries by model, field, dialect, template, semantic frame, department, job family, and benchmark source.

The project also includes a Streamlit-based bias measurement application and a dashboard. The software allows users to enter one sentence pair, upload CSV files, score benchmark datasets, visualize results, and export outputs. This software layer makes the benchmark easier to inspect, reproduce, and extend.

## 3.11 Summary

This methodology combines Arabic counterfactual benchmark construction, dialect-aware design, causal language model scoring, score-difference analysis, robustness evaluation, validation checks, and software implementation. The next section reports the experimental results across controlled benchmarks, expanded job-role contexts, and real-world ArabJobs-derived recruitment-language data.
