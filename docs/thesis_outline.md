# Thesis Outline

## Proposed Thesis Title

Counterfactual and Dialect-Aware Gender Bias Evaluation in Arabic Causal Language Models

---

## Chapter 1 — Introduction

### 1.1 Background

* Large Language Models and their use in Arabic NLP
* Gender bias as a fairness problem in NLP
* Why Arabic gender bias is different from English gender bias
* Grammatical gender in Arabic nouns, adjectives, verbs, and pronouns
* Importance of dialectal Arabic, especially Egyptian Arabic

### 1.2 Problem Statement

Most gender-bias benchmarks focus on English or general multilingual settings. Arabic remains underrepresented, especially dialectal Arabic. Existing Arabic bias resources often do not deeply control for grammatical gender agreement, dialect variation, or template-driven effects.

### 1.3 Research Aim

This thesis aims to build and evaluate a counterfactual Arabic gender-bias benchmark for causal language models, focusing on MSA and Egyptian Arabic.

### 1.4 Research Questions

RQ1. How do Arabic-specific and multilingual causal language models differ in masculine/feminine sentence preference?

RQ2. Does measured gender preference differ between MSA and Egyptian Arabic?

RQ3. Do occupation and trait items produce different gender-preference patterns?

RQ4. How does stereotype direction affect model preference patterns?

RQ5. How sensitive are Arabic gender-bias measurements to template construction?

### 1.5 Contributions

* A counterfactual Arabic gender-bias benchmark with masculine/feminine minimal pairs
* MSA and Egyptian Arabic coverage
* Occupation and trait dimensions
* concept_id, template_id, and stereotype_direction metadata
* Quality-control pipeline for template and concept effects
* Multi-model evaluation across Arabic-specific and multilingual causal language models

### 1.6 Thesis Structure

Brief description of each chapter.

---

## Chapter 2 — Literature Review

### 2.1 Gender Bias in NLP

* Bias in language models
* Counterfactual evaluation
* Gender bias in high-resource languages

### 2.2 Gender Bias in Arabic NLP

* Arabic word embedding bias
* Arabic LLM bias evaluation
* Arabic gender agreement challenges

### 2.3 Dialectal Arabic Evaluation

* MSA vs dialectal Arabic
* Egyptian Arabic
* Dialectal benchmarks such as AraDiCE and DialectalArabicMMLU

### 2.4 Grammatical Gender and Morphology

* Arabic grammatical gender
* Morphological agreement
* Relation to benchmarks such as MORPHOGEN

### 2.5 Template-Based Bias Benchmarks

* Strengths of template-based evaluation
* Template artifacts
* Need for template-level quality control

### 2.6 Research Gap

* Lack of dialect-aware Arabic gender-bias benchmarks
* Limited focus on causal LM sentence scoring
* Limited template-effect analysis in Arabic bias evaluation

---

## Chapter 3 — Methodology

### 3.1 Research Design

* Counterfactual benchmark design
* Masculine/feminine sentence-pair comparison

### 3.2 Benchmark Construction

* Concept selection
* Occupation concepts
* Trait concepts
* MSA forms
* Egyptian forms

### 3.3 Metadata Design

* id
* concept_id
* dimension
* dialect
* template_id
* stereotype_direction
* notes

### 3.4 Versioning Process

* v0.3 concept/template metadata
* v0.4 stable 48-item pilot
* v0.6 expanded 144-item attempt
* v0.7 selected expanded benchmark
* v0.8 template ablation

### 3.5 Scoring Method

* Average sentence log-probability
* Score difference formula
* Masculine/feminine preference decision

### 3.6 Evaluated Models

* AraGPT2-base
* AraGPT2-medium
* BLOOM-560m
* BLOOM-1b1

### 3.7 Analysis Levels

* Overall
* Dialect
* Dimension
* Stereotype direction
* Template
* Concept

### 3.8 Quality Control

* Template warnings
* Concept warnings
* Outlier rate
* Dialect balance
* Manual review and ablation

### 3.9 Reproducibility

* Python scripts
* GitHub
* CSV files
* Local and Colab testing

---

## Chapter 4 — Results and Analysis

### 4.1 Benchmark Version Selection

* Pilot versions
* Selection of v0.4 as stable pilot
* Selection of v0.7 as expanded pilot benchmark

### 4.2 Overall Multi-Model Results

* AraGPT2-base
* AraGPT2-medium
* BLOOM-560m
* BLOOM-1b1
* Overall masculine/feminine preference

### 4.3 Dialect-Level Results

* MSA vs Egyptian
* Dialect-sensitive behavior
* AraGPT2 vs BLOOM differences

### 4.4 Dimension-Level Results

* Occupation items
* Trait items
* Differences by model family

### 4.5 Stereotype-Direction Results

* male_stereotype
* female_stereotype
* neutral
* Whether model preference follows stereotype direction

### 4.6 Template-Level Effects

* v0.6, v0.7, v0.8 comparison
* Template sensitivity
* Importance of template metadata

### 4.7 Key Findings

* AraGPT2-medium most balanced overall
* BLOOM models show feminine-form preference
* Occupation dimension reveals stronger divergence
* Template construction affects measured bias
* Dialect-aware analysis is necessary

---

## Chapter 5 — Discussion

### 5.1 Interpretation of Findings

* What the results mean
* Differences between Arabic-specific and multilingual models

### 5.2 Arabic-Specific Challenges

* Grammatical gender
* Dialect variation
* Template effects

### 5.3 Implications for Arabic Bias Evaluation

* Why MSA-only evaluation is insufficient
* Why template-level metadata is necessary
* Why multiple model families should be compared

### 5.4 Limitations

* Dataset still small compared with large benchmarks
* Only MSA and Egyptian Arabic
* Only causal language models
* Sentence templates may still introduce artifacts
* Manual validation is still needed
* No mitigation/fine-tuning yet

### 5.5 Threats to Validity

* Lexical frequency effects
* Template artifacts
* Tokenization effects
* Model size differences
* Dialect authenticity
* Limited human annotation

---

## Chapter 6 — Conclusion and Future Work

### 6.1 Conclusion

* Summary of thesis contribution
* Summary of main findings

### 6.2 Future Work

* Expand benchmark size
* Add more Arabic dialects
* Add human validation
* Evaluate more Arabic and multilingual models
* Add masked-language models and instruction-tuned models
* Add mitigation experiments
* Add explainability/token-level analysis

---

## Appendices

### Appendix A — Benchmark Samples

* Sample MSA occupation items
* Sample Egyptian occupation items
* Sample trait items

### Appendix B — Scripts

* Benchmark generation scripts
* Scoring scripts
* Analysis scripts
* Quality-control scripts

### Appendix C — Full Tables

* Overall model comparison
* Dialect-level tables
* Dimension-level tables
* Stereotype-level tables

### Appendix D — Figures

* Overall preference count plot
* Average score difference plot
* Dialect-level plot
* Dimension-level plots
* Stereotype-level plot
