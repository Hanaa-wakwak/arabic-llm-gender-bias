# Run the Arabic Bias Measurement Software

This repository contains two Streamlit software tools:

1. Arabic Bias Measurement App
2. Arabic Bias Dashboard App

## 1. Bias Measurement App

The bias measurement app measures Arabic occupational gender bias using masculine-feminine counterfactual sentence pairs.

### Run with PowerShell

cd H:\arabic-llm-gender-bias
.\software_bias_measurement\run_bias_measurement_app.ps1

### Run with BAT File

Double-click:

software_bias_measurement\run_bias_measurement_app.bat

### Manual Command

cd H:\arabic-llm-gender-bias
python -m pip install -r software_bias_measurement\requirements.txt
python -m streamlit run software_bias_measurement\app.py

The app opens at:

http://localhost:8501

## 2. Dashboard App

The dashboard app allows users to inspect datasets, model results, validation outputs, robustness analyses, and cross-benchmark comparisons.

### Run with PowerShell

cd H:\arabic-llm-gender-bias
.\software_dashboard\run_dashboard_app.ps1

### Run with BAT File

Double-click:

software_dashboard\run_dashboard_app.bat

### Manual Command

cd H:\arabic-llm-gender-bias
python -m pip install -r software_dashboard\requirements.txt
python -m streamlit run software_dashboard\app.py

## Main Bias Equation

score_difference = masculine_score - feminine_score

## Interpretation

score_difference > 0 means masculine preference.
score_difference < 0 means feminine preference.
score_difference = 0 means equal preference.

## Required CSV Columns

masculine_sentence
feminine_sentence

Optional metadata columns are preserved in the output.

## Recommended First Test

Masculine sentence:

هذا الطبيب يعمل في المستشفى.

Feminine sentence:

هذه الطبيبة تعمل في المستشفى.

Recommended model:

aubmindlab/aragpt2-base

## Notes

- Large models may be slow on CPU.
- For full benchmark scoring, use the command-line scoring scripts.
- The software is a research prototype for measuring and inspecting Arabic occupational gender bias.
