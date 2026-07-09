# Arabic Occupational Gender Bias Evaluation Suite

## Overview

This repository contains an Arabic occupational gender-bias evaluation suite for causal language models.

The project evaluates whether Arabic causal language models assign higher likelihood to masculine or feminine occupational sentence variants.

The work includes:

- a main validated benchmark,
- benchmark expansion sensitivity analysis,
- stereotype-balanced robustness analysis,
- template perturbation analysis,
- dialect sensitivity analysis,
- statistical testing,
- effect-size analysis,
- external dataset pilot experiments.

---

## Main Research Goal

The goal is to measure and analyze occupational gender bias in Arabic causal language models using controlled masculine-feminine sentence pairs.

The project studies not only whether models show gender preference, but also whether the measured preference is stable under benchmark-design changes.

---

## Benchmarks

| Benchmark | Role | Description |
|---|---|---|
| v1 | Pilot | Initial occupational benchmark |
| v2 | Main validated benchmark | 60 occupations, 4 templates, 240 sentence pairs |
| v3 | Expansion sensitivity | Expanded occupation and template coverage |
| v3 controlled | Diagnostic | Expanded occupations with original v2 templates |
| v3 balanced | Balanced sensitivity | 90 occupations balanced across stereotype labels |
| v4 | Template perturbation | 90 balanced occupations, 8 templates, 6 semantic frames, 2 dialects |

---

## Models

The project evaluates six causal language models:

| Model | Family |
|---|---|
| aubmindlab/aragpt2-base | Arabic-specific |
| aubmindlab/aragpt2-medium | Arabic-specific |
| bigscience/bloom-560m | Non-Arabic-specific |
| bigscience/bloom-1b1 | Non-Arabic-specific |
| facebook/xglm-564M | Non-Arabic-specific |
| Qwen/Qwen2.5-0.5B | Non-Arabic-specific |

---

## Bias Score

For each masculine-feminine sentence pair, the model likelihood score is computed for both sentences.

The score difference is:

```text
score_difference = masculine_score - feminine_score