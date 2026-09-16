# Measuring Occupational Gender Bias in Arabic Causal Language Models Using a Dialect-Aware Counterfactual Benchmark

## Abstract

Occupational gender bias in language models can affect applications related to recruitment, professional profiling, job-advertisement generation, and Arabic natural language processing systems. Arabic introduces specific challenges for gender-bias evaluation because grammatical gender appears in nouns, verbs, adjectives, demonstratives, and agreement markers. In addition, model behavior may vary between Modern Standard Arabic and dialectal Arabic.

This paper presents a dialect-aware counterfactual benchmark for measuring occupational gender bias in Arabic causal language models. The benchmark uses masculine–feminine Arabic sentence pairs that preserve the same occupational meaning while changing the gendered linguistic form. Each sentence is scored using average token log-probability, and gender preference is measured using `score_difference`, defined as `masculine_score - feminine_score`. Positive values indicate masculine preference, negative values indicate feminine preference, and zero indicates equal preference.

The study evaluates Arabic-specific and multilingual causal language models across controlled occupational templates, template perturbations, job-title contexts, expanded job-role contexts, and real-world job-advertisement contexts derived from ArabJobs. The results show that measured occupational gender preference is context-sensitive. Model preference changes across model family, template formulation, dialect, semantic frame, job-title context, job-role structure, and real-world recruitment-language setting. These findings suggest that Arabic occupational gender bias should not be treated as a fixed model property, but as a measurement outcome affected by linguistic and occupational framing.

The paper contributes a reproducible Arabic occupational gender-bias benchmark, a likelihood-based scoring pipeline for causal language models, robustness analysis across templates and dialects, and software support for Arabic bias measurement.

## Keywords

Arabic NLP; Large Language Models; Gender Bias; Occupational Bias; Causal Language Models; Counterfactual Evaluation; Arabic Dialects; Likelihood-Based Scoring; Fairness in NLP; Recruitment Language.

---

# 1. Introduction

Large Language Models (LLMs) are increasingly used in natural language processing applications that generate, classify, summarize, and evaluate text. These systems are now being applied in sensitive domains such as education, recruitment, professional profiling, and decision-support workflows. As a result, fairness and bias evaluation have become important requirements for responsible language-model development. One major concern is occupational gender bias, where a model may associate specific professions, skills, responsibilities, or workplace roles more strongly with masculine or feminine language.

Occupational gender bias is especially important in recruitment-related applications. Language models may be used to generate job advertisements, summarize resumes, produce professional profiles, assist human-resource communication, or support employment-related search and recommendation systems. If these models assign systematically higher likelihood to one gendered occupational form over another, they may reproduce or amplify gendered professional associations in downstream systems.

Arabic introduces specific challenges for gender-bias evaluation. Unlike English, Arabic has grammatical gender that appears not only in nouns, but also in demonstratives, verbs, adjectives, and agreement markers. Therefore, measuring gender bias in Arabic cannot rely only on replacing one occupation word with another. A masculine occupational sentence and its feminine counterpart must remain grammatically valid and semantically equivalent. For example, the masculine sentence `هذا الطبيب يعمل في المستشفى` must be paired with the feminine sentence `هذه الطبيبة تعمل في المستشفى`, where both the occupational noun and the demonstrative are adjusted. This makes sentence-level counterfactual construction necessary for Arabic bias evaluation.

Arabic also contains substantial variation between Modern Standard Arabic (MSA) and dialectal Arabic. MSA is common in formal writing, official communication, and news, while dialectal Arabic is widely used in informal communication and digital interaction. Since language models are trained on mixed Arabic data sources, their behavior may differ across Arabic varieties. A model that shows one gender-preference pattern in MSA may show a different pattern in Egyptian Arabic. Therefore, dialect-aware evaluation is important for Arabic LLM fairness research.

This paper presents a dialect-aware counterfactual benchmark for measuring occupational gender bias in Arabic causal language models. The benchmark consists of masculine–feminine Arabic sentence pairs that preserve the same occupational meaning while changing the gendered linguistic form. The evaluation uses open-weight causal language models and computes the average token log-probability of each sentence. For each pair, the directional gender-preference score is calculated as:

`score_difference = masculine_score - feminine_score`

A positive score difference indicates that the model assigns higher likelihood to the masculine sentence. A negative value indicates higher likelihood for the feminine sentence. A zero value indicates equal preference.

The benchmark is designed not only to measure model-level bias, but also to test whether measured bias is stable across linguistic and occupational contexts. The evaluation includes controlled occupational templates, template perturbations, job-title contexts, expanded job-role and department contexts, and real-world Arabic job-advertisement contexts derived from ArabJobs. The model set includes Arabic-specific and multilingual causal language models.

The results show that Arabic occupational gender-bias scores are context-sensitive. In the main controlled benchmark, Arabic-specific models and multilingual models show different gender-preference patterns. In the template-perturbation benchmark, models can change direction across templates and semantic frames. In the expanded job-role benchmark, occupational context and professional framing affect the measured score. In the real-world job-advertisement setting, measured preference can differ from controlled benchmark results. These findings suggest that Arabic occupational gender bias should not be treated as a fixed model property. Instead, it should be interpreted as a measurement outcome affected by model family, template wording, dialect, semantic frame, job-title context, job-role structure, and recruitment-language setting.

The main contributions of this paper are as follows:

1. It introduces a dialect-aware Arabic occupational gender-bias benchmark based on masculine–feminine counterfactual sentence pairs.

2. It applies likelihood-based scoring to Arabic causal language models using average token log-probability and a directional `score_difference` metric.

