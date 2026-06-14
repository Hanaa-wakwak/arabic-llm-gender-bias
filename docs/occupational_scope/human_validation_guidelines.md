# Human Validation Guidelines

## Purpose

The goal of this validation is to check the quality of the occupational gender-bias benchmark.

The benchmark contains Arabic masculine/feminine sentence pairs for job-role descriptions.

Each pair should preserve the same meaning and context. Only the gender-marked Arabic forms should change.

## What Annotators Should Check

For each row, annotators should evaluate the masculine and feminine sentence pair using the following criteria.

## 1. Masculine Sentence Naturalness

Column:

`naturalness_masculine_1_to_5`

Score from 1 to 5:

* 1 = very unnatural
* 2 = somewhat unnatural
* 3 = acceptable
* 4 = natural
* 5 = very natural

## 2. Feminine Sentence Naturalness

Column:

`naturalness_feminine_1_to_5`

Score from 1 to 5:

* 1 = very unnatural
* 2 = somewhat unnatural
* 3 = acceptable
* 4 = natural
* 5 = very natural

## 3. Meaning Equivalence

Column:

`meaning_equivalence_1_to_5`

Score whether the masculine and feminine sentences have the same meaning.

* 1 = completely different meaning
* 2 = mostly different
* 3 = partially equivalent
* 4 = mostly equivalent
* 5 = fully equivalent

## 4. Dialect Correctness

Column:

`dialect_correct_yes_no`

Write:

* yes: if the sentence matches the stated dialect
* no: if the sentence does not match the stated dialect

For MSA rows, the sentence should sound like Modern Standard Arabic.

For Egyptian rows, the sentence should sound natural in Egyptian Arabic.

## 5. Gender Pair Correctness

Column:

`gender_pair_correct_yes_no`

Write:

* yes: if the masculine and feminine forms are grammatically correct
* no: if one of the gender forms is wrong

## 6. Occupation Field Correctness

Column:

`occupation_field_correct_yes_no`

Write:

* yes: if the occupation belongs to the stated field
* no: if the occupation should be assigned to another field

## 7. Suggested Fixes

If a sentence is not natural or not correct, write a corrected version in:

* `suggested_fix_masculine`
* `suggested_fix_feminine`

## 8. Final Decision

Column:

`final_decision_keep_revise_remove`

Use one of the following:

* keep: the pair is good
* revise: the pair needs editing
* remove: the pair should be removed from the benchmark

## Recommended Validation Rule

A sentence pair should be kept if:

* masculine naturalness is at least 4,
* feminine naturalness is at least 4,
* meaning equivalence is at least 4,
* dialect correctness is yes,
* gender pair correctness is yes.

Pairs that do not satisfy these rules should be revised or removed.
