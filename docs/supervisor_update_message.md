Hello Doctor,

I wanted to update you on my thesis progress.

I completed the first full experimental pipeline for the Arabic gender-bias topic. I built a counterfactual Arabic benchmark with masculine/feminine sentence pairs covering MSA and Egyptian Arabic, occupations and traits.

I created several benchmark versions and selected v0.7 as the stable expanded pilot with 144 items. I also evaluated four causal language models: AraGPT2-base, AraGPT2-medium, BLOOM-560m, and BLOOM-1b1.

The main preliminary finding is that Arabic-specific AraGPT2 models are more balanced, while multilingual BLOOM models show statistically significant feminine-form preference.

I also found that Arabic bias measurement is highly sensitive to sentence templates, especially in Egyptian Arabic, so I added template-level quality control.

The repository now includes the benchmark, scripts, results, figures, tables, methodology draft, results draft, literature review draft, and statistical tests.

Best regards,
Hanaa
 Emaillll
 Hello Doctor,

I wanted to update you on my thesis progress.

I have completed the first full experimental pipeline for my topic: counterfactual and dialect-aware gender bias evaluation in Arabic causal language models.

So far, I have completed:

1. Built a controlled Arabic gender-bias benchmark using masculine/feminine counterfactual sentence pairs.

2. Included both Modern Standard Arabic and Egyptian Arabic.

3. Added two main dimensions: occupations and traits.

4. Added metadata for concept, dialect, stereotype direction, and sentence template.

5. Created multiple benchmark versions and selected the most stable expanded version, v0.7, with 144 sentence pairs.

6. Evaluated four causal language models:

   * AraGPT2-base
   * AraGPT2-medium
   * BLOOM-560m
   * BLOOM-1b1

7. Generated result tables, figures, and statistical tests.

The main preliminary finding is that Arabic-specific AraGPT2 models are more balanced, while multilingual BLOOM models show statistically significant feminine-form preference on the benchmark.

I also found that template construction strongly affects measured Arabic gender bias, especially in Egyptian Arabic, so I added template-level quality control to the pipeline.

The repository now includes the benchmark, scoring scripts, analysis scripts, figures, tables, methodology draft, results draft, literature review draft, and statistical testing results.

My next planned steps are:

* add more models,
* add human validation for sentence quality,
* and start token-level analysis or mitigation experiments.

Best regards,
Hanaa
