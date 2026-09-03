# Chapter 2: Literature Review

## 2.1 Overview

This chapter reviews the academic literature related to gender-bias evaluation in language models, with emphasis on occupational bias, counterfactual evaluation, likelihood-based scoring, Arabic NLP, Arabic gender morphology, dialect-aware evaluation, job-advertisement data, validation, reproducibility, and bias mitigation.

The thesis is positioned at the intersection of three research areas. The first is fairness and bias evaluation in language models. The second is Arabic NLP and Arabic-specific bias evaluation. The third is reproducible software engineering for measuring, validating, and limiting bias in computational systems.

The main argument developed in this literature review is that existing bias-evaluation methods provide useful foundations, but they are not sufficient on their own for Arabic occupational gender-bias evaluation in causal language models. Arabic requires full-sentence counterfactual design because gender is expressed through morphology and grammatical agreement. Arabic bias evaluation also requires attention to dialect, template formulation, occupational context, and real-world recruitment language.

## 2.2 Bias in Language Models

Language models learn statistical patterns from large text corpora. These patterns can include useful linguistic knowledge, but they can also include social stereotypes and unequal associations. In the context of gender, a model may associate men and women with different occupations, traits, actions, or social roles. Such associations may appear in generated text, sentence likelihoods, masked-token predictions, embeddings, or downstream task behavior.

Bias in language models is especially important because LLMs are increasingly used in applications that affect users directly, including educational tools, recruitment systems, information retrieval, customer support, decision-support systems, and text-generation products. If a model encodes gendered occupational associations, these associations may affect how the model completes sentences, writes professional descriptions, ranks candidate-related text, or generates job advertisements.

Early work on bias in NLP often focused on static word embeddings. Later work expanded bias evaluation to contextual language models, masked language models, and generative models. This shift is important because modern language models do not represent words in isolation. Instead, model behavior depends on context, prompt wording, sentence structure, and task format.

## 2.3 Gender Bias in Word Embeddings

A foundational line of work showed that word embeddings can encode gender stereotypes. Bolukbasi et al. studied gender stereotypes in word embeddings and proposed methods for quantifying and reducing gender bias in embedding spaces. Their paper is widely known for showing occupational analogies such as the association between “man” and “computer programmer” and between “woman” and “homemaker.” This work is important because it established that statistical language representations can encode socially meaningful gender associations.

However, word-embedding bias methods are limited for this thesis because they usually operate on word vectors rather than full sentences. Arabic occupational gender bias cannot be fully captured by isolated word comparisons because Arabic gender marking affects sentence-level agreement. For example, changing an occupational noun from masculine to feminine may require changes in demonstratives, verbs, adjectives, or agreement markers. Therefore, word-embedding methods provide historical and conceptual foundations, but this thesis requires sentence-level evaluation.

## 2.4 Benchmark-Based Bias Evaluation

As language models became more contextual, bias evaluation shifted toward benchmark-based methods. Benchmark-based evaluation uses designed examples or datasets to measure whether models prefer stereotypical, anti-stereotypical, masculine, feminine, or otherwise socially marked variants.

CrowS-Pairs is a major benchmark in this area. Nangia et al. introduced CrowS-Pairs as a challenge dataset for measuring social biases in masked language models using paired sentences. Each pair contains two minimally different sentences that differ in the stereotypical association being tested. This paired-sentence design is highly relevant to the present thesis because it supports the idea that bias can be measured by comparing model preference between minimally different sentence variants.

StereoSet is another important benchmark. Nadeem et al. proposed StereoSet to measure stereotypical bias in pretrained language models across domains including gender, profession, race, and religion. StereoSet is relevant because it evaluates stereotypical and anti-stereotypical alternatives while also considering language-modeling ability.

These benchmarks provide the methodological foundation for paired comparison. However, they are not designed specifically for Arabic occupational gender morphology or dialect-aware Arabic causal language models. The present thesis adapts the paired-benchmark logic to Arabic masculine–feminine occupational sentence pairs.

## 2.5 Likelihood-Based Bias Scoring

Likelihood-based scoring is important for evaluating open-weight language models because these models can assign probabilities or losses to token sequences. Instead of relying only on generated text, likelihood-based methods measure which sentence variant the model considers more probable.

Kurita et al. studied bias in contextualized word representations and proposed probability-based approaches for measuring bias in context. Their work is relevant because it connects bias measurement to model probabilities rather than only static word-vector distances.

