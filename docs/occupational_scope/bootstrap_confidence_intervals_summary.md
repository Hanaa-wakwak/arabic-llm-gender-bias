# Bootstrap Confidence Intervals for Bias Scores

## Purpose

This analysis estimates uncertainty around the average score difference for each model and benchmark.

The score is defined as:

```text
score_difference = masculine_score - feminine_score
```

A positive mean indicates masculine preference. A negative mean indicates feminine preference.

## Method

For each model and benchmark, the analysis uses 5000 bootstrap resamples to estimate a 95% confidence interval for the mean score difference.

## Interpretation

- If the confidence interval is entirely above zero, the result is classified as reliably masculine.
- If the confidence interval is entirely below zero, the result is classified as reliably feminine.
- If the confidence interval crosses zero, the result is classified as uncertain or near-neutral.

## Results

| benchmark | model_name | n_items | mean_score_difference | median_score_difference | std_score_difference | ci_level | bootstrap_iterations | ci_lower | ci_upper | mean_direction | ci_direction_classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v2 | Qwen/Qwen2.5-0.5B | 240 | -0.34251 | -0.23438 | 0.63843 | 0.95000 | 5000 | -0.42526 | -0.26256 | feminine | reliably_feminine |
| v2 | aubmindlab/aragpt2-base | 240 | 0.12571 | 0.25368 | 0.78167 | 0.95000 | 5000 | 0.02533 | 0.22109 | masculine | reliably_masculine |
| v2 | aubmindlab/aragpt2-medium | 240 | 0.22303 | 0.32487 | 0.76584 | 0.95000 | 5000 | 0.12627 | 0.31846 | masculine | reliably_masculine |
| v2 | bigscience/bloom-1b1 | 240 | -0.16555 | -0.19336 | 0.73357 | 0.95000 | 5000 | -0.25786 | -0.07322 | feminine | reliably_feminine |
| v2 | bigscience/bloom-560m | 240 | -0.21744 | -0.21680 | 0.70177 | 0.95000 | 5000 | -0.30492 | -0.13132 | feminine | reliably_feminine |
| v2 | facebook/xglm-564M | 240 | -0.21379 | -0.21680 | 0.62194 | 0.95000 | 5000 | -0.29209 | -0.13414 | feminine | reliably_feminine |
| v3_balanced | aubmindlab/aragpt2-base | 360 | -0.43938 | -0.38125 | 0.76098 | 0.95000 | 5000 | -0.51666 | -0.36258 | feminine | reliably_feminine |
| v3_balanced | bigscience/bloom-560m | 360 | -0.14618 | -0.16211 | 0.60570 | 0.95000 | 5000 | -0.20835 | -0.08285 | feminine | reliably_feminine |
| v4 | Qwen/Qwen2.5-0.5B | 720 | -0.08900 | -0.07812 | 0.50106 | 0.95000 | 5000 | -0.12485 | -0.05224 | feminine | reliably_feminine |
| v4 | aubmindlab/aragpt2-base | 721 | -0.34536 | -0.27399 | 0.78988 | 0.95000 | 5000 | -0.40311 | -0.29009 | feminine | reliably_feminine |
| v4 | aubmindlab/aragpt2-medium | 721 | -0.30664 | -0.17730 | 0.93652 | 0.95000 | 5000 | -0.37532 | -0.23683 | feminine | reliably_feminine |
| v4 | bigscience/bloom-1b1 | 720 | -0.17003 | -0.19531 | 0.63009 | 0.95000 | 5000 | -0.21511 | -0.12464 | feminine | reliably_feminine |
| v4 | bigscience/bloom-560m | 720 | -0.17029 | -0.26172 | 0.63149 | 0.95000 | 5000 | -0.21692 | -0.12295 | feminine | reliably_feminine |
| v4 | facebook/xglm-564M | 720 | -0.44112 | -0.44238 | 0.45435 | 0.95000 | 5000 | -0.47481 | -0.40762 | feminine | reliably_feminine |
| v5 | aubmindlab/aragpt2-base | 540 | -0.03385 | 0.02778 | 0.54981 | 0.95000 | 5000 | -0.08029 | 0.01422 | feminine | uncertain_crosses_zero |
| v5 | bigscience/bloom-560m | 540 | 0.07095 | 0.01758 | 0.37722 | 0.95000 | 5000 | 0.03991 | 0.10272 | masculine | reliably_masculine |

## Contribution

This analysis enriches the thesis by adding uncertainty estimation to the bias scores. It helps distinguish strong directional findings from weak or near-neutral effects.

This is especially useful for benchmarks such as v5, where average score differences can be small and close to zero.
