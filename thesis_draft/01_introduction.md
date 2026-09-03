# Chapter 1: Introduction

## 1.1 Background

Large Language Models (LLMs) have become central components in modern Natural Language Processing (NLP) systems. They are used in text generation, question answering, summarization, translation, classification, recommendation systems, and decision-support applications. As these models become more widely deployed, their social behavior has become an important research concern. One major concern is that language models may reproduce, amplify, or hide social biases learned from their training data.

Gender bias is one of the most studied forms of bias in NLP. In occupational contexts, gender bias appears when a model associates certain jobs, skills, roles, or professional attributes more strongly with men or women. For example, a model may assign higher probability to a masculine sentence involving engineering or leadership, or to a feminine sentence involving education or care work. Such behavior is especially important in employment-related applications, where language models may be used to generate job advertisements, summarize CVs, classify occupations, recommend candidates, or assist in human-resource workflows.

Arabic presents additional challenges for gender-bias evaluation. Unlike English, Arabic has grammatical gender expressed through nouns, verbs, adjectives, demonstratives, and agreement markers. A gender change in an Arabic occupational sentence may require more than replacing one word. For example, the masculine sentence:

`هذا الطبيب يعمل في المستشفى.`

has a feminine counterfactual form:

`هذه الطبيبة تعمل في المستشفى.`

The gendered occupational noun changes from `طبيب` to `طبيبة`, and the demonstrative changes from `هذا` to `هذه`. This means that Arabic gender-bias evaluation must account for morphology, syntax, agreement, and naturalness.

Arabic is also dialectally diverse. Modern Standard Arabic (MSA) is widely used in formal writing, official communication, news, and education, while dialectal Arabic is used in informal communication, social media, and everyday interaction. A model may behave differently in MSA and Egyptian Arabic, even when the same occupational meaning is preserved. Therefore, Arabic bias evaluation should not be limited to one language variety.

This thesis focuses on measuring occupational gender bias in Arabic causal language models. It proposes a counterfactual, dialect-aware, robustness-oriented evaluation framework that compares masculine and feminine Arabic occupational sentence pairs using likelihood-based scoring.

## 1.2 Research Problem

Existing bias-evaluation approaches often rely on word associations, single templates, masked-token probabilities, or English-centered benchmark designs. These approaches are useful, but they are not sufficient for Arabic causal language models.

There are four main problems.

First, Arabic gender morphology is complex. Gender changes may require changes in multiple parts of a sentence, not only the occupation word. If this is ignored, the benchmark may contain unnatural or grammatically invalid counterfactual pairs.

Second, many bias benchmarks rely on a small number of templates. If the measured score changes when the template changes, then a single-template benchmark may give an incomplete or misleading estimate of model bias.

Third, Arabic dialect variation is often underrepresented. A model that appears to behave one way in MSA may behave differently in Egyptian Arabic or another dialectal context.

Fourth, controlled synthetic benchmarks may not fully represent real-world recruitment language. Since occupational bias is directly relevant to employment applications, bias evaluation should also be tested on job-advertisement contexts where possible.

Therefore, the research problem addressed in this thesis is:

`How can occupational gender bias in Arabic causal language models be measured, validated, and analyzed in a way that accounts for Arabic grammatical gender, dialect variation, template sensitivity, occupational context, and real-world recruitment-language data?`

## 1.3 Research Motivation

The motivation for this thesis comes from three areas: fairness in NLP, Arabic language technology, and software engineering reproducibility.

From the fairness perspective, language models may produce biased or unequal behavior when handling gendered occupational language. If such models are used in recruitment or professional systems, their preferences may influence generated job ads, professional descriptions, or ranking-related downstream systems.

From the Arabic NLP perspective, Arabic has linguistic characteristics that make direct transfer from English bias-evaluation methods insufficient. Arabic occupational forms are gendered, and sentence-level grammatical agreement is necessary. Arabic also includes multiple varieties, including MSA and dialectal Arabic. A robust Arabic evaluation framework must therefore be designed with Arabic-specific linguistic properties in mind.

