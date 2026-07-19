# Human Validation Protocol

## Purpose

This protocol validates a sample of Arabic masculine-feminine occupational counterfactual pairs used in the benchmark suite.

The validation checks whether the benchmark pairs are grammatically acceptable, meaning-preserving, gender-form correct, and dialect-appropriate.

## Validation Sample

The annotation sheet samples items from:

- v2 main benchmark
- v4 template perturbation benchmark
- v5 job-title benchmark

## Annotator Instructions

Each annotator should review the masculine and feminine sentence pair and fill the following fields.

### 1. grammaticality

Allowed labels:

- valid
- minor_issue
- invalid

Question:

Are both Arabic sentences grammatically acceptable?

### 2. meaning_preserved

Allowed labels:

- yes
- mostly
- no

Question:

Does the feminine sentence preserve the same meaning as the masculine sentence except for gendered occupation form?

### 3. gender_form_correct

Allowed labels:

- yes
- no

Question:

Are the masculine and feminine occupational forms correct?

### 4. dialect_correct

Allowed labels:

- yes
- no
- uncertain

Question:

Does the sentence match the intended Arabic variety or dialect?

### 5. keep_or_remove

Allowed labels:

- keep
- review
- remove

Question:

Should this pair be kept in the benchmark?

## Agreement Analysis

After annotation, the project will compute:

- percentage agreement
- Cohen's Kappa

## Thesis Use

The validation result will be used as a quality-control layer for the benchmark suite.

This strengthens the thesis by showing that the Arabic counterfactual pairs were reviewed for grammaticality, meaning preservation, gender-form correctness, and dialect appropriateness.
