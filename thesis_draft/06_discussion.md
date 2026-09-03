# Chapter 6: Discussion

## 6.1 Overview

This chapter discusses the main findings of the Arabic occupational gender-bias evaluation framework. The results show that occupational gender bias in Arabic causal language models is not a single fixed property of a model. Instead, it is highly sensitive to benchmark design, template formulation, dialect, semantic frame, job-title context, department, job-role framing, and real-world recruitment-language context.

The discussion is organized around the research questions introduced in Chapter 3. It interprets the results from the v2 main benchmark, v4 template perturbation benchmark, v5 job-title benchmark, v6 expanded job-role and department benchmark, and ArabJobs v7 external real-world benchmark. It also discusses the value of formula validation, implementation validation, human validation, token-length control, software implementation, and the counterfactual bias-mitigation experiment.

The central conclusion is that Arabic occupational gender-bias evaluation should not rely on a single template, a single benchmark, or a single model-level average. A reliable evaluation must consider linguistic variation, Arabic morphology, dialectal context, occupational framing, and external real-world language.

## 6.2 Interpretation of the Main Finding

The most important finding of this thesis is that measured gender preference changes across evaluation contexts. In the v2 main benchmark, Arabic-specific AraGPT2 models showed masculine preference, while several multilingual models showed feminine preference. However, in the v4 template perturbation benchmark, all six models showed an overall feminine preference. In the v5 job-title benchmark, AraGPT2-base became near-balanced or mixed, while BLOOM-560m showed weak masculine preference. In the v6 expanded job-role and department benchmark, most completed models showed feminine preference or near-neutral behavior. In ArabJobs v7, AraGPT2-base showed masculine preference on real-world job-advertisement contexts.

This pattern shows that a statement such as “a model is masculine-biased” or “a model is feminine-biased” is incomplete unless the benchmark context is specified. The same model can produce different measured directions under different templates, dialects, job-role structures, or data sources. Therefore, this thesis argues that Arabic occupational gender-bias scores are context-dependent measurement outcomes rather than stable model properties.

This does not mean that the bias scores are unreliable. Instead, it means that the evaluation framework reveals an important property of bias measurement itself: the measured result depends on the linguistic and social context in which the occupation is presented.

## 6.3 Discussion of RQ1: Measuring Occupational Gender Bias in Arabic Causal Language Models

RQ1 asked how occupational gender bias can be measured in Arabic causal language models using counterfactual sentence pairs.

The thesis answers this question by proposing a paired likelihood-based method. Each benchmark item contains a masculine Arabic sentence and a feminine counterfactual sentence. The two sentences preserve the same occupational meaning while changing the gendered form. Each sentence is scored using average token log-probability, and the difference between the masculine and feminine scores is used as the directional bias metric.

The main formula is:

`score_difference = masculine_score - feminine_score`

A positive score difference indicates masculine preference, a negative value indicates feminine preference, and zero indicates equal preference.

This formulation is suitable for open-weight causal language models because these models assign probabilities to token sequences. The use of average token log-probability allows full-sentence comparison while reducing sentence-length effects. This is especially important in Arabic because gender marking may affect nouns, demonstratives, verbs, adjectives, and agreement markers.

The contribution of this method is that it adapts likelihood-based bias evaluation to Arabic occupational gender morphology. Instead of comparing only isolated words, it compares complete Arabic sentence pairs. This makes the evaluation more realistic and more sensitive to grammatical context.

## 6.4 Discussion of RQ2: Differences Between Arabic-Specific and Multilingual Models

RQ2 asked whether Arabic-specific and multilingual causal language models show different occupational gender-preference patterns.

The v2 benchmark showed a clear model-family pattern. Arabic-specific AraGPT2 models leaned masculine, while non-Arabic-specific multilingual models leaned feminine. This suggests that model family and training orientation affect gender-preference patterns.

However, later results show that this model-family pattern is not absolute. In v4 and v6, AraGPT2 models shifted toward feminine preference. This means that model family matters, but it does not fully determine the direction of measured bias. Model-family effects interact with benchmark design, template wording, dialect, and occupational context.

