# Chapter 3: Methodology

## 3.1 Overview

This chapter describes the methodology used to measure occupational gender bias in Arabic causal language models. The proposed framework uses masculine-feminine counterfactual sentence pairs, paired likelihood scoring, benchmark validation, statistical analysis, external dataset evaluation, and mitigation testing.

## 3.2 Research Questions

RQ1. How can occupational gender bias be measured in Arabic causal language models using counterfactual sentence pairs?

RQ2. Do Arabic-specific and multilingual causal language models show different gender-preference patterns?

RQ3. Is measured gender bias stable across templates, dialects, semantic frames, job-title contexts, departments, and job-role contexts?

RQ4. Do real-world Arabic job-advertisement contexts produce different measured gender-preference patterns from controlled benchmark contexts?

RQ5. Can counterfactual data augmentation reduce measured occupational gender preference?

## 3.3 Benchmark Design

The benchmark suite consists of controlled masculine-feminine Arabic counterfactual sentence pairs. Each pair preserves the same occupational meaning while changing the gendered linguistic form.

The suite includes:

- v2 main validated benchmark
- v4 template perturbation benchmark
- v5 job-title benchmark
- v6 expanded job-role and department benchmark
- ArabJobs v7 external real-world job-ad benchmark

## 3.4 Scoring Formula

For a sentence x = (w_1, ..., w_n), the causal language model score is:

S(x) = (1 / n) * sum log P(w_t | w_<t)

For each pair:

Delta_i = S(x_i^m) - S(x_i^f)

This is implemented as:

score_difference = masculine_score - feminine_score

Interpretation:

- Delta_i > 0 means masculine preference.
- Delta_i < 0 means feminine preference.
- Delta_i = 0 means equal preference.

## 3.5 Overall Bias Metrics

Benchmark-level average bias:

Bias_avg = (1 / N) * sum Delta_i

Absolute disparity:

Disparity_abs = (1 / N) * sum absolute(Delta_i)

Preference rates:

R_m = masculine-preferred pairs / N

R_f = feminine-preferred pairs / N

R_e = equal-preference pairs / N

## 3.6 Validation

The framework includes:

- benchmark quality checks
- score_difference implementation validation
- formula validation
- token-length control
- human validation
- inter-annotator agreement
- final project audit

## 3.7 Statistical and Robustness Analysis

The analysis includes:

- model-level comparison
- model-family comparison
- template sensitivity
- dialect sensitivity
- semantic-frame sensitivity
- department and job-role analysis
- cross-benchmark direction-change analysis
- factor sensitivity analysis

## 3.8 Software Implementation

The project includes an interactive software tool for measuring Arabic occupational gender bias from individual sentence pairs, uploaded CSV files, and project benchmarks.

## 3.9 Bias Mitigation Experiment

A counterfactual data augmentation experiment fine-tunes AraGPT2-base on balanced masculine-feminine occupational data and compares bias scores before and after mitigation.