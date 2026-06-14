# Extra Models Results Summary

## Purpose

The main thesis experiment evaluated four causal language models:

* AraGPT2-base,
* AraGPT2-medium,
* BLOOM-560m,
* BLOOM-1b1.

To enrich the thesis and test robustness, additional multilingual/general causal language models were evaluated on the same final benchmark:

`occupational_bias_v2.csv`

The purpose is to check whether the main model-family pattern remains stable when more models are added.

## Final Benchmark Used

All extra models were evaluated on:

`data/occupational_benchmark/occupational_bias_v2.csv`

Benchmark size:

| Component                | Count |
| ------------------------ | ----: |
| Occupations              |    60 |
| Fields                   |     6 |
| Templates per occupation |     4 |
| Sentence pairs           |   240 |

## Extra Models Evaluated

| Model              | Category                       |
| ------------------ | ------------------------------ |
| facebook/xglm-564M | Multilingual causal LM         |
| Qwen/Qwen2.5-0.5B  | Multilingual/general causal LM |

## XGLM-564M Overall Result

| Metric                   |   Value |
| ------------------------ | ------: |
| Masculine preferred      |      92 |
| Feminine preferred       |     148 |
| Equal                    |       0 |
| Masculine %              |  38.33% |
| Feminine %               |  61.67% |
| Average score difference | -0.2138 |

Interpretation:

`facebook/xglm-564M` shows overall feminine occupational preference.

## Qwen2.5-0.5B Overall Result

| Metric                   |   Value |
| ------------------------ | ------: |
| Masculine preferred      |      80 |
| Feminine preferred       |     158 |
| Equal                    |       2 |
| Masculine %              |  33.33% |
| Feminine %               |  65.83% |
| Equal %                  |   0.83% |
| Average score difference | -0.3425 |

Interpretation:

`Qwen/Qwen2.5-0.5B` also shows overall feminine occupational preference.

## Extra Models Field-Level Pattern

### XGLM-564M

XGLM shows feminine preference in:

* Business,
* Education,
* Healthcare,
* Legal/Government.

It is close to balanced in Media/Creative and slightly masculine in STEM.

### Qwen2.5-0.5B

Qwen shows feminine preference in all six fields:

* Business,
* Education,
* Healthcare,
* Legal/Government,
* Media/Creative,
* STEM.

The strongest feminine preference appears in Business, Education, and Media/Creative.

## Relation to Main Thesis Result

The main thesis result was:

> Arabic-specific AraGPT2 models show masculine occupational preference, while multilingual BLOOM models show feminine occupational preference.

The extra model results support this pattern because both additional non-Arabic-specific models also show overall feminine occupational preference.

## Robustness Interpretation

The extra model experiment strengthens the thesis by showing that the feminine preference pattern is not limited to BLOOM models only.

Instead, the same overall direction appears in additional multilingual/general causal language models.

## Important Note

These extra models are used as robustness experiments.

The main thesis benchmark and primary result remain based on the final v2 benchmark and the original four-model comparison.