This is an important finding for Arabic LLM evaluation. It suggests that Arabic-specific models should not automatically be assumed to behave more fairly or more consistently than multilingual models. Arabic-specific pretraining may improve Arabic fluency or morphology, but it can still encode gendered occupational associations. Similarly, multilingual models may show different bias directions because their training data combines Arabic with other languages and distributions.

The thesis therefore supports a comparative approach. Evaluating only one model type would provide an incomplete picture. A robust Arabic bias evaluation should include both Arabic-specific and multilingual models.

## 6.5 Discussion of RQ3: Template, Dialect, Semantic-Frame, and Job-Role Sensitivity

RQ3 asked whether measured gender preference is stable across templates, dialects, semantic frames, job-title contexts, departments, and job-role contexts.

The results show that it is not stable. The v4 template perturbation benchmark provides the strongest evidence. All six models showed template-induced direction flips. This means that the same model could prefer masculine forms under one template and feminine forms under another.

This finding has major methodological implications. Template wording is not a neutral container for measuring bias. It can actively influence the measured result. For example, templates involving leadership, competence, promotion, workplace presence, or responsibility may activate different learned associations in the model. Therefore, a benchmark that uses only one or two templates may produce a narrow or misleading estimate of occupational gender bias.

Dialect also affected the results. Some models shifted direction between Modern Standard Arabic and Egyptian Arabic. This shows that Arabic dialect should be treated as a core evaluation variable, not as a minor linguistic detail. Since many Arabic language models are trained on mixed formal, dialectal, and web-based data, their gender-preference patterns may vary depending on whether the input is formal MSA or dialectal Arabic.

The v6 benchmark further strengthens this conclusion. By expanding the evaluation to job roles, departments, job families, seniority levels, and workplace contexts, v6 shows that occupational bias is not limited to job names. The professional frame around the occupation can change the measured preference.

This supports the thesis argument that Arabic occupational gender-bias evaluation should be multidimensional. It should report not only model-level averages, but also template-level, dialect-level, semantic-frame-level, department-level, and job-role-level patterns.

## 6.6 Discussion of RQ4: Controlled Benchmarks vs Real-World Job Advertisements

RQ4 asked whether real-world Arabic job-advertisement contexts produce different measured gender-preference patterns from controlled benchmark contexts.

The ArabJobs v7 result shows that they can. AraGPT2-base leaned feminine on the controlled v6 job-role benchmark, but leaned masculine on the ArabJobs v7 real-world job-advertisement benchmark. This contrast is one of the strongest findings of the thesis.

Controlled benchmarks and real-world datasets serve different purposes. Controlled benchmarks allow precise experimental comparison because the researcher can control templates, occupations, dialects, and gendered forms. They are useful for isolating the effect of specific variables. However, they may not fully reflect natural recruitment language.

Real-world job advertisements contain more linguistic variation, domain-specific wording, country-specific expressions, and recruitment-style phrasing. They may also reflect social and labor-market patterns present in real job ads. Therefore, they can produce different model preferences from controlled templates.

The thesis does not treat ArabJobs v7 as a replacement for controlled benchmarks. Instead, it treats it as an external validation layer. The combination of controlled and external data is stronger than either approach alone. Controlled benchmarks provide internal validity, while ArabJobs v7 provides ecological validity.

This is especially important because occupational gender bias has practical relevance in recruitment, employment platforms, CV screening, job-ad generation, and professional recommendation systems. A bias evaluation framework should therefore be tested not only on synthetic sentences, but also on recruitment-language contexts.

## 6.7 Discussion of RQ5: Bias Mitigation Through Counterfactual Data Augmentation

RQ5 asked whether counterfactual data augmentation can reduce measured occupational gender preference.

The thesis addresses this through a mitigation experiment. AraGPT2-base was fine-tuned on balanced masculine–feminine Arabic occupational counterfactual data, then re-evaluated on the benchmark suite. The mitigation effect was measured using:

`Mitigation_Gain = |Bias_before| - |Bias_after|`

A positive mitigation gain indicates that the absolute directional bias decreased after fine-tuning.

