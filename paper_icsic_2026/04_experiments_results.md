# 4. Experiments and Results

## 4.1 Experimental Setup

The experiments evaluate occupational gender preference in Arabic causal language models using masculine–feminine counterfactual sentence pairs. Each pair contains two Arabic sentences with the same occupational meaning, where one sentence uses the masculine form and the other uses the feminine form. The models are scored using average token log-probability, and gender preference is measured using:

`score_difference = masculine_score - feminine_score`

A positive value indicates masculine preference, a negative value indicates feminine preference, and zero indicates equal preference.

The evaluation includes Arabic-specific and multilingual causal language models. The main evaluated models are:

| Model                     | Model Type                     |
| ------------------------- | ------------------------------ |
| aubmindlab/aragpt2-base   | Arabic-specific causal LM      |
| aubmindlab/aragpt2-medium | Arabic-specific causal LM      |
| bigscience/bloom-560m     | Multilingual causal LM         |
| bigscience/bloom-1b1      | Multilingual causal LM         |
| facebook/xglm-564M        | Multilingual causal LM         |
| Qwen/Qwen2.5-0.5B         | Multilingual/general causal LM |

The experiments are organized across multiple benchmark settings:

| Benchmark   | Description                                     | Number of Pairs |
| ----------- | ----------------------------------------------- | --------------: |
| v2          | Main controlled occupational benchmark          |             240 |
| v4          | Template perturbation benchmark                 |             720 |
| v5          | Job-title benchmark                             |             540 |
| v6          | Expanded job-role and department benchmark      |           2,880 |
| ArabJobs v7 | External real-world job-advertisement benchmark |          14,532 |

This design allows the study to compare model behavior across controlled templates, dialect-aware examples, job-title contexts, expanded job-role contexts, and real-world recruitment-language data.

## 4.2 v2 Main Controlled Benchmark

The v2 benchmark contains 240 counterfactual sentence pairs generated from 60 occupations and four templates. It provides the main controlled baseline for comparing Arabic-specific and multilingual causal language models.

The overall v2 results are shown in Table 1.

**Table 1. Overall results on the v2 main benchmark**

| Model                     | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Direction |
| ------------------------- | ------------------: | -----------------: | ----: | -----------------------: | --------- |
| Qwen/Qwen2.5-0.5B         |                  80 |                158 |     2 |                   -0.343 | Feminine  |
| aubmindlab/aragpt2-base   |                 152 |                 88 |     0 |                    0.126 | Masculine |
| aubmindlab/aragpt2-medium |                 168 |                 72 |     0 |                    0.223 | Masculine |
| bigscience/bloom-1b1      |                  91 |                147 |     2 |                   -0.166 | Feminine  |
| bigscience/bloom-560m     |                  83 |                157 |     0 |                   -0.217 | Feminine  |
| facebook/xglm-564M        |                  92 |                148 |     0 |                   -0.214 | Feminine  |

The v2 benchmark shows a clear difference between Arabic-specific and multilingual models. The Arabic-specific AraGPT2 models show masculine preference, while the multilingual models show feminine preference. AraGPT2-medium has the strongest masculine average score difference at 0.223, while Qwen/Qwen2.5-0.5B has the strongest feminine average score difference at -0.343.

At the model-family level, the Arabic-specific models produce 320 masculine preferences and 160 feminine preferences, with an average score difference of 0.174. The non-Arabic-specific multilingual models produce 346 masculine preferences, 610 feminine preferences, and 4 equal preferences, with an average score difference of -0.235.

A chi-square test shows a statistically significant association between model family and preferred gender:

`χ² = 118.109, p = 1.641 × 10^-27`

This indicates that the distribution of masculine and feminine preferences differs significantly between Arabic-specific and multilingual model families in the v2 benchmark.

## 4.3 v4 Template Perturbation Benchmark

The v4 benchmark evaluates whether measured gender preference is stable across template wording and semantic framing. It contains 720 pairs generated from 90 occupations and eight templates.

The overall v4 results are shown in Table 2.

**Table 2. Overall results on the v4 template perturbation benchmark**