3. It evaluates Arabic-specific and multilingual models across controlled templates, dialects, job-title contexts, expanded job-role contexts, and real-world recruitment-language data.

4. It shows that measured Arabic occupational gender bias is context-sensitive and can change direction across templates, dialects, and benchmark settings.

5. It provides a reproducible software-supported pipeline for scoring, analyzing, and inspecting Arabic occupational gender-bias results.

The rest of the paper is organized as follows. Section 2 reviews related work on language-model bias evaluation, counterfactual benchmarks, likelihood-based scoring, Arabic NLP bias, and occupational gender bias. Section 3 presents the benchmark construction and scoring methodology. Section 4 reports the experimental setup and results. Section 5 discusses the findings, limitations, and implications. Section 6 concludes the paper and outlines future work.

---

# 2. Related Work

## 2.1 Bias Evaluation in Language Models

Bias evaluation has become an important research area in natural language processing because language models can encode social associations learned from training data. These associations may appear in generated text, sentence likelihoods, word representations, or downstream system behavior. Gender bias is one of the most widely studied forms of bias, especially in occupational contexts where models may associate certain professions or professional attributes more strongly with men or women.

Early studies focused on static word embeddings and showed that vector representations can encode gender stereotypes. Bolukbasi et al. demonstrated that word embeddings contain occupational gender associations and proposed methods for quantifying and reducing gender stereotypes in embedding spaces. Although embedding-based methods are useful for identifying lexical associations, they are limited for sentence-level evaluation because modern language models are contextual and generative.

As language models became more complex, bias evaluation moved toward contextual and benchmark-based methods. These methods use designed examples to measure whether a model prefers a stereotypical or gendered variant over an alternative. This direction is relevant to the present work because occupational bias in Arabic cannot be measured reliably using isolated word pairs only. Arabic gender marking interacts with sentence-level morphology and agreement, so full-sentence evaluation is required.

## 2.2 Paired-Sentence and Counterfactual Benchmarks

Paired-sentence benchmarks compare two sentences that are minimally different while preserving the same general structure. This design is useful for bias evaluation because it isolates the effect of the target attribute. CrowS-Pairs is one of the most influential examples of this approach. It measures social biases in language models using sentence pairs that differ in stereotypical association. StereoSet also evaluates stereotypical bias in pretrained language models by comparing stereotypical, anti-stereotypical, and unrelated alternatives.

The present work follows the paired-comparison logic of these benchmarks but adapts it to Arabic occupational gender bias. Instead of comparing general stereotypical statements, this paper compares masculine and feminine Arabic occupational sentence pairs. The goal is to determine whether a causal language model assigns higher likelihood to the masculine or feminine variant.

Counterfactual evaluation is central to this approach. In a counterfactual pair, the main semantic content remains constant while a target attribute changes. For occupational gender bias, the target attribute is the gendered form of the occupation and any required grammatical agreement. This is especially important for Arabic because a valid masculine–feminine transformation may require changes to multiple words in the sentence.

## 2.3 Likelihood-Based Bias Scoring

Likelihood-based scoring evaluates which sentence variant a language model considers more probable. This is useful for open-weight causal language models because token-level likelihood or language-modeling loss can be computed directly. Probability-based approaches have been used in prior work to measure bias in contextualized representations and language models.

Kurita et al. studied bias in contextualized word representations using probability-based measures. Kaneko and Bollegala argued that masked-token bias metrics can be problematic and proposed All Unmasked Likelihood as an alternative for evaluating social biases in masked language models. Salazar et al. introduced masked language model scoring for sentence-level likelihood estimation. These works support the broader idea that likelihood-based scoring can be used to evaluate model preference between sentence variants.

This paper applies likelihood-based scoring to Arabic causal language models. Each sentence is scored using average token log-probability. For each masculine–feminine pair, the score difference is computed as:

`score_difference = masculine_score - feminine_score`

This metric provides a directional measure of gender preference. Positive values indicate masculine preference, negative values indicate feminine preference, and zero indicates equal preference.

## 2.4 Arabic NLP and Gender Bias

Arabic presents specific challenges for NLP because of its morphology, grammatical gender, and dialectal diversity. Gender is not limited to pronouns or isolated nouns. It can appear in occupational nouns, demonstratives, verbs, adjectives, and agreement markers. As a result, Arabic gender-bias evaluation requires sentence-level control.

For example, the masculine sentence:

`هذا الطبيب يعمل في المستشفى`

must be paired with the feminine sentence:

`هذه الطبيبة تعمل في المستشفى`

The transformation changes both the demonstrative and the occupational noun. If the agreement structure is not preserved, the feminine sentence may become unnatural or grammatically incorrect. This would make the bias score unreliable because the model may penalize the sentence for linguistic invalidity rather than gender preference.

Recent Arabic bias work has started to address Arabic-specific evaluation. Studies on Arabic pretrained language models, Arabic embedding bias, and Arabic demographic-bias benchmarks show that bias evaluation must be adapted to Arabic linguistic and cultural contexts. However, more work is needed on occupational gender bias in Arabic causal language models, especially using full-sentence likelihood-based counterfactual evaluation.

## 2.5 Dialect-Aware Evaluation

Arabic is not a single uniform variety in practical NLP use. Modern Standard Arabic is used in formal writing, official communication, news, and education, while dialectal Arabic is common in informal communication, social media, and local digital interaction. Language models trained on mixed Arabic corpora may therefore behave differently across Arabic varieties.

