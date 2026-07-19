# Final Implementation Results Report

## Purpose

This report consolidates the main technical outputs of the Arabic occupational gender-bias evaluation suite.

The final implementation includes:

1. v2 main validated benchmark,
2. v3 sensitivity benchmarks,
3. v3 balanced benchmark,
4. v4 template perturbation benchmark,
5. statistical tests,
6. effect-size analysis.

## v2 Main Validated Benchmark

The v2 benchmark remains the main validated benchmark.

### v2 Overall by Model

| model_name | model_family | model_category | total_items | masculine_preferred_count | feminine_preferred_count | equal_count | masculine_preferred_percent | feminine_preferred_percent | equal_percent | average_score_difference | median_score_difference | min_score_difference | max_score_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen/Qwen2.5-0.5B | Non-Arabic-specific | General-multilingual-Qwen | 240 | 80 | 158 | 2 | 33.3333 | 65.8333 | 0.8333 | -0.3425 | -0.2344 | -2.8438 | 1.2188 |
| aubmindlab/aragpt2-base | Arabic-specific | Arabic-specific | 240 | 152 | 88 | 0 | 63.3333 | 36.6667 | 0.0000 | 0.1257 | 0.2537 | -3.3602 | 2.0434 |
| aubmindlab/aragpt2-medium | Arabic-specific | Arabic-specific | 240 | 168 | 72 | 0 | 70.0000 | 30.0000 | 0.0000 | 0.2230 | 0.3249 | -3.0709 | 2.1319 |
| bigscience/bloom-1b1 | Non-Arabic-specific | Multilingual-BLOOM | 240 | 91 | 147 | 2 | 37.9167 | 61.2500 | 0.8333 | -0.1656 | -0.1934 | -2.2227 | 2.5312 |
| bigscience/bloom-560m | Non-Arabic-specific | Multilingual-BLOOM | 240 | 83 | 157 | 0 | 34.5833 | 65.4167 | 0.0000 | -0.2174 | -0.2168 | -2.4531 | 2.2188 |
| facebook/xglm-564M | Non-Arabic-specific | Multilingual-XGLM | 240 | 92 | 148 | 0 | 38.3333 | 61.6667 | 0.0000 | -0.2138 | -0.2168 | -2.2344 | 1.3789 |

### v2 Model-Family Summary

_File not found or could not be read._

### v2 Chi-Square Test

_File not found or could not be read._

## v3 Balanced Sensitivity Benchmark

The v3 balanced benchmark was created to test whether stereotype balancing stabilizes the measured bias direction.

### Quality Check

| issue_type | details | count |
| --- | --- | --- |
| no_issues_found | v3 balanced benchmark passed quality checks | 0 |

### Stereotype Row Counts

| stereotype_label | count |
| --- | --- |
| male_stereotyped | 120 |
| female_stereotyped | 120 |
| neutral | 120 |

### Stereotype Occupation Counts

| stereotype_label | occupation_count |
| --- | --- |
| male_stereotyped | 30 |
| female_stereotyped | 30 |
| neutral | 30 |

### v3 Balanced Quick Model Results

AraGPT2-base:

| model_name | total_items | masculine_preferred_count | feminine_preferred_count | equal_count | masculine_preferred_percent | feminine_preferred_percent | equal_percent | average_score_difference | median_score_difference | min_score_difference | max_score_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| aubmindlab/aragpt2-base | 360 | 98 | 262 | 0 | 27.2222 | 72.7778 | 0.0000 | -0.4394 | -0.3813 | -3.4024 | 1.6848 |

BLOOM-560m:

| model_name | total_items | masculine_preferred_count | feminine_preferred_count | equal_count | masculine_preferred_percent | feminine_preferred_percent | equal_percent | average_score_difference | median_score_difference | min_score_difference | max_score_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bigscience/bloom-560m | 360 | 140 | 217 | 3 | 38.8889 | 60.2778 | 0.8333 | -0.1462 | -0.1621 | -1.9805 | 1.5742 |

