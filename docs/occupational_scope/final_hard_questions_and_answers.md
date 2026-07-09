# Final Hard Questions and Answers

## Q1. Why did you keep v2 as the main benchmark instead of v3 or v4?

v2 is the main validated benchmark because it was tested across six models and produced a clear statistically significant model-family pattern.

v3 and v4 are not replacements for v2. They are sensitivity benchmarks. Their role is to test whether the measured bias remains stable when the benchmark design changes.

This actually strengthens the thesis because it shows that benchmark design affects measured bias.

---

## Q2. Why did AraGPT2 change direction in v3 and v4?

The diagnostics showed that the change was not caused by one simple factor.

v3 changed occupation coverage and lexical/contextual formulation. Even after using the original v2-style templates in v3 controlled, AraGPT2-base still showed feminine preference.

This suggests that occupation wording and benchmark formulation can strongly affect likelihood-based bias measurement.

---

## Q3. Is v3 a failed benchmark?

No. v3 is not a failed benchmark.

It is an experimental sensitivity benchmark. It revealed that Arabic occupational gender-bias measurement is sensitive to occupation coverage and wording.

This is an important methodological finding.

---

## Q4. Why is v4 important?

v4 is important because it tests whether measured bias is stable across different templates, semantic frames, and dialects.

The result showed that all six models had template-induced direction flips.

This means the same model can show masculine preference in one template and feminine preference in another.

---

## Q5. What is Template-Induced Bias Direction Volatility?

It is the observation that a model’s measured gender-preference direction changes across templates.

For example, a model may prefer masculine occupational sentences in an experience template but prefer feminine occupational sentences in a workplace or competence template.

This shows that bias measurement should report template-level sensitivity, not only one overall score.

---

## Q6. Why was stereotype label not significant in v4?

In v4, the occupation set was balanced across 30 male-stereotyped, 30 female-stereotyped, and 30 neutral occupations.

After balancing, stereotype label was not statistically significant.

This suggests that, under this controlled setup, template formulation, semantic frame, and dialect were stronger drivers of measured preference than stereotype category alone.

---

## Q7. Why use likelihood scoring?

Likelihood scoring is suitable for causal language models because it measures how probable the model finds each sentence.

By comparing masculine and feminine variants of the same sentence, the setup controls the sentence structure and isolates gendered occupational formulation.

---

## Q8. What are the limitations?

The main limitations are:

1. The benchmark is manually constructed and needs larger human validation.
2. The scoring method depends on model likelihood and tokenization.
3. Dialect coverage is limited to MSA and Egyptian Arabic.
4. v3 and v4 show that benchmark design strongly affects results.
5. External datasets were used as pilots, not full-scale validation.

---

## Q9. What is the future work?

Future work includes:

1. human validation with inter-annotator agreement,
2. larger external dataset integration,
3. more Arabic dialects,
4. more model families,
5. mitigation experiments,
6. prompt-based and generation-based bias evaluation,
7. a public Arabic bias benchmark suite.

---

## Q10. What is the final thesis claim?

The final claim is that Arabic occupational gender-bias evaluation is both model-dependent and benchmark-design-dependent.

The thesis shows that model family matters, but template, semantic frame, and dialect can strongly affect measured bias direction.