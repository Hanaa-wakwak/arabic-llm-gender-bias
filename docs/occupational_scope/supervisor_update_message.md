# Supervisor Update Message

Dear Dr. [Name],

I would like to update you on the current thesis progress.

Based on your feedback, I narrowed the thesis scope to one clear domain: occupational gender bias in Arabic causal language models.

I built a controlled counterfactual benchmark where each item contains a masculine and feminine version of the same occupational sentence. The final benchmark version contains 60 occupations across six professional fields, with both MSA and Egyptian Arabic templates, resulting in 240 sentence pairs.

I evaluated four causal language models:

* AraGPT2-base
* AraGPT2-medium
* BLOOM-560m
* BLOOM-1b1

The models were selected to compare Arabic-specific models against multilingual models.

The main finding is that Arabic-specific AraGPT2 models show statistically significant masculine occupational preference, while multilingual BLOOM models show statistically significant feminine occupational preference.

The results were tested using binomial tests, Wilcoxon signed-rank tests, and chi-square analysis. The model-family association was highly significant, with chi-square p-value = 1.31e-20.

The next step is to finalize the methodology and results chapters, then prepare the final presentation.

Best regards,
[Your Name]
