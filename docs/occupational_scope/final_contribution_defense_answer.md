# Final Contribution Defense Answer

## If the examiner asks: What is your contribution?

My contribution is an Arabic occupational gender-bias evaluation suite for causal language models.

The contribution has two levels.

First, I created a main validated benchmark, v2, to measure occupational gender preference in Arabic causal language models. It uses controlled masculine-feminine sentence pairs and was evaluated on six models.

Second, I extended the work into a robustness and sensitivity suite. I created v3, v3 controlled, v3 balanced, and v4 to test whether measured bias remains stable when the benchmark design changes.

The most important contribution is the v4 template perturbation benchmark. It showed that measured bias can change depending on template, semantic frame, and dialect. All six models showed template-induced direction flips.

Statistical tests showed that template ID, semantic frame, dialect, model name, model family, and field significantly affect preferred gender. Effect-size analysis showed that template ID had the strongest practical effect.

So the thesis does not only answer whether Arabic models are biased. It also shows that Arabic gender-bias measurement itself is sensitive to benchmark design.

## Short Version

My contribution is a robustness-oriented Arabic occupational gender-bias evaluation suite. It measures bias and also tests whether the measurement is stable across benchmark versions, templates, dialects, and semantic frames.

## Strongest Sentence

Arabic occupational gender-bias evaluation is not only model-dependent; it is also benchmark-design-dependent.