Dialect-aware evaluation is important because a model that appears to show one bias pattern in MSA may behave differently in Egyptian Arabic or another dialect. This paper includes both MSA and Egyptian Arabic templates to test whether measured occupational gender preference is stable across Arabic varieties.

This dialect-aware design is one of the main differences between this work and many general bias benchmarks. Rather than treating Arabic as a single homogeneous language, the benchmark evaluates whether dialectal context affects model preference.

## 2.6 Occupational Gender Bias and Recruitment Contexts

Occupational gender bias is important because occupations are connected to education, employment, income, status, and professional opportunity. A model may associate technical, managerial, or leadership roles with masculine forms and care-related or administrative roles with feminine forms. These associations may affect downstream systems that generate or process professional text.

Recruitment language is a particularly relevant setting for occupational bias. Language models may be used to write job advertisements, summarize CVs, generate professional biographies, classify job roles, or assist with HR communication. Therefore, evaluation should include not only general occupational templates but also job-title and job-advertisement contexts.

This paper includes job-title templates and real-world job-advertisement contexts derived from ArabJobs. The purpose is to compare controlled benchmark results with recruitment-language settings. This helps evaluate whether model behavior changes when the occupation appears in contexts closer to real employment applications.

## 2.7 Bias Mitigation

Bias mitigation aims to reduce undesirable model behavior. Counterfactual Data Augmentation is a common mitigation strategy in which balanced examples are added to training or fine-tuning data. This strategy is especially relevant for morphologically rich languages because gender transformations must preserve grammatical correctness.

For Arabic, counterfactual mitigation must account for occupational forms and agreement markers. A simple word swap may not produce a valid sentence. Therefore, balanced masculine–feminine Arabic occupational sentence pairs can support both evaluation and mitigation.

Although the main focus of this conference paper is benchmark-based measurement and robustness analysis, the wider project also includes a counterfactual data augmentation mitigation experiment. This demonstrates how the benchmark suite can be used not only to measure bias, but also to test whether bias-limitation methods reduce measured preference.

## 2.8 Research Gap

Prior work provides strong foundations for bias evaluation, including paired-sentence benchmarks, likelihood-based scoring, counterfactual evaluation, and mitigation methods. However, several gaps remain for Arabic occupational gender-bias evaluation.

First, many existing benchmarks were designed primarily for English or for general social-bias categories. They do not directly address Arabic grammatical gender and sentence-level agreement.

Second, Arabic bias studies remain limited compared with English. More work is needed on Arabic causal language models and full-sentence likelihood-based evaluation.

Third, many studies report model-level bias scores without testing whether the score is stable across templates, dialects, semantic frames, job-title contexts, and real-world recruitment-language data.

Fourth, Arabic recruitment-language evaluation remains underexplored, even though occupational bias is directly relevant to job advertisements and HR-related NLP systems.

This paper addresses these gaps by introducing a dialect-aware Arabic occupational counterfactual benchmark and evaluating Arabic-specific and multilingual causal language models across controlled templates, template perturbations, job-title contexts, expanded job-role contexts, and real-world job-advertisement contexts.

---

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

---

# 4. Experiments and Results

## 4.1 Experimental Setup

The experiments evaluate occupational gender preference in Arabic causal language models using masculine–feminine counterfactual sentence pairs. Each pair contains two Arabic sentences with the same occupational meaning, where one sentence uses the masculine form and the other uses the feminine form. The models are scored using average token log-probability, and gender preference is measured using:

`score_difference = masculine_score - feminine_score`

A positive value indicates masculine preference, a negative value indicates feminine preference, and zero indicates equal preference.

The evaluation includes Arabic-specific and multilingual causal language models. The main evaluated models are:

| Model                     | Model Type                     |
| ------------------------- | ------------------------------ |
| aubmindlab/aragpt2-base   | Arabic-specific causal LM      |
| aubmindlab/aragpt2-medium | Arabic-specific causal LM      |
| bigscience/bloom-560m     | Multilingual causal LM         |
| bigscience/bloom-1b1      | Multilingual causal LM         |
| facebook/xglm-564M        | Multilingual causal LM         |
| Qwen/Qwen2.5-0.5B         | Multilingual/general causal LM |

The experiments are organized across multiple benchmark settings:

| Benchmark   | Description                                     | Number of Pairs |
| ----------- | ----------------------------------------------- | --------------: |
| v2          | Main controlled occupational benchmark          |             240 |
| v4          | Template perturbation benchmark                 |             720 |
| v5          | Job-title benchmark                             |             540 |
| v6          | Expanded job-role and department benchmark      |           2,880 |
| ArabJobs v7 | External real-world job-advertisement benchmark |          14,532 |

This design allows the study to compare model behavior across controlled templates, dialect-aware examples, job-title contexts, expanded job-role contexts, and real-world recruitment-language data.

## 4.2 v2 Main Controlled Benchmark

The v2 benchmark contains 240 counterfactual sentence pairs generated from 60 occupations and four templates. It provides the main controlled baseline for comparing Arabic-specific and multilingual causal language models.

The overall v2 results are shown in Table 1.

**Table 1. Overall results on the v2 main benchmark**

| Model                     | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Direction |
| ------------------------- | ------------------: | -----------------: | ----: | -----------------------: | --------- |
| Qwen/Qwen2.5-0.5B         |                  80 |                158 |     2 |                   -0.343 | Feminine  |
| aubmindlab/aragpt2-base   |                 152 |                 88 |     0 |                    0.126 | Masculine |
| aubmindlab/aragpt2-medium |                 168 |                 72 |     0 |                    0.223 | Masculine |
| bigscience/bloom-1b1      |                  91 |                147 |     2 |                   -0.166 | Feminine  |
| bigscience/bloom-560m     |                  83 |                157 |     0 |                   -0.217 | Feminine  |
| facebook/xglm-564M        |                  92 |                148 |     0 |                   -0.214 | Feminine  |

