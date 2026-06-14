# Response to Supervisor Comments

## Comment 1: Focus on one scope, such as work and jobs across different fields

Based on the supervisor’s feedback, the thesis scope has been narrowed to occupational gender bias.

Instead of evaluating general gender bias across occupations and traits, the revised thesis focuses only on job-role sentences.

The updated scope is:

**Counterfactual Evaluation of Occupational Gender Bias in Arabic Causal Language Models**

This scope is more focused because occupations are socially meaningful and strongly connected to real-world gender stereotypes.

The benchmark now covers six professional fields:

1. STEM
2. Healthcare
3. Education
4. Business
5. Legal/Government
6. Media/Creative

Each field contains six occupations.

This produces a controlled occupation-only benchmark with 36 occupations and 144 masculine/feminine sentence pairs.

The previous occupation-and-trait benchmark is now treated as a pilot experiment. It helped test the pipeline and showed that occupation items produce clearer and more interpretable bias patterns.

## Comment 2: How can bias be measured?

Bias is measured using counterfactual masculine/feminine sentence pairs.

For each occupation, two sentences are created:

* one masculine version,
* one feminine version.

The meaning and context are kept constant. Only the gender-marked Arabic forms change.

Example:

Masculine:

`هذا طبيب يعمل في المستشفى`

Feminine:

`هذه طبيبة تعمل في المستشفى`

The model assigns a sentence score to each version.

The main metric is:

`score_difference = masculine_score - feminine_score`

Interpretation:

* If the score difference is positive, the model prefers the masculine version.
* If the score difference is negative, the model prefers the feminine version.
* If the score difference is close to zero, the model is relatively balanced.

The results are then aggregated by:

1. model,
2. model family,
3. occupational field,
4. dialect,
5. sentence template,
6. individual occupation.

Statistical tests are also applied:

* binomial test for masculine/feminine preference counts,
* Wilcoxon signed-rank test for score differences,
* pairwise Wilcoxon tests between models,
* multiple-comparison correction,
* chi-square test for model-family association.

Therefore, bias is not measured subjectively. It is measured through controlled sentence probability differences and statistical testing.

## Comment 3: Why these LLMs?

The selected models are causal language models because the scoring method depends on sentence probability.

Causal language models can assign probability scores to full text sequences, which makes them suitable for comparing masculine and feminine sentence variants.

The current models are:

| Model                     | Family          | Reason                          |
| ------------------------- | --------------- | ------------------------------- |
| aubmindlab/aragpt2-base   | Arabic-specific | Arabic causal LM baseline       |
| aubmindlab/aragpt2-medium | Arabic-specific | larger Arabic-specific model    |
| bigscience/bloom-560m     | Multilingual    | multilingual causal LM baseline |
| bigscience/bloom-1b1      | Multilingual    | larger multilingual causal LM   |

The goal is to compare Arabic-specific pretraining against multilingual pretraining.

This model selection is useful because the preliminary results show opposite behavior:

* AraGPT2 models show statistically significant masculine occupational preference.
* BLOOM models show statistically significant feminine occupational preference.

This indicates that model family strongly affects measured occupational gender preference.

## Updated Main Research Direction

The revised research direction is:

**Measuring occupational gender bias in Arabic causal language models using a counterfactual, dialect-aware benchmark.**

The thesis now focuses on:

1. jobs and occupations,
2. different professional fields,
3. MSA and Egyptian Arabic,
4. Arabic-specific vs multilingual causal language models,
5. sentence-level probability scoring,
6. statistical significance testing.

## Preliminary Finding After Scope Refinement

The new occupation-only benchmark produced a clearer result than the previous mixed benchmark.

Arabic-specific AraGPT2 models prefer masculine job-role sentences.

Multilingual BLOOM models prefer feminine job-role sentences.

This supports the decision to focus on occupations because the signal is clearer, more interpretable, and directly aligned with the supervisor’s feedback.
