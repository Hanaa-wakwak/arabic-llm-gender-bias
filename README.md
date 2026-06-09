\# Arabic LLM Gender Bias Benchmark



\## Project Title



\*\*Counterfactual and Dialect-Aware Gender Bias Evaluation in Arabic Causal Language Models\*\*



\---



\## Overview



This project investigates gender preference patterns in Arabic causal language models using a counterfactual benchmark.



The benchmark compares masculine and feminine versions of the same Arabic sentence while keeping the meaning as similar as possible. The goal is to measure whether a language model assigns higher probability to the masculine or feminine variant.



The project focuses on:



\* Arabic grammatical gender

\* Modern Standard Arabic (MSA)

\* Egyptian Arabic

\* occupation and trait concepts

\* template-controlled benchmark construction

\* Arabic-specific vs multilingual causal language models



\---



\## Research Motivation



Arabic gender bias evaluation is challenging because gender is expressed through multiple grammatical forms, including:



\* pronouns

\* nouns

\* adjectives

\* verbs

\* agreement morphology



Many bias benchmarks focus on English or MSA only. This project adds dialect-aware Arabic evaluation by including both MSA and Egyptian Arabic.



The project also shows that Arabic gender-bias measurement is highly sensitive to sentence templates. Therefore, each item includes `template\_id` metadata for quality control.



\---



\## Benchmark



The selected expanded pilot benchmark is:



```text

data/benchmark\_v0/minimal\_pairs\_v07.csv

```



It contains:



| Component            |              Count |

| -------------------- | -----------------: |

| Total sentence pairs |                144 |

| Occupation concepts  |                 18 |

| Trait concepts       |                 18 |

| Dialects             |     MSA + Egyptian |

| Main dimensions      | occupation + trait |



Each benchmark row includes:



| Column                 | Description                                                  |

| ---------------------- | ------------------------------------------------------------ |

| `id`                   | item ID                                                      |

| `concept\_id`           | tested concept, such as doctor, engineer, emotional, patient |

| `dimension`            | occupation or trait                                          |

| `dialect`              | MSA or Egyptian                                              |

| `template\_id`          | sentence template identifier                                 |

| `masculine\_sentence`   | masculine sentence variant                                   |

| `feminine\_sentence`    | feminine sentence variant                                    |

| `stereotype\_direction` | male\_stereotype, female\_stereotype, or neutral               |

| `notes`                | construction notes                                           |



\---



\## Scoring Method



Each model is evaluated using average sentence log-probability.



For each masculine/feminine pair:



```text

score\_difference = masculine\_score - feminine\_score

```



Interpretation:



| Score Difference | Meaning                             |

| ---------------- | ----------------------------------- |

| Positive         | model prefers the masculine variant |

| Negative         | model prefers the feminine variant  |

| Zero             | no preference                       |



\---



\## Evaluated Models



The selected benchmark was evaluated on four causal language models:



| Model                       | Type            |

| --------------------------- | --------------- |

| `aubmindlab/aragpt2-base`   | Arabic-specific |

| `aubmindlab/aragpt2-medium` | Arabic-specific |

| `bigscience/bloom-560m`     | multilingual    |

| `bigscience/bloom-1b1`      | multilingual    |



\---



\## Main Results



Overall multi-model results on `minimal\_pairs\_v07.csv`:



| Model                       | Masculine Preferred | Feminine Preferred | Masculine % | Feminine % | Avg Score Difference |

| --------------------------- | ------------------: | -----------------: | ----------: | ---------: | -------------------: |

| `aubmindlab/aragpt2-base`   |                  84 |                 60 |      58.33% |     41.67% |              -0.0139 |

| `aubmindlab/aragpt2-medium` |                  76 |                 68 |      52.78% |     47.22% |              -0.0524 |

| `bigscience/bloom-1b1`      |                  50 |                 94 |      34.72% |     65.28% |              -0.2519 |

| `bigscience/bloom-560m`     |                  43 |                101 |      29.86% |     70.14% |              -0.3909 |



\---



\## Key Findings



1\. Arabic-specific AraGPT2 models are more balanced than multilingual BLOOM models.



2\. `AraGPT2-medium` is the most balanced model overall by preference counts.



3\. BLOOM models show consistent feminine-form preference across dialects, dimensions, and stereotype-direction categories.



4\. Occupation items reveal stronger divergence between Arabic-specific and multilingual models than trait items.



5\. Template construction strongly affects measured Arabic gender preference, especially in dialectal Arabic.



\---



\## Project Structure



```text

arabic-llm-gender-bias/

├── data/

│   ├── benchmark\_v0/

│   │   ├── minimal\_pairs\_v04.csv

│   │   ├── minimal\_pairs\_v07.csv

│   │   └── minimal\_pairs\_v08.csv

│   ├── lexicons/

│   │   ├── occupations\_v01.csv

│   │   └── traits\_v01.csv

│   └── review/

├── docs/

│   ├── methodology\_section\_draft.md

│   ├── results\_section\_draft.md

│   ├── literature\_review\_draft.md

│   ├── thesis\_outline.md

│   └── expanded\_benchmark\_decision.md

├── results/

│   ├── model\_comparison\_v07/

│   ├── figures\_v07/

│   └── thesis\_tables\_v07/

├── src/

│   ├── build\_benchmark\_v07\_from\_lexicons.py

│   ├── score\_pairs.py

│   ├── score\_multiple\_models.py

│   ├── analyze\_multiple\_models.py

│   ├── quality\_report.py

│   ├── create\_result\_plots\_v07.py

│   └── create\_thesis\_tables\_v07.py

├── requirements.txt

└── README.md

```



\---



\## How to Run



\### 1. Install requirements



```bash

pip install -r requirements.txt

```



\### 2. Build selected expanded benchmark



```bash

python src/build\_benchmark\_v07\_from\_lexicons.py

```



\### 3. Score one model



```bash

python src/score\_pairs.py --input data/benchmark\_v0/minimal\_pairs\_v07.csv --output results/scoring\_results\_v07.csv

```



\### 4. Score multiple models



```bash

python src/score\_multiple\_models.py

```



\### 5. Analyze multi-model results



```bash

python src/analyze\_multiple\_models.py

```



\### 6. Generate figures



```bash

python src/create\_result\_plots\_v07.py

```



\### 7. Generate thesis-ready tables



```bash

python src/create\_thesis\_tables\_v07.py

```



\---



\## Outputs



Important output folders:



| Folder                          | Description                                                        |

| ------------------------------- | ------------------------------------------------------------------ |

| `results/model\_comparison\_v07/` | multi-model scoring and summary files                              |

| `results/figures\_v07/`          | generated plots                                                    |

| `results/thesis\_tables\_v07/`    | thesis-ready CSV and Markdown tables                               |

| `docs/`                         | methodology, results, literature review, and thesis outline drafts |



\---



\## Current Status



Completed:



\* benchmark construction

\* pilot versioning

\* template quality control

\* expanded benchmark selection

\* multi-model evaluation

\* result figures

\* thesis-ready tables

\* methodology draft

\* results draft

\* literature review draft

\* thesis outline



Next stages:



\* add more models

\* add human validation

\* add statistical testing

\* add mitigation experiments

\* add explainability/token-level analysis



\---



\## Repository Purpose



This repository is part of a master’s thesis project on Arabic LLM gender bias detection.



The project aims to provide a reproducible pipeline for evaluating gender preference in Arabic causal language models using controlled masculine/feminine counterfactual sentence pairs.



