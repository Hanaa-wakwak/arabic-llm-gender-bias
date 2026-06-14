# Final Thesis Report Structure

## Thesis Title

**Measuring Occupational Gender Bias in Arabic Causal Language Models using a Counterfactual Dialect-Aware Benchmark**

---

# Chapter 1 — Introduction

## 1.1 Background

Introduce Large Language Models and their increasing use in NLP applications.

Explain that LLMs learn from large-scale textual data and may reproduce social biases found in that data.

Then introduce gender bias as one important fairness issue.

## 1.2 Motivation

Explain why Arabic needs special attention:

* Arabic has grammatical gender.
* Gender appears in nouns, verbs, adjectives, pronouns, and occupation names.
* Arabic includes multiple varieties, such as MSA and dialects.
* English bias benchmarks cannot be directly transferred to Arabic.

## 1.3 Problem Statement

Existing Arabic bias evaluation is limited, especially for occupational gender bias in causal language models.

There is a need for a controlled benchmark that compares masculine and feminine versions of the same Arabic occupational sentence.

## 1.4 Research Questions

RQ1. Do Arabic causal language models show systematic gender preference in occupational sentences?

RQ2. Does the gender preference direction differ between Arabic-specific and multilingual causal language models?

RQ3. Does occupational gender bias vary across professional fields?

RQ4. Does the pattern remain stable when the benchmark is expanded from v1 to v2?

## 1.5 Contributions

This thesis contributes:

1. A controlled Arabic occupational gender-bias benchmark.
2. A dialect-aware design covering MSA and Egyptian Arabic.
3. A counterfactual scoring method using masculine/feminine sentence pairs.
4. An empirical comparison between Arabic-specific and multilingual causal LMs.
5. Statistical analysis using binomial, Wilcoxon, chi-square, and pairwise tests.

## 1.6 Thesis Organization

Briefly describe what each chapter contains.

---

# Chapter 2 — Literature Review

## 2.1 Bias in Language Models

Discuss how LMs can encode social stereotypes and reproduce biased associations.

## 2.2 Gender Bias in NLP

Explain gender bias in text generation, classification, embeddings, and language modeling.

## 2.3 Occupational Gender Bias

Explain why occupations are commonly used in bias evaluation.

Examples:

* engineer vs nurse,
* manager vs teacher,
* judge vs secretary.

## 2.4 Arabic NLP and Gender Morphology

Explain that Arabic gender is morphologically rich.

Important points:

* masculine/feminine occupation forms,
* agreement in verbs and adjectives,
* demonstratives مثل هذا / هذه,
* pronouns هو / هي.

## 2.5 Counterfactual Bias Evaluation

Explain counterfactual evaluation:

Two sentences are identical in meaning except for the protected attribute.

In this thesis, the protected attribute is gender.

## 2.6 Arabic Bias Benchmarks

Review existing Arabic or multilingual bias datasets and explain the gap:

* limited dialect coverage,
* limited occupation-specific analysis,
* limited causal LM scoring,
* lack of controlled Arabic counterfactual occupational benchmark.

## 2.7 Summary of Literature Gap

Conclude that Arabic occupational gender-bias evaluation needs a focused, controlled, dialect-aware benchmark.

---

# Chapter 3 — Methodology

## 3.1 Research Design

Explain that the thesis uses a quantitative experimental design.

The experiment compares model scores for masculine and feminine occupational sentence pairs.

## 3.2 Benchmark Scope

The final benchmark focuses only on occupations.

Explain that the scope was narrowed based on supervisor feedback to make the project more focused and interpretable.

## 3.3 Benchmark Versions

### v1 Pilot Benchmark

* 36 occupations,
* 6 fields,
* 4 templates,
* 144 sentence pairs.

### v2 Final Benchmark

* 60 occupations,
* 6 fields,
* 4 templates,
* 240 sentence pairs.

State that v2 is the final benchmark and v1 is the pilot/sanity-check version.

## 3.4 Occupational Fields

The six fields are:

1. STEM
2. Healthcare
3. Education
4. Business
5. Legal/Government
6. Media/Creative

