# Expanded External Scraped Job-Title Pilot Result

## Purpose

This document summarizes the expanded external scraped job-title pilot.

The purpose of this pilot is to test whether the occupational gender-bias measurement pipeline can be extended from manually constructed benchmark sentences to real-world Arabic job-title contexts.

## Source Handling

The source list included multiple Arabic job-board pages.

The scraping pipeline checked robots.txt before fetching each source.

Sources that disallowed scraping were skipped.

Allowed pages were processed automatically, and the extracted pairs were treated as raw scraped data requiring quality control.

## Raw Scraping Output

The expanded scraping run produced:

- Enabled sources: 5
- Raw scraped mentions: 10
- Raw counterfactual pairs: 10
- Unique occupations: 5
- Unique fields: 4
- Status: completed

## Quality Filtering

The raw scraped output was manually and automatically inspected.

Some rows were removed because they were not true job-title contexts, such as job-seeker registration phrases.

One malformed counterfactual replacement was also removed because it produced an invalid form.

After filtering, the cleaned scraped subset contained 5 valid pairs.

## Clean Scraped Result

| Model | Clean Pairs | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Median Score Difference |
|---|---:|---:|---:|---:|---:|---:|
| aubmindlab/aragpt2-base | 5 | 1 | 4 | 0 | -0.298393 | -0.489377 |

## Interpretation

In the cleaned scraped job-title pilot, AraGPT2-base preferred feminine variants in 4 out of 5 cases and masculine variants in 1 out of 5 cases.

The average score difference was negative, indicating a feminine-leaning preference in this cleaned scraped subset.

Because the sample size is small, this is reported only as an external enrichment pilot, not as a statistically generalizable benchmark result.

## Relationship to Manual Visible Seed Pilot

A previous manual visible-seed pilot contained 10 pairs and showed a masculine-leaning result for AraGPT2-base.

The cleaned scraped subset showed a feminine-leaning result.

This difference supports the thesis argument that small external job-title samples are highly context-sensitive.

Therefore, external scraped/manual pilots are used for enrichment and extensibility demonstration, while the main thesis claims remain based on the controlled benchmark suite.

## Contribution

This expanded pilot strengthens the methodological contribution by showing that the evaluation pipeline can process real-world job-board contexts, apply robots-compliant source handling, perform quality filtering, and score cleaned counterfactual job-title pairs.