## v4 Template Perturbation Benchmark

The v4 benchmark tests template, semantic-frame, and dialect sensitivity using 90 balanced occupations and 8 templates.

### Quality Check

| issue_type | details | count |
| --- | --- | --- |
| no_issues_found | v4 template perturbation benchmark passed quality checks | 0 |

### v4 Overall by Model

| model_name | total_items | masculine_preferred_count | feminine_preferred_count | equal_count | average_score_difference | average_direction |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen/Qwen2.5-0.5B | 720 | 312 | 390 | 18 | -0.0890 | feminine |
| aubmindlab/aragpt2-base | 720 | 220 | 500 | 0 | -0.3484 | feminine |
| aubmindlab/aragpt2-medium | 720 | 290 | 430 | 0 | -0.3031 | feminine |
| bigscience/bloom-1b1 | 720 | 248 | 467 | 5 | -0.1700 | feminine |
| bigscience/bloom-560m | 720 | 256 | 460 | 4 | -0.1703 | feminine |
| facebook/xglm-564M | 720 | 104 | 614 | 2 | -0.4411 | feminine |

### v4 Template Volatility by Model

| model_name | num_templates | masculine_direction_templates | feminine_direction_templates | direction_flip_present | template_volatility_range | most_masculine_template | most_feminine_template |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen/Qwen2.5-0.5B | 8 | 4 | 4 | True | 1.1049 | egy_promotion_frame | msa_leadership_frame |
| aubmindlab/aragpt2-base | 8 | 2 | 6 | True | 1.3195 | egy_experience_statement | egy_workplace_original |
| aubmindlab/aragpt2-medium | 8 | 2 | 6 | True | 1.2230 | msa_workplace_original | egy_workplace_original |
| bigscience/bloom-1b1 | 8 | 1 | 7 | True | 1.3633 | egy_promotion_frame | egy_responsibility_frame |
| bigscience/bloom-560m | 8 | 2 | 6 | True | 1.4123 | egy_promotion_frame | msa_experience_statement |
| facebook/xglm-564M | 8 | 1 | 7 | True | 0.7285 | msa_workplace_original | msa_leadership_frame |

### v4 Dialect Shift

| model_name | msa_average_score_difference | egyptian_average_score_difference | egyptian_minus_msa | msa_direction | egyptian_direction |
| --- | --- | --- | --- | --- | --- |
| Qwen/Qwen2.5-0.5B | -0.3355 | 0.1575 | 0.4930 | feminine | masculine |
| aubmindlab/aragpt2-base | -0.2899 | -0.4069 | -0.1171 | feminine | feminine |
| aubmindlab/aragpt2-medium | -0.1907 | -0.4156 | -0.2249 | feminine | feminine |
| bigscience/bloom-1b1 | -0.2733 | -0.0668 | 0.2065 | feminine | feminine |
| bigscience/bloom-560m | -0.3937 | 0.0531 | 0.4467 | feminine | masculine |
| facebook/xglm-564M | -0.3977 | -0.4845 | -0.0868 | feminine | feminine |

### v4 Chi-Square Tests

| test_label | row_variable | column_variable | chi2 | p_value | degrees_of_freedom | significant_p_lt_0_05 | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| model_name_vs_preferred_gender | model_name | preferred_gender | 174.4099 | 8.36e-36 | 5 | True | ok |
| model_family_vs_preferred_gender | model_family | preferred_gender | 4.1247 | 0.0423 | 1 | True | ok |
| template_id_vs_preferred_gender | template_id | preferred_gender | 673.4476 | 3.65e-141 | 7 | True | ok |
| semantic_frame_vs_preferred_gender | semantic_frame | preferred_gender | 367.4253 | 3.10e-77 | 5 | True | ok |
| dialect_vs_preferred_gender | dialect | preferred_gender | 130.9404 | 2.55e-30 | 1 | True | ok |
| stereotype_label_vs_preferred_gender | stereotype_label | preferred_gender | 1.1783 | 0.5548 | 2 | False | ok |
| field_vs_preferred_gender | field | preferred_gender | 22.4276 | 0.0004 | 5 | True | ok |

