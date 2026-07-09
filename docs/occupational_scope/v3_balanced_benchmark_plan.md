# v3 Balanced Benchmark Plan

## Purpose

The purpose of v3_balanced is to create a more stable and interpretable enhanced benchmark after the v3 sensitivity analysis showed that benchmark expansion can change model preference direction.

## Motivation

The v3 benchmark increased coverage, but AraGPT2-base changed from masculine preference in v2 to feminine preference in v3.

Diagnostics suggest that model preference is sensitive to occupation coverage and lexical/contextual formulation.

Therefore, v3_balanced should be designed more carefully.

## Design Rules

v3_balanced should follow these rules:

1. Preserve all v2 occupations exactly where possible.
2. Preserve original v2 occupation wording.
3. Preserve original v2 workplace/context where possible.
4. Add new occupations only after manual review.
5. Balance stereotype labels.
6. Keep template structure controlled.
7. Perform human validation before using it as a main result.

## Proposed Size

| Component | Count |
|---|---:|
| Occupations | 75 or 90 |
| Templates | 4 |
| Sentence pairs | 300 or 360 |
| Stereotype labels | balanced |

## Stereotype Balance Target

For 90 occupations:

| Stereotype Label | Occupations |
|---|---:|
| male_stereotyped | 30 |
| female_stereotyped | 30 |
| neutral | 30 |

For 75 occupations:

| Stereotype Label | Occupations |
|---|---:|
| male_stereotyped | 25 |
| female_stereotyped | 25 |
| neutral | 25 |

## Recommended Use

v3_balanced should be used only after:

1. quality checks,
2. manual sentence validation,
3. stereotype-label validation,
4. quick two-model sanity test,
5. comparison with v2.

## Final Role

Until v3_balanced is validated, v2 remains the main benchmark.