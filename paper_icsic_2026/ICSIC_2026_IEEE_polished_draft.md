# Measuring Occupational Gender Bias in Arabic Causal Language Models Using a Dialect-Aware Counterfactual Benchmark

## Abstract

Occupational gender bias in language models can affect applications related to recruitment, professional profiling, job-advertisement generation, and Arabic natural language processing systems. Arabic introduces specific challenges for gender-bias evaluation because grammatical gender appears in nouns, verbs, adjectives, demonstratives, and agreement markers. In addition, model behavior may vary between Modern Standard Arabic and dialectal Arabic. This paper presents a dialect-aware counterfactual benchmark for measuring occupational gender bias in Arabic causal language models. The benchmark uses masculine–feminine Arabic sentence pairs that preserve the same occupational meaning while changing the gendered linguistic form. Each sentence is scored using average token log-probability, and gender preference is measured using `score_difference`, defined as `masculine_score - feminine_score`. Positive values indicate masculine preference, negative values indicate feminine preference, and zero indicates equal preference. The study evaluates Arabic-specific and multilingual causal language models across controlled occupational templates, template perturbations, job-title contexts, expanded job-role contexts, and real-world job-advertisement contexts derived from ArabJobs. The results show that measured occupational gender preference is context-sensitive and changes across model family, template formulation, dialect, semantic frame, job-title context, job-role structure, and real-world recruitment-language setting. The paper contributes a reproducible Arabic occupational gender-bias benchmark, a likelihood-based scoring pipeline for causal language models, robustness analysis across templates and dialects, and software support for Arabic bias measurement.

**Keywords—**Arabic NLP, large language models, gender bias, occupational bias, causal language models, counterfactual evaluation, Arabic dialects, likelihood-based scoring, fairness in NLP, recruitment language.

## I. Introduction

Large Language Models (LLMs) are increasingly used in natural language processing applications that generate, classify, summarize, and evaluate text. These systems are now being applied in sensitive domains such as education, recruitment, professional profiling, and decision-support workflows. As a result, fairness and bias evaluation have become important requirements for responsible language-model development. One major concern is occupational gender bias, where a model may associate specific professions, skills, responsibilities, or workplace roles more strongly with masculine or feminine language.

Occupational gender bias is especially important in recruitment-related applications. Language models may be used to generate job advertisements, summarize resumes, produce professional profiles, assist human-resource communication, or support employment-related search and recommendation systems. If these models assign systematically higher likelihood to one gendered occupational form over another, they may reproduce or amplify gendered professional associations in downstream systems.

Arabic introduces specific challenges for gender-bias evaluation. Unlike English, Arabic has grammatical gender that appears not only in nouns, but also in demonstratives, verbs, adjectives, and agreement markers. Therefore, measuring gender bias in Arabic cannot rely only on replacing one occupation word with another. A masculine occupational sentence and its feminine counterpart must remain grammatically valid and semantically equivalent. For example, the masculine sentence `هذا الطبيب يعمل في المستشفى` must be paired with the feminine sentence `هذه الطبيبة تعمل في المستشفى`, where both the occupational noun and the demonstrative are adjusted. This makes sentence-level counterfactual construction necessary for Arabic bias evaluation.

Arabic also contains substantial variation between Modern Standard Arabic (MSA) and dialectal Arabic. MSA is common in formal writing, official communication, and news, while dialectal Arabic is widely used in informal communication and digital interaction. Since language models are trained on mixed Arabic data sources, their behavior may differ across Arabic varieties. A model that shows one gender-preference pattern in MSA may show a different pattern in Egyptian Arabic. Therefore, dialect-aware evaluation is important for Arabic LLM fairness research.

This paper presents a dialect-aware counterfactual benchmark for measuring occupational gender bias in Arabic causal language models. The benchmark consists of masculine–feminine Arabic sentence pairs that preserve the same occupational meaning while changing the gendered linguistic form. The evaluation uses open-weight causal language models and computes the average token log-probability of each sentence. For each pair, the directional gender-preference score is calculated as:

`score_difference = masculine_score - feminine_score`

A positive score difference indicates that the model assigns higher likelihood to the masculine sentence. A negative value indicates higher likelihood for the feminine sentence. A zero value indicates equal preference.

The main contributions of this paper are as follows:

1. A dialect-aware Arabic occupational gender-bias benchmark based on masculine–feminine counterfactual sentence pairs.
2. A likelihood-based scoring method for Arabic causal language models using average token log-probability and a directional `score_difference` metric.
3. A multi-model evaluation across Arabic-specific and multilingual causal language models.
4. A robustness analysis across controlled templates, dialects, job-title contexts, expanded job-role contexts, and real-world recruitment-language data.
5. A reproducible software-supported pipeline for scoring, analyzing, and inspecting Arabic occupational gender-bias results.

The rest of the paper is organized as follows. Section II reviews related work. Section III presents the methodology. Section IV reports the experiments and results. Section V discusses the findings and limitations. Section VI concludes the paper.

## II. Related Work

Bias evaluation has become an important research area in natural language processing because language models can encode social associations learned from training data. These associations may appear in generated text, sentence likelihoods, word representations, or downstream system behavior. Gender bias is one of the most widely studied forms of bias, especially in occupational contexts where models may associate certain professions or professional attributes more strongly with men or women.

Early studies focused on static word embeddings and showed that vector representations can encode gender stereotypes. Bolukbasi et al. demonstrated that word embeddings contain occupational gender associations and proposed methods for quantifying and reducing gender stereotypes in embedding spaces [1]. Although embedding-based methods are useful for identifying lexical associations, they are limited for sentence-level evaluation because modern language models are contextual and generative.

Paired-sentence benchmarks provide an important foundation for bias evaluation. CrowS-Pairs measures social biases in language models using sentence pairs that differ in stereotypical association [2]. StereoSet evaluates stereotypical bias in pretrained language models by comparing stereotypical, anti-stereotypical, and unrelated alternatives [3]. The present work follows the paired-comparison logic of these benchmarks but adapts it to Arabic occupational gender bias using masculine–feminine counterfactual sentence pairs.

Likelihood-based scoring is also relevant to this work. Kurita et al. studied bias in contextualized word representations using probability-based measures [4]. Kaneko and Bollegala argued that masked-token bias metrics can be problematic and proposed All Unmasked Likelihood as an alternative for evaluating social biases in masked language models [5]. Salazar et al. introduced masked language model scoring for sentence-level likelihood estimation [6]. This paper applies likelihood-based scoring to Arabic causal language models by comparing average token log-probability across masculine and feminine sentence variants.

Arabic presents specific challenges for NLP because of its morphology, grammatical gender, and dialectal diversity. Gender is not limited to pronouns or isolated nouns; it can appear in occupational nouns, demonstratives, verbs, adjectives, and agreement markers. Recent Arabic bias work has started to address Arabic-specific evaluation. ArGAN, for example, provides an Arabic dataset for evaluating gender, ability, and nationality biases in large language models [13]. ArabJobs provides a real-world Arabic job-advertisement corpus relevant to recruitment-language analysis [14]. The present work differs by focusing on Arabic causal language models, full-sentence likelihood scoring, dialect-aware occupational templates, job-role contexts, and external job-advertisement evaluation.

Bias mitigation is another related area. Counterfactual Data Augmentation has been used to reduce gender stereotypes in morphologically rich languages [7], while self-debiasing methods have been proposed to reduce corpus-based bias in NLP systems [8]. Although mitigation is not the main focus of this conference paper, the wider project includes a counterfactual mitigation experiment using balanced masculine–feminine Arabic occupational data.

## III. Methodology

This section presents the methodology used to measure occupational gender bias in Arabic causal language models. The method is based on masculine–feminine counterfactual sentence pairs. Each pair preserves the same occupational meaning while changing the gendered linguistic form and required Arabic grammatical agreement.

