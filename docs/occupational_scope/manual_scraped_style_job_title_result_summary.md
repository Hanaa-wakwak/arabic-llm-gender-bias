# Robots-Compliant Manual Scraped-Style Job-Title Pilot Result

## Purpose

This pilot extends the Arabic occupational gender-bias evaluation suite beyond manually constructed benchmarks.

The original plan was to scrape public Arabic job-title pages and build masculine-feminine counterfactual sentence pairs.

However, the selected job website disallowed automated scraping through robots.txt. The scraper respected this restriction and did not scrape the blocked page.

Therefore, a small manual visible-seed pilot was created from publicly visible job-title contexts.

## Ethical and Technical Note

The pipeline is robots-compliant.

When robots.txt disallowed automated scraping, the script skipped the source and produced an empty automated scraping output.

A manual visible-seed file was then created as a small external enrichment pilot.

This pilot is not a replacement for the validated benchmark suite.

## Pilot Design

The manual scraped-style pilot includes:

- 10 visible job-title contexts,
- public Arabic job-board style phrases,
- masculine-feminine counterfactual pairs,
- AraGPT2-base scoring using the same likelihood-based scoring pipeline.

## Result

| Model | Total Items | Masculine Preferred | Feminine Preferred | Equal | Average Score Difference | Median Score Difference |
|---|---:|---:|---:|---:|---:|---:|
| aubmindlab/aragpt2-base | 10 | 6 | 4 | 0 | +0.291986 | +0.795344 |

## Interpretation

AraGPT2-base preferred masculine variants in 60% of the manual scraped-style job-title contexts and feminine variants in 40%.

The average score difference was positive, indicating a masculine-leaning preference in this small pilot sample.

However, because the sample size is only 10 pairs, this should be interpreted as an external pilot result, not as a statistically generalizable benchmark result.

## Relationship to the Thesis

This pilot supports the extensibility of the thesis framework.

It shows that the same paired-likelihood measurement pipeline can be applied not only to manually constructed benchmark templates, but also to real-world visible job-title contexts.

## Contribution

This adds a robots-compliant external job-title measurement pilot.

The contribution is methodological: it demonstrates how the benchmark framework can be extended to real-world job-title data while respecting web scraping restrictions.
