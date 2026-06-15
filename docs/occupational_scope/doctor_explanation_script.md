# Doctor Explanation Script

## If the doctor asks: What did you do?

I built a controlled benchmark to measure occupational gender bias in Arabic causal language models.

The benchmark compares masculine and feminine versions of the same occupational sentence.

For example:

```text
هذا مهندس يعمل في الشركة
هذه مهندسة تعمل في الشركة
```

The meaning is kept the same, and only the grammatical gender changes.

The final benchmark contains 60 occupations, 6 professional fields, 4 templates per occupation, and 240 masculine/feminine sentence pairs.

---

## If the doctor asks: What is the main idea?

The main idea is to test whether Arabic language models prefer masculine or feminine occupational forms when the sentence meaning is controlled.

I use a counterfactual design:

```text
masculine sentence vs feminine sentence
```

Then I compare their model likelihood scores.

---

## If the doctor asks: How did you measure bias?

I used this score:

```text
score_difference = masculine_score - feminine_score
```

If the score is positive, the model prefers the masculine sentence.

If the score is negative, the model prefers the feminine sentence.

If the score is near zero, there is no clear preference.

---

## If the doctor asks: What models did you test?

I tested six causal language models:

| Model          | Family              |
| -------------- | ------------------- |
| AraGPT2-base   | Arabic-specific     |
| AraGPT2-medium | Arabic-specific     |
| BLOOM-560m     | Non-Arabic-specific |
| BLOOM-1b1      | Non-Arabic-specific |
| XGLM-564M      | Non-Arabic-specific |
| Qwen2.5-0.5B   | Non-Arabic-specific |

---

## If the doctor asks: What is the main result?

The main result is that the direction of bias differs by model family.

Arabic-specific AraGPT2 models showed masculine occupational preference.

Non-Arabic-specific multilingual/general models showed feminine occupational preference.

| Model Family        | Total Items | Masculine Preferred | Feminine Preferred | Direction |
| ------------------- | ----------: | ------------------: | -----------------: | --------- |
| Arabic-specific     |         480 |                 320 |                160 | Masculine |
| Non-Arabic-specific |         960 |                 346 |                610 | Feminine  |

The chi-square test showed that this model-family difference is statistically significant.

```text
p-value = 1.64e-27
```

---

## If the doctor asks: Why is this important?

This is important because it shows that Arabic gender bias is not the same across all models.

The bias direction changes depending on the model family.

So we cannot say that all Arabic models behave the same way.

The training data, tokenizer, and model background may affect gender preference.

---

## If the doctor asks: Why did you use occupations?

I used occupations because professional roles are a common area where gender stereotypes appear.

Examples include:

```text
doctor / engineer / teacher / manager / lawyer / journalist
```

Occupations also allow clear masculine and feminine Arabic forms, so they are suitable for controlled counterfactual testing.

---

## If the doctor asks: Why Arabic is special here?

Arabic is morphologically gendered.

Gender appears in many parts of the sentence:

* nouns,
* verbs,
* adjectives,
* pronouns,
* demonstratives.

For example:

```text
هو / هي
هذا / هذه
مهندس / مهندسة
يعمل / تعمل
محترف / محترفة
```

So Arabic gender-bias evaluation needs full sentence-level control, not only word replacement.

---

## If the doctor asks: What is new in your work?

The novelty is that I created a controlled Arabic occupational benchmark with:

1. masculine/feminine counterfactual sentence pairs,
2. MSA and Egyptian Arabic templates,
3. 60 occupations across 6 fields,
4. six-model comparison,
5. statistical testing,
6. external dataset pilots using APGC-format and ArGAN-format samples.

---

## If the doctor asks: What are APGC and ArGAN doing here?

The main benchmark is still my occupational benchmark.

APGC and ArGAN are external pilot validations.

APGC checks whether the same sentence-pair scoring method can work beyond occupations.

ArGAN checks whether prompt-based Arabic bias evaluation is possible.

So:

| Dataset            | Role                              |
| ------------------ | --------------------------------- |
| Occupational v2    | Main quantitative benchmark       |
| APGC-format pilot  | External sentence-pair validation |
| ArGAN-format pilot | Qualitative prompt-based pilot    |

---

## If the doctor asks: Are APGC and ArGAN final results?

No.

They are pilot experiments.

APGC has only 10 sentence pairs, so it validates the pipeline but is not enough for statistical claims.

ArGAN depends on generation quality and needs manual annotation, so it is reported as qualitative validation and future work.

---

## If the doctor asks: What are the limitations?

The main limitations are:

1. the benchmark focuses only on occupations,
2. it covers only MSA and Egyptian Arabic,
3. only six models were tested,
4. APGC and ArGAN are pilot-level only,
5. mitigation was not implemented yet.

---

## If the doctor asks: What is your future work?

Future work includes:

1. expanding the benchmark to more occupations and dialects,
2. integrating the full APGC dataset,
3. evaluating the full ArGAN gender subset,
4. testing stronger Arabic instruction models,
5. applying bias mitigation,
6. adding explainability to identify which tokens drive gender preference.

---

## Very Short 1-Minute Explanation

My thesis measures occupational gender bias in Arabic causal language models.

I created a controlled benchmark of 240 masculine/feminine Arabic occupational sentence pairs. The meaning stays the same, and only gender changes.

For each pair, I compute:

```text
score_difference = masculine_score - feminine_score
```

Positive means masculine preference, negative means feminine preference.

I tested six models. AraGPT2 Arabic-specific models showed masculine preference, while non-Arabic-specific models such as BLOOM, XGLM, and Qwen showed feminine preference.

The model-family difference was statistically significant with a chi-square p-value of 1.64e-27.

I also added APGC and ArGAN pilot experiments to show that the pipeline can be extended to external Arabic gender-bias datasets, but the main result remains the occupational benchmark.
