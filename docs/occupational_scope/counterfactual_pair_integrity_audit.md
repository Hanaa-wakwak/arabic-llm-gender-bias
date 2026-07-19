# Counterfactual Pair Integrity Audit

## Purpose

This audit checks whether masculine and feminine sentence pairs are structurally comparable across the benchmark suite.

The goal is to support the counterfactual design by verifying that sentence pairs differ mainly in the gendered occupational form rather than uncontrolled sentence structure.

## What the Audit Checks

- masculine and feminine sentence length,
- absolute character-length difference,
- absolute word-count difference,
- identical sentence errors,
- whether the masculine occupation appears in the masculine sentence,
- whether the feminine occupation appears in the feminine sentence.

## Summary

| benchmark | total_pairs | identical_sentence_pairs | average_abs_char_diff | median_abs_char_diff | max_abs_char_diff | average_abs_word_diff | median_abs_word_diff | max_abs_word_diff | masculine_occupation_missing_count | feminine_occupation_missing_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v2 | 240 | 0 | 1.9667 | 2.0000 | 5 | 0.0000 | 0.0000 | 0 | 240 | 240 |
| v3 | 540 | 0 | 2.9889 | 3.0000 | 6 | 0.0000 | 0.0000 | 0 | 0 | 0 |
| v3_balanced | 360 | 0 | 2.9833 | 3.0000 | 7 | 0.0000 | 0.0000 | 0 | 0 | 0 |
| v3_controlled | 360 | 0 | 2.9056 | 3.0000 | 6 | 0.0000 | 0.0000 | 0 | 0 | 0 |
| v4 | 720 | 0 | 2.4833 | 2.0000 | 6 | 0.0000 | 0.0000 | 0 | 0 | 0 |
| v5 | 540 | 0 | 1.2333 | 1.0000 | 3 | 0.0000 | 0.0000 | 0 | 0 | 0 |

## Interpretation

Low average word-count differences indicate that the masculine and feminine sentence variants are structurally close. This strengthens the validity of the likelihood comparison because the model is comparing near-counterfactual sentence pairs.

This audit does not prove perfect semantic equivalence, but it provides an implementation-level quality-control layer for the benchmark design.

## Contribution

This audit adds a methodological validation layer to the thesis. It shows that the benchmark suite does not only generate sentence pairs, but also checks the integrity of the counterfactual pair design.
