# Benchmark Enhancement Plan v3

## Purpose

The purpose of v3 is to strengthen the occupational gender-bias benchmark by increasing coverage, adding stereotype labels, and improving validation.

The current v2 benchmark remains the main confirmed benchmark.

v3 is added as an enhanced robustness benchmark.

## Current v2

| Component | Count |
|---|---:|
| Occupations | 60 |
| Fields | 6 |
| Templates | 4 |
| Sentence pairs | 240 |

## Proposed v3

| Component | Count |
|---|---:|
| Occupations | 90 |
| Fields | 6 or 8 |
| Templates | 6 |
| Sentence pairs | 540 |

## New Columns

v3 should include the following additional columns:

| Column | Purpose |
|---|---|
| stereotype_label | male_stereotyped / female_stereotyped / neutral |
| dialect | MSA / Egyptian |
| template_type | workplace / said_role / achievement / leadership / skill / evaluation |
| grammatical_gender_marker | noun / verb / adjective / demonstrative / mixed |
| validation_status | pending / accepted / rejected |

## Why v3 Improves the Thesis

v3 improves the thesis by:

1. increasing benchmark size,
2. improving occupational coverage,
3. allowing stereotype-level analysis,
4. supporting stronger robustness checks,
5. making the benchmark more publishable.

## Important Rule

v3 should not replace v2 until it passes quality checks and validation.

v2 remains the stable main benchmark.

v3 is reported as an enhanced robustness benchmark.