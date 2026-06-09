# Experiment 08 — Multi-Model Evaluation on v0.7

## Goal

The goal of this experiment is to evaluate multiple Arabic and multilingual causal language models on the selected expanded pilot benchmark.

The selected benchmark version is:

minimal_pairs_v07.csv

## Models

The evaluated models are:

1. aubmindlab/aragpt2-base
2. aubmindlab/aragpt2-medium
3. bigscience/bloom-560m
4. bigscience/bloom-1b1

## Dataset

Benchmark version: minimal_pairs_v07.csv

Total items: 144

The benchmark includes:

* MSA and Egyptian Arabic
* occupation and trait concepts
* masculine/feminine counterfactual sentence pairs
* concept_id metadata
* template_id metadata
* stereotype_direction metadata

## Overall Results

| Model                     | Masculine Preferred | Feminine Preferred | Masculine % | Feminine % | Avg Score Difference |
| ------------------------- | ------------------: | -----------------: | ----------: | ---------: | -------------------: |
| aubmindlab/aragpt2-base   |                  84 |                 60 |      58.33% |     41.67% |              -0.0139 |
| aubmindlab/aragpt2-medium |                  76 |                 68 |      52.78% |     47.22% |              -0.0524 |
| bigscience/bloom-1b1      |                  50 |                 94 |      34.72% |     65.28% |              -0.2519 |
| bigscience/bloom-560m     |                  43 |                101 |      29.86% |     70.14% |              -0.3909 |

## Main Finding

The models show different gender-preference patterns on the same controlled Arabic counterfactual benchmark.

The Arabic-specific AraGPT2 models are more balanced than the BLOOM multilingual models. In particular, AraGPT2-medium is the most balanced model by preference counts.

The BLOOM models show a stronger preference for feminine sentence variants, especially BLOOM-560m.

## Interpretation

These results suggest that measured Arabic gender preference depends strongly on the model being evaluated.

The benchmark is therefore useful for comparing Arabic and multilingual language models under the same counterfactual evaluation setup.

## Preliminary Conclusion

AraGPT2-medium is the most balanced model in this experiment, while BLOOM-560m shows the strongest feminine preference.

Further analysis by dialect, dimension, stereotype direction, concept, and template is needed before making final claims.
