# Final Thesis Results Summary

## Thesis Direction

The thesis investigates occupational gender bias in Arabic causal language models using a controlled counterfactual benchmark.

The final thesis title direction is:

**Measuring Occupational Gender Bias in Arabic Causal Language Models using a Counterfactual Dialect-Aware Benchmark**

## Final Benchmark

The final benchmark used in the thesis is:

`data/occupational_benchmark/occupational_bias_v2.csv`

The earlier benchmark version, `occupational_bias_v1.csv`, is treated as a pilot / sanity-check benchmark.

## Benchmark Design

The benchmark is designed to compare masculine and feminine versions of the same occupational sentence.

Each item contains:

* a masculine occupation sentence,
* a feminine occupation sentence,
* the same semantic meaning,
* the same professional field,
* the same template structure.

The benchmark includes both Modern Standard Arabic and Egyptian Arabic.

## Benchmark Size

| Component                     | Count |
| ----------------------------- | ----: |
| Occupational fields           |     6 |
| Occupations                   |    60 |
| Templates per occupation      |     4 |
| Counterfactual sentence pairs |   240 |

## Occupational Fields

The benchmark covers six professional fields:

1. STEM
2. Healthcare
3. Education
4. Business
5. Legal/Government
6. Media/Creative

Each field contains 10 occupations.

## Dialects

The benchmark includes two Arabic varieties:

1. Modern Standard Arabic
2. Egyptian Arabic

This allows the thesis to study whether gender preference patterns appear across different Arabic varieties.

## Sentence Templates

Each occupation is tested using four templates:

1. MSA demonstrative workplace template
2. MSA reported professional template
3. Egyptian direct workplace template
4. Egyptian reported role template

This improves robustness because the result is not based on one sentence structure only.

## Bias Measurement

For each masculine/feminine sentence pair, the model assigns a score to both sentences.

The score difference is calculated as:

```text
score_difference = masculine_score - feminine_score
```

Interpretation:

| Score Difference | Meaning                        |
| ---------------: | ------------------------------ |
|         Positive | Masculine sentence preferred   |
|         Negative | Feminine sentence preferred    |
|        Near zero | Balanced / no clear preference |

The preferred gender is assigned based on the sign of the score difference.

## Evaluated Models

The thesis evaluates four causal language models.

| Model                     | Family          |
| ------------------------- | --------------- |
| aubmindlab/aragpt2-base   | Arabic-specific |
| aubmindlab/aragpt2-medium | Arabic-specific |
| bigscience/bloom-560m     | Multilingual    |
| bigscience/bloom-1b1      | Multilingual    |

## Why These Models?

The models were selected to compare two model families:

1. Arabic-specific causal language models
2. Multilingual causal language models

This directly supports the research question of whether occupational gender bias differs between Arabic-focused models and multilingual models.

## Overall v2 Results

| Model          | Family          | Masculine Preferred | Feminine Preferred | Equal | Direction |
| -------------- | --------------- | ------------------: | -----------------: | ----: | --------- |
| AraGPT2-base   | Arabic-specific |                 152 |                 88 |     0 | Masculine |
| AraGPT2-medium | Arabic-specific |                 168 |                 72 |     0 | Masculine |
| BLOOM-1b1      | Multilingual    |                  91 |                147 |     2 | Feminine  |
| BLOOM-560m     | Multilingual    |                  83 |                157 |     0 | Feminine  |

## Overall Percentages

| Model          | Masculine % | Feminine % | Direction |
| -------------- | ----------: | ---------: | --------- |
| AraGPT2-base   |      63.33% |     36.67% | Masculine |
| AraGPT2-medium |      70.00% |     30.00% | Masculine |
| BLOOM-1b1      |      37.92% |     61.25% | Feminine  |
| BLOOM-560m     |      34.58% |     65.42% | Feminine  |

## Average Score Differences

| Model          | Average Score Difference | Median Score Difference | Direction |
| -------------- | -----------------------: | ----------------------: | --------- |
| AraGPT2-base   |                  +0.1257 |                 +0.2537 | Masculine |
| AraGPT2-medium |                  +0.2230 |                 +0.3249 | Masculine |
| BLOOM-1b1      |                  -0.1656 |                 -0.1934 | Feminine  |
| BLOOM-560m     |                  -0.2174 |                 -0.2168 | Feminine  |

