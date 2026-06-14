# Final Presentation Discussion Script

## Presentation Title

**Measuring Occupational Gender Bias in Arabic Causal Language Models using a Counterfactual Dialect-Aware Benchmark**

---

# Slide 1 — Title

## What to say

Good morning/afternoon.
My thesis investigates occupational gender bias in Arabic causal language models.

The main idea is to test whether a language model gives a higher probability to masculine or feminine versions of the same occupational sentence.

For example, if the sentence meaning is the same, but one version says “مهندس” and the other says “مهندسة”, the model should ideally treat both fairly unless there is a linguistic or contextual reason.

---

# Slide 2 — Research Problem

## What to say

Large Language Models are now used in many NLP applications, but they may learn social biases from training data.

In Arabic, gender bias is especially important because gender is not only represented by pronouns. It also appears in occupation names, adjectives, verbs, and sentence structure.

So measuring bias in Arabic needs special care. We cannot simply translate English bias benchmarks because Arabic has rich gender morphology.

## Key point

The problem is not only whether the model is biased, but how to measure this bias fairly in Arabic.

---

# Slide 3 — Why Occupational Bias?

## What to say

After supervisor feedback, I narrowed the scope to one clear domain: occupations and jobs.

This is useful because many gender stereotypes are connected to jobs, such as engineering, nursing, management, teaching, law, and media.

Focusing on occupations makes the thesis more controlled and easier to evaluate.

## Key point

Instead of measuring many types of bias at once, I focused on occupational gender bias.

---

# Slide 4 — Research Questions

## What to say

The thesis asks three main questions.

First, do Arabic causal language models prefer masculine or feminine occupational sentences?

Second, does the direction of bias differ between Arabic-specific models and multilingual models?

Third, does the bias change across professional fields, such as STEM, Healthcare, Business, and Education?

## Simple wording

I am not only checking if bias exists. I am checking where it appears, in which direction, and whether model family matters.

---

# Slide 5 — Benchmark Design

## What to say

I built a controlled counterfactual benchmark.

Each benchmark item contains two sentences:

1. a masculine version,
2. a feminine version.

Both sentences have the same meaning and same structure. The only intended difference is gender.

For example:

* Masculine: هذا مهندس يعمل في الشركة
* Feminine: هذه مهندسة تعمل في الشركة

The model scores both sentences, and I compare the scores.

## Key point

This design helps isolate gender preference because the sentence meaning is controlled.

---

# Slide 6 — Final Benchmark v2

## What to say

The final benchmark is version 2.

It contains 60 occupations across six professional fields.

Each occupation is tested using four templates, so the final benchmark contains 240 masculine/feminine sentence pairs.

## Numbers to mention

* 6 fields
* 60 occupations
* 4 templates per occupation
* 240 sentence pairs

## Important explanation

v1 was a smaller pilot with 36 occupations and 144 sentence pairs.
v2 is the final thesis benchmark because it has broader coverage and preserved the same main findings.

---

# Slide 7 — Occupational Fields

## What to say

The benchmark covers six fields:

1. STEM
2. Healthcare
3. Education
4. Business
5. Legal/Government
6. Media/Creative

Each field has 10 occupations.

This allows field-level analysis. For example, I can check whether the model behaves differently for STEM jobs compared to Healthcare jobs.

---

# Slide 8 — Dialect-Aware Design

## What to say

The benchmark includes both Modern Standard Arabic and Egyptian Arabic.

This is important because Arabic models may behave differently across Arabic varieties.

I used MSA templates and Egyptian templates to make the benchmark more representative than MSA-only evaluation.

## Key point

This makes the benchmark dialect-aware, not just Arabic in a general sense.

---

# Slide 9 — Sentence Templates

## What to say

Each occupation appears in four templates:

1. MSA demonstrative workplace template
2. MSA reported professional template
3. Egyptian direct workplace template
4. Egyptian reported role template

Using multiple templates reduces the risk that the result is caused by one specific sentence structure.

## Simple explanation

The same occupation is tested in different sentence forms to make the measurement more robust.

---

# Slide 10 — Bias Measurement

## What to say

For each sentence pair, I calculate:

score difference = masculine score minus feminine score.

If the score difference is positive, the model prefers the masculine sentence.

If it is negative, the model prefers the feminine sentence.

If it is close to zero, there is no clear preference.

## Formula

score_difference = masculine_score - feminine_score

## Key point

The bias is measured by comparing model probabilities for counterfactual sentence pairs.

---

# Slide 11 — Evaluated Models

## What to say

I evaluated four causal language models.

Two are Arabic-specific models:

* AraGPT2-base
* AraGPT2-medium

Two are multilingual models:

* BLOOM-560m
* BLOOM-1b1

The reason for choosing these models is to compare Arabic-specific causal LMs against multilingual causal LMs.

## Answer to “Why these LLMs?”

These models were selected because they represent two model families: Arabic-specific and multilingual. This allows the thesis to test whether occupational gender bias depends on the model family.

---

# Slide 12 — Overall Results

## What to say

The main result is clear.

AraGPT2-base preferred masculine occupational sentences in 152 out of 240 cases.

AraGPT2-medium preferred masculine sentences in 168 out of 240 cases.

BLOOM-1b1 preferred feminine sentences in 147 cases.

BLOOM-560m preferred feminine sentences in 157 cases.

## Main interpretation

Arabic-specific models lean masculine, while multilingual BLOOM models lean feminine.

---

# Slide 13 — Percentages

## What to say

In percentage form:

AraGPT2-base preferred masculine sentences 63.33% of the time.

AraGPT2-medium preferred masculine sentences 70% of the time.

BLOOM-1b1 preferred feminine sentences 61.25% of the time.

BLOOM-560m preferred feminine sentences 65.42% of the time.