The v2 benchmark shows a clear difference between Arabic-specific and multilingual models. The Arabic-specific AraGPT2 models show masculine preference, while the multilingual models show feminine preference. AraGPT2-medium has the strongest masculine average score difference at 0.223, while Qwen/Qwen2.5-0.5B has the strongest feminine average score difference at -0.343.

At the model-family level, the Arabic-specific models produce 320 masculine preferences and 160 feminine preferences, with an average score difference of 0.174. The non-Arabic-specific multilingual models produce 346 masculine preferences, 610 feminine preferences, and 4 equal preferences, with an average score difference of -0.235.

A chi-square test shows a statistically significant association between model family and preferred gender:

`χ² = 118.109, p = 1.641 × 10^-27`

This indicates that the distribution of masculine and feminine preferences differs significantly between Arabic-specific and multilingual model families in the v2 benchmark.

## 4.3 v4 Template Perturbation Benchmark

The v4 benchmark evaluates whether measured gender preference is stable across template wording and semantic framing. It contains 720 pairs generated from 90 occupations and eight templates.

The overall v4 results are shown in Table 2.

**Table 2. Overall results on the v4 template perturbation benchmark**

| Model                     | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Direction |
| ------------------------- | ------------------: | -----------------: | ----: | -----------------------: | --------- |
| Qwen/Qwen2.5-0.5B         |                 312 |                390 |    18 |                   -0.089 | Feminine  |
| aubmindlab/aragpt2-base   |                 220 |                500 |     0 |                   -0.348 | Feminine  |
| aubmindlab/aragpt2-medium |                 290 |                430 |     0 |                   -0.303 | Feminine  |
| bigscience/bloom-1b1      |                 248 |                467 |     5 |                   -0.170 | Feminine  |
| bigscience/bloom-560m     |                 256 |                460 |     4 |                   -0.170 | Feminine  |
| facebook/xglm-564M        |                 104 |                614 |     2 |                   -0.441 | Feminine  |

Unlike the v2 benchmark, all six models show overall feminine preference on v4. This is important because the Arabic-specific AraGPT2 models shift from masculine preference in v2 to feminine preference in v4. This result shows that benchmark formulation can change the measured direction of gender preference.

## 4.4 Template-Induced Direction Changes

The v4 benchmark also reveals that all evaluated models show direction changes across templates. This means that the same model can prefer masculine variants in some templates and feminine variants in others.

**Table 3. Template direction changes in v4**

| Model                     | Masculine-Direction Templates | Feminine-Direction Templates | Direction Change | Range of Template Means |
| ------------------------- | ----------------------------: | ---------------------------: | ---------------- | ----------------------: |
| Qwen/Qwen2.5-0.5B         |                             4 |                            4 | Yes              |                   1.105 |
| aubmindlab/aragpt2-base   |                             2 |                            6 | Yes              |                   1.320 |
| aubmindlab/aragpt2-medium |                             2 |                            6 | Yes              |                   1.223 |
| bigscience/bloom-1b1      |                             1 |                            7 | Yes              |                   1.363 |
| bigscience/bloom-560m     |                             2 |                            6 | Yes              |                   1.412 |
| facebook/xglm-564M        |                             1 |                            7 | Yes              |                   0.729 |

The largest template range is observed for BLOOM-560m, with a range of 1.412 across template means. AraGPT2-base also shows high template sensitivity, with a range of 1.320. These results show that template wording is one of the strongest factors affecting measured occupational gender preference.

## 4.5 Dialect Sensitivity

The v4 benchmark includes both Modern Standard Arabic and Egyptian Arabic templates. The dialect-level analysis shows that some models change direction or magnitude depending on the Arabic variety.

**Table 4. Dialect-level average score differences in v4**

| Model                     | MSA Average | Egyptian Average | Dialect Shift |
| ------------------------- | ----------: | ---------------: | ------------: |
| Qwen/Qwen2.5-0.5B         |      -0.336 |            0.158 |         0.493 |
| aubmindlab/aragpt2-base   |      -0.290 |           -0.407 |        -0.117 |
| aubmindlab/aragpt2-medium |      -0.191 |           -0.416 |        -0.225 |
| bigscience/bloom-1b1      |      -0.273 |           -0.067 |         0.207 |
| bigscience/bloom-560m     |      -0.394 |            0.053 |         0.447 |
| facebook/xglm-564M        |      -0.398 |           -0.485 |        -0.087 |

Qwen/Qwen2.5-0.5B and BLOOM-560m shift from feminine preference in MSA to masculine preference in Egyptian Arabic. This result supports the need for dialect-aware Arabic bias evaluation. A model’s behavior in MSA does not necessarily represent its behavior in dialectal Arabic.

## 4.6 v5 Job-Title Benchmark

The v5 benchmark evaluates explicit job-title contexts such as CVs, job advertisements, HR records, and professional profiles. It contains 540 counterfactual pairs.

**Table 5. Results on the v5 job-title benchmark**

| Model                   | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Direction            |
| ----------------------- | ------------------: | -----------------: | ----: | -----------------------: | -------------------- |
| aubmindlab/aragpt2-base |                 284 |                256 |     0 |                   -0.034 | Near-neutral / Mixed |
| bigscience/bloom-560m   |                 278 |                261 |     1 |                    0.071 | Weak Masculine       |

