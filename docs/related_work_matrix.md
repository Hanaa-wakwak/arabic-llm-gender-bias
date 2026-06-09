# Related Work Matrix

## Purpose

This matrix summarizes the most relevant prior work for the thesis topic:

Detecting and mitigating gender bias in Arabic large language models using counterfactual, dialect-aware, and template-controlled evaluation.

The goal is to identify what each prior work contributes, what limitations remain, and how the current thesis extends the literature.

---

## Related Work Matrix

| ID  | Work                                                                                                  | Main Focus                                                  | Language / Dialect Coverage                     | Method / Benchmark Type                                          | Key Contribution                                                                   | Limitation / Gap                                                                                                                       | How This Thesis Extends It                                                                                                     |
| --- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | ----------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| R1  | Detecting gender bias in Arabic text through word embeddings                                          | Gender bias in Arabic word embeddings                       | Arabic                                          | WEAT and Direct Bias adapted to Arabic                           | Measures gender bias in Arabic embeddings, especially around occupations           | Focuses on word embeddings rather than causal LLMs; limited dialectal analysis; not based on sentence-level counterfactual LLM scoring | Extends Arabic gender-bias analysis from embeddings to causal LMs using sentence-level masculine/feminine counterfactual pairs |
| R2  | ArGAN: Arabic Gender, Ability, and Nationality Dataset for Evaluating Biases in Large Language Models | Demographic bias evaluation in Arabic LLMs                  | Arabic                                          | Template-based dataset covering gender, ability, and nationality | Provides an Arabic bias dataset for evaluating multiple demographic axes in LLMs   | Broader demographic focus; does not deeply isolate grammatical gender agreement across MSA and Egyptian templates                      | Focuses specifically on Arabic grammatical gender and adds dialect-aware template-level quality control                        |
| R3  | A Benchmark to Evaluate Gender Bias in Arabic Language Models                                         | Gender bias in Arabic language models                       | Arabic                                          | Benchmark-based bias evaluation                                  | Early Arabic benchmark for measuring gender bias in language models                | Limited dialectal coverage; may not focus on Egyptian Arabic or template-level instability                                             | Adds explicit MSA vs Egyptian comparison and analyzes template effects during benchmark construction                           |
| R4  | Quantifying Gender Bias in Arabic Pre-trained Language Models                                         | Gender bias in Arabic pre-trained models                    | Arabic                                          | Template-based masked-token evaluation                           | Evaluates Arabic pre-trained language models using template-based bias measurement | More focused on masked language models and token prediction; less focused on causal LM sentence scoring                                | Uses causal language model scoring based on average sentence log-probability                                                   |
| R5  | AraDiCE: Benchmarks for Dialectal and Cultural Capabilities in LLMs                                   | Dialectal and cultural evaluation of Arabic LLMs            | MSA and Arabic dialects                         | Dialectal and cultural benchmark                                 | Shows that dialectal Arabic remains underrepresented and difficult for LLMs        | Focuses on dialectal/cultural capability, not specifically gender-bias counterfactual evaluation                                       | Combines dialect-aware evaluation with gender-bias detection                                                                   |
| R6  | DialectalArabicMMLU                                                                                   | Dialectal Arabic reasoning benchmark                        | MSA, Egyptian, Syrian, Emirati, Saudi, Moroccan | Multiple-choice QA benchmark                                     | Extends MMLU-style evaluation to Arabic dialects                                   | Focuses on knowledge/reasoning rather than gender bias                                                                                 | Uses the same motivation of dialect inclusion but applies it to gender-bias evaluation                                         |
| R7  | MORPHOGEN: A Multilingual Benchmark for Evaluating Gender-Aware Morphology                            | Gender-aware morphology in grammatically gendered languages | French, Arabic, Hindi                           | Counterfactual sentence-pair benchmark                           | Includes Arabic in a multilingual grammatical-gender counterfactual benchmark      | Multilingual focus; may not deeply analyze Arabic dialect variation such as Egyptian                                                   | Provides a dedicated Arabic-focused benchmark with MSA/Egyptian comparison and Arabic-specific template analysis               |
| R8  | Arabic LLM survey                                                                                     | Survey of Arabic LLMs and resources                         | Arabic, MSA, dialectal Arabic                   | Literature survey                                                | Summarizes Arabic LLM architectures, datasets, and challenges                      | Survey only; does not propose a gender-bias benchmark                                                                                  | Provides background motivation for evaluating Arabic-specific and multilingual LLMs                                            |
| R9  | Gender Bias in NLP / GeBNLP line of work                                                              | Gender bias evaluation and mitigation                       | Mostly multilingual, often English-heavy        | Bias benchmarks, probing, mitigation                             | Establishes gender bias as a major NLP fairness problem                            | Arabic and dialectal Arabic remain underrepresented compared with English                                                              | Contributes a focused Arabic benchmark and evaluation pipeline                                                                 |
| R10 | General counterfactual fairness / counterfactual probing work                                         | Bias detection through paired examples                      | Mostly English or multilingual                  | Counterfactual pairs                                             | Shows that counterfactual examples can reveal model preference patterns            | Often does not handle Arabic grammatical gender complexity                                                                             | Applies counterfactual probing to Arabic grammatical gender with dialect and template metadata                                 |

---

## Literature Gap Summary

The reviewed literature shows four main gaps:

1. Arabic gender-bias evaluation is still less developed than English gender-bias evaluation.

2. Many Arabic bias studies focus on MSA or general Arabic, while dialectal Arabic is less represented.

3. Existing Arabic bias benchmarks often do not deeply analyze template effects, even though template construction can strongly change measured bias.

4. Some studies evaluate embeddings or masked language models, while fewer studies evaluate causal LMs using sentence-level counterfactual probability scoring.

---

## Thesis Positioning

This thesis addresses these gaps by proposing a counterfactual Arabic gender-bias benchmark that is:

* sentence-level
* grammatical-gender-aware
* dialect-aware
* template-controlled
* suitable for causal language model evaluation
* designed with explicit concept_id and template_id metadata
* evaluated across Arabic-specific and multilingual models

---

## Contribution Statement

The main contribution of this thesis is a controlled Arabic gender-bias evaluation pipeline that detects and analyzes model preference between masculine and feminine counterfactual sentence variants across MSA and Egyptian Arabic.

Unlike prior work that focuses mainly on general Arabic, embeddings, or broad demographic categories, this work emphasizes Arabic grammatical gender, dialect-sensitive construction, and template-level quality control.