Each field contains 10 occupations in v2.

## 3.5 Dialect-Aware Templates

The benchmark includes:

* Modern Standard Arabic,
* Egyptian Arabic.

Each occupation has four templates:

1. MSA demonstrative workplace template
2. MSA reported professional template
3. Egyptian direct workplace template
4. Egyptian reported role template

## 3.6 Counterfactual Pair Construction

Each benchmark item contains:

* masculine sentence,
* feminine sentence,
* same field,
* same occupation meaning,
* same template,
* same workplace/context.

Example:

Masculine:

```text
هذا مهندس يعمل في الشركة
```

Feminine:

```text
هذه مهندسة تعمل في الشركة
```

## 3.7 Model Selection

The thesis evaluates four causal language models.

| Model                     | Family          |
| ------------------------- | --------------- |
| aubmindlab/aragpt2-base   | Arabic-specific |
| aubmindlab/aragpt2-medium | Arabic-specific |
| bigscience/bloom-560m     | Multilingual    |
| bigscience/bloom-1b1      | Multilingual    |

The purpose is to compare Arabic-specific models against multilingual models.

## 3.8 Scoring Method

For each sentence pair:

```text
score_difference = masculine_score - feminine_score
```

Interpretation:

| Score Difference | Meaning              |
| ---------------: | -------------------- |
|         Positive | Masculine preference |
|         Negative | Feminine preference  |
|        Near zero | Balanced             |

## 3.9 Statistical Tests

Use:

1. Binomial test
   To test whether masculine/feminine preference counts differ from chance.

2. Wilcoxon signed-rank test
   To test whether score differences differ significantly from zero.

3. Chi-square test
   To test association between model family and preference direction.

4. Pairwise Wilcoxon tests
   To compare models directly, with multiple-comparison correction.

## 3.10 Quality Control

Explain:

* benchmark quality check script,
* no missing values,
* no duplicate sentence pairs,
* no identical masculine/feminine sentences,
* human validation plan.

---

# Chapter 4 — Experiments and Results

## 4.1 Experimental Setup

Describe:

* benchmark file,
* models,
* scoring pipeline,
* output files,
* analysis scripts.

## 4.2 Overall v2 Results

| Model          | Family          | Masculine Preferred | Feminine Preferred | Equal | Direction |
| -------------- | --------------- | ------------------: | -----------------: | ----: | --------- |
| AraGPT2-base   | Arabic-specific |                 152 |                 88 |     0 | Masculine |
| AraGPT2-medium | Arabic-specific |                 168 |                 72 |     0 | Masculine |
| BLOOM-1b1      | Multilingual    |                  91 |                147 |     2 | Feminine  |
| BLOOM-560m     | Multilingual    |                  83 |                157 |     0 | Feminine  |

## 4.3 Overall Percentages

| Model          | Masculine % | Feminine % | Direction |
| -------------- | ----------: | ---------: | --------- |
| AraGPT2-base   |      63.33% |     36.67% | Masculine |
| AraGPT2-medium |      70.00% |     30.00% | Masculine |
| BLOOM-1b1      |      37.92% |     61.25% | Feminine  |
| BLOOM-560m     |      34.58% |     65.42% | Feminine  |

## 4.4 Average Score Differences

| Model          | Average Score Difference | Median Score Difference | Direction |
| -------------- | -----------------------: | ----------------------: | --------- |
| AraGPT2-base   |                  +0.1257 |                 +0.2537 | Masculine |
| AraGPT2-medium |                  +0.2230 |                 +0.3249 | Masculine |
| BLOOM-1b1      |                  -0.1656 |                 -0.1934 | Feminine  |
| BLOOM-560m     |                  -0.2174 |                 -0.2168 | Feminine  |

## 4.5 Statistical Significance

### Binomial Test

| Model          | Direction |  p-value | Significant |
| -------------- | --------- | -------: | ----------- |
| AraGPT2-base   | Masculine | 4.33e-05 | Yes         |
| AraGPT2-medium | Masculine | 5.13e-10 | Yes         |
| BLOOM-1b1      | Feminine  | 3.44e-04 | Yes         |
| BLOOM-560m     | Feminine  | 2.05e-06 | Yes         |