### v4 Effect Sizes

| variable | levels | chi2 | p_value | degrees_of_freedom | cramers_v | effect_size_interpretation | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| template_id | 8 | 673.4476 | 3.65e-141 | 7 | 0.3962 | medium | ok |
| semantic_frame | 6 | 367.4253 | 3.10e-77 | 5 | 0.2926 | small | ok |
| model_name | 6 | 174.4099 | 8.36e-36 | 5 | 0.2016 | small | ok |
| dialect | 2 | 130.9404 | 2.55e-30 | 1 | 0.1747 | small | ok |
| field | 6 | 22.4276 | 0.0004 | 5 | 0.0723 | very_small | ok |
| model_family | 2 | 4.1247 | 0.0423 | 1 | 0.0310 | very_small | ok |
| stereotype_label | 3 | 1.1783 | 0.5548 | 2 | 0.0166 | very_small | ok |

## Final Technical Conclusion

The final implementation shows that Arabic occupational gender-bias evaluation is both model-dependent and benchmark-design-dependent.

The v2 benchmark provides the main validated model-family result. The v3 and v3 balanced benchmarks demonstrate sensitivity to occupation coverage and lexical formulation. The v4 benchmark demonstrates that template formulation, semantic frame, and dialect can significantly affect measured gender preference.

The strongest practical factor in v4 was template ID, based on Cramér's V effect-size analysis.

## v5 Job-Title Benchmark

The v5 benchmark isolates occupations as explicit job titles in CV, job advertisement, HR record, and professional profile contexts.

### AraGPT2-base v5 Result

| model_name | total_items | masculine_preferred_count | feminine_preferred_count | equal_count | masculine_preferred_percent | feminine_preferred_percent | equal_percent | average_score_difference | median_score_difference | min_score_difference | max_score_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| aubmindlab/aragpt2-base | 540 | 284 | 256 | 0 | 52.5926 | 47.4074 | 0.0000 | -0.0338 | 0.0278 | -2.1030 | 2.4911 |

### BLOOM-560m v5 Result

| model_name | total_items | masculine_preferred_count | feminine_preferred_count | equal_count | masculine_preferred_percent | feminine_preferred_percent | equal_percent | average_score_difference | median_score_difference | min_score_difference | max_score_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bigscience/bloom-560m | 540 | 278 | 261 | 1 | 51.4815 | 48.3333 | 0.1852 | 0.0709 | 0.0176 | -1.1406 | 1.5000 |

### v4-v5 Context Comparison

| benchmark | benchmark_role | model_name | total_items | masculine_preferred_count | feminine_preferred_count | equal_count | masculine_preferred_percent | feminine_preferred_percent | average_score_difference | median_score_difference | direction_by_average | direction_by_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v4 | template_perturbation_broader_sentence_contexts | aubmindlab/aragpt2-base | 720 | 220 | 500 | 0 | 30.5556 | 69.4444 | -0.3484 | -0.2755 | feminine | feminine |
| v4 | template_perturbation_broader_sentence_contexts | bigscience/bloom-560m | 720 | 256 | 460 | 4 | 35.5556 | 63.8889 | -0.1703 | -0.2617 | feminine | feminine |
| v5 | explicit_job_title_context | aubmindlab/aragpt2-base | 540 | 284 | 256 | 0 | 52.5926 | 47.4074 | -0.0338 | 0.0278 | feminine | masculine |
| v5 | explicit_job_title_context | bigscience/bloom-560m | 540 | 278 | 261 | 1 | 51.4815 | 48.3333 | 0.0709 | 0.0176 | masculine | masculine |

The v5 results show that explicit job-title contexts can behave differently from broader occupational sentence templates. This further supports the claim that Arabic occupational gender-bias measurement is benchmark-design-dependent.
