# v4 vs v5 Job-Title Context Comparison

## Purpose

This comparison tests whether explicit job-title contexts behave differently from broader occupational sentence templates.

v4 evaluates occupations inside broader semantic frames such as workplace presence, experience, competence, leadership, achievement, and responsibility.

v5 isolates the occupation as an explicit job title in CV, job advertisement, HR record, and professional profile contexts.

## Comparison Table

| benchmark | model_name | total_items | masculine_preferred_count | feminine_preferred_count | equal_count | average_score_difference | median_score_difference | direction_by_average | direction_by_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v4 | aubmindlab/aragpt2-base | 720 | 220 | 500 | 0 | -0.3484 | -0.2755 | feminine | feminine |
| v4 | bigscience/bloom-560m | 720 | 256 | 460 | 4 | -0.1703 | -0.2617 | feminine | feminine |
| v5 | aubmindlab/aragpt2-base | 540 | 284 | 256 | 0 | -0.0338 | 0.0278 | feminine | masculine |
| v5 | bigscience/bloom-560m | 540 | 278 | 261 | 1 | 0.0709 | 0.0176 | masculine | masculine |

## Interpretation

The v5 benchmark shows that explicit job-title contexts can produce weaker or different gender-preference directions compared with broader v4 sentence contexts.

AraGPT2-base is near-balanced in v5, while BLOOM-560m shows weak masculine preference. This contrasts with the broader v4 setting, where both models showed overall feminine preference.

## Thesis Relevance

This comparison strengthens the thesis claim that Arabic occupational gender-bias measurement is benchmark-design-dependent. The measured direction can change when the occupation is presented as a direct job title rather than embedded in a broader occupational sentence frame.
