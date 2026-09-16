# 2. Related Work

## 2.1 Bias Evaluation in Language Models

Bias evaluation has become an important research area in natural language processing because language models can encode social associations learned from training data. These associations may appear in generated text, sentence likelihoods, word representations, or downstream system behavior. Gender bias is one of the most widely studied forms of bias, especially in occupational contexts where models may associate certain professions or professional attributes more strongly with men or women.

Early studies focused on static word embeddings and showed that vector representations can encode gender stereotypes. Bolukbasi et al. demonstrated that word embeddings contain occupational gender associations and proposed methods for quantifying and reducing gender stereotypes in embedding spaces. Although embedding-based methods are useful for identifying lexical associations, they are limited for sentence-level evaluation because modern language models are contextual and generative.

As language models became more complex, bias evaluation moved toward contextual and benchmark-based methods. These methods use designed examples to measure whether a model prefers a stereotypical or gendered variant over an alternative. This direction is relevant to the present work because occupational bias in Arabic cannot be measured reliably using isolated word pairs only. Arabic gender marking interacts with sentence-level morphology and agreement, so full-sentence evaluation is required.

## 2.2 Paired-Sentence and Counterfactual Benchmarks

Paired-sentence benchmarks compare two sentences that are minimally different while preserving the same general structure. This design is useful for bias evaluation because it isolates the effect of the target attribute. CrowS-Pairs is one of the most influential examples of this approach. It measures social biases in language models using sentence pairs that differ in stereotypical association. StereoSet also evaluates stereotypical bias in pretrained language models by comparing stereotypical, anti-stereotypical, and unrelated alternatives.

The present work follows the paired-comparison logic of these benchmarks but adapts it to Arabic occupational gender bias. Instead of comparing general stereotypical statements, this paper compares masculine and feminine Arabic occupational sentence pairs. The goal is to determine whether a causal language model assigns higher likelihood to the masculine or feminine variant.

Counterfactual evaluation is central to this approach. In a counterfactual pair, the main semantic content remains constant while a target attribute changes. For occupational gender bias, the target attribute is the gendered form of the occupation and any required grammatical agreement. This is especially important for Arabic because a valid masculine–feminine transformation may require changes to multiple words in the sentence.

## 2.3 Likelihood-Based Bias Scoring

Likelihood-based scoring evaluates which sentence variant a language model considers more probable. This is useful for open-weight causal language models because token-level likelihood or language-modeling loss can be computed directly. Probability-based approaches have been used in prior work to measure bias in contextualized representations and language models.

Kurita et al. studied bias in contextualized word representations using probability-based measures. Kaneko and Bollegala argued that masked-token bias metrics can be problematic and proposed All Unmasked Likelihood as an alternative for evaluating social biases in masked language models. Salazar et al. introduced masked language model scoring for sentence-level likelihood estimation. These works support the broader idea that likelihood-based scoring can be used to evaluate model preference between sentence variants.

This paper applies likelihood-based scoring to Arabic causal language models. Each sentence is scored using average token log-probability. For each masculine–feminine pair, the score difference is computed as:

`score_difference = masculine_score - feminine_score`

This metric provides a directional measure of gender preference. Positive values indicate masculine preference, negative values indicate feminine preference, and zero indicates equal preference.

## 2.4 Arabic NLP and Gender Bias

Arabic presents specific challenges for NLP because of its morphology, grammatical gender, and dialectal diversity. Gender is not limited to pronouns or isolated nouns. It can appear in occupational nouns, demonstratives, verbs, adjectives, and agreement markers. As a result, Arabic gender-bias evaluation requires sentence-level control.

For example, the masculine sentence:

`هذا الطبيب يعمل في المستشفى`

must be paired with the feminine sentence:

`هذه الطبيبة تعمل في المستشفى`

The transformation changes both the demonstrative and the occupational noun. If the agreement structure is not preserved, the feminine sentence may become unnatural or grammatically incorrect. This would make the bias score unreliable because the model may penalize the sentence for linguistic invalidity rather than gender preference.