| Model                     | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Direction |
| ------------------------- | ------------------: | -----------------: | ----: | -----------------------: | --------- |
| Qwen/Qwen2.5-0.5B         |                 312 |                390 |    18 |                   -0.089 | Feminine  |
| aubmindlab/aragpt2-base   |                 220 |                500 |     0 |                   -0.348 | Feminine  |
| aubmindlab/aragpt2-medium |                 290 |                430 |     0 |                   -0.303 | Feminine  |
| bigscience/bloom-1b1      |                 248 |                467 |     5 |                   -0.170 | Feminine  |
| bigscience/bloom-560m     |                 256 |                460 |     4 |                   -0.170 | Feminine  |
| facebook/xglm-564M        |                 104 |                614 |     2 |                   -0.441 | Feminine  |

Unlike the v2 benchmark, all six models show overall feminine preference on v4. This is important because the Arabic-specific AraGPT2 models shift from masculine preference in v2 to feminine preference in v4. This result shows that benchmark formulation can change the measured direction of gender preference.

## 4.4 Template-Induced Direction Changes

The v4 benchmark also reveals that all evaluated models show direction changes across templates. This means that the same model can prefer masculine variants in some templates and feminine variants in others.

**Table 3. Template direction changes in v4**

| Model                     | Masculine-Direction Templates | Feminine-Direction Templates | Direction Change | Range of Template Means |
| ------------------------- | ----------------------------: | ---------------------------: | ---------------- | ----------------------: |
| Qwen/Qwen2.5-0.5B         |                             4 |                            4 | Yes              |                   1.105 |
| aubmindlab/aragpt2-base   |                             2 |                            6 | Yes              |                   1.320 |
| aubmindlab/aragpt2-medium |                             2 |                            6 | Yes              |                   1.223 |
| bigscience/bloom-1b1      |                             1 |                            7 | Yes              |                   1.363 |
| bigscience/bloom-560m     |                             2 |                            6 | Yes              |                   1.412 |
| facebook/xglm-564M        |                             1 |                            7 | Yes              |                   0.729 |

The largest template range is observed for BLOOM-560m, with a range of 1.412 across template means. AraGPT2-base also shows high template sensitivity, with a range of 1.320. These results show that template wording is one of the strongest factors affecting measured occupational gender preference.

## 4.5 Dialect Sensitivity

The v4 benchmark includes both Modern Standard Arabic and Egyptian Arabic templates. The dialect-level analysis shows that some models change direction or magnitude depending on the Arabic variety.

**Table 4. Dialect-level average score differences in v4**

| Model                     | MSA Average | Egyptian Average | Dialect Shift |
| ------------------------- | ----------: | ---------------: | ------------: |
| Qwen/Qwen2.5-0.5B         |      -0.336 |            0.158 |         0.493 |
| aubmindlab/aragpt2-base   |      -0.290 |           -0.407 |        -0.117 |
| aubmindlab/aragpt2-medium |      -0.191 |           -0.416 |        -0.225 |
| bigscience/bloom-1b1      |      -0.273 |           -0.067 |         0.207 |
| bigscience/bloom-560m     |      -0.394 |            0.053 |         0.447 |
| facebook/xglm-564M        |      -0.398 |           -0.485 |        -0.087 |

Qwen/Qwen2.5-0.5B and BLOOM-560m shift from feminine preference in MSA to masculine preference in Egyptian Arabic. This result supports the need for dialect-aware Arabic bias evaluation. A model’s behavior in MSA does not necessarily represent its behavior in dialectal Arabic.

## 4.6 v5 Job-Title Benchmark

The v5 benchmark evaluates explicit job-title contexts such as CVs, job advertisements, HR records, and professional profiles. It contains 540 counterfactual pairs.

**Table 5. Results on the v5 job-title benchmark**

| Model                   | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Direction            |
| ----------------------- | ------------------: | -----------------: | ----: | -----------------------: | -------------------- |
| aubmindlab/aragpt2-base |                 284 |                256 |     0 |                   -0.034 | Near-neutral / Mixed |
| bigscience/bloom-560m   |                 278 |                261 |     1 |                    0.071 | Weak Masculine       |

The v5 results differ from the v4 results. In v4, both AraGPT2-base and BLOOM-560m show feminine preference. In v5, AraGPT2-base becomes near-neutral, while BLOOM-560m shows weak masculine preference. This suggests that job-title contexts behave differently from general occupational sentence templates.

## 4.7 v6 Expanded Job-Role Benchmark

The v6 benchmark expands the evaluation to structured job roles and departments. It contains 2,880 pairs generated from 120 job roles and 24 templates. The benchmark includes metadata such as department, field, job family, seniority level, job-role type, workplace context, semantic frame, and dialect.