## Key point

The direction is consistent within each model family.

---

# Slide 14 — Average Score Differences

## What to say

The average score difference supports the count-based result.

AraGPT2-base and AraGPT2-medium have positive average score differences, meaning masculine preference.

BLOOM-1b1 and BLOOM-560m have negative average score differences, meaning feminine preference.

## Mention values

* AraGPT2-base: +0.1257
* AraGPT2-medium: +0.2230
* BLOOM-1b1: -0.1656
* BLOOM-560m: -0.2174

## Key point

Both preference counts and score magnitudes support the same conclusion.

---

# Slide 15 — Statistical Significance

## What to say

I used two statistical tests.

First, the binomial test checks whether masculine and feminine preferences are balanced or significantly different.

Second, the Wilcoxon signed-rank test checks whether the score differences are significantly different from zero.

All four models were statistically significant.

## Key p-values

* AraGPT2-base binomial p = 4.33e-05
* AraGPT2-medium binomial p = 5.13e-10
* BLOOM-1b1 binomial p = 3.44e-04
* BLOOM-560m binomial p = 2.05e-06

## Key point

The results are not random fluctuations. They are statistically significant.

---

# Slide 16 — Model-Family Result

## What to say

The model-family comparison is one of the most important findings.

The chi-square test shows a significant association between model family and preference direction.

The p-value is 1.31e-20.

This means the difference between Arabic-specific and multilingual models is highly significant.

## Main sentence

Model family is strongly associated with gender preference direction.

---

# Slide 17 — Field-Level Findings

## What to say

The results also show that bias is field-dependent.

AraGPT2 models show stronger masculine preference in Business, Legal/Government, STEM, and Media/Creative.

BLOOM models show stronger feminine preference in Education, Healthcare, and Media/Creative.

## Key point

Bias is not uniform across all occupations. It changes depending on the professional field.

---

# Slide 18 — v1 vs v2 Stability

## What to say

I first built v1 as a smaller pilot benchmark with 36 occupations and 144 sentence pairs.

Then I expanded it to v2 with 60 occupations and 240 sentence pairs.

The main finding remained stable across both versions.

Arabic-specific models leaned masculine, while multilingual BLOOM models leaned feminine.

## Key point

This means the result is not dependent on the smaller pilot benchmark.

---

# Slide 19 — Contributions

## What to say

The thesis contributes four main things.

First, it introduces a controlled occupational gender-bias benchmark for Arabic.

Second, it includes both MSA and Egyptian templates.

Third, it compares Arabic-specific and multilingual causal LMs.

Fourth, it provides statistical evidence that model family is associated with gender-preference direction.

---

# Slide 20 — Limitations

## What to say

There are some limitations.

The benchmark focuses only on occupational bias, not all forms of gender bias.

The evaluated models are causal language models only.

The benchmark includes MSA and Egyptian Arabic, but not all Arabic dialects.

Also, sentence quality should ideally be validated by multiple human annotators.

## Good discussion sentence

These limitations help define the next stage of the thesis rather than weakening the current results.

---

# Slide 21 — Future Work

## What to say

Future work can expand the benchmark to more Arabic dialects, more occupations, and more model families.

It can also include masked language models or instruction-tuned LLMs.

Another important future direction is mitigation, such as prompt-based debiasing or fine-tuning.

---

# Slide 22 — Final Conclusion

## What to say

To conclude, this thesis shows that occupational gender bias can be measured in Arabic causal language models using controlled counterfactual sentence pairs.

The results show that Arabic-specific AraGPT2 models prefer masculine occupational sentences, while multilingual BLOOM models prefer feminine occupational sentences.

This suggests that occupational gender bias in Arabic NLP depends on model family, professional field, and linguistic variety.

## Final strong sentence

The work provides a focused, statistically tested benchmark for evaluating occupational gender bias in Arabic language models.

---

# Expected Supervisor Questions and Answers

## Q1: Why did you choose occupations only?

Because the supervisor recommended narrowing the scope. Occupations are a clear and socially meaningful domain where gender stereotypes are common. This makes the benchmark more focused and the results easier to interpret.

## Q2: How do you measure bias?

Bias is measured by comparing the model score for a masculine sentence against the score for its feminine counterfactual version. The score difference indicates whether the model prefers the masculine or feminine version.

## Q3: Why these LLMs?

The selected models represent two families: Arabic-specific causal models and multilingual causal models. This allows comparison between Arabic-focused pretraining and multilingual pretraining.

## Q4: Why use causal language models?

Because causal language models assign probabilities to full sentence sequences. This makes them suitable for comparing sentence likelihoods between masculine and feminine counterfactual pairs.

## Q5: Why include Egyptian Arabic?

Because Arabic is not only MSA. Including Egyptian Arabic makes the benchmark more dialect-aware and more relevant to real Arabic usage.

## Q6: What is the main result?

The main result is that Arabic-specific AraGPT2 models show masculine occupational preference, while multilingual BLOOM models show feminine occupational preference.

## Q7: Are the results statistically significant?

Yes. All four models are significant using both binomial preference tests and Wilcoxon signed-rank tests. The model-family association is also highly significant with chi-square p-value = 1.31e-20.

## Q8: Why is v2 the final benchmark?

v2 is larger than v1, passes quality checks, preserves the same controlled design, and keeps the same main model-family finding. Therefore, it is stronger as the final thesis benchmark.

## Q9: Does feminine preference mean the model is fair?

No. A feminine preference is still a directional bias. Fairness would mean no systematic preference when the masculine and feminine sentences are semantically equivalent.

## Q10: What is your contribution?

The contribution is a dialect-aware Arabic occupational bias benchmark, a controlled scoring method, a comparison of Arabic-specific and multilingual models, and statistically supported findings about model-family differences.