Each benchmark item contains two sentences: a masculine sentence and a feminine sentence. For example:

`Masculine: هذا الطبيب يعمل في المستشفى.`

`Feminine: هذه الطبيبة تعمل في المستشفى.`

The pair changes the occupational noun from `الطبيب` to `الطبيبة` and the demonstrative from `هذا` to `هذه`. This is necessary because Arabic grammatical gender affects agreement. A valid Arabic counterfactual pair must therefore modify all required gendered elements, not only the occupation word.

The study uses multiple benchmark versions to test robustness across linguistic and occupational contexts. The v2 benchmark is the main controlled benchmark and contains 240 pairs generated from 60 occupations and four templates. The v4 benchmark contains 720 pairs and tests template sensitivity across eight templates and multiple semantic frames. The v5 benchmark contains 540 pairs and evaluates explicit job-title contexts such as CVs, job advertisements, HR records, and professional profiles. The v6 benchmark contains 2,880 pairs generated from 120 structured job roles and 24 templates. It includes metadata such as department, field, job family, seniority level, job-role type, workplace context, template type, semantic frame, and dialect. The ArabJobs v7 benchmark contains 14,532 pairs derived from real-world Arabic job-advertisement contexts.

The benchmark includes both MSA and Egyptian Arabic templates. This dialect-aware design is necessary because Arabic language models may behave differently across Arabic varieties. A model trained on mixed Arabic data may assign different likelihoods to MSA and dialectal sentence forms.

The evaluation uses open-weight causal language models. A causal language model estimates the probability of each token given the preceding tokens. For a sentence:

`x = (w_1, w_2, ..., w_n)`

the sentence score is defined as average token log-probability:

`S(x) = (1 / n) Σ log P(w_t | w_<t)`

where `n` is the number of tokens in the sentence and `P(w_t | w_<t)` is the probability assigned to token `w_t` given the previous tokens. Average token log-probability is used instead of total sentence probability to reduce sentence-length effects.

For each masculine–feminine pair, the score difference is computed as:

`score_difference = masculine_score - feminine_score`

The interpretation is:

`score_difference > 0`: masculine preference.

`score_difference < 0`: feminine preference.

`score_difference = 0`: equal preference.

For each model and benchmark, the analysis reports total items, masculine-preferred count, feminine-preferred count, equal count, masculine-preferred percentage, feminine-preferred percentage, average score difference, median score difference, and score-difference range.

The project also includes validation and quality-control checks. Benchmark quality checks verify required columns, row counts, sentence completeness, dialect labels, template distributions, and metadata fields. Score-difference validation checks that the stored score difference is correctly computed as masculine score minus feminine score. Preference-label validation checks that the preferred-gender label matches the sign of the score difference. Token-length control checks whether masculine and feminine sentence variants have balanced word counts.

## IV. Experiments and Results

### A. Experimental Setup

The experiments evaluate Arabic-specific and multilingual causal language models. The evaluated models include AraGPT2-base, AraGPT2-medium, BLOOM-560m, BLOOM-1b1, XGLM-564M, and Qwen2.5-0.5B.

**Table I. Evaluated benchmark settings**

| Benchmark   | Description                                     |  Pairs |
| ----------- | ----------------------------------------------- | -----: |
| v2          | Main controlled occupational benchmark          |    240 |
| v4          | Template perturbation benchmark                 |    720 |
| v5          | Job-title benchmark                             |    540 |
| v6          | Expanded job-role and department benchmark      |  2,880 |
| ArabJobs v7 | External real-world job-advertisement benchmark | 14,532 |

### B. v2 Main Controlled Benchmark

**Table II. Overall results on the v2 benchmark**