The v5 results differ from the v4 results. In v4, both AraGPT2-base and BLOOM-560m show feminine preference. In v5, AraGPT2-base becomes near-neutral, while BLOOM-560m shows weak masculine preference. This suggests that job-title contexts behave differently from general occupational sentence templates.

## 4.7 v6 Expanded Job-Role Benchmark

The v6 benchmark expands the evaluation to structured job roles and departments. It contains 2,880 pairs generated from 120 job roles and 24 templates. The benchmark includes metadata such as department, field, job family, seniority level, job-role type, workplace context, semantic frame, and dialect.

**Table 6. Results on the v6 expanded job-role benchmark**

| Model                     | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Direction            |
| ------------------------- | ------------------: | -----------------: | ----: | -----------------------: | -------------------- |
| aubmindlab/aragpt2-base   |                 970 |               1910 |     0 |                   -0.302 | Feminine             |
| aubmindlab/aragpt2-medium |                1136 |               1744 |     0 |                   -0.244 | Feminine             |
| bigscience/bloom-1b1      |                1328 |               1547 |     5 |                   -0.081 | Feminine             |
| bigscience/bloom-560m     |                1500 |               1375 |     5 |                   -0.016 | Near-neutral / Mixed |

The v6 benchmark shows mostly feminine or near-neutral patterns. AraGPT2-base and AraGPT2-medium both show feminine preference, which contrasts with their masculine preference in the v2 main benchmark. BLOOM-560m is close to neutral, with an average score difference of -0.016.

These results show that expanded occupational context changes the measured direction and magnitude of gender preference. Job roles, departments, professional responsibilities, and workplace framing are therefore important factors in Arabic occupational bias evaluation.

## 4.8 ArabJobs v7 External Real-World Benchmark

The ArabJobs v7 benchmark evaluates real-world Arabic job-advertisement contexts. It contains 14,532 counterfactual pairs derived from matched ArabJobs data.

**Table 7. AraGPT2-base result on ArabJobs v7**

| Model                   | Total Items | Masculine Preferred | Feminine Preferred | Average Score Difference | Direction |
| ----------------------- | ----------: | ------------------: | -----------------: | -----------------------: | --------- |
| aubmindlab/aragpt2-base |      14,532 |               8,404 |              6,128 |                    0.089 | Masculine |

AraGPT2-base shows masculine preference on ArabJobs v7, with 57.83% masculine-preferred pairs and 42.17% feminine-preferred pairs. The average score difference is 0.089.

This result contrasts with v6, where AraGPT2-base shows feminine preference with an average score difference of -0.302. The contrast suggests that real-world recruitment-language contexts can produce different gender-preference patterns from controlled benchmark contexts.

## 4.9 Controlled vs Real-World Comparison

The comparison between v6 and ArabJobs v7 is important because both are occupational and recruitment-related, but they differ in data source and linguistic naturalness.

**Table 8. AraGPT2-base comparison across controlled and external contexts**

| Benchmark                | Total Items | Average Score Difference | Direction            |
| ------------------------ | ----------: | -----------------------: | -------------------- |
| v2 main benchmark        |         240 |                    0.126 | Masculine            |
| v4 template perturbation |         720 |                   -0.348 | Feminine             |
| v5 job titles            |         540 |                   -0.034 | Near-neutral / Mixed |
| v6 job roles             |       2,880 |                   -0.302 | Feminine             |
| ArabJobs v7 external     |      14,532 |                    0.089 | Masculine            |

The same model changes direction across benchmark settings. AraGPT2-base is masculine-leaning in v2, feminine-leaning in v4, near-neutral in v5, feminine-leaning in v6, and masculine-leaning in ArabJobs v7. This confirms that measured gender preference is context-dependent.

## 4.10 Token-Length Control

A token-length control analysis was conducted to examine whether score differences could be explained by simple word-count differences between masculine and feminine sentence variants.

The analysis showed that masculine and feminine sentence variants had identical mean word counts in the v6 and ArabJobs v7 evaluated outputs.

**Table 9. Word-count control results**

| Dataset      | Model                     | Total Items | Mean Masculine Word Count | Mean Feminine Word Count | Same Word Count |
| ------------ | ------------------------- | ----------: | ------------------------: | -----------------------: | --------------: |
| ArabJobs v7  | aubmindlab/aragpt2-base   |      14,532 |                     8.669 |                    8.669 |          100.0% |
| ArabJobs v7  | bigscience/bloom-560m     |      14,532 |                     8.669 |                    8.669 |          100.0% |
| v6 job roles | aubmindlab/aragpt2-base   |       2,880 |                     8.625 |                    8.625 |          100.0% |
| v6 job roles | aubmindlab/aragpt2-medium |       2,880 |                     8.625 |                    8.625 |          100.0% |
| v6 job roles | bigscience/bloom-1b1      |       2,880 |                     8.625 |                    8.625 |          100.0% |
| v6 job roles | bigscience/bloom-560m     |       2,880 |                     8.625 |                    8.625 |          100.0% |

Since the word-count difference is zero in these evaluated outputs, the observed score differences cannot be explained by simple word-count imbalance. This supports the interpretation that measured preferences reflect model likelihood differences under controlled linguistic conditions rather than sentence-length artifacts.

## 4.11 Factor Sensitivity

A factor sensitivity analysis was conducted for v6 and ArabJobs v7. The analysis measures the range of average score differences across levels of each factor. Larger ranges indicate stronger sensitivity.

**Table 10. Strongest factor sensitivities**

