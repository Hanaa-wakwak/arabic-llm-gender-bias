# Measuring Occupational Gender Bias in Arabic Causal Language Models Using a Dialect-Aware Counterfactual Benchmark

## Abstract

Occupational gender bias in language models can affect applications related to recruitment, professional profiling, job-advertisement generation, and Arabic natural language processing systems. Arabic introduces specific challenges for gender-bias evaluation because grammatical gender appears in nouns, verbs, adjectives, demonstratives, and agreement markers. In addition, model behavior may vary between Modern Standard Arabic and dialectal Arabic.

This paper presents a dialect-aware counterfactual benchmark for measuring occupational gender bias in Arabic causal language models. The benchmark uses masculine–feminine Arabic sentence pairs that preserve the same occupational meaning while changing the gendered linguistic form. Each sentence is scored using average token log-probability, and gender preference is measured using `score_difference`, defined as `masculine_score - feminine_score`. Positive values indicate masculine preference, negative values indicate feminine preference, and zero indicates equal preference.

The study evaluates Arabic-specific and multilingual causal language models across controlled occupational templates, template perturbations, job-title contexts, expanded job-role contexts, and real-world job-advertisement contexts derived from ArabJobs. The results show that measured occupational gender preference is context-sensitive. Model preference changes across model family, template formulation, dialect, semantic frame, job-title context, job-role structure, and real-world recruitment-language setting. These findings suggest that Arabic occupational gender bias should not be treated as a fixed model property, but as a measurement outcome affected by linguistic and occupational framing.

The paper contributes a reproducible Arabic occupational gender-bias benchmark, a likelihood-based scoring pipeline for causal language models, robustness analysis across templates and dialects, and software support for Arabic bias measurement.

## Keywords

Arabic NLP; Large Language Models; Gender Bias; Occupational Bias; Causal Language Models; Counterfactual Evaluation; Arabic Dialects; Likelihood-Based Scoring; Fairness in NLP; Recruitment Language.
