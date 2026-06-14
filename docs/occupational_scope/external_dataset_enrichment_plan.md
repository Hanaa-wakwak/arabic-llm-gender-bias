# External Dataset Enrichment Plan

## Purpose

The current thesis uses `occupational_bias_v2.csv` as the main controlled benchmark for measuring occupational gender bias in Arabic causal language models.

The enrichment phase adds external datasets and auxiliary benchmarks to test whether the main findings remain robust beyond the internally created occupational benchmark.

The goal is not to replace the main benchmark. The goal is to provide external validation and broader evidence.

---

## Current Main Benchmark

The main benchmark is:

`data/occupational_benchmark/occupational_bias_v2.csv`

It contains:

| Component                | Count |
| ------------------------ | ----: |
| Occupations              |    60 |
| Fields                   |     6 |
| Templates per occupation |     4 |
| Sentence pairs           |   240 |

The main benchmark is still the core contribution of the thesis.

---

## Why Add External Datasets?

External datasets strengthen the thesis by answering:

1. Does the model-family pattern appear outside the custom occupational benchmark?
2. Are the findings specific to occupations, or related to broader Arabic grammatical gender?
3. Can the thesis connect its findings to existing Arabic fairness resources?
4. Can we compare controlled sentence likelihood scoring with other bias-evaluation styles?
5. Does the bias pattern remain stable across different dataset designs?

---

# Dataset 1 — ArGAN

## Description

ArGAN is an Arabic dataset for evaluating bias in large language models. It focuses on Modern Standard Arabic and covers gender, ability, and nationality bias.

## Role in This Thesis

ArGAN should be used as an external Arabic LLM bias dataset.

It can be used for:

1. gender-bias prompt evaluation,
2. comparison with the occupational benchmark,
3. broader fairness discussion beyond occupations.

## Recommended Use

Use only the gender-related subset first.

Possible analysis:

* run selected models on ArGAN gender prompts,
* classify outputs as biased / neutral / stereotypical,
* compare whether models that show occupational bias also show broader gender bias.

## Thesis Framing

ArGAN is not a replacement for the occupational benchmark. It is an external validation dataset.

Recommended wording:

> To test whether the observed occupational gender-bias pattern generalizes beyond the constructed benchmark, the study also considers ArGAN as an external Arabic LLM bias resource.

---

# Dataset 2 — Arabic Parallel Gender Corpus APGC

## Description

The Arabic Parallel Gender Corpus provides parallel Arabic sentences across grammatical gender forms. It is designed for research involving Arabic gender identification and gender rewriting.

APGC 2.0 expands earlier versions and includes multiple gender combinations involving first and second person contexts.

## Role in This Thesis

APGC is useful for testing grammatical gender preference beyond occupations.

It can answer:

> Do models systematically prefer masculine or feminine Arabic grammatical forms even when the sentence is not occupational?

## Recommended Use

Convert parallel masculine/feminine sentence variants into scoring pairs.

For each pair:

```text
score_difference = masculine_score - feminine_score
```

Then compare the result with the occupational benchmark.

## Thesis Framing

APGC is used as an auxiliary grammatical-gender benchmark.

Recommended wording:

> APGC is used to test whether the model preference observed in occupational sentences also appears in broader Arabic grammatical-gender contexts.

---

# Dataset 3 — AraWEAT

## Description

AraWEAT provides Arabic bias test specifications for measuring bias in Arabic word embeddings.

It includes Arabic word lists and bias dimensions that can support lexical association analysis.

## Role in This Thesis

AraWEAT should be used as a lexical-level comparison resource.

It is not directly the same as the causal-LM sentence scoring benchmark, but it is useful for connecting this thesis to existing Arabic bias-evaluation work.

## Recommended Use

Use AraWEAT in one of two ways:

1. Related-work comparison.
2. Auxiliary lexical association analysis.

Possible use:

* compare occupation words in our benchmark with AraWEAT-style gender association lists,
* discuss whether sentence-level model preferences align with earlier lexical bias findings.

## Thesis Framing

AraWEAT supports the literature and provides a lexical baseline, while the thesis contribution remains sentence-level counterfactual evaluation.

---

# Dataset 4 — Occupational Benchmark v3

## Description

v3 is a proposed expansion of the thesis-created occupational benchmark.

## Proposed v3 Size

| Component                | Proposed Count |
| ------------------------ | -------------: |
| Fields                   |              6 |
| Occupations per field    |             15 |
| Total occupations        |             90 |
| Templates per occupation |              6 |
| Sentence pairs           |            540 |

## Proposed Additions

v3 can add:

1. more occupations,
2. more templates,
3. more Arabic dialects,
4. more workplace contexts,
5. more neutral sentence forms,
6. more stereotype categories.

## Recommended New Dialect

Add one additional Arabic variety:

* Gulf Arabic, or
* Levantine Arabic.

The safest option is to add Gulf Arabic only if a native or fluent reviewer can validate the sentences.

## Thesis Framing

v3 should be treated as an extended robustness benchmark.

v2 remains the main final benchmark unless v3 is fully validated.

---

# Recommended Priority

The recommended order is:

1. Add documentation and dataset tracking.
2. Add APGC integration plan.
3. Add ArGAN integration plan.
4. Add AraWEAT comparison plan.
5. Build occupational benchmark v3 only if there is enough time for validation.
6. Run a small pilot first before scoring all models.

---

# Final Enrichment Strategy

The final enriched thesis structure should be:

| Part               | Dataset              | Purpose                                      |
| ------------------ | -------------------- | -------------------------------------------- |
| Main experiment    | occupational_bias_v2 | Main controlled occupational benchmark       |
| Robustness 1       | extra models on v2   | Model-family stability                       |
| Robustness 2       | APGC                 | Broader Arabic grammatical-gender preference |
| Robustness 3       | ArGAN                | External Arabic LLM bias validation          |
| Related comparison | AraWEAT              | Lexical-level Arabic bias comparison         |
| Optional extension | occupational_bias_v3 | Larger custom benchmark                      |

---

# Recommended Thesis Wording

> The main contribution of the thesis is the controlled occupational counterfactual benchmark. External datasets are added as robustness and validation resources, allowing the study to compare occupational bias with broader Arabic gender-bias resources.