Kaneko and Bollegala argued that some masked-language-model bias metrics are problematic because masked-token prediction can be unreliable, disconnected from downstream usage, and affected by word frequency. They proposed All Unmasked Likelihood as an alternative likelihood-based method for masked language models. This is relevant to the thesis because it supports the broader argument that likelihood-based sentence evaluation can provide a more complete view than isolated masked-token prediction.

The present thesis uses likelihood-based scoring for causal language models. For a sentence:

`x = (w_1, ..., w_n)`

the score is defined as average token log-probability:

`S(x) = (1 / n) * sum log P(w_t | w_<t)`

For each masculine–feminine pair:

`score_difference = masculine_score - feminine_score`

This formula is an operational adaptation for Arabic occupational counterfactual evaluation. It is grounded in the literature on paired-sentence and likelihood-based bias evaluation, but it is designed specifically for open-weight causal language models and Arabic sentence-level gender morphology.

## 2.6 Counterfactual Evaluation

Counterfactual evaluation measures whether a model changes its behavior when a protected attribute changes while the main meaning remains constant. In gender-bias evaluation, this often means comparing a masculine version of a sentence with a feminine version of the same sentence.

Counterfactual evaluation is useful because it isolates the effect of gendered language. If two sentences have the same occupational meaning but differ only in gender form, then a difference in model likelihood can be interpreted as a model preference between gendered variants under that context.

This thesis uses counterfactual evaluation as its central benchmark design principle. Each item contains a masculine Arabic sentence and a feminine counterfactual sentence. The sentences preserve the same occupation, template, semantic frame, and professional context. The gendered form and necessary grammatical agreement are changed.

For Arabic, counterfactual construction is more difficult than simple word replacement. A masculine form such as:

`هذا الطبيب يعمل في المستشفى.`

must be paired with a grammatically valid feminine form such as:

`هذه الطبيبة تعمل في المستشفى.`

This example shows why Arabic counterfactual evaluation must operate at the sentence level rather than only at the target-word level.

## 2.7 Arabic NLP and Gender Morphology

Arabic has rich morphology and grammatical gender. Many nouns have masculine and feminine forms, and gender agreement can appear in demonstratives, adjectives, verbs, and other sentence elements. This makes Arabic gender-bias evaluation more complex than evaluation in languages with less visible grammatical gender.

Arabic gender morphology is especially important in occupational language. Many Arabic job titles have masculine and feminine forms, such as:

`مهندس / مهندسة`

`طبيب / طبيبة`

`مدير / مديرة`

`معلم / معلمة`

These forms are not only lexical alternatives. They interact with sentence grammar. Therefore, a valid benchmark must preserve both semantic equivalence and grammatical correctness.

This thesis addresses this challenge by constructing full masculine–feminine counterfactual sentence pairs rather than isolated word pairs. The benchmark design changes both the occupational form and the surrounding agreement markers where necessary.

## 2.8 Arabic Gender-Bias Evaluation

Recent work has begun to study gender bias specifically in Arabic language models and Arabic text representations. Alrajhi et al. studied gender bias in Arabic pre-trained language models and reported corpus-level and model-level gender skew using Arabic NLP tools and template-based evaluation across Arabic pre-trained models. Their work is important because it shows that Arabic gender bias is affected by training corpora and can be measured through Arabic-specific benchmark design.

ArGAN is another important recent Arabic benchmark. Aly et al. introduced ArGAN, an Arabic Gender, Ability, and Nationality dataset for evaluating biases in LLMs. ArGAN is relevant because it shows the need for Arabic-specific LLM bias resources and adaptations of existing evaluation methods for Arabic demographic bias.

Mourad et al. studied gender bias in Arabic text through word embeddings and adapted association-based methods such as WEAT to Arabic corpora. Their work is relevant because it connects Arabic gender-bias analysis to occupations and shows that Arabic textual corpora can encode gendered associations.

These studies support the need for Arabic-specific bias evaluation. However, the present thesis differs from them in several ways. It focuses on open-weight causal language models, full-sentence likelihood scoring, occupational counterfactual pairs, dialect-aware templates, robustness across benchmark versions, job-role and department contexts, real-world job-advertisement evaluation, software implementation, and mitigation testing.

## 2.9 Occupational Gender Bias

Occupational gender bias is a particularly important form of gender bias because occupations are connected to employment, education, social status, economic opportunity, and professional identity. A model that systematically associates certain occupations with one gender may reproduce occupational stereotypes.

In NLP, occupational gender bias can appear in many forms. A model may predict masculine pronouns for technical jobs, feminine pronouns for care-related jobs, or generate different descriptions for male and female professionals. It may also assign higher likelihood to one gendered occupational form than another, even when the meaning is otherwise equivalent.