From the software engineering perspective, bias evaluation should not be only a one-time experiment. It should be reproducible, auditable, and usable. This thesis therefore includes not only datasets and results, but also scoring scripts, validation scripts, analysis scripts, human-validation files, software tools, run instructions, mitigation experiments, and final audit reports.

## 1.4 Aim of the Study

The aim of this thesis is to develop and evaluate a reproducible framework for measuring occupational gender bias in Arabic causal language models using masculine–feminine counterfactual sentence pairs.

The framework is designed to answer whether a model assigns higher likelihood to masculine or feminine occupational variants, and whether this preference remains stable across models, templates, dialects, semantic frames, job-title contexts, departments, job roles, and real-world job-advertisement data.

## 1.5 Research Objectives

The main objectives of the thesis are:

1. To construct Arabic masculine–feminine occupational counterfactual sentence-pair benchmarks.

2. To design the benchmarks in a way that accounts for Arabic grammatical gender and sentence-level agreement.

3. To include both Modern Standard Arabic and Egyptian Arabic contexts.

4. To evaluate multiple open-weight causal language models using likelihood-based scoring.

5. To define and implement a directional score-difference metric:

`score_difference = masculine_score - feminine_score`

6. To analyze whether measured gender preference varies across model family, template formulation, dialect, semantic frame, job-title context, department, and job-role context.

7. To extend the evaluation to real-world Arabic job-advertisement contexts using ArabJobs-derived data.

8. To validate the formula, implementation, datasets, and human annotation quality.

9. To build software that allows users to measure Arabic occupational gender bias interactively.

10. To test whether counterfactual data augmentation can reduce measured occupational gender preference.

## 1.6 Research Questions

The thesis is guided by the following research questions:

**RQ1:** How can occupational gender bias be measured in Arabic causal language models using masculine–feminine counterfactual sentence pairs?

**RQ2:** Do Arabic-specific and multilingual causal language models show different occupational gender-preference patterns?

**RQ3:** Is measured gender preference stable across templates, dialects, semantic frames, job-title contexts, departments, and job-role contexts?

**RQ4:** Do real-world Arabic job-advertisement contexts produce different measured gender-preference patterns from controlled benchmark contexts?

**RQ5:** Can counterfactual data augmentation reduce measured occupational gender preference in Arabic causal language models?

## 1.7 Scope of the Study

This thesis focuses on Arabic occupational gender bias in open-weight causal language models. The study uses models where likelihood or language-modeling loss can be computed. The main evaluation method is based on full-sentence paired likelihood scoring.

The scope includes:

* Arabic occupational terms,
* masculine and feminine grammatical forms,
* MSA and Egyptian Arabic templates,
* controlled benchmark construction,
* job-title contexts,
* expanded job-role and department contexts,
* real-world job-advertisement contexts,
* open-weight causal language models,
* score-difference validation,
* human validation,
* software implementation,
* mitigation testing.

The scope does not include full evaluation of black-box API models such as commercial chat systems, because such systems often do not provide token-level probabilities. These models can be evaluated in future work using generation-based counterfactual parity metrics.

The thesis also focuses on binary masculine–feminine grammatical forms because this is the dominant grammatical gender contrast in Arabic occupational morphology. This does not cover all gender identities and should be treated as a limitation of the current scope.

## 1.8 Methodological Overview

The thesis uses a counterfactual evaluation design. Each benchmark item contains a masculine Arabic sentence and a feminine counterfactual sentence. The two sentences preserve the same occupational meaning while changing the gendered form and any necessary agreement markers.

For each sentence, the causal language model computes an average token log-probability score. The main score difference is computed as:

`score_difference = masculine_score - feminine_score`

The interpretation is:

* positive score difference means masculine preference,
* negative score difference means feminine preference,
* zero means equal preference.

The benchmark-level bias score is calculated as the mean score difference across all pairs. The thesis also reports absolute disparity and preference rates.

To test robustness, the framework evaluates multiple benchmark versions:

* v2 main validated benchmark,
* v4 template perturbation benchmark,
* v5 job-title benchmark,
* v6 expanded job-role and department benchmark,
* ArabJobs v7 external real-world job-advertisement benchmark.

The analysis includes model-level summaries, family-level comparison, template sensitivity, dialect sensitivity, semantic-frame analysis, job-title analysis, department and job-role analysis, cross-benchmark direction-change analysis, factor sensitivity analysis, token-length control, human validation, and mitigation evaluation.

## 1.9 Main Contributions

This thesis makes the following main contributions.

### 1.9.1 Arabic Occupational Counterfactual Benchmark Suite

The thesis introduces a suite of Arabic occupational gender-bias benchmarks based on masculine–feminine counterfactual sentence pairs. The suite includes controlled templates, dialect-aware forms, job-title contexts, expanded job-role contexts, and external real-world job-advertisement contexts.

### 1.9.2 Likelihood-Based Bias Measurement Formula

The thesis defines and implements a paired likelihood-based score-difference metric for open-weight causal language models:

`score_difference = masculine_score - feminine_score`

This metric provides a directional measure of whether a model prefers the masculine or feminine sentence variant.

### 1.9.3 Dialect-Aware Arabic Evaluation

The benchmark suite includes both MSA and Egyptian Arabic, allowing the thesis to evaluate whether measured gender preference changes across Arabic varieties.

### 1.9.4 Template and Semantic-Frame Robustness Analysis

The thesis evaluates whether bias measurements remain stable across different templates and semantic frames. This shows whether measured bias is robust or dependent on sentence formulation.

### 1.9.5 Expanded Job-Role and Department Benchmark

The thesis expands occupational bias evaluation beyond simple job titles by introducing a structured job-role and department benchmark. This benchmark evaluates gender preference across departments, job families, seniority levels, workplace contexts, and professional responsibilities.

### 1.9.6 External Real-World ArabJobs Evaluation

The thesis includes an external real-world evaluation using ArabJobs-derived job-advertisement contexts. This connects the evaluation framework to recruitment-language data and tests whether controlled benchmark findings transfer to real-world job-ad contexts.

### 1.9.7 Formula, Implementation, and Quality Validation

The project validates the scoring formula, score-difference implementation, benchmark structure, result files, and final repository completeness. These validation layers strengthen the reliability and reproducibility of the framework.

### 1.9.8 Human Validation

The thesis includes a human-validation package with 500 sampled counterfactual pairs. Two annotators evaluate grammaticality, meaning preservation, gender-form correctness, dialect correctness, job-title correctness, and keep/remove decisions. The agreement analysis reports percentage agreement and Cohen’s Kappa.

### 1.9.9 Interactive Bias-Measurement Software

The thesis includes software for measuring Arabic occupational gender bias. The software allows users to input one sentence pair, upload a CSV file, select a model, compute score differences, classify preference direction, visualize results, and export outputs.

### 1.9.10 Counterfactual Bias-Mitigation Experiment

The thesis includes a mitigation experiment using counterfactual data augmentation. AraGPT2-base is fine-tuned on balanced masculine–feminine Arabic occupational sentences and then re-evaluated to measure whether absolute directional bias decreases.

## 1.10 Significance of the Study

This thesis is significant for Arabic NLP, fairness research, and software engineering.

For Arabic NLP, it provides a framework that accounts for Arabic grammatical gender, full-sentence agreement, and dialect variation. This is important because Arabic gender bias cannot be reliably evaluated using methods designed only for English or only for isolated word pairs.

For fairness research, the thesis shows that occupational gender-bias scores are context-sensitive. A model’s measured preference can change depending on template, dialect, job-title context, department, job-role framing, and real-world data source. This challenges the idea that a single model-level bias score is sufficient.