| Dataset      | Factor         | Levels | Range of Group Means | Strongest Feminine Level | Strongest Masculine Level |
| ------------ | -------------- | -----: | -------------------: | ------------------------ | ------------------------- |
| v6 job roles | template_type  |     14 |                1.248 | daily_work_context       | job_title_record          |
| v6 job roles | semantic_frame |     13 |                1.248 | routine_work             | formal_record             |
| v6 job roles | job_family     |    109 |                0.836 | nursing                  | digital_marketing         |
| v6 job roles | job_role_type  |     37 |                0.604 | technical_specialist     | technical_role            |
| ArabJobs v7  | job_family     |     51 |                0.974 | pharmacy                 | administration            |
| ArabJobs v7  | job_role_type  |     26 |                0.913 | clinical_support_role    | administrative_role       |
| ArabJobs v7  | template_type  |      6 |                0.556 | application_context      | recruitment_context       |
| ArabJobs v7  | semantic_frame |      6 |                0.556 | candidate_application    | hiring_language           |

In v6, template type and semantic frame are the strongest sensitivity factors, both with a range of 1.248. In ArabJobs v7, job family and job-role type are the strongest sensitivity factors, with ranges of 0.974 and 0.913 respectively.

These findings reinforce the main conclusion that Arabic occupational gender-bias measurement depends heavily on linguistic and occupational framing.

## 4.12 Mitigation Experiment

The wider project includes a counterfactual data augmentation mitigation experiment. AraGPT2-base was fine-tuned on balanced masculine–feminine Arabic occupational sentences and evaluated before and after mitigation.

**Table 11. Counterfactual mitigation results**

| Benchmark            | Before Avg Difference | After Avg Difference | Before Direction     | After Direction      | Mitigation Gain | Bias Reduced |
| -------------------- | --------------------: | -------------------: | -------------------- | -------------------- | --------------: | ------------ |
| v2 main              |                 0.126 |               -0.051 | Masculine            | Feminine             |           0.075 | Yes          |
| v5 job titles        |                -0.034 |                0.035 | Near-neutral / Mixed | Near-neutral / Mixed |          -0.001 | No           |
| v6 job roles         |                -0.302 |               -0.053 | Feminine             | Feminine             |           0.249 | Yes          |
| ArabJobs v7 external |                 0.089 |               -0.192 | Masculine            | Feminine             |          -0.103 | No           |

The mitigation experiment reduces absolute bias in v2 and v6, but not in v5 or ArabJobs v7. The strongest reduction is observed in v6, where absolute bias decreases from 0.302 to 0.053. However, the ArabJobs v7 result shows that mitigation does not generalize uniformly to real-world recruitment-language contexts.

This result suggests that counterfactual data augmentation can reduce measured bias in some controlled settings, but mitigation must be evaluated across multiple contexts before being considered reliable.

## 4.13 Summary of Findings

The experiments show five main findings.

First, Arabic causal language models show measurable occupational gender preference under paired likelihood evaluation.

Second, model family affects measured preference. In the v2 benchmark, Arabic-specific AraGPT2 models lean masculine, while multilingual models lean feminine.

Third, template formulation strongly affects measured bias. In v4, all evaluated models show template-induced direction changes.

Fourth, dialect affects model behavior. Some models shift between MSA and Egyptian Arabic.

Fifth, controlled and real-world recruitment-language settings can produce different results. AraGPT2-base leans feminine on v6 but masculine on ArabJobs v7.

Overall, the results support the main claim of the paper: Arabic occupational gender-bias scores should not be interpreted as fixed model properties. They are context-sensitive measurement outcomes affected by model family, template wording, dialect, semantic frame, job-title context, job-role structure, and real-world recruitment-language setting.

---

# 5. Discussion

## 5.1 Overview

The experimental results show that Arabic occupational gender-bias measurement is highly sensitive to linguistic and occupational context. The same model can produce different gender-preference directions depending on the benchmark version, template wording, dialect, semantic frame, job-title context, job-role structure, and real-world recruitment-language setting.

This finding is important because it challenges the idea that occupational gender bias can be represented by a single model-level score. A model may appear masculine-leaning in one benchmark, feminine-leaning in another, and near-neutral in a third. Therefore, Arabic occupational gender bias should be interpreted as a context-dependent measurement outcome rather than a fixed model property.

## 5.2 Interpretation of Model-Family Differences

The v2 main benchmark shows that Arabic-specific AraGPT2 models lean masculine, while multilingual models such as BLOOM, XGLM, and Qwen lean feminine. This suggests that model family and pretraining orientation affect measured occupational gender preference.

However, this model-family pattern does not remain stable across all benchmarks. In v4 and v6, AraGPT2 models shift toward feminine preference. This means that model family is important, but it does not fully determine the direction of bias. Instead, model-family effects interact with benchmark structure, sentence formulation, dialect, and occupational context.

This result suggests that Arabic-specific models should not automatically be assumed to produce more stable or less biased behavior. Arabic-specific pretraining may improve Arabic language modeling, but it can still encode gendered occupational associations. Similarly, multilingual models may show different patterns because their training data reflects broader multilingual distributions.

## 5.3 Template Sensitivity

One of the strongest findings is that template wording affects measured gender preference. In the v4 template-perturbation benchmark, all evaluated models show direction changes across templates. This means that the same model may prefer masculine forms in one template and feminine forms in another.

This has an important implication for benchmark design. A bias benchmark that uses only one or two templates may produce a result that is strongly dependent on the selected wording. For example, a workplace-presence template may produce a different result from a leadership, competence, promotion, or responsibility template. Therefore, Arabic occupational gender-bias benchmarks should include multiple templates and report template-level results.