This experiment extends the thesis beyond measurement. It tests whether the same counterfactual framework used for evaluation can also support bias limitation. The purpose is not to claim that gender bias can be completely removed. Instead, the purpose is to test whether exposure to balanced Arabic occupational forms can reduce measured preference under the proposed scoring metric.

The mitigation results should be interpreted carefully. A reduction in average directional bias does not necessarily mean that all forms of bias are removed. It may reduce bias in one benchmark while leaving bias unchanged or increasing it in another. This is because mitigation can interact with template, dialect, job-role context, and real-world language. Therefore, mitigation should be evaluated across multiple benchmarks, not only on the training-like dataset.

The experiment is still valuable because it demonstrates a complete research cycle: measurement, validation, analysis, and mitigation testing.

## 6.8 Importance of Full-Sentence Counterfactual Evaluation

A key methodological choice in this thesis is the use of full-sentence counterfactual pairs rather than isolated word pairs. This is important for Arabic because gender is grammatical and contextual. A masculine occupational noun may require masculine agreement in surrounding words, while the feminine counterpart may require changes in demonstratives, verbs, or adjectives.

For example:

`هذا الطبيب يعمل في المستشفى.`

and:

`هذه الطبيبة تعمل في المستشفى.`

The difference is not only the occupation word. The demonstrative also changes from `هذا` to `هذه`. If the benchmark changed only the occupation word and ignored agreement, the sentence might become ungrammatical or unnatural. Therefore, Arabic gender-bias evaluation requires sentence-level control.

Full-sentence scoring also captures model preference in context. A model may assign different probabilities to a gendered occupational form depending on whether the sentence describes leadership, competence, promotion, daily work, or recruitment. This makes sentence-level evaluation more informative than isolated word comparison.

## 6.9 Importance of Dialect-Aware Evaluation

Arabic is not a single uniform language variety in practical NLP use. Modern Standard Arabic is common in formal writing, news, official documents, and education, while dialectal Arabic is common in social media, conversation, local platforms, and informal digital communication.

The inclusion of Egyptian Arabic templates makes the benchmark more realistic and more relevant to Arabic NLP applications. The results show that dialect can shift measured gender preference. Therefore, evaluating only MSA would hide part of model behavior.

Dialect-aware evaluation is particularly important for fairness. A model that appears less biased in MSA may behave differently in dialectal Arabic. Since users may interact with Arabic language technologies in both formal and dialectal forms, bias evaluation should include both.

## 6.10 Importance of Template Perturbation

The template perturbation results show that template selection can strongly affect measured bias. This has implications for benchmark design.

If a researcher uses only one template, the result may reflect the chosen wording more than the model’s general occupational associations. For example, a template about leadership may produce a different gender preference from a template about workplace presence. A template about promotion may produce a different preference from a template about daily work.

Therefore, this thesis recommends that Arabic occupational gender-bias benchmarks should include multiple templates and report template-level results. Model-level averages should be interpreted together with template sensitivity analysis. This reduces the risk of overgeneralizing from a narrow prompt design.

## 6.11 Importance of Job-Title and Job-Role Contexts

The v5 and v6 results show that occupational bias changes when the benchmark moves from general occupation sentences to job-title and job-role contexts.

Job-title contexts are important because they appear in CVs, job advertisements, HR records, professional profiles, and employment databases. These contexts are directly connected to real-world employment systems.

Job-role contexts are also important because real occupations are not only names. They include responsibilities, departments, seniority levels, workplace settings, and professional functions. The v6 benchmark captures this complexity by expanding the evaluation to structured job roles and departments.

This strengthens the thesis contribution because it moves beyond simple occupation lists. It evaluates occupational gender bias in more realistic professional structures.

## 6.12 Importance of Validation

Validation is a major strength of the project. The framework includes multiple validation layers:

* benchmark quality validation,
* score-difference implementation validation,
* formula validation,
* token-length control,
* human validation,
* final project audit.

These validation layers reduce the risk that results are caused by dataset errors, formula mistakes, implementation inconsistencies, sentence-length artifacts, or invalid Arabic constructions.