| Model             | M Pref. | F Pref. | Equal | Avg. Diff. | Direction |
| ----------------- | ------: | ------: | ----: | ---------: | --------- |
| Qwen/Qwen2.5-0.5B |      80 |     158 |     2 |     -0.343 | F         |
| AraGPT2-base      |     152 |      88 |     0 |      0.126 | M         |
| AraGPT2-medium    |     168 |      72 |     0 |      0.223 | M         |
| BLOOM-1b1         |      91 |     147 |     2 |     -0.166 | F         |
| BLOOM-560m        |      83 |     157 |     0 |     -0.217 | F         |
| XGLM-564M         |      92 |     148 |     0 |     -0.214 | F         |

The v2 benchmark shows a clear difference between Arabic-specific and multilingual models. AraGPT2-base and AraGPT2-medium show masculine preference, while the multilingual models show feminine preference. At the model-family level, Arabic-specific models produce 320 masculine preferences and 160 feminine preferences, with an average score difference of 0.174. Non-Arabic-specific multilingual models produce 346 masculine preferences, 610 feminine preferences, and 4 equal preferences, with an average score difference of -0.235. A chi-square test shows a significant association between model family and preferred gender: `χ² = 118.109, p = 1.641 × 10^-27`.

### C. v4 Template Perturbation Benchmark

**Table III. Overall results on the v4 benchmark**

| Model             | M Pref. | F Pref. | Equal | Avg. Diff. | Direction |
| ----------------- | ------: | ------: | ----: | ---------: | --------- |
| Qwen/Qwen2.5-0.5B |     312 |     390 |    18 |     -0.089 | F         |
| AraGPT2-base      |     220 |     500 |     0 |     -0.348 | F         |
| AraGPT2-medium    |     290 |     430 |     0 |     -0.303 | F         |
| BLOOM-1b1         |     248 |     467 |     5 |     -0.170 | F         |
| BLOOM-560m        |     256 |     460 |     4 |     -0.170 | F         |
| XGLM-564M         |     104 |     614 |     2 |     -0.441 | F         |

Unlike v2, all six models show overall feminine preference on v4. This is important because the AraGPT2 models shift from masculine preference in v2 to feminine preference in v4, showing that benchmark formulation can change the measured direction of gender preference.

### D. Template and Dialect Sensitivity

All evaluated models show direction changes across templates in v4.

**Table IV. Template direction changes in v4**

| Model             | M Templates | F Templates | Range |
| ----------------- | ----------: | ----------: | ----: |
| Qwen/Qwen2.5-0.5B |           4 |           4 | 1.105 |
| AraGPT2-base      |           2 |           6 | 1.320 |
| AraGPT2-medium    |           2 |           6 | 1.223 |
| BLOOM-1b1         |           1 |           7 | 1.363 |
| BLOOM-560m        |           2 |           6 | 1.412 |
| XGLM-564M         |           1 |           7 | 0.729 |

The largest template range is observed for BLOOM-560m, with a range of 1.412. This confirms that template wording strongly affects measured occupational gender preference.

Dialect-level analysis also shows important shifts.

**Table V. Dialect-level average score differences in v4**

| Model             | MSA Avg. | Egyptian Avg. |  Shift |
| ----------------- | -------: | ------------: | -----: |
| Qwen/Qwen2.5-0.5B |   -0.336 |         0.158 |  0.493 |
| AraGPT2-base      |   -0.290 |        -0.407 | -0.117 |
| AraGPT2-medium    |   -0.191 |        -0.416 | -0.225 |
| BLOOM-1b1         |   -0.273 |        -0.067 |  0.207 |
| BLOOM-560m        |   -0.394 |         0.053 |  0.447 |
| XGLM-564M         |   -0.398 |        -0.485 | -0.087 |

Qwen2.5-0.5B and BLOOM-560m shift from feminine preference in MSA to masculine preference in Egyptian Arabic. This result supports the need for dialect-aware Arabic bias evaluation.

### E. Job-Title and Job-Role Benchmarks

**Table VI. Results on the v5 job-title benchmark**

