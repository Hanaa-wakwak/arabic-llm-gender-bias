# Results and Analysis Draft

## 1. Benchmark Version Selection

Several benchmark versions were developed and evaluated during the pilot construction phase.

The selected stable pilot benchmark is `minimal_pairs_v04.csv`, which contains 48 controlled Arabic gender counterfactual pairs. This version was selected because it showed strong dialect-level balance between MSA and Egyptian Arabic.

After that, the benchmark was expanded using controlled lexicon files for occupations and traits. The expanded versions contained 144 items. Among the expanded versions, `minimal_pairs_v07.csv` was selected as the expanded pilot benchmark.

The selected expanded benchmark contains:

* 144 minimal gender counterfactual pairs
* 18 occupation concepts
* 18 trait concepts
* MSA and Egyptian Arabic subsets
* concept-level metadata
* template-level metadata
* stereotype-direction metadata

Version v0.7 was selected because it provided the best balance between benchmark size, overall score stability, dialect-level balance, and acceptable outlier rate.

## 2. Multi-Model Evaluation Setup

The selected benchmark version `minimal_pairs_v07.csv` was used to evaluate four causal language models:

1. `aubmindlab/aragpt2-base`
2. `aubmindlab/aragpt2-medium`
3. `bigscience/bloom-560m`
4. `bigscience/bloom-1b1`

Each model was evaluated using average sentence log-probability. For each masculine/feminine counterfactual pair, the score difference was computed as:

`score_difference = masculine_score - feminine_score`

A positive score difference indicates that the model assigns a higher probability to the masculine sentence variant. A negative score difference indicates that the model assigns a higher probability to the feminine sentence variant.

## 3. Overall Model Comparison

The overall results show clear differences between Arabic-specific models and multilingual models.

`AraGPT2-medium` was the most balanced model by preference counts, with 76 masculine-preferred items and 68 feminine-preferred items.

`AraGPT2-base` showed a moderate masculine-preference count pattern, with 84 masculine-preferred items and 60 feminine-preferred items. However, its average score difference was close to zero, indicating that the overall magnitude of preference was relatively balanced.

In contrast, the BLOOM models showed stronger feminine-form preference. `BLOOM-1b1` preferred feminine variants in 94 out of 144 items, while `BLOOM-560m` preferred feminine variants in 101 out of 144 items.

This suggests that the multilingual BLOOM models behave differently from the Arabic-specific AraGPT2 models on the proposed Arabic gender counterfactual benchmark.

## 4. Dialect-Level Analysis

The dialect-level results show that model behavior differs across MSA and Egyptian Arabic.

`AraGPT2-base` showed identical preference-count distributions across the two dialects:

* Egyptian: 42 masculine-preferred items and 30 feminine-preferred items
* MSA: 42 masculine-preferred items and 30 feminine-preferred items

This suggests that `AraGPT2-base` is relatively stable across the MSA and Egyptian subsets in this benchmark.

`AraGPT2-medium` showed dialect-sensitive behavior. It preferred feminine variants more often in Egyptian Arabic, but masculine variants more often in MSA.

Both BLOOM models showed feminine-form preference across both dialects. `BLOOM-560m` showed the strongest feminine preference, especially in the MSA subset.

## 5. Dimension-Level Analysis

The benchmark includes two main dimensions: occupation and trait.

The occupation dimension produced stronger divergence between Arabic-specific and multilingual models.

For occupation items, both AraGPT2 models preferred masculine variants more often:

* `AraGPT2-base`: 47 masculine-preferred and 25 feminine-preferred
* `AraGPT2-medium`: 45 masculine-preferred and 27 feminine-preferred

In contrast, BLOOM models strongly preferred feminine variants in occupation items:

* `BLOOM-1b1`: 20 masculine-preferred and 52 feminine-preferred
* `BLOOM-560m`: 18 masculine-preferred and 54 feminine-preferred

Trait items were more balanced for `AraGPT2-base`, but still showed feminine preference for `AraGPT2-medium` and BLOOM models.

## 6. Stereotype-Direction Analysis

The stereotype-direction analysis shows that AraGPT2 models partially follow the stereotype direction encoded in the benchmark.

For female-stereotype items, AraGPT2 models preferred feminine variants more often. For male-stereotype items, AraGPT2 models showed higher masculine preference. This suggests that AraGPT2 models may reflect stereotype-associated gender patterns.

In contrast, BLOOM models showed feminine preference across female-stereotype, male-stereotype, and neutral categories. This suggests that BLOOM models may have a more general feminine-form preference rather than a stereotype-direction-specific pattern.

## 7. Main Findings

The results support the following findings:

1. Arabic-specific AraGPT2 models are more balanced than multilingual BLOOM models on the proposed Arabic counterfactual gender benchmark.

2. `AraGPT2-medium` is the most balanced model overall by preference counts.

3. BLOOM models show consistent feminine-form preference across dialects, dimensions, and stereotype-direction categories.

4. Occupation items reveal stronger divergence between Arabic-specific and multilingual models than trait items.

5. `AraGPT2-base` shows the most stable dialect-level preference-count distribution across MSA and Egyptian Arabic.

6. Arabic gender-bias evaluation is highly sensitive to model family, dialect, and sentence-template construction.

## 8. Preliminary Conclusion

The proposed benchmark successfully reveals measurable differences between Arabic-specific and multilingual causal language models.

The results show that evaluating Arabic gender bias requires more than a simple MSA-only benchmark. Dialect, grammatical gender agreement, template structure, and model family all affect the measured bias pattern.

Therefore, counterfactual, dialect-aware, and template-controlled evaluation is necessary for reliable gender-bias analysis in Arabic language models.
