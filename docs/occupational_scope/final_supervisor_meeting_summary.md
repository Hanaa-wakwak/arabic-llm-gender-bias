## Enriched Six-Model Result

To strengthen the robustness of the thesis, two additional non-Arabic-specific causal language models were evaluated:

* `facebook/xglm-564M`
* `Qwen/Qwen2.5-0.5B`

Both models were evaluated on the same final benchmark, `occupational_bias_v2.csv`.

After adding these models, the full experiment includes six models:

| Model          | Family              | Direction |
| -------------- | ------------------- | --------- |
| AraGPT2-base   | Arabic-specific     | Masculine |
| AraGPT2-medium | Arabic-specific     | Masculine |
| BLOOM-560m     | Non-Arabic-specific | Feminine  |
| BLOOM-1b1      | Non-Arabic-specific | Feminine  |
| XGLM-564M      | Non-Arabic-specific | Feminine  |
| Qwen2.5-0.5B   | Non-Arabic-specific | Feminine  |

The aggregated family-level result is:

| Model Family        | Masculine Preferred | Feminine Preferred | Equal | Direction |
| ------------------- | ------------------: | -----------------: | ----: | --------- |
| Arabic-specific     |                 320 |                160 |     0 | Masculine |
| Non-Arabic-specific |                 346 |                610 |     4 | Feminine  |

The model-family association remains highly significant:

```text
chi-square p-value = 1.64e-27
```

This strengthens the thesis because the feminine preference pattern is not limited to BLOOM models. It also appears in XGLM-564M and Qwen2.5-0.5B.
