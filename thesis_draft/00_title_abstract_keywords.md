# Measuring Occupational Gender Bias in Arabic Causal Language Models using a Counterfactual Dialect-Aware Benchmark

## Abstract Draft

This thesis presents a robustness-oriented framework for measuring occupational gender bias in Arabic causal language models. The framework uses masculine-feminine counterfactual sentence pairs to compare model preference between gendered occupational forms while preserving the same semantic context. Each sentence is scored using average token log-probability, and gender preference is measured using score_difference, defined as masculine_score minus feminine_score.

The project introduces a suite of Arabic occupational benchmarks covering Modern Standard Arabic and Egyptian Arabic, controlled templates, job-title contexts, expanded job-role and department contexts, and real-world Arabic job-advertisement data derived from ArabJobs. The evaluation includes multiple open-weight causal language models, statistical and robustness analyses, token-length controls, formula and implementation validation, human validation with inter-annotator agreement, an interactive bias-measurement software tool, and a counterfactual bias-mitigation experiment.

The findings show that Arabic occupational gender-bias scores are not stable model properties. Instead, measured bias varies across model family, template formulation, dialect, semantic frame, job-role context, department, and real-world recruitment-language setting. The thesis contributes a reproducible evaluation framework, benchmark resources, validation procedures, software implementation, and mitigation analysis for Arabic LLM fairness research.

## Keywords

Arabic NLP; Large Language Models; Gender Bias; Occupational Bias; Counterfactual Evaluation; Causal Language Models; Arabic Dialects; Fairness; Bias Mitigation; Software Engineering

# Measuring Occupational Gender Bias in Arabic Causal Language Models using a Counterfactual Dialect-Aware Benchmark

## Abstract

Large Language Models are increasingly used in language-generation and decision-support applications, including contexts related to employment, recruitment, professional profiling, and job-advertisement generation. These applications raise fairness concerns because language models may reproduce or amplify gendered occupational associations learned from training data. Arabic introduces additional challenges for gender-bias evaluation because grammatical gender is expressed through nouns, verbs, adjectives, demonstratives, and agreement markers, and because model behavior may vary across Modern Standard Arabic and dialectal Arabic.

This thesis presents a robustness-oriented framework for measuring occupational gender bias in Arabic causal language models using masculine–feminine counterfactual sentence pairs. Each benchmark item contains two Arabic sentences that preserve the same occupational meaning while changing the gendered linguistic form and the required grammatical agreement. The framework evaluates open-weight causal language models using average token log-probability. For each pair, gender preference is measured using `score_difference`, defined as `masculine_score - feminine_score`. Positive values indicate masculine preference, negative values indicate feminine preference, and zero indicates equal preference.

The project introduces a suite of Arabic occupational benchmarks covering controlled occupational templates, dialect-aware sentence variants, template perturbations, job-title contexts, expanded job-role and department contexts, and real-world Arabic job-advertisement contexts derived from ArabJobs. The evaluation includes Arabic-specific and multilingual causal language models, including AraGPT2, BLOOM, XGLM, and Qwen variants. The framework also includes formula validation, score-difference implementation validation, benchmark quality checks, token-length control, factor sensitivity analysis, cross-benchmark direction-change analysis, human validation with inter-annotator agreement, interactive bias-measurement software, a results dashboard, and a counterfactual data augmentation mitigation experiment.

The results show that Arabic occupational gender-bias scores are not stable model properties. Instead, measured preference varies across model family, template formulation, dialect, semantic frame, job-title context, department, job-role structure, and real-world recruitment-language setting. In the main v2 benchmark, Arabic-specific AraGPT2 models leaned masculine, while non-Arabic-specific multilingual models leaned feminine. In the v4 template-perturbation benchmark, all evaluated models showed template-induced direction changes. In the v6 expanded job-role benchmark, several models shifted toward feminine or near-neutral patterns. In the ArabJobs v7 external benchmark, AraGPT2-base shifted toward masculine preference in real-world job-advertisement contexts. These findings demonstrate that Arabic occupational gender-bias evaluation should not rely on a single template, dataset, or model-level average.

The thesis contributes a reproducible Arabic LLM fairness-evaluation framework, a dialect-aware occupational counterfactual benchmark suite, validated likelihood-based scoring scripts, human-validation resources, robustness analyses, software tools, external recruitment-language evaluation, and a mitigation experiment. The final project audit passed with zero failed checks, supporting the reproducibility and stability of the framework for thesis submission and future Q1 journal publication.

## Keywords

Arabic NLP; Large Language Models; Causal Language Models; Gender Bias; Occupational Bias; Counterfactual Evaluation; Arabic Dialects; Likelihood-Based Scoring; Fairness in NLP; Bias Mitigation; Recruitment Language; Software Engineering; Human Validation
