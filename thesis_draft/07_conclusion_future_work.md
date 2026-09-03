# Chapter 7: Conclusion and Future Work

## 7.1 Overview

This chapter concludes the thesis by summarizing the research problem, methodology, main findings, contributions, limitations, and future research directions. The thesis investigated occupational gender bias in Arabic causal language models using a robustness-oriented counterfactual evaluation framework. The framework was designed to measure whether language models assign higher likelihood to masculine or feminine occupational sentence variants and to examine whether this measured preference remains stable across benchmark design choices.

The project demonstrates that Arabic occupational gender-bias measurement requires more than a single benchmark or a single model-level score. Arabic is morphologically gendered, dialectally diverse, and context-sensitive. Therefore, bias evaluation must consider masculine–feminine counterfactual construction, grammatical agreement, dialectal variation, template formulation, semantic framing, job-title context, department structure, job-role context, and real-world recruitment-language data.

The final framework includes controlled benchmark construction, multi-model likelihood-based evaluation, formula and implementation validation, human validation, token-length control, factor sensitivity analysis, cross-benchmark robustness analysis, real-world ArabJobs evaluation, interactive software implementation, and a counterfactual bias-mitigation experiment.

## 7.2 Research Summary

The thesis addressed the problem of measuring occupational gender bias in Arabic causal language models. The central methodological challenge was to create a fair comparison between masculine and feminine Arabic occupational forms while preserving semantic meaning.

To address this challenge, the thesis used counterfactual sentence pairs. Each benchmark item contains a masculine sentence and a feminine sentence with the same occupational meaning. For example, a masculine occupational form such as `طبيب` is paired with its feminine counterpart `طبيبة`, while the surrounding sentence is adjusted for grammatical agreement.

The main scoring method uses average token log-probability. For each sentence, the causal language model assigns a likelihood score. The difference between the masculine and feminine sentence scores is then calculated as:

`score_difference = masculine_score - feminine_score`

A positive score difference indicates masculine preference, a negative score difference indicates feminine preference, and zero indicates equal preference.

The thesis extended this method across multiple benchmark versions, including the v2 main benchmark, v4 template perturbation benchmark, v5 job-title benchmark, v6 expanded job-role benchmark, and ArabJobs v7 external real-world job-advertisement benchmark.

## 7.3 Answers to the Research Questions

### 7.3.1 RQ1: How can occupational gender bias be measured in Arabic causal language models using counterfactual sentence pairs?

Occupational gender bias can be measured by constructing masculine–feminine Arabic counterfactual sentence pairs and comparing the likelihood assigned by a causal language model to each variant. The thesis defines the sentence score as average token log-probability and computes the pairwise score difference as masculine score minus feminine score.

This method provides a directional measure of model preference. It is appropriate for open-weight causal language models because these models provide access to token-level likelihood or language-modeling loss. The method is also suitable for Arabic because it evaluates full sentences rather than isolated words, allowing grammatical agreement and context to be preserved.

### 7.3.2 RQ2: Do Arabic-specific and multilingual causal language models show different occupational gender-preference patterns?

Yes. The v2 main benchmark showed that Arabic-specific AraGPT2 models leaned masculine, while several multilingual models leaned feminine. This indicates that model family and training orientation can influence occupational gender-preference patterns.

However, later benchmarks showed that this model-family pattern is not stable across all contexts. AraGPT2 models shifted direction in v4 and v6, showing that model family interacts with template design, dialect, semantic frame, and job-role context. Therefore, model family is important, but it is not the only factor affecting measured bias.

### 7.3.3 RQ3: Is measured gender preference stable across templates, dialects, semantic frames, job-title contexts, departments, and job-role contexts?

No. The results show that measured gender preference is highly context-sensitive. The v4 template perturbation benchmark showed that all six models experienced template-induced direction flips. This means the same model could prefer masculine variants under one template and feminine variants under another.

Dialect also affected measured preference. Some models changed direction between Modern Standard Arabic and Egyptian Arabic. The v5 job-title benchmark showed that explicit job-title contexts behave differently from general occupational templates. The v6 expanded job-role benchmark showed that department, job family, seniority level, workplace context, and job-role framing can also affect measured bias.

These findings support the thesis claim that Arabic occupational gender-bias scores are context-dependent measurement outcomes, not fixed model properties.

### 7.3.4 RQ4: Do real-world Arabic job-advertisement contexts produce different measured gender-preference patterns from controlled benchmark contexts?

Yes. The ArabJobs v7 external evaluation showed that real-world recruitment-language contexts can produce different measured preferences from controlled benchmark contexts. AraGPT2-base leaned feminine on the controlled v6 benchmark but leaned masculine on ArabJobs v7.