The present thesis focuses on occupational gender bias because Arabic occupational forms provide a clear linguistic site for counterfactual evaluation. Masculine and feminine job titles can be paired while preserving professional meaning. This enables a controlled comparison of model preference across occupational fields, job-title contexts, departments, job roles, and real-world recruitment language.

## 2.10 Template Sensitivity in Bias Evaluation

Template design is a known challenge in bias evaluation. A model’s measured behavior can change depending on how a sentence or prompt is written. This means that a benchmark using only one template may measure the effect of that template rather than a stable model property.

CrowS-Pairs and StereoSet both use structured examples to evaluate bias, but broader bias-evaluation literature shows that context and formulation can affect model outputs and scores. StereoSet explicitly notes limitations in bias evaluation when models are assessed on artificial sentences and when language-modeling ability is not considered alongside bias measurement.

This thesis addresses template sensitivity directly through the v4 template perturbation benchmark. Rather than assuming that one occupational template is sufficient, the thesis evaluates multiple templates and semantic frames, including workplace presence, leadership, competence, promotion, responsibility, and professional experience.

The purpose is to test whether measured bias remains stable under template changes. If the direction changes across templates, this means that gender preference should be reported with template-level analysis rather than only a single aggregate score.

## 2.11 Dialect-Aware Arabic Evaluation

Arabic NLP must account for dialectal variation. Modern Standard Arabic is used in formal communication, education, news, and official writing, while dialects such as Egyptian Arabic are common in everyday communication, social media, and informal digital text.

Bias evaluation that uses only MSA may fail to capture model behavior in dialectal contexts. This is important because LLMs may be trained on mixed Arabic data, including news, books, websites, social media, and informal user-generated text. A model may therefore behave differently when the input is formal MSA versus dialectal Arabic.

The present thesis includes both MSA and Egyptian Arabic templates. This allows the framework to evaluate whether gender preference changes across Arabic varieties. Dialect-aware evaluation is one of the central contributions of the thesis because it treats Arabic linguistic variation as an evaluation variable rather than a minor preprocessing issue.

## 2.12 Real-World Job-Advertisement Data

Controlled benchmarks provide internal validity because the researcher can control sentence structure, occupation, gender form, and template. However, controlled benchmarks may not fully reflect the complexity of real-world language.

Job advertisements are an important real-world context for occupational gender bias. They contain recruitment language, job titles, required skills, professional descriptions, workplace expectations, and sometimes explicit or implicit gender-related signals.

ArabJobs is a relevant external dataset for this thesis. El-Haj introduced ArabJobs as a multinational corpus of Arabic job advertisements. The corpus includes job ads collected from Egypt, Jordan, Saudi Arabia, and the United Arab Emirates. This makes it useful for Arabic NLP and labor-market research.

The ArabJobs paper and related materials describe the dataset as useful for fairness-aware Arabic NLP and labor-market research. This aligns closely with the thesis because the project evaluates occupational gender bias in recruitment-language contexts.

The present thesis uses ArabJobs-derived contexts as an external validation layer. It does not replace controlled benchmarks with real-world data. Instead, it compares controlled benchmark results with real-world job-advertisement results to test whether measured gender preference changes across data sources.

## 2.13 Bias Mitigation

Bias mitigation aims to reduce harmful or undesirable model behavior. In NLP, mitigation can occur at different stages, including data preprocessing, training, fine-tuning, decoding, post-processing, or model auditing.

Counterfactual Data Augmentation (CDA) is especially relevant to this thesis. Zmigrod et al. proposed counterfactual data augmentation for mitigating gender stereotypes in languages with rich morphology. Their work is important because it recognizes that simple gender swapping can produce ungrammatical results in morphologically rich languages.

This is highly relevant to Arabic. Like the languages discussed in CDA work, Arabic requires attention to morphological and grammatical agreement. A mitigation dataset must therefore include valid masculine and feminine sentence variants rather than naive word substitutions.

Self-debiasing is another mitigation approach. Schick et al. proposed self-diagnosis and self-debiasing as a decoding-time method for reducing corpus-based bias in language models without changing model parameters. This is relevant as future work, especially for generation-based systems.

The present thesis implements a counterfactual mitigation experiment. It creates balanced masculine–feminine Arabic occupational training data and fine-tunes AraGPT2-base. The mitigated model is then evaluated using the same benchmark suite to determine whether measured absolute bias decreases.

## 2.14 Human Validation and Inter-Annotator Agreement

Human validation is important for benchmark quality, especially when evaluating Arabic counterfactual sentences. Automatic generation of masculine–feminine pairs may introduce grammatical errors, unnatural phrasing, incorrect gender agreement, or dialect mismatches.

