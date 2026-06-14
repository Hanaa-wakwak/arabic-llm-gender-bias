# Enrichment Plan: Additional Datasets and Models

## Goal

The current thesis already has a strong main benchmark:

`occupational_bias_v2.csv`

This benchmark contains 60 occupations, 6 professional fields, 4 templates, and 240 masculine/feminine counterfactual sentence pairs.

The goal of the enrichment phase is not to replace the main benchmark. Instead, the goal is to add robustness experiments using additional models and external datasets.

## Current Main Experiment

The current main experiment evaluates four causal language models:

| Model                     | Family          |
| ------------------------- | --------------- |
| aubmindlab/aragpt2-base   | Arabic-specific |
| aubmindlab/aragpt2-medium | Arabic-specific |
| bigscience/bloom-560m     | Multilingual    |
| bigscience/bloom-1b1      | Multilingual    |

The main result is:

> Arabic-specific AraGPT2 models show masculine occupational preference, while multilingual BLOOM models show feminine occupational preference.

## Why Enrichment Is Needed

The enrichment phase strengthens the thesis by answering:

1. Does the result remain stable with more models?
2. Does the result appear only in our benchmark, or also in external resources?
3. Are Arabic-specific models consistently different from multilingual models?
4. Does model size affect gender-preference direction?
5. Do dialect and template choices affect the result?

## Enrichment Part 1 — More Models

The additional model experiment should evaluate the same final benchmark, `occupational_bias_v2.csv`, on more causal language models.

### Recommended Additional Arabic-Focused Models

| Model                                    | Why Add It                                                           |
| ---------------------------------------- | -------------------------------------------------------------------- |
| stabilityai/ar-stablelm-2-base           | Small Arabic-centric causal model, practical for local/Colab scoring |
| inceptionai/jais-family-2p7b or jais-13b | Arabic-English bilingual model family                                |
| FreedomIntelligence/AceGPT-v2-8B         | Arabic-focused LLM based on Llama architecture                       |
| humain-ai/ALLaM-7B-Instruct-preview      | Arabic language technology model family                              |

### Recommended Additional Multilingual Models

| Model                           | Why Add It                                               |
| ------------------------------- | -------------------------------------------------------- |
| bigscience/bloom-3b             | Larger BLOOM model for size comparison                   |
| facebook/xglm-564M or xglm-1.7B | Multilingual causal baseline                             |
| Qwen/Qwen2.5-1.5B or Qwen2.5-3B | Strong multilingual causal baseline                      |
| meta-llama/Llama-3.2-1B or 3B   | General multilingual-ish baseline if access is available |

## Model Selection Rule

Models should be selected based on:

1. causal/decoder-only architecture,
2. Arabic support,
3. open availability,
4. feasible hardware requirements,
5. tokenizer compatibility with Arabic,
6. ability to compute sentence likelihood scores.

## Enrichment Part 2 — External Datasets

External datasets should be used as comparison or validation resources.

### Recommended External Resources

| Dataset/Resource                  | Use in Thesis                                                                            |
| --------------------------------- | ---------------------------------------------------------------------------------------- |
| ArGAN                             | External Arabic bias dataset for LLM evaluation                                          |
| Arabic Parallel Gender Corpus 2.0 | Arabic grammatical-gender resource for sentence/gender analysis                          |
| AraWEAT                           | Arabic bias specifications useful for literature and comparison                          |
| ArabicMMLU                        | General Arabic utility benchmark, useful to check whether bias reduction affects utility |
| ORCA                              | Broad Arabic NLU benchmark collection, useful as general Arabic evaluation reference     |

## How to Use External Datasets

External datasets should not replace the occupational benchmark.

They should be used in one of three ways:

1. Related-work comparison,
2. external validation,
3. utility or robustness analysis.

## Enrichment Part 3 — Possible Benchmark v3

A future v3 benchmark can expand the current benchmark further.

Possible additions:

1. more occupations,
2. more Arabic dialects,
3. more sentence templates,
4. more workplace contexts,
5. more stereotype labels,
6. more human validation.

## Recommended v3 Direction

The best v3 direction is:

* keep the same 6 fields,
* increase occupations from 60 to 90,
* add Gulf Arabic or Levantine Arabic,
* add one neutral template,
* add one family/context-free template.

This would produce a larger benchmark while preserving comparability with v2.

## Priority Order

The recommended priority is:

1. Score more models on v2.
2. Add external dataset comparison.
3. Add utility evaluation using ArabicMMLU or ORCA.
4. Build v3 only if time allows.

## Final Thesis Framing

The enriched thesis should be framed as:

> The main experiment uses a controlled occupational benchmark. Additional models and external datasets are used to test the robustness and generalizability of the findings.

## Expected Contribution After Enrichment

After enrichment, the thesis contribution becomes stronger:

1. A controlled Arabic occupational bias benchmark.
2. A dialect-aware counterfactual design.
3. A multi-model comparison across Arabic-specific and multilingual LMs.
4. External validation using Arabic/fairness datasets.
5. Statistical analysis of bias direction and model-family effects.


## Completed Extra Model: Qwen2.5-0.5B

`Qwen/Qwen2.5-0.5B` was evaluated as an additional multilingual/general causal language model.

The model preferred feminine occupational sentences in 158 out of 240 pairs, masculine sentences in 80 pairs, and produced 2 equal cases.

This corresponds to:

- 65.83% feminine preference,
- 33.33% masculine preference,
- 0.83% equal,
- average score difference ≈ -0.3425.

This result further supports the robustness of the multilingual/general-model pattern, where additional non-Arabic-specific models show feminine occupational preference on the Arabic occupational benchmark.