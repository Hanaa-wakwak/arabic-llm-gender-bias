# Q1 Bias Mitigation Training Data Summary

## Purpose

This file documents the construction of balanced Arabic masculine-feminine counterfactual training data for the Q1 bias mitigation experiment.

## Method

- Load controlled Arabic occupational counterfactual pairs.
- Extract both masculine and feminine sentence variants.
- Balance masculine and feminine variants exactly.
- Export a text corpus for causal language model fine-tuning.

## Output Files

- Training CSV: `data\q1_bias_mitigation\arabic_counterfactual_mitigation_train.csv`
- Training TXT: `data\q1_bias_mitigation\arabic_counterfactual_mitigation_train.txt`
- Summary CSV: `data\q1_bias_mitigation\arabic_counterfactual_mitigation_training_summary.csv`

## Training Sentences

- Total balanced training sentences: 6840
- Masculine sentences: 3420
- Feminine sentences: 3420

## Publication Value

This dataset supports a counterfactual data augmentation mitigation experiment, testing whether exposure to balanced Arabic masculine-feminine occupational contexts reduces measured gender preference.