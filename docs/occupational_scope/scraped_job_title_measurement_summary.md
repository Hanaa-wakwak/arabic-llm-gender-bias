# Scraped Job-Title Measurement Summary

## Purpose

This pilot collects public Arabic job-title mentions, matches them to an occupation lexicon, and builds masculine-feminine counterfactual pairs.

## Summary

- enabled_sources: 5
- scraped_mentions: 10
- counterfactual_pairs: 10
- unique_occupations: 5
- unique_fields: 4
- manual_review_required: True
- status: completed

## Output Files

- Raw text debug: `results\external_datasets\job_scraping\scraped_raw_text_debug.txt`
- Contexts debug: `results\external_datasets\job_scraping\scraped_contexts_debug.csv`
- Mentions: `results\external_datasets\job_scraping\scraped_job_title_mentions.csv`
- Pairs: `data\external_datasets\job_scraping\scraped_job_title_bias_pairs.csv`
- Summary: `results\external_datasets\job_scraping\scraped_job_title_measurement_summary.csv`

## Note

This remains an external enrichment pilot because scraped counterfactual replacements may require manual grammatical review.
