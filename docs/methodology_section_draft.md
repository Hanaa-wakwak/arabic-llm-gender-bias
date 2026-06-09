# Methodology Draft

## 1. Research Objective

The objective of this work is to detect gender preference patterns in Arabic causal language models using a counterfactual benchmark.

The benchmark is designed to compare masculine and feminine variants of the same sentence while keeping the semantic meaning as similar as possible.

The study focuses on Arabic because grammatical gender is strongly expressed in nouns, adjectives, verbs, and pronouns. It also includes both Modern Standard Arabic (MSA) and Egyptian Arabic to examine whether measured gender preference changes across dialects.

## 2. Benchmark Design

The benchmark uses minimal counterfactual sentence pairs. Each pair contains:

* one masculine sentence
* one feminine sentence

The two sentences are designed to differ only in gender-marked forms. This allows the evaluation to focus on whether a language model assigns higher probability to the masculine or feminine variant of the same underlying meaning.

Each benchmark item contains the following metadata:

* `id`
* `concept_id`
* `dimension`
* `dialect`
* `template_id`
* `masculine_sentence`
* `feminine_sentence`
* `stereotype_direction`
* `notes`

The `concept_id` identifies the occupation or trait being tested. The `dimension` field indicates whether the item belongs to the occupation dimension or the trait dimension. The `dialect` field indicates whether the item is written in MSA or Egyptian Arabic. The `template_id` field identifies the sentence template used to generate the item.

## 3. Benchmark Dimensions

The benchmark includes two main dimensions:

### 3.1 Occupation Dimension

The occupation dimension tests professional and social role concepts such as doctor, engineer, programmer, manager, nurse, teacher, secretary, researcher, and others.

Each occupation concept includes masculine and feminine forms in both MSA and Egyptian Arabic.

### 3.2 Trait Dimension

The trait dimension tests descriptive attributes such as intelligent, strong, decisive, emotional, tender, patient, organized, creative, calm, and hardworking.

Each trait concept includes masculine and feminine adjective forms in both MSA and Egyptian Arabic.

## 4. Dialect Coverage

The benchmark includes two dialectal varieties:

1. Modern Standard Arabic (MSA)
2. Egyptian Arabic

MSA items use formal Arabic structures, while Egyptian items use Egyptian lexical and syntactic patterns.

The inclusion of Egyptian Arabic is important because many Arabic bias benchmarks focus only on MSA, while real-world Arabic usage often includes dialectal forms.

## 5. Template-Controlled Construction

The benchmark was created through several iterative versions.

Early versions showed that measured gender preference can be strongly affected by sentence templates. For example, some Egyptian templates created strong masculine or feminine preference independent of the tested concept.

To control this issue, later versions included explicit `template_id` metadata and quality-control analysis by template.

The selected expanded benchmark version is:

`minimal_pairs_v07.csv`

This version contains 144 items generated from controlled lexicon files and template structures.

## 6. Benchmark Versioning and Selection

Several benchmark versions were created and evaluated:

* v0.3 introduced concept and template metadata.
* v0.4 was selected as the stable 48-item pilot benchmark.
* v0.6 expanded the benchmark to 144 items.
* v0.7 improved the expanded benchmark and was selected as the expanded pilot benchmark.
* v0.8 was treated as a template ablation experiment.

The final selected expanded benchmark is v0.7 because it provides the best balance between dataset size, dialect-level stability, overall score stability, and acceptable outlier rate.

## 7. Scoring Method

Each model was evaluated using average sentence log-probability.

For each counterfactual pair, the model assigns a score to the masculine sentence and a score to the feminine sentence.

The score difference is computed as:

`score_difference = masculine_score - feminine_score`

The interpretation is:

* positive score difference: the model prefers the masculine variant
* negative score difference: the model prefers the feminine variant
* zero score difference: no preference

The preferred gender is assigned based on the sign of the score difference.

## 8. Evaluated Models

The selected benchmark was used to evaluate four causal language models:

1. `aubmindlab/aragpt2-base`
2. `aubmindlab/aragpt2-medium`
3. `bigscience/bloom-560m`
4. `bigscience/bloom-1b1`

The first two models are Arabic-specific models, while the BLOOM models are multilingual models.

This model selection allows comparison between Arabic-specific and multilingual language models under the same evaluation setting.

## 9. Analysis Levels

The results were analyzed at multiple levels:

### 9.1 Overall Model Level

This level compares the total number of masculine-preferred and feminine-preferred items for each model.

### 9.2 Dialect Level

This level compares model behavior on MSA items versus Egyptian Arabic items.

### 9.3 Dimension Level

This level compares occupation items versus trait items.

### 9.4 Stereotype-Direction Level

This level compares model behavior across male-stereotype, female-stereotype, and neutral concepts.

### 9.5 Template Level

This level identifies whether specific sentence templates introduce unintended masculine or feminine preference.

## 10. Quality Control

Quality control was performed throughout benchmark construction.

The following indicators were used:

* average score difference
* median score difference
* masculine/feminine preference counts
* dialect-level balance
* template-level warnings
* concept-level warnings
* outlier rate

Items and templates with high score differences or strong dominance patterns were flagged for review.

This quality-control process showed that Arabic gender-bias evaluation is highly sensitive to template design, especially in dialectal Arabic.

## 11. Reproducibility

The project was implemented using Python scripts and structured CSV files.

The pipeline includes scripts for:

* benchmark generation
* model scoring
* score analysis
* quality reporting
* multi-model comparison
* figure generation
* thesis-ready table generation

The project was version-controlled using Git and pushed to GitHub. The pipeline was also tested across local and Colab environments to confirm reproducibility.
