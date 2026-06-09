# Literature Review Draft

## 1. Gender Bias in NLP and Language Models

Gender bias has become a major concern in Natural Language Processing because language models often learn social associations from large-scale training data. These associations can appear in model predictions, generated text, or probability scores. In gendered languages, the problem becomes more complex because gender is not only expressed through pronouns, but also through nouns, adjectives, verbs, and agreement morphology.

Most early work on gender bias focused on English and other high-resource languages. However, Arabic requires special attention because grammatical gender is deeply encoded in its morphology. A sentence may change across several words when switching from a masculine form to a feminine form. Therefore, Arabic gender-bias evaluation cannot rely only on English-style pronoun substitution.

This motivates the use of counterfactual sentence pairs in which masculine and feminine versions of the same sentence are compared while preserving the core meaning.

## 2. Arabic Gender-Bias Evaluation

Recent work has started to investigate gender bias in Arabic language technologies. Some studies focus on Arabic word embeddings and measure gender associations using embedding-based metrics such as WEAT and direct bias. These approaches are useful for detecting lexical associations, especially around occupations and social roles.

However, embedding-based methods do not fully capture the behavior of modern causal language models. Large language models assign probabilities to full sequences, and their behavior depends on sentence structure, morphology, and context. Therefore, sentence-level counterfactual evaluation is needed to understand how models treat masculine and feminine Arabic variants.

Arabic LLM bias benchmarks have also begun to appear. For example, ArGAN provides an Arabic dataset for evaluating bias across gender, ability, and nationality in large language models. This is important because it shows growing attention to Arabic-specific bias evaluation. However, the present thesis focuses more narrowly on grammatical gender and introduces dialect-aware and template-controlled analysis.

## 3. Dialectal Arabic Evaluation

Arabic is not a single uniform variety. Modern Standard Arabic is widely used in formal writing, but dialects are common in everyday communication. Many Arabic NLP benchmarks still focus mainly on MSA, which can limit their ability to evaluate real-world Arabic model behavior.

Recent dialectal benchmarks address this limitation. AraDiCE introduces Arabic dialect and cultural evaluation resources and highlights the underrepresentation of dialectal Arabic in LLM evaluation. DialectalArabicMMLU extends benchmark evaluation to multiple Arabic dialects, including Egyptian Arabic. These works show that dialectal evaluation is becoming an important direction in Arabic NLP.

The present thesis builds on this motivation by including both MSA and Egyptian Arabic. However, instead of evaluating general reasoning or cultural knowledge, it evaluates gender preference patterns using controlled masculine/feminine counterfactual pairs.

## 4. Counterfactual and Morphological Gender Benchmarks

Counterfactual evaluation is a common method for bias detection. The key idea is to create paired inputs that differ only in the demographic attribute being tested. If a model assigns different scores or outputs to the two versions, this may indicate a preference or bias pattern.

For Arabic, counterfactual gender evaluation must account for grammatical gender agreement. A masculine-to-feminine transformation may require changing nouns, adjectives, verbs, and pronouns. This makes Arabic different from English, where gender counterfactuals often involve changing only pronouns or names.

MORPHOGEN is a recent multilingual benchmark that evaluates gender-aware morphological generation in languages including Arabic, French, and Hindi. It shows that grammatical gender and morphology are important challenges for multilingual LLMs. The present thesis shares this motivation, but focuses specifically on Arabic bias detection rather than morphological generation alone. It also adds dialect-level comparison between MSA and Egyptian Arabic.

## 5. Template Sensitivity in Bias Evaluation

Template-based bias benchmarks are useful because they allow controlled comparison across concepts and demographic categories. However, this thesis found that template construction can strongly affect measured gender preference.

During benchmark development, some templates produced strong masculine or feminine preference independent of the target concept. This means that bias scores may reflect template artifacts rather than genuine concept-level gender associations.

To address this issue, the proposed benchmark includes explicit `template_id` metadata and analyzes results at the template level. Templates with strong dominance patterns or high score differences are flagged for review. This quality-control process is important because Arabic grammatical gender interacts with sentence structure in ways that can affect model probability scores.

## 6. Arabic-Specific vs Multilingual Models

Another important theme in Arabic LLM evaluation is the comparison between Arabic-specific and multilingual models. Arabic-specific models are trained with greater focus on Arabic data, while multilingual models are trained across many languages. Prior dialectal evaluation work has shown that model family and training data can affect Arabic and dialectal performance.

The experiments in this thesis compare Arabic-specific AraGPT2 models with multilingual BLOOM models. The results show different gender-preference patterns across model families. AraGPT2 models are more balanced overall, while BLOOM models show a stronger feminine-form preference across dialects, dimensions, and stereotype categories.

This supports the need to evaluate multiple model families rather than assuming that all Arabic-capable models behave similarly.

## 7. Research Gap

The reviewed literature reveals several gaps.

First, Arabic gender-bias evaluation remains less developed than English gender-bias evaluation.

Second, many Arabic bias studies focus on MSA or general Arabic, while dialectal Arabic receives less attention.

Third, existing benchmarks often do not deeply analyze the effect of sentence templates, even though template construction can change the measured direction and strength of gender preference.

Fourth, some prior work focuses on word embeddings, masked-language models, or general demographic bias, while fewer studies evaluate causal LMs using sentence-level masculine/feminine probability comparisons.

## 8. Thesis Positioning

This thesis addresses these gaps by developing a counterfactual Arabic gender-bias evaluation pipeline that is:

* sentence-level
* grammatical-gender-aware
* dialect-aware
* template-controlled
* suitable for causal language models
* evaluated across Arabic-specific and multilingual model families

The benchmark includes MSA and Egyptian Arabic, occupation and trait dimensions, stereotype-direction metadata, and explicit concept and template identifiers.

The main contribution is not only the benchmark itself, but also the quality-control methodology showing that Arabic gender-bias evaluation must account for dialect and template effects.