In this thesis, human validation is used to verify that benchmark pairs are acceptable for evaluation. Annotators review grammaticality, meaning preservation, gender-form correctness, dialect correctness, job-title correctness, and keep/remove decisions. Inter-annotator agreement is measured using percentage agreement and Cohen’s Kappa.

Human validation strengthens benchmark reliability because it provides evidence that the examples being scored are linguistically valid and semantically controlled. This is especially important for Q1 publication because reviewers are likely to ask whether Arabic counterfactual examples were manually checked.

## 2.15 Reproducibility in Bias Evaluation

Bias evaluation should be reproducible. A benchmark study is stronger when other researchers can inspect the datasets, run the scoring scripts, verify the formulas, reproduce the results, and audit the outputs.

This thesis treats reproducibility as a software engineering requirement. The project includes benchmark CSV files, scoring scripts, analysis scripts, validation scripts, human-validation files, software tools, run commands, documentation, mitigation scripts, and final audit reports.

This is important because bias evaluation can be affected by small implementation decisions, including sign conventions, tokenization, sentence length normalization, model version, input encoding, and aggregation logic. Formula validation and score-difference validation reduce the risk of reporting results based on inconsistent implementations.

## 2.16 Research Gap

The reviewed literature provides important foundations, but several gaps remain.

First, many foundational bias benchmarks were designed primarily for English or for general social-bias categories. They provide paired-sentence logic, but they do not directly address Arabic occupational morphology.

Second, Arabic gender-bias research exists, but much of it focuses on masked language models, word embeddings, corpus analysis, or broad demographic prompts. Less attention has been given to open-weight Arabic causal language models using full-sentence paired likelihood scoring.

Third, many studies report model-level bias scores but do not fully test whether the score is stable across templates, dialects, semantic frames, job-title contexts, departments, and job-role structures.

Fourth, real-world Arabic recruitment-language evaluation is still limited. ArabJobs provides an important data source, but more work is needed to connect Arabic job-advertisement corpora to LLM fairness evaluation.

Fifth, some studies measure bias but do not include full validation layers such as formula validation, implementation validation, human validation, token-length controls, and final reproducibility audits.

This thesis addresses these gaps by proposing a robustness-oriented Arabic occupational gender-bias evaluation framework for causal language models. The framework combines controlled counterfactual benchmark construction, dialect-aware templates, likelihood-based scoring, multi-model evaluation, template and dialect sensitivity analysis, job-title and job-role context analysis, ArabJobs external evaluation, human validation, formula validation, token-length control, software implementation, and counterfactual bias mitigation.

## 2.17 Positioning of the Present Thesis

The present thesis builds on prior work but differs in its target language, model type, evaluation unit, and robustness design.

Compared with CrowS-Pairs, the thesis adopts the idea of paired sentence comparison but applies it to Arabic masculine–feminine occupational counterfactual pairs and causal language models.

Compared with StereoSet, the thesis shares the goal of measuring stereotypical preference in language models, but it focuses specifically on Arabic occupational gender and benchmark-design sensitivity.

Compared with Kurita et al. and Kaneko and Bollegala, the thesis adopts likelihood-based reasoning but operationalizes it as full-sentence average token log-probability for open-weight causal language models.

Compared with Arabic embedding-bias work, the thesis moves from word-vector association to sentence-level causal-LM scoring.

Compared with Arabic benchmark work such as ArGAN, the thesis focuses specifically on occupational gender, dialect-aware templates, job-role and department contexts, external job-ad data, and mitigation.

Compared with CDA mitigation work, the thesis applies counterfactual balancing to Arabic occupational gender forms and evaluates the before/after effect using the same paired-likelihood framework.

## 2.18 Chapter Summary

This chapter reviewed the literature on language-model bias, gender bias, occupational stereotypes, benchmark-based evaluation, likelihood-based scoring, counterfactual evaluation, Arabic gender morphology, Arabic bias research, dialect-aware evaluation, job-advertisement data, human validation, reproducibility, and bias mitigation.

The literature shows that paired-sentence evaluation, likelihood scoring, and counterfactual methods are established foundations for bias measurement. However, Arabic occupational gender-bias evaluation requires additional design considerations because Arabic is morphologically gendered, dialectally diverse, and context-sensitive.

The research gap addressed by this thesis is the lack of a robustness-oriented Arabic occupational gender-bias evaluation framework for causal language models that combines controlled benchmarks, dialect awareness, job-role context, real-world recruitment-language evaluation, validation, software implementation, and mitigation. The next chapter presents the methodology developed to address this gap.
