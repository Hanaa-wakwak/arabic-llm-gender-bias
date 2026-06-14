# ArGAN Integration Plan

## Purpose

This document explains how ArGAN can be integrated into the thesis as an external Arabic LLM bias dataset.

The main thesis benchmark remains:

`data/occupational_benchmark/occupational_bias_v2.csv`

ArGAN is added as an external validation dataset, not as a replacement for the occupational benchmark.

---

## Why ArGAN Is Useful

ArGAN is relevant because it focuses on evaluating bias in Arabic large language models.

It covers multiple bias axes, including:

* gender,
* ability,
* nationality.

For this thesis, the first priority is the gender subset because the thesis focuses on gender bias.

---

## Difference Between ArGAN and the Occupational Benchmark

The occupational benchmark is a controlled sentence-pair likelihood benchmark.

Each item has:

* masculine sentence,
* feminine sentence,
* same meaning,
* same template,
* same occupation context.

ArGAN is more suitable for prompt-based evaluation.

This means that instead of comparing sentence probabilities directly, the model may be asked to complete or respond to prompts, then the output is analyzed for biased, stereotypical, or neutral behavior.

---

## Recommended Role in the Thesis

ArGAN should be used as:

1. external validation,
2. prompt-based robustness experiment,
3. broader Arabic bias comparison.

It should not replace the main occupational benchmark.

---

## Integration Strategy

The integration should happen in stages.

### Stage 1 — Dataset Inspection

After obtaining the real ArGAN files, inspect:

* file format,
* columns,
* prompt text,
* bias axis labels,
* target group labels,
* expected output type,
* annotation labels if available.

### Stage 2 — Gender Subset Extraction

Extract only gender-related items first.

The gender subset should be saved as:

`data/external_datasets/argan/argan_gender_subset.csv`

### Stage 3 — Standardize Format

Convert ArGAN gender prompts into a standard thesis format:

| Column               | Description                              |
| -------------------- | ---------------------------------------- |
| id                   | unique prompt ID                         |
| source_dataset       | ArGAN                                    |
| bias_axis            | gender                                   |
| target_group         | gender group or gender marker            |
| prompt_ar            | Arabic prompt                            |
| prompt_type          | completion / generation / classification |
| expected_output_type | text response                            |
| notes                | processing notes                         |

### Stage 4 — Model Generation

Run selected models on the ArGAN gender prompts.

The model output should be saved with:

| Column           | Description        |
| ---------------- | ------------------ |
| id               | prompt ID          |
| model_name       | evaluated model    |
| prompt_ar        | input prompt       |
| generated_output | model response     |
| bias_axis        | gender             |
| target_group     | group label        |
| decoding_config  | generation setting |

### Stage 5 — Output Evaluation

Evaluate outputs using one or more methods:

1. keyword-based stereotype detection,
2. sentiment analysis,
3. manual annotation,
4. LLM-assisted annotation,
5. comparison with ArGAN labels if labels exist.

### Stage 6 — Compare With Main Benchmark

Compare ArGAN results with the occupational benchmark results.

Main question:

> Do models that show occupational gender bias also show gender bias on external Arabic prompts?

---

## Recommended First Pilot

Before using the full ArGAN dataset, create a small ArGAN-format pilot sample.

This pilot should include 10–20 Arabic gender-bias prompts.

The purpose is only to test the generation and analysis pipeline.

---

## Thesis Framing

Recommended wording:

> ArGAN is used as an external Arabic bias-evaluation resource to test whether the model-family patterns observed in the occupational benchmark also appear in prompt-based Arabic gender-bias evaluation.

---

## Expected Contribution

Adding ArGAN strengthens the thesis by providing:

1. external dataset validation,
2. prompt-based bias analysis,
3. broader Arabic fairness comparison,
4. evidence beyond the internally constructed occupational benchmark.

---

## Important Limitation

ArGAN-style prompt evaluation is not directly identical to sentence-pair likelihood scoring.

Therefore, ArGAN results should be discussed as complementary evidence, not as a direct replacement for the occupational benchmark.