This contrast shows that controlled synthetic benchmarks and real-world recruitment-language data capture different aspects of model behavior. Controlled benchmarks provide internal validity and allow precise comparison, while external job-advertisement data improves ecological validity.

The thesis therefore concludes that Arabic occupational gender-bias evaluation should include both controlled counterfactual benchmarks and external real-world evaluation where possible.

### 7.3.5 RQ5: Can counterfactual data augmentation reduce measured occupational gender preference?

The thesis tested this through a counterfactual bias-mitigation experiment. AraGPT2-base was fine-tuned on balanced masculine–feminine Arabic occupational sentence pairs and then re-evaluated on the benchmark suite.

The mitigation effect was measured using:

`Mitigation_Gain = |Bias_before| - |Bias_after|`

A positive value indicates that absolute directional bias decreased after mitigation. The experiment extends the framework from bias measurement to bias limitation. It does not claim that bias can be removed completely, but it demonstrates how the benchmark suite can be used to evaluate whether counterfactual fine-tuning reduces measured gender preference.

## 7.4 Main Contributions

This thesis makes the following contributions.

### 7.4.1 Arabic Occupational Counterfactual Benchmark Suite

The thesis introduces a suite of Arabic occupational gender-bias benchmarks based on masculine–feminine counterfactual sentence pairs. The suite includes controlled benchmark versions, template perturbation, job-title contexts, expanded job-role and department contexts, and external job-advertisement contexts.

### 7.4.2 Likelihood-Based Gender Preference Metric

The thesis defines and implements a paired likelihood-based scoring method for open-weight causal language models. The main metric is:

`score_difference = masculine_score - feminine_score`

This provides a directional measure of gender preference at the sentence-pair level.

### 7.4.3 Dialect-Aware Evaluation

The framework includes both Modern Standard Arabic and Egyptian Arabic templates. This allows the thesis to test whether measured gender preference changes across Arabic varieties.

### 7.4.4 Template and Semantic-Frame Robustness Analysis

The v4 template perturbation benchmark shows that template formulation and semantic framing strongly affect measured gender preference. This contribution demonstrates that Arabic bias evaluation should report template-level robustness rather than relying only on model-level averages.

### 7.4.5 Job-Title Context Analysis

The v5 benchmark evaluates explicit job-title contexts such as CVs, job advertisements, HR records, and professional profiles. This contribution connects the evaluation framework to employment-related applications.

### 7.4.6 Expanded Job-Role and Department Benchmark

The v6 benchmark expands the framework to 2,880 counterfactual pairs generated from structured job roles, departments, job families, seniority levels, workplace contexts, semantic frames, and dialects. This contribution moves the benchmark beyond simple occupation lists.

### 7.4.7 ArabJobs v7 External Real-World Evaluation

The thesis adds an external real-world job-advertisement evaluation using ArabJobs-derived contexts. This contribution tests whether the framework can operate beyond controlled synthetic templates and supports comparison between controlled and real-world recruitment-language settings.

### 7.4.8 Formula and Implementation Validation

The project includes formula validation and score-difference implementation validation. These checks confirm that the theoretical metric is correctly implemented and that preference labels match the sign of the score difference.

### 7.4.9 Human Validation and Inter-Annotator Agreement

The thesis includes a human-validation package with 500 sampled counterfactual pairs. Two annotators evaluate grammaticality, meaning preservation, gender-form correctness, dialect correctness, job-title correctness, and keep/remove decisions. Percentage agreement and Cohen’s Kappa are reported.

### 7.4.10 Token-Length Control and Factor Sensitivity Analysis

The framework includes token-length control to check whether score differences are driven by superficial length differences. It also includes factor sensitivity analysis to identify which linguistic and occupational metadata factors most influence measured gender preference.

### 7.4.11 Interactive Bias-Measurement Software

The thesis includes an interactive software tool that allows users to measure Arabic gender bias from one sentence pair, uploaded CSV files, or project benchmarks. It also includes a dashboard for inspecting datasets, results, validation outputs, and robustness analyses.

### 7.4.12 Counterfactual Bias-Mitigation Experiment

The thesis includes a mitigation experiment based on counterfactual data augmentation. This experiment tests whether fine-tuning on balanced masculine–feminine occupational sentences can reduce measured gender preference.

### 7.4.13 Reproducible Project Audit

The final project audit verifies the presence and structural validity of datasets, scripts, results, documentation, software files, validation outputs, mitigation outputs, and Git tracking. The final audit passed with zero failed checks.

## 7.5 Main Findings

The thesis produced several major findings.

First, Arabic causal language models show measurable occupational gender preference when evaluated using masculine–feminine counterfactual sentence pairs.

Second, model family affects measured preference. In the v2 benchmark, Arabic-specific models leaned masculine while multilingual models leaned feminine.

