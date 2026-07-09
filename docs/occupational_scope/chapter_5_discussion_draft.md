# Chapter 5 — Discussion

## 5.1 Introduction

This chapter discusses the findings presented in Chapter 4.

The thesis evaluated occupational gender bias in Arabic causal language models using a controlled counterfactual benchmark. The main result shows that Arabic-specific AraGPT2 models prefer masculine occupational sentences, while non-Arabic-specific multilingual/general models prefer feminine occupational sentences.

The discussion focuses on the interpretation of this model-family difference, the role of occupational fields, the importance of Arabic gender morphology, and the contribution of external dataset pilots.

---

## 5.2 Interpretation of the Main Finding

The main finding is that gender-preference direction differs by model family.

Arabic-specific models showed a masculine preference:

| Model Family    | Masculine Preferred | Feminine Preferred | Direction |
| --------------- | ------------------: | -----------------: | --------- |
| Arabic-specific |                 320 |                160 | Masculine |

Non-Arabic-specific models showed a feminine preference:

| Model Family        | Masculine Preferred | Feminine Preferred | Direction |
| ------------------- | ------------------: | -----------------: | --------- |
| Non-Arabic-specific |                 346 |                610 | Feminine  |

This means that occupational gender bias is not uniform across language models. The direction of bias changes depending on the model family and pretraining background.

The chi-square result supports this interpretation:

```text
chi-square p-value = 1.64e-27
```

This highly significant result indicates that the association between model family and preference direction is unlikely to be random.

---

## 5.3 Why Model Family May Matter

The difference between Arabic-specific and non-Arabic-specific models may be related to several factors.

First, the models were trained on different corpora. Arabic-specific models are more likely to have seen Arabic occupational forms in Arabic-focused contexts. Non-Arabic-specific models may represent Arabic through a broader multilingual distribution.

Second, tokenization may affect Arabic gendered forms differently. Arabic words often encode gender morphologically, such as:

```text
مهندس / مهندسة
طبيب / طبيبة
مدير / مديرة
```

A model’s tokenizer may split these words differently, which can affect likelihood scoring.

Third, the models may have learned different distributions for masculine and feminine occupational terms. If masculine forms are more frequent in Arabic occupational contexts, Arabic-specific models may assign higher probability to masculine sentences. On the other hand, multilingual/general models may behave differently because their Arabic representations are shaped by cross-lingual training data.

Therefore, the result should not be interpreted as a simple property of Arabic language only. It is also a property of the model, its tokenizer, and its training distribution.

---

## 5.4 Feminine Preference Is Still Bias

An important point is that feminine preference does not automatically mean fairness.

In this thesis, the masculine and feminine sentence versions are designed to be semantically equivalent. Therefore, a systematic preference in either direction indicates directional bias.

A model can be biased toward masculine forms or biased toward feminine forms. The fairness issue is the existence of systematic preference when the content is controlled.

For this reason, the BLOOM, XGLM, and Qwen results are not interpreted as “fair” simply because they prefer feminine sentences. They are interpreted as showing a different direction of bias compared with AraGPT2.

---

## 5.5 Field-Level Interpretation

The results also show that bias is field-dependent.

For Arabic-specific models, masculine preference was stronger in fields such as:

* Business,
* Legal/Government,
* STEM,
* Media/Creative.

For non-Arabic-specific models, feminine preference was stronger in fields such as:

* Education,
* Healthcare,
* Media/Creative.

This suggests that occupational gender bias cannot be fully understood using only one overall score. The professional field matters.

A model may show strong masculine preference in one domain but weaker or even opposite preference in another domain. Therefore, field-level analysis gives a more precise view of model behavior.

---

## 5.6 Arabic Gender Morphology and Bias Measurement

Arabic makes gender-bias measurement more complex than English because gender appears in many linguistic forms.

Gender can appear in:

* pronouns,
* nouns,
* occupation names,
* verbs,
* adjectives,
* demonstratives.

Examples include:

```text
هو / هي
هذا / هذه
مهندس / مهندسة
محترف / محترفة
يعمل / تعمل
```

Because of this, Arabic bias evaluation cannot rely only on replacing pronouns. The whole sentence must be checked for grammatical agreement.

The counterfactual design used in this thesis addresses this issue by constructing complete masculine/feminine sentence pairs with controlled agreement.

---

## 5.7 Value of the Counterfactual Design

The benchmark is based on counterfactual comparison.

Each item has:

* the same occupation,
* the same field,
* the same context,
* the same template,
* different grammatical gender.

This allows the analysis to isolate gender as the main variable.

The sentence-pair design is stronger than simple word-frequency comparison because it evaluates model preference in context.

For example, comparing only the words `مهندس` and `مهندسة` is less informative than comparing complete sentences such as:

```text
هذا مهندس يعمل في الشركة
هذه مهندسة تعمل في الشركة
```

The sentence-level design better reflects how language models process real text.

---

## 5.8 v1 vs v2 Stability

The thesis first used a smaller pilot benchmark, v1, containing 36 occupations and 144 sentence pairs.

The benchmark was then expanded to v2 with 60 occupations and 240 sentence pairs.

The main model-family pattern remained stable across both versions:

> Arabic-specific models leaned masculine, while non-Arabic-specific models leaned feminine.

This stability supports the reliability of the benchmark design.

v2 was selected as the final benchmark because it has broader occupational coverage while preserving the same controlled sentence-pair methodology.

---

## 5.9 Contribution of Extra Models

The original experiment used four models:

* AraGPT2-base,
* AraGPT2-medium,
* BLOOM-560m,
* BLOOM-1b1.

The enriched experiment added:

* XGLM-564M,
* Qwen2.5-0.5B.

The two additional non-Arabic-specific models also showed overall feminine occupational preference.

This strengthens the thesis because the feminine preference pattern is not limited to the BLOOM model family. It also appears in other non-Arabic-specific causal language models.

Therefore, the enriched six-model analysis provides stronger evidence for a model-family effect.

---

## 5.10 Role of External Dataset Pilots

Two external dataset pilots were added:

1. APGC-format pilot,
2. ArGAN-format pilot.

These pilots are not replacements for the main occupational benchmark. They are used to test whether the evaluation pipeline can be extended to external Arabic gender-bias resources.

---

## 5.11 APGC-Format Pilot Discussion

The APGC-format pilot tested the sentence-pair scoring pipeline on broader Arabic grammatical-gender examples.

The pilot contained 10 masculine/feminine sentence pairs.

The results were mixed:

| Model          | Direction          |
| -------------- | ------------------ |
| AraGPT2-base   | Masculine by count |
| AraGPT2-medium | Masculine by count |
| BLOOM-560m     | Almost balanced    |
| BLOOM-1b1      | Balanced           |
| XGLM-564M      | Feminine           |
| Qwen2.5-0.5B   | Feminine           |

Because the pilot contains only 10 pairs, it should not be treated as a final statistical result.

However, it is useful because it confirms that the scoring method can be applied beyond occupations. This prepares the thesis for future integration with the full APGC dataset.

---

## 5.12 ArGAN-Format Pilot Discussion

The ArGAN-format pilot tested prompt-based Arabic gender-bias evaluation.

Unlike the occupational benchmark, ArGAN-style evaluation requires generation and output annotation.

The improved pilot used Qwen2.5-0.5B-Instruct.

The generation-quality analysis showed:

| Metric                        | Value |
| ----------------------------- | ----: |
| Total outputs                 |    10 |
| Empty outputs                 |     0 |
| Prompt echo outputs           |     0 |
| Repetition outputs            |     0 |
| Gender mismatch outputs       |     2 |
| Outputs needing manual review |     2 |
| Needs manual review percent   |   20% |
| Average output word count     |    23 |

These results show that prompt-based Arabic bias evaluation is possible, but it depends heavily on instruction-following quality.

Therefore, ArGAN is reported as a qualitative external pilot rather than a final quantitative result.

---

## 5.13 Why the Occupational Benchmark Remains the Main Result

The occupational benchmark remains the main thesis benchmark for three reasons.

First, it is controlled. Each sentence pair differs mainly in gender, while the occupation, field, template, and context remain constant.

Second, it supports direct quantitative scoring. Causal language models can assign likelihood scores to both sentence versions.

Third, the results are statistically tested across six models and 240 sentence pairs.

The external pilots are useful, but they serve different roles:

| Dataset            | Role                                       |
| ------------------ | ------------------------------------------ |
| Occupational v2    | Main quantitative benchmark                |
| APGC-format pilot  | External sentence-pair pipeline validation |
| ArGAN-format pilot | Qualitative prompt-based external pilot    |

This framing keeps the thesis focused while still showing broader extensibility.

---

## 5.14 Limitations

The thesis has several limitations.