### Wilcoxon Test

| Model          |  p-value | Significant |
| -------------- | -------: | ----------- |
| AraGPT2-base   | 2.79e-04 | Yes         |
| AraGPT2-medium | 3.29e-08 | Yes         |
| BLOOM-1b1      | 8.51e-05 | Yes         |
| BLOOM-560m     | 5.76e-07 | Yes         |

## 4.6 Model-Family Analysis

The chi-square p-value is:

```text
1.31e-20
```

This shows a strong association between model family and preference direction.

## 4.7 Field-Level Results

Summarize:

Arabic-specific models show stronger masculine preference in:

* Business,
* Legal/Government,
* STEM,
* Media/Creative.

Multilingual models show stronger feminine preference in:

* Education,
* Healthcare,
* Media/Creative.

## 4.8 Pairwise Model Comparison

Explain:

* AraGPT2 models significantly differ from BLOOM models.
* BLOOM-1b1 and BLOOM-560m do not significantly differ from each other.
* The largest separation is between model families.

## 4.9 v1 vs v2 Stability

Explain that v1 and v2 show the same main model-family pattern.

v2 is selected as final because it is larger and more robust.

---

# Chapter 5 — Discussion

## 5.1 Interpretation of Main Finding

The results show that occupational gender preference is not uniform across language models.

Arabic-specific models lean masculine.

Multilingual BLOOM models lean feminine.

## 5.2 Why Model Family Matters

Discuss possible reasons:

* different training corpora,
* different Arabic coverage,
* different tokenizer behavior,
* different multilingual distribution,
* different exposure to gendered occupation forms.

## 5.3 Field Dependency

Explain that bias changes by professional field.

This means it is not enough to say “the model is biased”; we should ask:

* biased in which field?
* in which direction?
* for which model family?

## 5.4 Feminine Preference Is Still Bias

Clarify that feminine preference does not automatically mean fairness.

A systematic feminine preference is still directional bias when the two sentences are semantically equivalent.

## 5.5 Arabic-Specific Challenges

Discuss Arabic grammar:

* gendered nouns,
* adjective agreement,
* verb agreement,
* dialect differences,
* occupation forms.

## 5.6 Answering the Research Questions

Directly answer each RQ using results.

## 5.7 Relation to Prior Work

Connect the findings back to the literature review.

---

# Chapter 6 — Conclusion and Future Work

## 6.1 Conclusion

Summarize the thesis:

This thesis proposed a controlled, dialect-aware Arabic benchmark for occupational gender bias in causal language models.

## 6.2 Main Findings

1. AraGPT2 models show masculine occupational preference.
2. BLOOM models show feminine occupational preference.
3. Model family is significantly associated with preference direction.
4. Bias varies across occupational fields.
5. v2 confirms the stability of the main finding.

## 6.3 Contributions

Repeat contributions clearly:

* benchmark,
* scoring pipeline,
* model-family comparison,
* statistical analysis,
* dialect-aware Arabic design.

## 6.4 Limitations

Mention:

* only occupational bias,
* only MSA and Egyptian Arabic,
* only causal LMs,
* limited number of models,
* human validation still needs expansion.

## 6.5 Future Work

Future work can include:

1. More Arabic dialects.
2. More model families.
3. Instruction-tuned LLMs.
4. Masked language models.
5. Larger human validation.
6. Bias mitigation experiments.
7. Explainability analysis.
8. Fine-tuning or prompt-based debiasing.

---

# Appendix

## Appendix A — Occupation Lexicon

Include `occupations_fields_v2.csv`.

## Appendix B — Benchmark Samples

Include examples from `occupational_bias_v2.csv`.

## Appendix C — Statistical Test Outputs

Include:

* binomial test tables,
* Wilcoxon tables,
* chi-square result,
* pairwise model comparison.

## Appendix D — Human Validation Sheet

Include validation guidelines and sample rows.

## Appendix E — Code Repository Structure

Briefly explain the main scripts and folders.