| Model        | M Pref. | F Pref. | Equal | Avg. Diff. | Direction |
| ------------ | ------: | ------: | ----: | ---------: | --------- |
| AraGPT2-base |     284 |     256 |     0 |     -0.034 | Mixed     |
| BLOOM-560m   |     278 |     261 |     1 |      0.071 | Weak M    |

The v5 results differ from v4. AraGPT2-base becomes near-neutral, while BLOOM-560m shows weak masculine preference. This suggests that explicit job-title contexts behave differently from general occupational sentence templates.

**Table VII. Results on the v6 expanded job-role benchmark**

| Model          | M Pref. | F Pref. | Equal | Avg. Diff. | Direction |
| -------------- | ------: | ------: | ----: | ---------: | --------- |
| AraGPT2-base   |     970 |    1910 |     0 |     -0.302 | F         |
| AraGPT2-medium |    1136 |    1744 |     0 |     -0.244 | F         |
| BLOOM-1b1      |    1328 |    1547 |     5 |     -0.081 | F         |
| BLOOM-560m     |    1500 |    1375 |     5 |     -0.016 | Mixed     |

The v6 benchmark shows mostly feminine or near-neutral patterns. AraGPT2-base and AraGPT2-medium both show feminine preference, contrasting with their masculine preference in v2. This shows that expanded occupational context changes the measured direction and magnitude of gender preference.

### F. ArabJobs v7 External Benchmark

**Table VIII. AraGPT2-base result on ArabJobs v7**

| Model        |  Items | M Pref. | F Pref. | Avg. Diff. | Direction |
| ------------ | -----: | ------: | ------: | ---------: | --------- |
| AraGPT2-base | 14,532 |   8,404 |   6,128 |      0.089 | M         |

AraGPT2-base shows masculine preference on ArabJobs v7, with 57.83% masculine-preferred pairs and 42.17% feminine-preferred pairs. This contrasts with v6, where the same model shows feminine preference with an average score difference of -0.302. The contrast suggests that real-world recruitment-language contexts can produce different gender-preference patterns from controlled benchmark contexts.

### G. Token-Length Control and Factor Sensitivity

Token-length control shows that masculine and feminine variants have identical mean word counts in v6 and ArabJobs v7 outputs. The same-word-count percentage is 100% for all evaluated v6 and ArabJobs v7 model outputs. Therefore, the observed score differences cannot be explained by simple word-count imbalance.

Factor sensitivity analysis shows that template type and semantic frame are the strongest factors in v6, each with a range of 1.248 across group means. In ArabJobs v7, job family and job-role type are the strongest factors, with ranges of 0.974 and 0.913 respectively. These results reinforce the conclusion that Arabic occupational gender-bias measurement depends on linguistic and occupational framing.

### H. Mitigation Experiment

The wider project includes a counterfactual data augmentation mitigation experiment. AraGPT2-base was fine-tuned on balanced masculine–feminine Arabic occupational sentences and evaluated before and after mitigation.

**Table IX. Counterfactual mitigation results**

| Benchmark     | Before Avg. | After Avg. | Before Dir. | After Dir. |   Gain | Reduced |
| ------------- | ----------: | ---------: | ----------- | ---------- | -----: | ------- |
| v2 main       |       0.126 |     -0.051 | M           | F          |  0.075 | Yes     |
| v5 job titles |      -0.034 |      0.035 | Mixed       | Mixed      | -0.001 | No      |
| v6 job roles  |      -0.302 |     -0.053 | F           | F          |  0.249 | Yes     |
| ArabJobs v7   |       0.089 |     -0.192 | M           | F          | -0.103 | No      |

The mitigation experiment reduces absolute bias in v2 and v6, but not in v5 or ArabJobs v7. This suggests that counterfactual data augmentation can reduce measured bias in some controlled settings, but mitigation does not generalize uniformly across all contexts.

## V. Discussion

The results show that Arabic occupational gender-bias measurement is highly sensitive to linguistic and occupational context. The same model can produce different gender-preference directions depending on benchmark version, template wording, dialect, semantic frame, job-title context, job-role structure, and real-world recruitment-language setting.

