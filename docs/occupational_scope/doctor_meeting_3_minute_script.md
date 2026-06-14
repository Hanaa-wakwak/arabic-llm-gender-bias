# 3-Minute Doctor Meeting Script

## Opening

Based on your feedback, I refined the thesis scope.

Instead of studying broad Arabic gender bias across occupations and traits, I narrowed the work to one clear domain:

**occupational gender bias in Arabic causal language models.**

So the new thesis direction is:

**Counterfactual Evaluation of Occupational Gender Bias in Arabic Causal Language Models.**

## Why I focused on occupations

I chose occupations because job roles are socially meaningful and directly connected to real-world gender stereotypes.

Also, in my earlier pilot, occupation items produced clearer and more interpretable patterns than trait items.

So the previous occupation-and-trait work is now treated as a pilot, and the main thesis benchmark focuses only on jobs across different professional fields.

## Benchmark design

I built a new occupation-only benchmark called:

`occupational_bias_v1.csv`

It contains:

* 144 masculine/feminine sentence pairs,
* 36 occupations,
* 6 professional fields,
* MSA and Egyptian Arabic,
* 4 sentence templates.

The six fields are:

1. STEM
2. Healthcare
3. Education
4. Business
5. Legal/Government
6. Media/Creative

Each item is a counterfactual pair.

For example:

Masculine:

`هذا طبيب يعمل في المستشفى`

Feminine:

`هذه طبيبة تعمل في المستشفى`

The meaning and context are the same. Only the gender-marked Arabic forms change.

## How I measure bias

For each pair, I calculate the model score for the masculine sentence and the feminine sentence.

Then I use:

`score_difference = masculine_score - feminine_score`

If the value is positive, the model prefers the masculine sentence.

If the value is negative, the model prefers the feminine sentence.

If the value is near zero, the model is relatively balanced.

Then I aggregate the results by model, professional field, dialect, and template.

I also apply statistical tests: binomial test, Wilcoxon test, pairwise Wilcoxon comparison, multiple-comparison correction, and chi-square test.

## Why these LLMs

I selected four causal language models:

* AraGPT2-base
* AraGPT2-medium
* BLOOM-560m
* BLOOM-1b1

The reason is to compare Arabic-specific causal LMs against multilingual causal LMs.

AraGPT2 represents Arabic-specific pretraining.

BLOOM represents multilingual pretraining.

This comparison is useful because the results show opposite behavior between the two model families.

## Main preliminary result

The Arabic-specific AraGPT2 models show statistically significant masculine occupational preference.

AraGPT2-base preferred masculine sentences in 96 out of 144 pairs.

AraGPT2-medium preferred masculine sentences in 105 out of 144 pairs.

In contrast, the multilingual BLOOM models show statistically significant feminine occupational preference.

BLOOM-1b1 preferred feminine sentences in 98 out of 144 pairs.

BLOOM-560m preferred feminine sentences in 105 out of 144 pairs.

The chi-square test between model family and gender preference was significant with:

`p = 5.74e-22`

This means model family is strongly associated with measured occupational gender preference.

## Current conclusion

The refined occupation-only scope gives a clearer and more defensible thesis direction.

The main finding is that Arabic-specific and multilingual causal language models show opposite occupational gender-preference patterns on the same Arabic counterfactual benchmark.

## Next steps

The next steps are:

1. human validation of the benchmark,
2. expanding occupations per field,
3. adding more Arabic and multilingual models,
4. dialect-level analysis,
5. template robustness analysis,
6. token-level explainability,
7. mitigation experiments.