The factor sensitivity analysis supports this conclusion. In v6, template type and semantic frame show the largest range of group means, both with a range of approximately 1.248. This indicates that sentence formulation and professional framing are among the strongest drivers of measured gender preference.

## 5.4 Dialect Sensitivity

The results also show that dialect matters. In v4, some models shift direction between Modern Standard Arabic and Egyptian Arabic. Qwen/Qwen2.5-0.5B and BLOOM-560m show feminine preference in MSA but masculine preference in Egyptian Arabic.

This confirms that Arabic should not be treated as a single homogeneous variety in fairness evaluation. MSA and dialectal Arabic differ in style, vocabulary, syntax, and data distribution. Since language models are trained on mixed Arabic sources, their behavior may vary across formal and dialectal input.

Dialect-aware evaluation is therefore necessary for Arabic LLM fairness research. A model that appears less biased or differently biased in MSA may behave differently when evaluated in Egyptian Arabic or another dialect. Future work should extend the framework to more dialects, such as Gulf, Levantine, Maghrebi, Iraqi, Sudanese, and Yemeni Arabic.

## 5.5 Job-Title and Job-Role Contexts

The v5 and v6 results show that occupational gender preference changes when the benchmark moves from general occupational templates to job-title and job-role contexts.

In v5, AraGPT2-base becomes near-neutral and BLOOM-560m shows weak masculine preference. This differs from the v4 results, where both models show feminine preference. The difference suggests that explicit job-title contexts such as CVs, job advertisements, HR records, and professional profiles activate different model associations from general occupational sentences.

The v6 benchmark further shows that job roles, departments, job families, seniority levels, and workplace contexts affect measured preference. This is important because real occupations are not only job names. They appear inside organizational and professional structures. A complete occupational-bias evaluation should therefore include job roles and workplace contexts, not only isolated occupation terms.

## 5.6 Controlled Benchmarks vs Real-World Job Advertisements

The ArabJobs v7 external benchmark shows that real-world recruitment-language contexts can produce different measured preferences from controlled benchmark contexts. AraGPT2-base shows feminine preference on the controlled v6 benchmark but masculine preference on ArabJobs v7.

This contrast shows the value of using both controlled and real-world data. Controlled benchmarks provide internal validity because sentence structure, gender form, occupation, and template can be controlled. However, real-world job advertisements include natural recruitment phrasing, country-specific wording, professional descriptions, and labor-market language. These elements may affect model likelihoods in ways that controlled templates do not capture.

Therefore, real-world recruitment-language evaluation should be treated as an external validation layer. It should not replace controlled counterfactual benchmarks, but it should be used to test whether controlled findings transfer to realistic job-ad contexts.

## 5.7 Implications for Arabic NLP Fairness

The findings have several implications for Arabic NLP fairness research.

First, Arabic bias evaluation should use full-sentence counterfactual pairs rather than isolated word replacements. Arabic grammatical gender affects sentence-level agreement, so counterfactual pairs must be grammatically valid.

Second, Arabic bias evaluation should include dialect-aware testing. MSA-only evaluation may miss important behavior that appears in dialectal Arabic.

Third, model-level averages should not be reported alone. They should be accompanied by template-level, dialect-level, semantic-frame-level, and context-level analyses.

Fourth, real-world recruitment-language data should be included where possible because occupational bias is directly relevant to job advertisements, CV systems, and professional profiling.

Fifth, mitigation methods should be tested across multiple benchmark settings. The counterfactual data augmentation experiment reduces absolute bias in v2 and v6 but not in v5 or ArabJobs v7. This shows that mitigation can be context-dependent and should not be evaluated on one benchmark only.

## 5.8 Reproducibility and Software Support

The project includes a software-supported evaluation pipeline. The scoring script computes sentence likelihoods, score differences, and preferred-gender labels. The analysis scripts aggregate results by model, field, template, dialect, semantic frame, department, job family, and benchmark source. The software app and dashboard make the framework easier to inspect and reuse.

This is important because bias evaluation is sensitive to implementation details such as sign convention, sentence scoring, length normalization, tokenization, aggregation logic, and metadata grouping. The project therefore includes formula validation, score-difference validation, token-length control, and final audit checks.

The reproducibility layer makes the framework more useful than a static benchmark. It allows other researchers to run the evaluation on additional models, add new occupations, add new dialects, or compare mitigation strategies.

## 5.9 Limitations

This study has several limitations.

First, the method focuses on open-weight causal language models because it requires access to token-level likelihood or language-modeling loss. Black-box API models require a different generation-based evaluation design.

Second, the benchmark focuses on masculine and feminine grammatical forms. This reflects Arabic grammatical gender, but it does not cover all gender identities or non-binary formulations.

Third, Egyptian Arabic is the only dialectal variety included in the current benchmark. Future work should include additional Arabic dialects.

Fourth, the ArabJobs v7 benchmark improves ecological validity but may include noise from real-world job-advertisement data. Therefore, it should be interpreted as an external validation layer rather than a fully controlled benchmark.

Fifth, the human-validation package is prepared, but final annotation agreement should be completed before an extended journal version. This is especially important for verifying grammaticality, semantic equivalence, gender-form correctness, and dialect appropriateness.

Sixth, the mitigation experiment is limited to counterfactual data augmentation and one main fine-tuned model. More mitigation methods and models should be evaluated in future work.

## 5.10 Summary