**Table 6. Results on the v6 expanded job-role benchmark**

| Model                     | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Direction            |
| ------------------------- | ------------------: | -----------------: | ----: | -----------------------: | -------------------- |
| aubmindlab/aragpt2-base   |                 970 |               1910 |     0 |                   -0.302 | Feminine             |
| aubmindlab/aragpt2-medium |                1136 |               1744 |     0 |                   -0.244 | Feminine             |
| bigscience/bloom-1b1      |                1328 |               1547 |     5 |                   -0.081 | Feminine             |
| bigscience/bloom-560m     |                1500 |               1375 |     5 |                   -0.016 | Near-neutral / Mixed |

The v6 benchmark shows mostly feminine or near-neutral patterns. AraGPT2-base and AraGPT2-medium both show feminine preference, which contrasts with their masculine preference in the v2 main benchmark. BLOOM-560m is close to neutral, with an average score difference of -0.016.

These results show that expanded occupational context changes the measured direction and magnitude of gender preference. Job roles, departments, professional responsibilities, and workplace framing are therefore important factors in Arabic occupational bias evaluation.

## 4.8 ArabJobs v7 External Real-World Benchmark

The ArabJobs v7 benchmark evaluates real-world Arabic job-advertisement contexts. It contains 14,532 counterfactual pairs derived from matched ArabJobs data.

**Table 7. AraGPT2-base result on ArabJobs v7**

| Model                   | Total Items | Masculine Preferred | Feminine Preferred | Average Score Difference | Direction |
| ----------------------- | ----------: | ------------------: | -----------------: | -----------------------: | --------- |
| aubmindlab/aragpt2-base |      14,532 |               8,404 |              6,128 |                    0.089 | Masculine |

AraGPT2-base shows masculine preference on ArabJobs v7, with 57.83% masculine-preferred pairs and 42.17% feminine-preferred pairs. The average score difference is 0.089.

This result contrasts with v6, where AraGPT2-base shows feminine preference with an average score difference of -0.302. The contrast suggests that real-world recruitment-language contexts can produce different gender-preference patterns from controlled benchmark contexts.

## 4.9 Controlled vs Real-World Comparison

The comparison between v6 and ArabJobs v7 is important because both are occupational and recruitment-related, but they differ in data source and linguistic naturalness.

**Table 8. AraGPT2-base comparison across controlled and external contexts**

| Benchmark                | Total Items | Average Score Difference | Direction            |
| ------------------------ | ----------: | -----------------------: | -------------------- |
| v2 main benchmark        |         240 |                    0.126 | Masculine            |
| v4 template perturbation |         720 |                   -0.348 | Feminine             |
| v5 job titles            |         540 |                   -0.034 | Near-neutral / Mixed |
| v6 job roles             |       2,880 |                   -0.302 | Feminine             |
| ArabJobs v7 external     |      14,532 |                    0.089 | Masculine            |

The same model changes direction across benchmark settings. AraGPT2-base is masculine-leaning in v2, feminine-leaning in v4, near-neutral in v5, feminine-leaning in v6, and masculine-leaning in ArabJobs v7. This confirms that measured gender preference is context-dependent.

## 4.10 Token-Length Control

A token-length control analysis was conducted to examine whether score differences could be explained by simple word-count differences between masculine and feminine sentence variants.

The analysis showed that masculine and feminine sentence variants had identical mean word counts in the v6 and ArabJobs v7 evaluated outputs.

**Table 9. Word-count control results**

| Dataset      | Model                     | Total Items | Mean Masculine Word Count | Mean Feminine Word Count | Same Word Count |
| ------------ | ------------------------- | ----------: | ------------------------: | -----------------------: | --------------: |
| ArabJobs v7  | aubmindlab/aragpt2-base   |      14,532 |                     8.669 |                    8.669 |          100.0% |
| ArabJobs v7  | bigscience/bloom-560m     |      14,532 |                     8.669 |                    8.669 |          100.0% |
| v6 job roles | aubmindlab/aragpt2-base   |       2,880 |                     8.625 |                    8.625 |          100.0% |
| v6 job roles | aubmindlab/aragpt2-medium |       2,880 |                     8.625 |                    8.625 |          100.0% |
| v6 job roles | bigscience/bloom-1b1      |       2,880 |                     8.625 |                    8.625 |          100.0% |
| v6 job roles | bigscience/bloom-560m     |       2,880 |                     8.625 |                    8.625 |          100.0% |

