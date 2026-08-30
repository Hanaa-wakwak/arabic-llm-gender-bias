# Final External Dataset Expansion Summary

## Purpose

This document summarizes the expanded real-world and job-role dataset components added to strengthen the Arabic occupational gender-bias evaluation framework.

## Added Dataset Components

### v6 Expanded Job Roles and Departments

- Controlled expanded benchmark
- 120 structured job roles
- 24 templates
- 2,880 masculine-feminine counterfactual pairs per model
- Dimensions: department, job family, seniority level, job-role type, workplace context, template type, semantic frame, and dialect

### ArabJobs v7 External Real-World Job Ads

- External real-world Arabic job-ad corpus
- Derived counterfactual sentence pairs from matched job titles and recruitment metadata
- Includes country, job category, sub-category, profession, original gender label, and original job title metadata
- Used as external validation beyond controlled templates

## v6 Overall Model Results

### aubmindlab/aragpt2-base

- Total items: 2880
- Masculine preferred: 970 (33.68055555555556%)
- Feminine preferred: 1910 (66.31944444444444%)
- Equal: 0 (0.0%)
- Average score difference: -0.3019826209379567
- Median score difference: -0.2294025421142578
- Direction: feminine

### aubmindlab/aragpt2-medium

- Total items: 2880
- Masculine preferred: 1136 (39.44444444444444%)
- Feminine preferred: 1744 (60.55555555555555%)
- Equal: 0 (0.0%)
- Average score difference: -0.2435836901267369
- Median score difference: -0.1814496517181396
- Direction: feminine

### bigscience/bloom-1b1

- Total items: 2880
- Masculine preferred: 1328 (46.11111111111112%)
- Feminine preferred: 1547 (53.71527777777778%)
- Equal: 5 (0.1736111111111111%)
- Average score difference: -0.0808241102430555
- Median score difference: -0.0546875
- Direction: feminine

### bigscience/bloom-560m

- Total items: 2880
- Masculine preferred: 1500 (52.083333333333336%)
- Feminine preferred: 1375 (47.74305555555556%)
- Equal: 5 (0.1736111111111111%)
- Average score difference: -0.0163350423177083
- Median score difference: 0.03125
- Direction: near_neutral_or_mixed

## ArabJobs v7 Overall Model Results

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

## Main Interpretation

The v6 and ArabJobs v7 extensions strengthen the thesis by showing that Arabic occupational gender-bias measurements are sensitive to the form of the evaluation data. Controlled job-role templates and real-world recruitment-language contexts can produce different measured gender-preference directions, demonstrating the importance of robustness-oriented benchmark design.

## Publication Value

These additions improve Q1-readiness by expanding the work from a controlled benchmark study into a broader evaluation framework that includes structured labor-market dimensions and external real-world Arabic job-ad validation.