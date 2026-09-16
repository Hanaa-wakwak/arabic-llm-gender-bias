# 6. Conclusion

This paper presented a dialect-aware counterfactual benchmark for measuring occupational gender bias in Arabic causal language models. The proposed benchmark uses masculine–feminine Arabic sentence pairs that preserve the same occupational meaning while changing the gendered linguistic form and the required grammatical agreement. Each sentence is scored using average token log-probability, and gender preference is measured using `score_difference`, defined as `masculine_score - feminine_score`.

The study evaluated Arabic-specific and multilingual causal language models across several benchmark settings, including a main controlled occupational benchmark, a template perturbation benchmark, a job-title benchmark, an expanded job-role and department benchmark, and an external real-world job-advertisement benchmark derived from ArabJobs.

The results show that Arabic occupational gender preference is context-sensitive. In the main controlled benchmark, Arabic-specific AraGPT2 models showed masculine preference, while multilingual models showed feminine preference. In the template perturbation benchmark, all evaluated models showed template-induced direction changes. In the expanded job-role benchmark, several models shifted toward feminine or near-neutral patterns. In the ArabJobs external benchmark, AraGPT2-base showed masculine preference in real-world recruitment-language contexts.

These findings suggest that Arabic occupational gender-bias scores should not be interpreted as fixed model properties. Instead, they should be understood as measurement outcomes affected by model family, template wording, dialect, semantic frame, job-title context, job-role structure, and real-world recruitment-language setting.

The paper contributes a reproducible Arabic occupational gender-bias benchmark, a likelihood-based scoring method for causal language models, robustness analysis across templates and dialects, external recruitment-language evaluation, and software support for measuring and inspecting Arabic occupational gender-bias results.

Future work should extend the benchmark to additional Arabic dialects, include larger and newer Arabic and multilingual LLMs, evaluate black-box API models using generation-based metrics, complete larger-scale human validation, expand real-world recruitment-language evaluation, and test additional bias-mitigation methods.

Overall, the results demonstrate the need for robustness-oriented Arabic LLM fairness evaluation. Reliable occupational gender-bias measurement should combine controlled counterfactual design, dialect-aware templates, context-rich occupational framing, external validation, and reproducible software-supported analysis.