Third, template formulation is a major driver of measured bias. In v4, all six models showed template-induced direction flips.

Fourth, dialect matters. Some models shifted direction between Modern Standard Arabic and Egyptian Arabic.

Fifth, job-title contexts behave differently from general occupational contexts. This shows that recruitment-related uses require specific evaluation.

Sixth, expanded job-role and department contexts can change measured gender-preference patterns.

Seventh, real-world job-advertisement contexts can produce different results from controlled benchmark contexts.

Eighth, formula validation, implementation validation, human validation, token-length control, and final auditing improve the reliability of the framework.

Ninth, counterfactual data augmentation can be evaluated as a bias-limitation method using the same benchmark suite.

## 7.6 Limitations

Although the thesis provides a broad and reproducible framework, several limitations remain.

First, the main scoring method applies to open-weight causal language models. Black-box API models require generation-based evaluation because token-level probabilities are not usually accessible.

Second, the benchmark focuses on binary masculine–feminine grammatical forms. This reflects Arabic grammatical gender but does not cover all gender identities or non-binary formulations.

Third, Egyptian Arabic is included as the dialectal component, but other Arabic dialects are not fully represented.

Fourth, external evaluation through ArabJobs v7 improves ecological validity but also introduces noise from real-world data.

Fifth, the mitigation experiment is limited to counterfactual data augmentation and one main fine-tuned model.

Sixth, likelihood preference does not directly equal real-world discrimination. It is a model-behavior indicator under controlled linguistic conditions.

Seventh, the software is a research prototype rather than a production-level fairness-auditing platform.

## 7.7 Practical Recommendations

Based on the findings, the thesis recommends the following.

Arabic occupational gender-bias evaluation should use full-sentence counterfactual pairs rather than isolated word pairs.

Benchmark design should include multiple templates and semantic frames.

Dialect should be treated as a core evaluation variable.

Job-title and job-role contexts should be evaluated separately from general occupational contexts.

External real-world recruitment-language evaluation should be included where licensing and ethics allow.

Model-level averages should be accompanied by template-level, dialect-level, and context-level analysis.

Bias mitigation should be evaluated across multiple benchmarks rather than only on training-like examples.

Software tools and audit reports should be included to improve reproducibility.

## 7.8 Future Work

Future work can extend this thesis in several directions.

### 7.8.1 More Arabic Dialects

The benchmark can be extended beyond Egyptian Arabic to include Gulf, Levantine, Maghrebi, Sudanese, Iraqi, Yemeni, and other Arabic dialects. This would provide broader dialectal coverage and improve generalizability.

### 7.8.2 More Models

Future evaluation can include larger and newer Arabic and multilingual models, including instruction-tuned LLMs, mixture-of-experts models, and region-specific Arabic models.

### 7.8.3 Black-Box API Evaluation

Future work can extend the framework to black-box models using generation-based metrics such as Counterfactual Parity Score. This would allow evaluation of commercial systems where token probabilities are unavailable.

### 7.8.4 More Real-World Datasets

The ArabJobs evaluation can be expanded with additional job-advertisement datasets, CV datasets, recruitment-platform data, and professional social-media data, subject to privacy, licensing, and ethical constraints.

### 7.8.5 Stronger Mitigation Methods

Future mitigation work can compare counterfactual data augmentation with prompt-based debiasing, decoding-time debiasing, representation editing, data filtering, and post-processing interventions.

### 7.8.6 Production-Ready Software

The software can be expanded into a complete Arabic fairness-auditing toolkit with batch processing, model registry support, report generation, user authentication, API access, and deployment documentation.

### 7.8.7 Extension to Other Bias Dimensions

The framework can be adapted to evaluate other forms of bias in Arabic LLMs, including nationality, religion, disability, age, dialect, region, and socioeconomic status.

## 7.9 Final Conclusion

This thesis presented a robustness-oriented framework for measuring occupational gender bias in Arabic causal language models. The framework uses masculine–feminine counterfactual sentence pairs, average token log-probability scoring, directional score differences, validation procedures, statistical analysis, external job-advertisement evaluation, software implementation, and bias-mitigation testing.

The main conclusion is that Arabic occupational gender-bias scores are not stable model properties. They are context-sensitive measurement outcomes affected by model family, template wording, dialect, semantic frame, job-title context, department, job-role structure, and real-world recruitment-language data.

The thesis contributes a reproducible benchmark suite and software framework for Arabic LLM fairness research. It shows that reliable Arabic gender-bias evaluation requires controlled counterfactual design, dialect awareness, robustness testing, external validation, human validation, implementation validation, and careful interpretation.

By combining measurement, validation, analysis, software implementation, and mitigation, the project provides a strong foundation for future Arabic NLP fairness research and Q1 journal publication.
