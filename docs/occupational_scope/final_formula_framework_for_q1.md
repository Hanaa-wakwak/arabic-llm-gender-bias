# Final Formula Framework for Arabic Occupational Gender Bias Evaluation

## Main Setting

This project evaluates open-weight causal language models using paired masculine-feminine Arabic counterfactual sentences.

Each benchmark item is defined as:

(x_i^m, x_i^f)

where:

- x_i^m is the masculine Arabic sentence.
- x_i^f is the feminine Arabic counterfactual sentence.

## Sentence Score

For a sentence x = (w_1, ..., w_n), the causal language model score is defined as average token log-probability:

S(x) = (1 / n) * sum log P(w_t | w_<t)

This normalization reduces sentence-length effects compared with total sentence probability.

## Pairwise Score Difference

For each masculine-feminine counterfactual pair:

Delta_i = S(x_i^m) - S(x_i^f)

This is implemented as:

score_difference = masculine_score - feminine_score

## Interpretation

Delta_i > 0 means masculine preference.
Delta_i < 0 means feminine preference.
Delta_i = 0 means equal preference.

## Overall Benchmark Bias

For N benchmark pairs:

Bias_avg = (1 / N) * sum Delta_i

## Absolute Disparity

Disparity_abs = (1 / N) * sum absolute(Delta_i)

## Preference Rates

R_m = number of masculine-preferred pairs / N
R_f = number of feminine-preferred pairs / N
R_e = number of equal-preference pairs / N

## Validation

The formula is validated in two ways:

1. The implementation recomputes score_difference as masculine_score minus feminine_score.
2. The implementation checks that preferred_gender matches the sign of score_difference.

## Relation to Prior Work

The exact Arabic occupational equation is this project's operational definition, but it is grounded in prior paired-sentence and likelihood-based bias evaluation methods, especially CrowS-Pairs, StereoSet, Kurita et al.'s log-probability bias scoring, and Kaneko and Bollegala's likelihood-based bias evaluation work.

## Black-Box API Extension

For black-box generative APIs where token probabilities are unavailable, a Counterfactual Parity Score can be used as a future extension:

CPS = 1 - mean absolute difference between f(y_f) and f(y_m)

This is not the main method of the current project. The main method is paired likelihood scoring for open-weight causal language models.
