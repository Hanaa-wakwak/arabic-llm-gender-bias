# Research Log

## 8 June 2026

### What I did today
I created the initial project folder structure for my Arabic LLM gender bias thesis.

### Thesis direction
The thesis focuses on detecting and mitigating gender bias in Arabic Large Language Models using a counterfactual and dialect-aware approach.

### Initial scope
- MSA and Egyptian Arabic
- Occupational gender stereotypes
- Trait/adjective gender stereotypes
- Minimal gender pairs as the first benchmark format

### Why this scope
Arabic marks gender through grammatical agreement, so masculine and feminine sentence pairs can be used to measure whether a model shows preference toward one gendered form over another.

### Next step
Create the first pilot CSV file containing Arabic masculine/feminine minimal pairs.
## Step 4 Completed

I wrote the first benchmark specification document.

The benchmark v0 contains:
- 50 Arabic gender minimal pairs
- MSA and Egyptian Arabic
- Occupation and trait/adjective stereotypes
- Masculine and feminine sentence versions
- A first scoring idea based on masculine/feminine score difference

Next step:
Create a notebook to load and inspect the CSV dataset.
## Step 6 Completed

I prepared the project requirements file and created a dataset summary script.

The script reads the pilot benchmark CSV and saves a summary file inside the results folder.

Current output:
- Dataset summary saved in results/dataset_summary_v0.csv

Next step:
Create the first model scoring script to compare masculine and feminine sentence scores.
## Step 8 Completed

I created the first analysis script for the pilot scoring results.

The script generates:
- Overall preference summary
- Analysis by dialect
- Analysis by dimension
- Analysis by stereotype direction
- Detailed grouped analysis

Generated output files:
- results/analysis_summary_v0.csv
- results/analysis_by_dialect_v0.csv
- results/analysis_by_dimension_v0.csv
- results/analysis_by_stereotype_v0.csv
- results/analysis_detailed_groups_v0.csv

Next step:
Interpret the first pilot results and write an experiment note.
## Step 9 Completed

I wrote the first experiment note for the pilot scoring experiment.

Main result:
- Masculine preferred: 25 items
- Feminine preferred: 25 items
- Average score difference: -0.4021
- Median score difference: 0.1239

Initial interpretation:
The scoring pipeline works, but the pilot dataset is too small to make a strong bias claim.

Next step:
Analyze dialect, dimension, stereotype direction, and outlier items.
## Step 14 Completed

I created a generic scoring script called src/score_pairs.py.

The script can score any CSV file that contains:
- masculine_sentence
- feminine_sentence

It preserves all existing metadata columns and adds:
- masculine_score
- feminine_score
- score_difference
- preferred_gender

This makes the scoring pipeline reusable for future benchmark versions and template tests.

## Step 15 Completed

I created a generic analysis script called src/analyze_pairs.py.

The script analyzes any scoring results file that contains:
- score_difference
- preferred_gender

It generates:
- overall summary
- grouped analysis by available metadata columns
- detailed grouped analysis when multiple metadata columns exist

This makes the analysis pipeline reusable for benchmark versions and template tests.
## Step 16 Completed

I initialized a Git repository for the project and committed the first working version.

The first commit includes:
- pilot benchmark files
- scoring scripts
- analysis scripts
- result files
- experiment documentation

This creates a reproducible checkpoint for the initial pilot pipeline.
## Step 17 Completed

I created benchmark v0.2 with balanced template types.

Main improvement:
- Added template_type column
- Reduced uncontrolled repetition
- Separated Egyptian templates using "بيشتغل/بتشتغل" and "شغال/شغالة"
- Balanced MSA and Egyptian items more clearly
- Prepared the dataset for template-level analysis

Next step:
Compare v0.1 and v0.2 results and decide which templates should remain in the next benchmark version.

## Step 18 Completed

I wrote the second experiment note about template effects in benchmark v0.2.

Main finding:
The Egyptian feminine preference is strongly affected by occupation templates, especially "هو شغال / هي شغالة".

Important conclusion:
Dialect-level bias analysis must control for template effects before making strong claims.

Next step:
Design benchmark v0.3 with concept IDs and template IDs.

## Step 20 Completed

I updated the generic analysis script to support concept-level and template-level analysis.

New supported grouping columns:
- dialect
- dimension
- stereotype_direction
- template_type
- template_id
- concept_id

This allows the v0.3 benchmark to separate concept effects from template effects.

