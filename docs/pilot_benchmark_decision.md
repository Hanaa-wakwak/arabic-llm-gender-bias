# Pilot Benchmark Decision

## Selected Pilot Version

The selected stable pilot benchmark is:

minimal_pairs_v04.csv

## Reason

Benchmark v0.4 provides the best balance between overall gender preference, dialect-level stability, and template-level quality.

## Version Comparison Summary

v0.3 introduced concept_id and template_id metadata and improved the analysis pipeline, but it still showed a dialect-level difference between Egyptian and MSA.

v0.4 reduced the dialect gap substantially. Egyptian and MSA subsets produced almost identical average score differences, indicating that template-driven effects were better controlled.

v0.5 tested automatic cleaning and rewriting based on manual review suggestions. Although it improved some concepts, it introduced a new masculine preference in the Egyptian occupation said-role template. Therefore, v0.5 is treated as a cleaning ablation rather than the selected baseline.

## Final Decision

Use v0.4 as the stable pilot benchmark.

Use v0.5 as evidence that automatic rewriting must be validated carefully because it can introduce new template effects.

## Next Step

The next stage is to expand v0.4 carefully by adding more concepts and more controlled templates, while keeping concept_id and template_id metadata for quality control.