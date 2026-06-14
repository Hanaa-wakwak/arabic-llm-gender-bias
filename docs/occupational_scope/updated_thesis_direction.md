# Updated Thesis Direction

## Updated Thesis Title

**Counterfactual Evaluation of Occupational Gender Bias in Arabic Causal Language Models**

## Alternative Title

**Measuring Occupational Gender Bias in Arabic Causal Language Models using a Counterfactual Dialect-Aware Benchmark**

## Refined Thesis Scope

This thesis focuses on occupational gender bias in Arabic causal language models.

The benchmark evaluates whether models prefer masculine or feminine forms when scoring Arabic job-role sentences.

The scope is limited to:

* occupations and job roles,
* professional fields,
* Modern Standard Arabic,
* Egyptian Arabic,
* Arabic-specific causal LMs,
* multilingual causal LMs.

Traits and general personality descriptions are no longer part of the main thesis scope. They are treated as an earlier pilot experiment.

## Updated Problem Statement

Gender bias in language models can appear when models associate certain occupations more strongly with one gender than another.

In Arabic, this problem is linguistically complex because gender is expressed through grammatical agreement across pronouns, nouns, adjectives, verbs, and sentence structure.

Most existing bias evaluations are either English-focused, MSA-focused, or not specialized for occupational gender bias in Arabic.

Therefore, this thesis proposes a controlled Arabic occupational gender-bias benchmark using masculine/feminine counterfactual sentence pairs across MSA and Egyptian Arabic.

## Updated Research Aim

The aim of this thesis is to measure occupational gender bias in Arabic causal language models using a counterfactual, dialect-aware benchmark.

## Updated Research Questions

### RQ1

Do Arabic causal language models show statistically significant masculine or feminine preference in occupational sentence pairs?

### RQ2

Does occupational gender preference differ across professional fields such as STEM, Healthcare, Education, Business, Legal/Government, and Media/Creative?

### RQ3

Does measured occupational gender bias differ between Modern Standard Arabic and Egyptian Arabic?

### RQ4

Do Arabic-specific causal language models and multilingual causal language models show different occupational gender-preference patterns?

### RQ5

How sensitive are measured occupational gender-bias scores to Arabic sentence templates?

## Updated Contribution

This thesis contributes:

1. A controlled Arabic occupational gender-bias benchmark based on masculine/feminine counterfactual sentence pairs.

2. A field-aware benchmark structure covering multiple professional domains.

3. A dialect-aware design covering Modern Standard Arabic and Egyptian Arabic.

4. A reproducible scoring pipeline for causal language models using sentence-level probability differences.

5. A multi-model comparison between Arabic-specific and multilingual causal language models.

6. Statistical testing of occupational gender preference using binomial tests, Wilcoxon tests, chi-square tests, and multiple-comparison correction.

7. Evidence that model family strongly affects measured occupational gender preference in Arabic causal language models.

## Updated Main Hypothesis

Arabic-specific causal language models and multilingual causal language models differ in their occupational gender-preference patterns.

## Preliminary Finding

The current occupational benchmark results support this hypothesis.

Arabic-specific AraGPT2 models show statistically significant masculine occupational preference.

Multilingual BLOOM models show statistically significant feminine occupational preference.

This suggests that model family is strongly associated with measured occupational gender preference.

## Current Benchmark

The current benchmark is:

`data/occupational_benchmark/occupational_bias_v1.csv`

It contains:

* 144 sentence pairs,
* 36 occupations,
* 6 occupational fields,
* 2 Arabic varieties,
* 4 sentence templates.

## Current Models

The evaluated models are:

| Model                     | Family          |
| ------------------------- | --------------- |
| aubmindlab/aragpt2-base   | Arabic-specific |
| aubmindlab/aragpt2-medium | Arabic-specific |
| bigscience/bloom-560m     | Multilingual    |
| bigscience/bloom-1b1      | Multilingual    |

## Current Bias Metric

The main metric is:

`score_difference = masculine_score - feminine_score`

Interpretation:

* positive value: masculine preference,
* negative value: feminine preference,
* near zero: balanced preference.

## Next Research Steps

The next steps are:

1. Add human validation for sentence naturalness and masculine/feminine equivalence.

2. Add more occupation examples per field.

3. Add more Arabic and multilingual causal language models.

4. Add dialect-level statistical analysis.

5. Add template robustness analysis.

6. Add token-level explainability.

7. Add bias mitigation experiments.
