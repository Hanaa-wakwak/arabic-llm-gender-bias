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
