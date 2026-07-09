# Final Presentation Storyline

## Slide 1 — Title

Detecting and Analyzing Occupational Gender Bias in Arabic Causal Language Models

Say:
This thesis studies whether Arabic causal language models prefer masculine or feminine occupational sentences.

---

## Slide 2 — Motivation

Arabic is morphologically gendered, so gender bias can appear in occupational wording.

Say:
In Arabic, many occupations have masculine and feminine forms. This makes Arabic an important language for studying gender bias in language models.

---

## Slide 3 — Research Problem

Most bias evaluation work focuses on English or on general multilingual settings.

Say:
Arabic has dialects, grammatical gender, and occupation-specific gender forms, so it needs targeted evaluation.

---

## Slide 4 — Main Method

I compare masculine and feminine versions of the same sentence.

Say:
For each pair, I score both sentences using model likelihood and calculate masculine score minus feminine score.

---

## Slide 5 — Bias Score

score_difference = masculine_score - feminine_score

Say:
Positive means masculine preference. Negative means feminine preference. Zero means equal preference.

---

## Slide 6 — v2 Main Benchmark

60 occupations, 4 templates, 240 sentence pairs.

Say:
This is the main validated benchmark used for the core thesis result.

---

## Slide 7 — Models

Six causal language models:
AraGPT2-base, AraGPT2-medium, BLOOM-560m, BLOOM-1b1, XGLM-564M, Qwen2.5-0.5B.

Say:
I compared Arabic-specific models with non-Arabic-specific multilingual/general models.

---

## Slide 8 — v2 Main Result

Arabic-specific models showed masculine preference.
Non-Arabic-specific models showed feminine preference.

Say:
This result was statistically significant and forms the main empirical result.

---

## Slide 9 — Why More Benchmarks?

Say:
After obtaining the main result, I wanted to test whether the measurement is stable. So I created additional benchmark versions.

---

## Slide 10 — v3 Sensitivity

v3 expanded occupations and templates.

Say:
v3 showed that benchmark expansion can change measured bias direction, so v3 became a sensitivity benchmark rather than a replacement for v2.

---

## Slide 11 — v3 Controlled

Say:
v3 controlled used the expanded occupation list but only the original v2-style templates. This helped separate occupation effects from template effects.

---

## Slide 12 — v3 Balanced

90 occupations:
30 male-stereotyped,
30 female-stereotyped,
30 neutral.

Say:
Even after balancing stereotype labels, measured direction still changed. This showed that stereotype balance alone is not enough.

---

## Slide 13 — v4 Template Perturbation

90 occupations, 8 templates, 6 semantic frames, 2 dialects, 720 pairs.

Say:
v4 is the strongest methodological extension. It tests template, semantic frame, and dialect sensitivity.

---

## Slide 14 — v4 All-Model Result

All six models were overall feminine on v4.

Say:
The overall result was feminine, but the more important finding is the template-level behavior.

---

## Slide 15 — Template-Induced Direction Flips

All six models showed direction flips.

Say:
The same model can prefer masculine sentences in one template and feminine sentences in another template.

---

## Slide 16 — Statistical Tests

Template ID, semantic frame, dialect, model name, model family, and field were significant.
Stereotype label was not significant after balancing.

Say:
This shows that benchmark design strongly affects measured bias.

---

## Slide 17 — Effect Sizes

Template ID had the strongest practical effect using Cramér’s V.

Say:
Template formulation was stronger than model family and stereotype label in practical effect size.

---

## Slide 18 — External Pilots

APGC and ArGAN pilots.

Say:
These pilots show how the pipeline can be extended to external Arabic gender datasets and qualitative generation-based bias analysis.

---

## Slide 19 — Final Contribution

Say:
The thesis contributes a robustness-oriented Arabic occupational gender-bias evaluation suite.

---

## Slide 20 — Conclusion

Say:
Arabic occupational gender-bias evaluation is both model-dependent and benchmark-design-dependent.