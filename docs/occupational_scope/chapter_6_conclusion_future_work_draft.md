# Chapter 6 — Conclusion and Future Work

## 6.1 Conclusion

This thesis investigated occupational gender bias in Arabic causal language models.

The work focused on measuring whether Arabic language models assign different likelihoods to masculine and feminine occupational sentence variants when the meaning and context are controlled.

The main contribution is a counterfactual dialect-aware occupational benchmark for Arabic gender-bias evaluation.

The final benchmark contains:

| Component                |                   Count |
| ------------------------ | ----------------------: |
| Occupations              |                      60 |
| Occupational fields      |                       6 |
| Templates per occupation |                       4 |
| Sentence pairs           |                     240 |
| Arabic varieties         | MSA and Egyptian Arabic |

Each benchmark item contains a masculine and feminine version of the same sentence. The score is computed as:

```text
score_difference = masculine_score - feminine_score
```

A positive score indicates masculine preference, while a negative score indicates feminine preference.

---

## 6.2 Main Findings

The main finding is that model family is strongly associated with gender-preference direction.

Arabic-specific AraGPT2 models showed masculine occupational preference.

Non-Arabic-specific multilingual/general causal language models showed feminine occupational preference.

The six-model analysis showed:

| Model Family        | Total Items | Masculine Preferred | Feminine Preferred | Direction |
| ------------------- | ----------: | ------------------: | -----------------: | --------- |
| Arabic-specific     |         480 |                 320 |                160 | Masculine |
| Non-Arabic-specific |         960 |                 346 |                610 | Feminine  |

The chi-square test confirmed that this association is statistically significant.

```text
chi-square p-value = 1.64e-27
```

This result supports the conclusion that occupational gender bias in Arabic language models is not uniform. It varies by model family.

---

## 6.3 Contribution of the Thesis

This thesis contributes:

1. a controlled Arabic occupational gender-bias benchmark,
2. a dialect-aware design covering MSA and Egyptian Arabic,
3. a counterfactual sentence-pair scoring method,
4. a six-model comparison across Arabic-specific and non-Arabic-specific causal language models,
5. field-level bias analysis across six professional domains,
6. external dataset pilots using APGC-format and ArGAN-format samples.

The thesis also shows that Arabic gender-bias evaluation must account for Arabic morphology, where gender can appear in nouns, verbs, adjectives, demonstratives, and pronouns.

---

## 6.4 External Dataset Enrichment

Two external dataset pilots were added.

The APGC-format pilot tested whether the sentence-pair scoring pipeline can be reused for broader Arabic grammatical-gender examples. It confirmed that the method can be extended beyond occupations, but because it contains only 10 sentence pairs, it is treated as pipeline validation rather than final statistical evidence.

The ArGAN-format pilot tested prompt-based Arabic bias evaluation. The improved Qwen2.5-0.5B-Instruct pilot showed that generation-based evaluation is possible, but it requires instruction-tuned models and manual output annotation. Therefore, ArGAN is reported as a qualitative external pilot.

The final thesis framing is:

| Dataset                   | Role                                |
| ------------------------- | ----------------------------------- |
| Occupational benchmark v2 | Main quantitative benchmark         |
| APGC-format pilot         | External sentence-pair validation   |
| ArGAN-format pilot        | Qualitative prompt-based validation |

---

## 6.5 Limitations

This thesis has several limitations.

First, the main benchmark focuses on occupations only. Other social contexts, such as family roles, education, politics, or media representation, are not included.

Second, the dialect-aware design includes MSA and Egyptian Arabic only. Other Arabic varieties, such as Gulf, Levantine, Moroccan, and Sudanese Arabic, should be studied in future work.

Third, the model set includes six causal language models, but more Arabic-specific and instruction-tuned models should be evaluated.

Fourth, the external datasets were used as pilots only. Full APGC and full ArGAN integration remain future work.

Fifth, the thesis measures bias but does not yet apply mitigation methods.

---

## 6.6 Future Work

Future work can extend this thesis in several directions.

### 6.6.1 Benchmark Expansion

The occupational benchmark can be expanded by adding:

* more occupations,
* more fields,
* more sentence templates,
* more Arabic dialects,
* more intersectional attributes.

### 6.6.2 Full APGC Integration

The full APGC dataset can be converted into the thesis pairwise format and scored using the same likelihood-based method.

This would allow broader evaluation of Arabic grammatical-gender bias beyond occupations.

### 6.6.3 Full ArGAN Integration

The full ArGAN gender subset can be evaluated using stronger Arabic-capable instruction models.

This would require:

* prompt generation,
* output annotation,
* stereotype detection,
* manual validation,
* inter-annotator agreement.

### 6.6.4 Mitigation

Future work can test bias-mitigation methods such as:

* prompt rewriting,
* counterfactual data augmentation,
* fairness-aware fine-tuning,
* calibration,
* decoding-time constraints.

### 6.6.5 Explainability

Future work can also apply explainability methods to identify which tokens or phrases drive model preference.

This would help answer whether bias comes from:

* occupation tokens,
* gender suffixes,
* verbs,
* adjectives,
* dialect markers,
* template structure.

---

## 6.7 Final Statement

This thesis shows that Arabic occupational gender bias can be measured using a controlled counterfactual benchmark.

The results demonstrate a statistically significant model-family effect: Arabic-specific models prefer masculine occupational forms, while non-Arabic-specific multilingual/general models prefer feminine forms.

The work provides a focused foundation for future Arabic fairness evaluation, benchmark expansion, external dataset validation, and bias mitigation.
