# Final Benchmark Decision Note

## Decision

The final thesis should keep occupational benchmark v2 as the main validated benchmark.

Benchmark v3 is reported as an experimental sensitivity analysis.

## Reason

Benchmark v2 produced a stable and statistically significant model-family pattern across six models:

- Arabic-specific models preferred masculine occupational sentences.
- Non-Arabic-specific models preferred feminine occupational sentences.

Benchmark v3 expanded the occupation list and template set, but a quick diagnostic test showed that AraGPT2-base changed direction from masculine preference to feminine preference.

Further diagnostics showed that this change was not mainly caused by the new templates. Instead, the result suggests sensitivity to occupation coverage and lexical/contextual formulation.

## Final Role of Each Benchmark

| Benchmark | Role |
|---|---|
| v1 | Pilot benchmark |
| v2 | Main validated benchmark |
| v3 | Experimental sensitivity analysis |
| v3 controlled | Diagnostic benchmark |
| future v3 balanced | Future extension |

## Recommended Thesis Wording

The v2 benchmark remains the main benchmark because it is validated, stable, and statistically tested across six models. The v3 benchmark is included as an experimental sensitivity analysis showing that Arabic occupational gender-bias measurement is sensitive to benchmark expansion and lexical formulation. This supports the need for careful benchmark validation and future balanced benchmark design.

## Final Contribution After v4

The final contribution is not only a single benchmark result.

The thesis contributes an Arabic occupational gender-bias evaluation suite composed of:

1. a main validated benchmark,
2. benchmark-expansion sensitivity analysis,
3. stereotype-balanced sensitivity analysis,
4. template-perturbation sensitivity analysis,
5. external dataset pilots.

This allows the thesis to study not only whether models show gender preference, but also whether the measured preference is stable under controlled benchmark design changes.