# ArabJobs v7 Model Result Summary

## Dataset

- Dataset: ArabJobs v7 external real-world Arabic job-ad benchmark
- Source: ArabJobs: A Multinational Corpus of Arabic Job Ads
- Evaluation type: external real-world recruitment-language validation
- Counterfactual pairs are generated from matched ArabJobs job-title contexts

## Overall Results

### aubmindlab/aragpt2-base

- Total items: 14532
- Masculine preferred: 8404 (57.83099366914396%)
- Feminine preferred: 6128 (42.16900633085604%)
- Equal: 0 (0.0%)
- Average score difference: 0.0894636630749459
- Median score difference: 0.0525455474853515
- Direction: masculine

### bigscience/bloom-560m

- Total items: 14532
- Masculine preferred: 8463 (58.236994219653184%)
- Feminine preferred: 5994 (41.24690338563171%)
- Equal: 75 (0.5161023947151115%)
- Average score difference: 0.1089576828292733
- Median score difference: 0.0859375
- Direction: masculine

## Interpretation

ArabJobs v7 extends the thesis beyond controlled benchmark construction by evaluating the same paired-likelihood scoring method on real-world Arabic recruitment-language data. This allows comparison between controlled job-role benchmarks and naturally occurring job-ad contexts.

## Thesis Value

This external dataset strengthens the Q1-readiness of the work by adding real-world validation from Arabic job advertisements and showing whether measured gender preference remains stable outside synthetic templates.