For software engineering, the thesis provides a reproducible implementation. The project includes scripts, datasets, result files, validation outputs, software tools, run instructions, and final audit reports. This makes the work auditable and reusable.

For real-world applications, the ArabJobs evaluation and software tool connect the research to employment-related NLP systems. The framework can help evaluate and monitor gender preference in job-ad generation, CV-related language processing, and professional text systems.

## 1.11 Expected Outcomes

The expected outcomes of the thesis are:

1. A validated Arabic occupational counterfactual benchmark suite.

2. A likelihood-based scoring pipeline for Arabic causal language models.

3. Model-level and model-family-level bias results.

4. Evidence of template, dialect, semantic-frame, job-title, department, and job-role sensitivity.

5. External real-world evaluation using ArabJobs-derived job-advertisement data.

6. Human-validation and inter-annotator agreement results.

7. Formula and implementation validation reports.

8. Token-length control and factor sensitivity analyses.

9. An interactive bias-measurement software tool and dashboard.

10. A counterfactual bias-mitigation experiment.

11. A reproducible GitHub package with final audit results.

## 1.12 Definitions of Key Terms

**Large Language Model (LLM):** A neural language model trained on large text corpora to predict or generate natural language.

**Causal Language Model:** A language model that predicts each token based on the previous tokens in a sequence.

**Occupational Gender Bias:** A model preference or association that favors masculine or feminine forms in occupational contexts.

**Counterfactual Pair:** A pair of sentences that preserve the same meaning while changing a target attribute, such as gender.

**Masculine Sentence:** The sentence variant containing masculine occupational and agreement forms.

**Feminine Sentence:** The sentence variant containing feminine occupational and agreement forms.

**Score Difference:** The main metric used in this thesis, computed as masculine score minus feminine score.

**Dialect-Aware Evaluation:** Evaluation that accounts for different Arabic varieties, such as MSA and Egyptian Arabic.

**Template Perturbation:** Testing whether model behavior changes when the sentence template or semantic frame changes.

**Human Validation:** Manual review of benchmark pairs by annotators to evaluate grammaticality, meaning preservation, gender-form correctness, dialect correctness, and keep/remove decisions.

**Bias Mitigation:** A method intended to reduce measured bias, without claiming to eliminate bias completely.

## 1.13 Thesis Organization

The rest of the thesis is organized as follows.

**Chapter 2** reviews related work on language-model bias evaluation, gender bias benchmarks, counterfactual evaluation, likelihood-based scoring, Arabic NLP bias, occupational gender bias, job-advertisement datasets, and bias mitigation.

**Chapter 3** presents the methodology of the proposed framework, including benchmark construction, counterfactual pair design, scoring formula, validation procedures, statistical analysis, external evaluation, software implementation, and mitigation design.

**Chapter 4** describes the implementation of the framework, including repository structure, benchmark files, scoring scripts, analysis scripts, validation scripts, software tools, mitigation scripts, run instructions, and final audit.

**Chapter 5** reports the experimental results, including v2, v4, v5, v6, and ArabJobs v7 findings, along with validation, robustness, software, mitigation, and audit results.

**Chapter 6** discusses the findings, implications, limitations, threats to validity, practical relevance, and publication potential.

**Chapter 7** concludes the thesis and presents future work.

## 1.14 Chapter Summary

This chapter introduced the research problem, motivation, aim, objectives, research questions, scope, methodology, contributions, significance, expected outcomes, key definitions, and thesis organization.

The thesis addresses the need for a robust Arabic occupational gender-bias evaluation framework for causal language models. It argues that Arabic bias evaluation must account for grammatical gender, dialect variation, template formulation, occupational context, real-world recruitment-language data, validation, software reproducibility, and mitigation. The next chapter reviews the academic literature that supports and motivates this research.
