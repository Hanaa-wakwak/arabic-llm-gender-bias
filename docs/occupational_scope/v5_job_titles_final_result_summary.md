# v5 Job-Title Benchmark Final Result Summary

## Purpose

The v5 benchmark is a job-title-specific extension of the Arabic occupational gender-bias evaluation suite.

Unlike v2, v3, and v4, which place occupations inside broader sentence contexts, v5 isolates the occupation as an explicit professional title.

The goal is to test whether Arabic causal language models prefer masculine or feminine job-title forms in contexts such as CVs, job advertisements, HR records, and professional profiles.

## Benchmark Design

v5 was built from the v3 balanced occupation lexicon.

It contains:

- 90 occupations,
- 30 male-stereotyped occupations,
- 30 female-stereotyped occupations,
- 30 neutral occupations,
- 6 job-title templates,
- 2 Arabic varieties: MSA and Egyptian Arabic,
- 540 masculine-feminine sentence pairs.

## Score Definition

For each item:

```text
score_difference = masculine_score - feminine_score