Recent Arabic bias work has started to address Arabic-specific evaluation. Studies on Arabic pretrained language models, Arabic embedding bias, and Arabic demographic-bias benchmarks show that bias evaluation must be adapted to Arabic linguistic and cultural contexts. However, more work is needed on occupational gender bias in Arabic causal language models, especially using full-sentence likelihood-based counterfactual evaluation.

## 2.5 Dialect-Aware Evaluation

Arabic is not a single uniform variety in practical NLP use. Modern Standard Arabic is used in formal writing, official communication, news, and education, while dialectal Arabic is common in informal communication, social media, and local digital interaction. Language models trained on mixed Arabic corpora may therefore behave differently across Arabic varieties.

Dialect-aware evaluation is important because a model that appears to show one bias pattern in MSA may behave differently in Egyptian Arabic or another dialect. This paper includes both MSA and Egyptian Arabic templates to test whether measured occupational gender preference is stable across Arabic varieties.

This dialect-aware design is one of the main differences between this work and many general bias benchmarks. Rather than treating Arabic as a single homogeneous language, the benchmark evaluates whether dialectal context affects model preference.

## 2.6 Occupational Gender Bias and Recruitment Contexts

Occupational gender bias is important because occupations are connected to education, employment, income, status, and professional opportunity. A model may associate technical, managerial, or leadership roles with masculine forms and care-related or administrative roles with feminine forms. These associations may affect downstream systems that generate or process professional text.

Recruitment language is a particularly relevant setting for occupational bias. Language models may be used to write job advertisements, summarize CVs, generate professional biographies, classify job roles, or assist with HR communication. Therefore, evaluation should include not only general occupational templates but also job-title and job-advertisement contexts.

This paper includes job-title templates and real-world job-advertisement contexts derived from ArabJobs. The purpose is to compare controlled benchmark results with recruitment-language settings. This helps evaluate whether model behavior changes when the occupation appears in contexts closer to real employment applications.

## 2.7 Bias Mitigation

Bias mitigation aims to reduce undesirable model behavior. Counterfactual Data Augmentation is a common mitigation strategy in which balanced examples are added to training or fine-tuning data. This strategy is especially relevant for morphologically rich languages because gender transformations must preserve grammatical correctness.

For Arabic, counterfactual mitigation must account for occupational forms and agreement markers. A simple word swap may not produce a valid sentence. Therefore, balanced masculine–feminine Arabic occupational sentence pairs can support both evaluation and mitigation.

Although the main focus of this conference paper is benchmark-based measurement and robustness analysis, the wider project also includes a counterfactual data augmentation mitigation experiment. This demonstrates how the benchmark suite can be used not only to measure bias, but also to test whether bias-limitation methods reduce measured preference.

## 2.8 Research Gap

Prior work provides strong foundations for bias evaluation, including paired-sentence benchmarks, likelihood-based scoring, counterfactual evaluation, and mitigation methods. However, several gaps remain for Arabic occupational gender-bias evaluation.

First, many existing benchmarks were designed primarily for English or for general social-bias categories. They do not directly address Arabic grammatical gender and sentence-level agreement.

Second, Arabic bias studies remain limited compared with English. More work is needed on Arabic causal language models and full-sentence likelihood-based evaluation.

Third, many studies report model-level bias scores without testing whether the score is stable across templates, dialects, semantic frames, job-title contexts, and real-world recruitment-language data.

Fourth, Arabic recruitment-language evaluation remains underexplored, even though occupational bias is directly relevant to job advertisements and HR-related NLP systems.

This paper addresses these gaps by introducing a dialect-aware Arabic occupational counterfactual benchmark and evaluating Arabic-specific and multilingual causal language models across controlled templates, template perturbations, job-title contexts, expanded job-role contexts, and real-world job-advertisement contexts.
