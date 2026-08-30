# ArabJobs v7 External Dataset Integration Summary

## Purpose

This integration adds ArabJobs as an external real-world Arabic job-ad corpus to the occupational gender-bias evaluation framework.

## Source

- Dataset: ArabJobs: A Multinational Corpus of Arabic Job Ads
- Source file: data/external_datasets/arabjobs/ArabJobs.csv
- Integrated output: data/external_datasets/arabjobs/arabjobs_v7_counterfactual_pairs.csv

## Preparation Summary

- arabjobs_total_rows: 8546
- matched_rows: 2422
- unmatched_rows: 6124
- counterfactual_pairs: 14532
- templates_per_matched_row: 6
- unique_countries_matched: 4
- unique_job_categories_matched: 20
- unique_departments_matched: 10
- unique_roles_matched: 54
- requires_manual_validation: True

## Method

The converter matches ArabJobs job titles, professions, and descriptions against the v6 masculine-feminine job-role lexicon. Matched rows are converted into controlled masculine-feminine counterfactual sentence pairs while preserving ArabJobs metadata such as country, original gender label, job category, sub-category, profession, and original job title.

## Thesis Value

ArabJobs strengthens the thesis by adding external validation from real Arabic recruitment texts across multiple Arab countries. It supports a stronger claim that the proposed framework can move from controlled benchmark construction to real-world job-ad contexts.

## Important Limitation

The generated pairs require human validation because real-world job advertisements may contain noisy titles, mixed dialects, inconsistent gender markers, or multi-role descriptions.