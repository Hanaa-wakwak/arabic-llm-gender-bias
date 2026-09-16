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