Formula validation confirms that the score difference is correctly computed as masculine score minus feminine score. Implementation validation confirms that preference labels match the sign of the score difference. Human validation provides linguistic evidence that the counterfactual pairs are grammatically and semantically acceptable. Token-length control checks whether length differences are likely to explain score differences. The final audit confirms that the repository is complete and reproducible.

Together, these validation layers make the framework stronger for thesis defense and publication.

## 6.13 Importance of Software Implementation

The software implementation turns the thesis from a static benchmark study into a usable bias-measurement framework. The bias measurement app allows users to input sentence pairs, upload CSV files, select models, compute scores, classify preferred gender, visualize outputs, and export results.

The dashboard app allows users to inspect datasets, model summaries, validation reports, robustness analyses, and cross-benchmark comparisons.

This software layer is important for a Software Engineering or Computer Science thesis because it demonstrates implementation, usability, reproducibility, and practical application. It also supports future researchers who may want to extend the benchmark, test additional models, or evaluate new Arabic occupational contexts.

## 6.14 Implications for Arabic NLP Fairness Research

The findings have several implications for Arabic NLP fairness research.

First, Arabic bias evaluation should account for morphology. Gendered occupational forms are not always simple word substitutions. They interact with agreement, syntax, and sentence naturalness.

Second, Arabic bias evaluation should account for dialect. MSA-only evaluation may miss important model behavior in dialectal Arabic.

Third, occupational bias should be measured across multiple professional contexts. Generic templates, job titles, job roles, departments, and real-world job ads can produce different results.

Fourth, evaluation should include validation. Without formula validation, implementation validation, human validation, and robustness checks, it is difficult to know whether measured bias reflects model behavior or benchmark artifacts.

Fifth, mitigation should be tested across multiple contexts. A mitigation method that reduces bias in one benchmark may not generalize to another benchmark.

## 6.15 Implications for Real-World Recruitment Systems

The ArabJobs v7 evaluation makes the thesis relevant to recruitment-language systems. LLMs may be used to generate job ads, summarize CVs, recommend candidates, classify occupations, or support HR-related decision-making. If these models encode gendered occupational preferences, they may influence downstream systems.

This thesis does not claim that likelihood differences directly equal real-world discrimination. However, they can indicate model preferences that may matter in employment-related applications. If a model consistently assigns higher likelihood to one gendered form in professional contexts, this may affect generated text, ranking behavior, or user-facing outputs.

Therefore, Arabic recruitment-related NLP systems should be evaluated for gender bias before deployment. Evaluation should include both controlled counterfactual examples and real-world job-advertisement language.

## 6.16 Limitations

Although the framework is extensive, it has several limitations.

First, the method focuses on open-weight causal language models. It requires access to model likelihoods or losses. Black-box API models that only return generated text require a different evaluation method, such as counterfactual parity scoring over generated outputs.

Second, the benchmark focuses on masculine and feminine occupational forms. It does not cover all gender identities or non-binary formulations. This reflects the grammatical structure of Arabic and the scope of the thesis, but it remains a limitation.

Third, Egyptian Arabic is included as the dialectal component, but other Arabic dialects are not fully covered. Future work should extend the benchmark to Gulf, Levantine, Maghrebi, Sudanese, and other Arabic varieties.

Fourth, the ArabJobs v7 external benchmark is derived from real-world job-advertisement data and may contain noise. It improves ecological validity but is less controlled than synthetic benchmark templates.

Fifth, the mitigation experiment is limited to one main intervention: counterfactual data augmentation. It does not test all possible bias-reduction methods, such as reinforcement learning, decoding-time debiasing, representation editing, or data filtering.

Sixth, the software is a research prototype. It supports measurement, inspection, and export, but it is not a production-level fairness auditing platform.

Seventh, likelihood-based bias scores should be interpreted as model preference indicators, not as direct evidence of social discrimination. They show how a model scores linguistic variants, not necessarily how a deployed system will affect real users.

## 6.17 Threats to Validity

Several threats to validity must be considered.

### 6.17.1 Construct Validity

The main construct is occupational gender bias as measured through likelihood preference between masculine and feminine counterfactual sentences. This is a useful operational definition, but it does not capture every form of gender bias. Bias may also appear in generated descriptions, sentiment, salary suggestions, leadership assumptions, or candidate evaluations.

