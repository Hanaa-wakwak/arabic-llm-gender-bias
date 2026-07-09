# Final Viva 2-Minute Script

My thesis studies occupational gender bias in Arabic causal language models.

The main idea is to compare masculine and feminine versions of the same Arabic occupational sentence and measure which one receives a higher likelihood from the model.

I built a controlled benchmark where each item contains a masculine sentence and a feminine sentence. The score is calculated as:

score_difference = masculine_score - feminine_score

A positive score means the model prefers the masculine sentence, while a negative score means it prefers the feminine sentence.

The main validated benchmark is v2. It contains 60 occupations, 4 templates, and 240 sentence pairs. I tested six causal language models. The v2 result showed a statistically significant model-family pattern: Arabic-specific AraGPT2 models preferred masculine occupational sentences, while non-Arabic-specific multilingual models preferred feminine occupational sentences.

Then I enhanced the work by testing whether this measurement is stable. I created v3, v3 controlled, and v3 balanced benchmarks. These experiments showed that benchmark expansion and occupation wording can change measured bias direction. Therefore, I kept v2 as the main validated benchmark and treated v3 as sensitivity analysis.

The strongest extension is v4, the template perturbation benchmark. It uses 90 balanced occupations, 8 templates, 6 semantic frames, and 2 dialects. I tested all six models. All models showed overall feminine preference in v4, but more importantly, all models showed template-induced direction flips. This means the same model can prefer masculine sentences under one template and feminine sentences under another.

I also ran chi-square tests and Cramér’s V effect-size analysis. The strongest practical factor was template ID, followed by semantic frame, model name, and dialect. Stereotype label was not significant after balancing.

So the final contribution is not only detecting bias. The thesis contributes a robustness-oriented Arabic occupational gender-bias evaluation suite and shows that Arabic bias measurement is both model-dependent and benchmark-design-dependent.