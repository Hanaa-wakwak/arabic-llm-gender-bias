# Benchmark Datasheet

## Benchmark Name

Arabic Occupational Gender Bias Evaluation Suite

## Purpose

This benchmark suite is designed to evaluate occupational gender preference in Arabic causal language models.

The benchmark compares masculine and feminine variants of Arabic occupational sentences and measures which variant receives a higher likelihood score from the model.

## Main Evaluation Question

Do Arabic causal language models assign higher likelihood to masculine or feminine occupational sentence variants?

## Extended Evaluation Questions

The benchmark suite also evaluates whether measured gender preference remains stable across:

- benchmark versions,
- occupation sets,
- template wording,
- semantic frames,
- dialects,
- stereotype-label balance,
- explicit job-title contexts.

## Benchmark Versions

| Version | Purpose |
|---|---|
| v2 | Main validated benchmark |
| v3 | Expansion sensitivity |
| v3 controlled | Occupation-vs-template diagnostic |
| v3 balanced | Stereotype-balanced sensitivity |
| v4 | Template, semantic-frame, and dialect sensitivity |
| v5 | Explicit job-title context sensitivity |

## Data Structure

Each benchmark item contains:

- masculine sentence,
- feminine sentence,
- occupation field,
- masculine occupation form,
- feminine occupation form,
- dialect,
- template ID,
- semantic frame,
- stereotype label when available.

## Score Definition

For each masculine-feminine pair:

```text
score_difference = masculine_score - feminine_score