The v2 benchmark shows that model family can affect measured preference. Arabic-specific AraGPT2 models lean masculine, while multilingual models lean feminine. However, this pattern does not remain stable across all benchmarks. In v4 and v6, AraGPT2 models shift toward feminine preference. This means that model family is important but does not fully determine bias direction.

Template wording is one of the strongest factors affecting the score. In v4, every evaluated model shows template-induced direction changes. Therefore, bias evaluation using only one or two templates may produce results that are strongly dependent on the selected wording. Arabic occupational gender-bias benchmarks should include multiple templates and report template-level results.

Dialect also matters. Some models shift between MSA and Egyptian Arabic. This confirms that Arabic should not be treated as a single homogeneous variety in fairness evaluation. Since LLMs are trained on mixed Arabic sources, dialect-aware evaluation is necessary.

The v5 and v6 benchmarks show that occupational context matters. Job-title contexts behave differently from general occupational sentences, and structured job-role contexts produce different patterns from simple occupation templates. This is important for recruitment-related applications because job titles, departments, and professional responsibilities are common in employment language.

The ArabJobs v7 result shows the value of real-world evaluation. Controlled benchmarks provide internal validity, but real-world job advertisements contain natural recruitment phrasing, country-specific wording, and labor-market language. External job-advertisement evaluation should therefore complement controlled benchmarks.

The study has limitations. It focuses on open-weight causal language models because likelihood scoring requires access to model loss or token probabilities. It focuses on binary masculine–feminine grammatical forms because of Arabic morphology. Egyptian Arabic is the only dialectal variety included beyond MSA. The ArabJobs-derived benchmark improves ecological validity but may contain real-world noise. Finally, the human-validation package is prepared, but final annotation agreement should be completed before an extended journal version.

## VI. Conclusion

This paper presented a dialect-aware counterfactual benchmark for measuring occupational gender bias in Arabic causal language models. The benchmark uses masculine–feminine Arabic sentence pairs that preserve the same occupational meaning while changing the gendered linguistic form and required grammatical agreement. Each sentence is scored using average token log-probability, and gender preference is measured using `score_difference`.

The results show that Arabic occupational gender preference is context-sensitive. Arabic-specific and multilingual models differ in the main controlled benchmark, but these patterns change across template perturbations, dialects, job-title contexts, expanded job-role contexts, and real-world job-advertisement settings. These findings suggest that Arabic occupational gender-bias scores should not be interpreted as fixed model properties. Instead, they should be understood as measurement outcomes affected by model family, template wording, dialect, semantic frame, job-title context, job-role structure, and recruitment-language setting.

Future work should extend the benchmark to additional Arabic dialects, include larger and newer Arabic and multilingual LLMs, evaluate black-box API models using generation-based metrics, complete larger-scale human validation, expand real-world recruitment-language evaluation, and test additional bias-mitigation methods.

## References

[1] T. Bolukbasi, K.-W. Chang, J. Zou, V. Saligrama, and A. Kalai, “Man is to computer programmer as woman is to homemaker? Debiasing word embeddings,” in *Advances in Neural Information Processing Systems 29*, 2016, pp. 4349–4357.

[2] N. Nangia, C. Vania, R. Bhalerao, and S. R. Bowman, “CrowS-Pairs: A challenge dataset for measuring social biases in masked language models,” in *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing*, 2020, pp. 1953–1967.

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

[13] R. Aly, Y. Allam, R. Gaber, and C. Basta, “ArGAN: Arabic gender, ability, and nationality dataset for evaluating biases in large language models,” in *Proceedings of the 6th Workshop on Gender Bias in Natural Language Processing*, 2025, pp. 256–267.

[14] M. El-Haj, “ArabJobs: A multinational corpus of Arabic job ads,” in *Proceedings of The Third Arabic Natural Language Processing Conference*, 2025, pp. 16–25.