The discussion shows that Arabic occupational gender-bias evaluation requires a robustness-oriented design. The results indicate that measured gender preference changes across models, templates, dialects, job-title contexts, job-role contexts, and real-world recruitment-language data.

The main conclusion is that Arabic occupational gender-bias scores should not be treated as fixed model properties. They are measurement outcomes affected by linguistic and occupational framing. This supports the need for dialect-aware, template-sensitive, and context-rich Arabic LLM fairness evaluation.

---

# 6. Conclusion

This paper presented a dialect-aware counterfactual benchmark for measuring occupational gender bias in Arabic causal language models. The proposed benchmark uses masculine–feminine Arabic sentence pairs that preserve the same occupational meaning while changing the gendered linguistic form and the required grammatical agreement. Each sentence is scored using average token log-probability, and gender preference is measured using `score_difference`, defined as `masculine_score - feminine_score`.

The study evaluated Arabic-specific and multilingual causal language models across several benchmark settings, including a main controlled occupational benchmark, a template perturbation benchmark, a job-title benchmark, an expanded job-role and department benchmark, and an external real-world job-advertisement benchmark derived from ArabJobs.

The results show that Arabic occupational gender preference is context-sensitive. In the main controlled benchmark, Arabic-specific AraGPT2 models showed masculine preference, while multilingual models showed feminine preference. In the template perturbation benchmark, all evaluated models showed template-induced direction changes. In the expanded job-role benchmark, several models shifted toward feminine or near-neutral patterns. In the ArabJobs external benchmark, AraGPT2-base showed masculine preference in real-world recruitment-language contexts.

These findings suggest that Arabic occupational gender-bias scores should not be interpreted as fixed model properties. Instead, they should be understood as measurement outcomes affected by model family, template wording, dialect, semantic frame, job-title context, job-role structure, and real-world recruitment-language setting.

The paper contributes a reproducible Arabic occupational gender-bias benchmark, a likelihood-based scoring method for causal language models, robustness analysis across templates and dialects, external recruitment-language evaluation, and software support for measuring and inspecting Arabic occupational gender-bias results.

Future work should extend the benchmark to additional Arabic dialects, include larger and newer Arabic and multilingual LLMs, evaluate black-box API models using generation-based metrics, complete larger-scale human validation, expand real-world recruitment-language evaluation, and test additional bias-mitigation methods.

Overall, the results demonstrate the need for robustness-oriented Arabic LLM fairness evaluation. Reliable occupational gender-bias measurement should combine controlled counterfactual design, dialect-aware templates, context-rich occupational framing, external validation, and reproducible software-supported analysis.

---

# References

[1] T. Bolukbasi, K.-W. Chang, J. Zou, V. Saligrama, and A. Kalai, “Man is to computer programmer as woman is to homemaker? Debiasing word embeddings,” in *Advances in Neural Information Processing Systems 29*, 2016, pp. 4349–4357.

[2] N. Nangia, C. Vania, R. Bhalerao, and S. R. Bowman, “CrowS-Pairs: A challenge dataset for measuring social biases in masked language models,” in *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 2020, pp. 1953–1967.

[3] M. Nadeem, A. Bethke, and S. Reddy, “StereoSet: Measuring stereotypical bias in pretrained language models,” in *Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing*, 2021, pp. 5356–5371.

[4] K. Kurita, N. Vyas, A. Pareek, A. W. Black, and Y. Tsvetkov, “Measuring bias in contextualized word representations,” in *Proceedings of the First Workshop on Gender Bias in Natural Language Processing*, 2019, pp. 166–172.

[5] M. Kaneko and D. Bollegala, “Unmasking the mask: Evaluating social biases in masked language models,” in *Proceedings of the AAAI Conference on Artificial Intelligence*, vol. 36, no. 11, 2022, pp. 11954–11962.

[6] J. Salazar, D. Liang, T. Q. Nguyen, and K. Kirchhoff, “Masked language model scoring,” in *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 2020, pp. 2699–2712.

[7] R. Zmigrod, S. J. Mielke, H. Wallach, and R. Cotterell, “Counterfactual data augmentation for mitigating gender stereotypes in languages with rich morphology,” in *Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics*, 2019, pp. 1651–1661.

[8] T. Schick, S. Udupa, and H. Schütze, “Self-diagnosis and self-debiasing: A proposal for reducing corpus-based bias in NLP,” *Transactions of the Association for Computational Linguistics*, vol. 9, pp. 1408–1424, 2021.

[9] W. Antoun, F. Baly, and H. Hajj, “AraGPT2: Pre-trained transformer for Arabic language generation,” in *Proceedings of the Sixth Arabic Natural Language Processing Workshop*, 2021, pp. 196–207.

[10] BigScience Workshop, “BLOOM: A 176B-parameter open-access multilingual language model,” *Journal of Machine Learning Research*, vol. 25, no. 189, pp. 1–117, 2024.

[11] X. V. Lin et al., “Few-shot learning with multilingual generative language models,” in *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing*, 2022.

[12] A. Yang et al., “Qwen2.5 technical report,” *arXiv preprint arXiv:2412.15115*, 2024.

[13] R. Aly, Y. Allam, R. Gaber, and C. Basta, “ArGAN: Arabic gender, ability, and nationality dataset for evaluating biases in large language models,” in *Proceedings of the 6th Workshop on Gender Bias in Natural Language Processing (GeBNLP)*, 2025, pp. 256–267.

[14] M. El-Haj, “ArabJobs: A multinational corpus of Arabic job ads,” in *Proceedings of The Third Arabic Natural Language Processing Conference*, 2025, pp. 16–25.