Since the word-count difference is zero in these evaluated outputs, the observed score differences cannot be explained by simple word-count imbalance. This supports the interpretation that measured preferences reflect model likelihood differences under controlled linguistic conditions rather than sentence-length artifacts.

## 4.11 Factor Sensitivity

A factor sensitivity analysis was conducted for v6 and ArabJobs v7. The analysis measures the range of average score differences across levels of each factor. Larger ranges indicate stronger sensitivity.

**Table 10. Strongest factor sensitivities**

| Dataset      | Factor         | Levels | Range of Group Means | Strongest Feminine Level | Strongest Masculine Level |
| ------------ | -------------- | -----: | -------------------: | ------------------------ | ------------------------- |
| v6 job roles | template_type  |     14 |                1.248 | daily_work_context       | job_title_record          |
| v6 job roles | semantic_frame |     13 |                1.248 | routine_work             | formal_record             |
| v6 job roles | job_family     |    109 |                0.836 | nursing                  | digital_marketing         |
| v6 job roles | job_role_type  |     37 |                0.604 | technical_specialist     | technical_role            |
| ArabJobs v7  | job_family     |     51 |                0.974 | pharmacy                 | administration            |
| ArabJobs v7  | job_role_type  |     26 |                0.913 | clinical_support_role    | administrative_role       |
| ArabJobs v7  | template_type  |      6 |                0.556 | application_context      | recruitment_context       |
| ArabJobs v7  | semantic_frame |      6 |                0.556 | candidate_application    | hiring_language           |

In v6, template type and semantic frame are the strongest sensitivity factors, both with a range of 1.248. In ArabJobs v7, job family and job-role type are the strongest sensitivity factors, with ranges of 0.974 and 0.913 respectively.

These findings reinforce the main conclusion that Arabic occupational gender-bias measurement depends heavily on linguistic and occupational framing.

## 4.12 Mitigation Experiment

The wider project includes a counterfactual data augmentation mitigation experiment. AraGPT2-base was fine-tuned on balanced masculine–feminine Arabic occupational sentences and evaluated before and after mitigation.

**Table 11. Counterfactual mitigation results**

| Benchmark            | Before Avg Difference | After Avg Difference | Before Direction     | After Direction      | Mitigation Gain | Bias Reduced |
| -------------------- | --------------------: | -------------------: | -------------------- | -------------------- | --------------: | ------------ |
| v2 main              |                 0.126 |               -0.051 | Masculine            | Feminine             |           0.075 | Yes          |
| v5 job titles        |                -0.034 |                0.035 | Near-neutral / Mixed | Near-neutral / Mixed |          -0.001 | No           |
| v6 job roles         |                -0.302 |               -0.053 | Feminine             | Feminine             |           0.249 | Yes          |
| ArabJobs v7 external |                 0.089 |               -0.192 | Masculine            | Feminine             |          -0.103 | No           |

The mitigation experiment reduces absolute bias in v2 and v6, but not in v5 or ArabJobs v7. The strongest reduction is observed in v6, where absolute bias decreases from 0.302 to 0.053. However, the ArabJobs v7 result shows that mitigation does not generalize uniformly to real-world recruitment-language contexts.

This result suggests that counterfactual data augmentation can reduce measured bias in some controlled settings, but mitigation must be evaluated across multiple contexts before being considered reliable.

## 4.13 Summary of Findings

The experiments show five main findings.

First, Arabic causal language models show measurable occupational gender preference under paired likelihood evaluation.

Second, model family affects measured preference. In the v2 benchmark, Arabic-specific AraGPT2 models lean masculine, while multilingual models lean feminine.

Third, template formulation strongly affects measured bias. In v4, all evaluated models show template-induced direction changes.

Fourth, dialect affects model behavior. Some models shift between MSA and Egyptian Arabic.

Fifth, controlled and real-world recruitment-language settings can produce different results. AraGPT2-base leans feminine on v6 but masculine on ArabJobs v7.

Overall, the results support the main claim of the paper: Arabic occupational gender-bias scores should not be interpreted as fixed model properties. They are context-sensitive measurement outcomes affected by model family, template wording, dialect, semantic frame, job-title context, job-role structure, and real-world recruitment-language setting.
