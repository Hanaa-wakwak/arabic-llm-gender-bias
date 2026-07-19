# Clean Scraped Job-Title Pair Summary

## Purpose

This step filters the raw scraped job-title counterfactual pairs before scoring.

## Removed Cases

The cleaner removes non-job-title contexts such as job-seeker registration phrases and malformed counterfactual replacements such as incorrect plural substitutions.

## Summary

- raw_pairs: 10
- clean_pairs: 5
- removed_pairs: 5
- unique_clean_occupations: 3
- unique_clean_fields: 3
- manual_review_required: True
- status: cleaning_completed

## Output Files

- Clean pairs: `data\external_datasets\job_scraping\clean_scraped_job_title_bias_pairs.csv`
- Removed pairs: `results\external_datasets\job_scraping\removed_scraped_job_title_pairs.csv`
- Summary: `results\external_datasets\job_scraping\clean_scraped_job_title_pairs_summary.csv`

## Note

The cleaned scraped dataset is still an external enrichment pilot and requires manual review.