Positive values indicate masculine preference. Negative values indicate feminine preference.

## Statistical Significance

### Binomial Preference Test

| Model          | Direction | Binomial p-value | Significant |
| -------------- | --------- | ---------------: | ----------- |
| AraGPT2-base   | Masculine |         4.33e-05 | Yes         |
| AraGPT2-medium | Masculine |         5.13e-10 | Yes         |
| BLOOM-1b1      | Feminine  |         3.44e-04 | Yes         |
| BLOOM-560m     | Feminine  |         2.05e-06 | Yes         |

### Wilcoxon Signed-Rank Test

| Model          | Wilcoxon p-value | Significant |
| -------------- | ---------------: | ----------- |
| AraGPT2-base   |         2.79e-04 | Yes         |
| AraGPT2-medium |         3.29e-08 | Yes         |
| BLOOM-1b1      |         8.51e-05 | Yes         |
| BLOOM-560m     |         5.76e-07 | Yes         |

Both tests show that the overall gender preference is statistically significant for all four models.

## Model-Family Result

The model-family association is highly significant:

```text
Chi-square p-value = 1.31e-20
```

This means that gender preference direction is strongly associated with model family.

The Arabic-specific models lean masculine, while the multilingual models lean feminine.

## Field-Level Findings

### Arabic-Specific Models

AraGPT2 models show stronger masculine preference in:

* Business,
* Legal/Government,
* STEM,
* Media/Creative.

Healthcare is weaker and less stable, showing that occupational gender bias is field-dependent.

### Multilingual Models

BLOOM models show stronger feminine preference in:

* Education,
* Healthcare,
* Media/Creative.

Business and Legal/Government are closer to balanced or weaker.

## Pairwise Model Comparison

Pairwise Wilcoxon comparisons show:

1. AraGPT2-base and AraGPT2-medium differ significantly in v2.
2. Each AraGPT2 model differs significantly from each BLOOM model.
3. BLOOM-1b1 and BLOOM-560m do not significantly differ from each other.

This supports the idea that the biggest difference is between model families, not merely between individual models.

## Main Finding

The main thesis finding is:

> Arabic-specific AraGPT2 causal language models show statistically significant masculine occupational preference, while multilingual BLOOM causal language models show statistically significant feminine occupational preference.

## Why v2 Is the Final Benchmark

v2 is used as the final benchmark because it:

1. expands the benchmark from 36 to 60 occupations,
2. increases the number of sentence pairs from 144 to 240,
3. preserves the same controlled counterfactual design,
4. preserves the same six professional fields,
5. passes basic quality checks,
6. produces statistically significant results,
7. preserves the same model-family pattern observed in v1.

## How to Present This Result

A simple explanation for discussion:

> I first built a smaller controlled occupational benchmark, v1, to test the scoring pipeline and sentence templates. After validating the pipeline, I expanded the benchmark to v2 with 60 occupations and 240 counterfactual sentence pairs. The main result remained stable: Arabic-specific AraGPT2 models preferred masculine occupational sentences, while multilingual BLOOM models preferred feminine occupational sentences. This suggests that occupational gender bias in Arabic language models depends not only on the occupation itself, but also on the model family and training background.

## Final Conclusion

The thesis demonstrates that occupational gender bias can be measured in Arabic causal language models using controlled counterfactual sentence pairs.

The results show that bias direction is not uniform across models. Instead, Arabic-specific and multilingual models exhibit different gender-preference patterns.

This makes the work useful for Arabic NLP fairness evaluation, especially because it combines:

* Arabic gender morphology,
* occupational stereotypes,
* dialect-aware templates,
* causal language model scoring,
* statistical significance testing.
## Enriched Six-Model Robustness Experiment

In addition to the original four-model experiment, two extra non-Arabic-specific causal language models were evaluated:

- `facebook/xglm-564M`
- `Qwen/Qwen2.5-0.5B`

Both models were evaluated on the same final benchmark, `occupational_bias_v2.csv`.

The enriched six-model analysis shows:

| Model Family | Masculine Preferred | Feminine Preferred | Equal | Direction |
|---|---:|---:|---:|---|
| Arabic-specific | 320 | 160 | 0 | Masculine |
| Non-Arabic-specific | 346 | 610 | 4 | Feminine |

The model-family association remains highly significant:

```text
chi-square p-value = 1.64e-27