### 6.17.2 Internal Validity

Internal validity may be affected by template wording, sentence length, tokenization, or grammatical differences between masculine and feminine forms. The thesis addresses these threats through template perturbation, average token log-probability, token-length control, formula validation, and human validation.

### 6.17.3 External Validity

The findings may not generalize to all Arabic models, all dialects, all occupations, or all recruitment settings. The thesis improves external validity through ArabJobs v7, but further real-world datasets are still needed.

### 6.17.4 Conclusion Validity

Statistical significance can be affected by sample size. Therefore, the thesis reports effect sizes and robustness analyses, not only p-values. The cross-benchmark analysis also prevents overgeneralization from one dataset.

### 6.17.5 Reproducibility Validity

Reproducibility depends on the availability of code, benchmark files, model versions, and external data. The final audit, GitHub repository, software run instructions, and validation reports address this threat.

## 6.18 Why the Framework Is Stronger Than a Single Benchmark

A single benchmark can answer whether a model prefers masculine or feminine variants under one set of conditions. However, it cannot show whether the result is robust.

This thesis is stronger because it evaluates multiple benchmark contexts:

* main controlled benchmark,
* template perturbation benchmark,
* job-title benchmark,
* expanded job-role and department benchmark,
* real-world ArabJobs benchmark.

It also includes:

* six-model evaluation,
* statistical testing,
* effect-size analysis,
* formula validation,
* implementation validation,
* token-length control,
* human validation,
* software implementation,
* mitigation experiment,
* final audit.

This makes the contribution a complete evaluation framework rather than only a dataset.

## 6.19 Publication Implications

For publication, the strongest contribution is the robustness-oriented framing. The paper should not be presented only as an Arabic gender-bias benchmark. It should be presented as a framework showing that Arabic occupational gender-bias measurement varies across benchmark design, dialect, template formulation, job-role context, and real-world recruitment language.

The most publishable claim is:

`Arabic occupational gender-bias scores are not stable model properties; they are context-sensitive measurement outcomes affected by linguistic and occupational framing.`

This claim is supported by the cross-benchmark direction changes, v4 template-induced flips, v6 job-role expansion, ArabJobs external validation, and validation layers.

The thesis is therefore suitable for transformation into a Q1 journal paper after final polishing, complete human-validation reporting, and careful related-work positioning.

## 6.20 Future Work

Future work can extend the framework in several directions.

First, the model set can be expanded to include newer Arabic and multilingual LLMs, including larger open-weight models and instruction-tuned models.

Second, the benchmark can be extended to more Arabic dialects, including Gulf, Levantine, Maghrebi, Sudanese, Iraqi, and Yemeni Arabic.

Third, black-box API models can be evaluated using generation-based counterfactual parity metrics, since token-level probabilities may not be available.

Fourth, additional real-world datasets can be incorporated, including recruitment platforms, CV corpora, job descriptions, and professional social-media content, subject to ethical and licensing constraints.

Fifth, mitigation can be expanded beyond counterfactual data augmentation to include decoding-time debiasing, prompt-based mitigation, representation-level editing, and controlled data filtering.

Sixth, the software can be expanded into a full fairness-auditing toolkit with user authentication, batch processing, model comparison, report generation, and deployment-ready documentation.

Seventh, the framework can be adapted to other types of bias in Arabic, such as nationality, religion, dialect, disability, age, or socioeconomic status.

## 6.21 Chapter Summary

This chapter discussed the findings of the Arabic occupational gender-bias evaluation framework. The results show that measured gender preference varies across model family, template formulation, dialect, semantic frame, job-title context, department, job-role framing, and real-world recruitment-language data.

The discussion showed that the framework’s main strength is its robustness-oriented design. It does not rely on a single benchmark or a single model-level average. Instead, it combines controlled benchmarks, external validation, statistical analysis, validation checks, software implementation, and mitigation testing.

The chapter also discussed limitations, threats to validity, real-world implications, publication implications, and future work. The next chapter concludes the thesis by summarizing the contributions and presenting final recommendations for Arabic LLM gender-bias evaluation.
