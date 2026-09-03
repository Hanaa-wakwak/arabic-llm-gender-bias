# Measuring Occupational Gender Bias in Arabic Causal Language Models using a Counterfactual Dialect-Aware Benchmark

## Abstract Draft

This thesis presents a robustness-oriented framework for measuring occupational gender bias in Arabic causal language models. The framework uses masculine-feminine counterfactual sentence pairs to compare model preference between gendered occupational forms while preserving the same semantic context. Each sentence is scored using average token log-probability, and gender preference is measured using score_difference, defined as masculine_score minus feminine_score.

The project introduces a suite of Arabic occupational benchmarks covering Modern Standard Arabic and Egyptian Arabic, controlled templates, job-title contexts, expanded job-role and department contexts, and real-world Arabic job-advertisement data derived from ArabJobs. The evaluation includes multiple open-weight causal language models, statistical and robustness analyses, token-length controls, formula and implementation validation, human validation with inter-annotator agreement, an interactive bias-measurement software tool, and a counterfactual bias-mitigation experiment.

The findings show that Arabic occupational gender-bias scores are not stable model properties. Instead, measured bias varies across model family, template formulation, dialect, semantic frame, job-role context, department, and real-world recruitment-language setting. The thesis contributes a reproducible evaluation framework, benchmark resources, validation procedures, software implementation, and mitigation analysis for Arabic LLM fairness research.

## Keywords

Arabic NLP; Large Language Models; Gender Bias; Occupational Bias; Counterfactual Evaluation; Causal Language Models; Arabic Dialects; Fairness; Bias Mitigation; Software Engineering