First, the main benchmark focuses only on occupations. It does not cover all forms of gender bias.

Second, the dialect-aware design includes MSA and Egyptian Arabic only. Other Arabic varieties such as Gulf, Levantine, and Moroccan Arabic are not included.

Third, the model set is still limited. Although six models were evaluated, more Arabic-specific and instruction-tuned models should be tested in future work.

Fourth, the APGC and ArGAN experiments are pilot-level only. They validate pipeline extensibility but do not yet provide full external statistical validation.

Fifth, ArGAN-style prompt evaluation requires manual annotation and stronger instruction-tuned models.

---

## 5.15 Future Work

Future work can extend the thesis in several directions.

First, the occupational benchmark can be expanded to more occupations, fields, templates, and dialects.

Second, the full APGC dataset can be converted into the pairwise scoring format and evaluated across the same model set.

Third, the full ArGAN gender subset can be evaluated using stronger Arabic-capable instruction models with human annotation.

Fourth, mitigation methods can be tested, including:

* prompt rewriting,
* counterfactual data augmentation,
* fine-tuning,
* calibration,
* decoding constraints.

Fifth, explainability methods can be used to inspect which tokens or phrases drive the gender preference.

---

## 5.16 Summary

This chapter discussed the main findings of the thesis.

The results show that occupational gender preference in Arabic causal language models is statistically significant and associated with model family.

Arabic-specific AraGPT2 models prefer masculine occupational sentences, while non-Arabic-specific multilingual/general models prefer feminine occupational sentences.

The field-level results show that bias is domain-dependent.

The external dataset pilots show that the pipeline can be extended beyond the main occupational benchmark, but APGC and ArGAN should currently be treated as pilot validation steps rather than final quantitative evidence.

Overall, the thesis provides a focused and statistically supported approach for measuring occupational gender bias in Arabic causal language models.
## v3 Sensitivity Analysis Discussion

An experimental v3 benchmark was created to test whether the main benchmark pattern remains stable after expanding occupation coverage and template diversity.

The v3 benchmark passed automatic quality checks, but the quick two-model test showed that AraGPT2-base changed direction compared with v2.

In v2, AraGPT2-base showed masculine occupational preference. In v3, AraGPT2-base showed feminine occupational preference.

Further diagnostics showed that this reversal was not mainly caused by the newly added templates. The newly added templates were almost balanced. Instead, the stronger feminine direction appeared in the old v2-style templates when applied to the expanded v3 occupation list.

This suggests that Arabic occupational gender-bias measurement is sensitive to benchmark design, especially occupation coverage and lexical/contextual formulation.

This finding is important because it shows that benchmark expansion should not be assumed to preserve earlier patterns automatically.

For this reason, v2 remains the main validated benchmark, while v3 is treated as an experimental sensitivity benchmark that motivates future balanced benchmark construction and human validation.
## Interpretation of v3 Balanced Results

The v3 balanced benchmark was designed to address the imbalance observed in the earlier v3 expansion.

It used 30 male-stereotyped, 30 female-stereotyped, and 30 neutral occupations, with four controlled templates.

However, AraGPT2-base still showed feminine preference on v3 balanced.

This suggests that stereotype-label balance alone is not sufficient to reproduce the v2 model-family pattern.

The result supports a broader methodological conclusion: Arabic occupational gender-bias evaluation is sensitive not only to stereotype-label distribution, but also to the exact occupation terms and sentence formulations used in the benchmark.

For this reason, v2 remains the main benchmark, and v3 balanced is reported as a sensitivity analysis.
## Template-Induced Bias Direction Volatility

The v4 template perturbation benchmark revealed a major methodological finding: measured gender-bias direction is not stable across templates.

All six tested models showed template-induced direction flips. This means that the same model can prefer masculine occupational sentences under one template and feminine occupational sentences under another.

This finding is important because it shows that Arabic bias evaluation should not rely on a single sentence template.

The strongest statistical effects came from template ID, semantic frame, and dialect. In contrast, stereotype label was not statistically significant after balancing.

This suggests that, once the occupation set is balanced, sentence formulation and dialect can become stronger drivers of measured bias than the stereotype category itself.

Therefore, the thesis contribution is not only the detection of gender bias in Arabic models. It also demonstrates the instability of bias measurement under controlled benchmark-design changes.

This supports the final methodological claim:

Arabic occupational gender-bias evaluation should report both model-level bias and benchmark-design sensitivity.