from pathlib import Path
import pandas as pd


OUTPUT_DIR = Path("results/final_package")
OUTPUT_CSV = OUTPUT_DIR / "claim_evidence_traceability_matrix.csv"
OUTPUT_MD = Path("docs/occupational_scope/claim_evidence_traceability_matrix.md")


CLAIMS = [
    {
        "claim_id": "CL1",
        "claim": "v2 is the main validated benchmark.",
        "evidence": "v2 contains 60 occupations, 4 templates, and 240 sentence pairs with quality checks passed.",
        "evidence_file": "data/occupational_benchmark/occupational_bias_v2.csv",
        "supporting_result": "results/occupational_benchmark_quality/occupational_bias_v2_quality_summary.csv",
        "claim_type": "benchmark_design",
    },
    {
        "claim_id": "CL2",
        "claim": "Arabic-specific and non-Arabic-specific models show different preference patterns in v2.",
        "evidence": "v2 six-model combined analysis and model-family summary.",
        "evidence_file": "results/occupational_benchmark_v2_all_models/combined_analysis/overall_by_model.csv",
        "supporting_result": "results/occupational_benchmark_v2_all_models/combined_analysis/family_summary.csv",
        "claim_type": "empirical_result",
    },
    {
        "claim_id": "CL3",
        "claim": "The v2 model-family pattern is statistically significant.",
        "evidence": "Chi-square test on model family versus preferred gender.",
        "evidence_file": "results/occupational_benchmark_v2_all_models/combined_analysis/chi_square_model_family.csv",
        "supporting_result": "results/occupational_benchmark_v2_all_models/combined_analysis/chi_square_model_family.csv",
        "claim_type": "statistical_result",
    },
    {
        "claim_id": "CL4",
        "claim": "Benchmark expansion can change measured bias direction.",
        "evidence": "v3 and v3 controlled sensitivity results show direction changes compared with v2.",
        "evidence_file": "data/occupational_benchmark/occupational_bias_v3.csv",
        "supporting_result": "docs/occupational_scope/v3_sensitivity_analysis_summary.md",
        "claim_type": "sensitivity_result",
    },
    {
        "claim_id": "CL5",
        "claim": "Stereotype balancing alone does not guarantee stable bias direction.",
        "evidence": "v3 balanced benchmark results remain different from the v2 direction for quick models.",
        "evidence_file": "data/occupational_benchmark/occupational_bias_v3_balanced.csv",
        "supporting_result": "docs/occupational_scope/v3_balanced_final_result_summary.md",
        "claim_type": "robustness_result",
    },
    {
        "claim_id": "CL6",
        "claim": "Template formulation can cause direction flips.",
        "evidence": "v4 template volatility analysis shows direction_flip_present=True for all six models.",
        "evidence_file": "results/occupational_benchmark_v4_template_perturbation_all_models/combined_sensitivity_analysis/template_volatility_by_model.csv",
        "supporting_result": "docs/occupational_scope/v4_all_models_final_result_summary.md",
        "claim_type": "robustness_result",
    },
    {
        "claim_id": "CL7",
        "claim": "Dialect affects measured gender preference.",
        "evidence": "v4 dialect-shift analysis compares MSA and Egyptian Arabic directions.",
        "evidence_file": "results/occupational_benchmark_v4_template_perturbation_all_models/combined_sensitivity_analysis/dialect_shift_by_model.csv",
        "supporting_result": "docs/occupational_scope/v4_all_models_final_result_summary.md",
        "claim_type": "dialect_result",
    },
    {
        "claim_id": "CL8",
        "claim": "Template ID has the strongest practical effect in v4.",
        "evidence": "Cramér’s V effect-size analysis ranks template_id as the strongest effect.",
        "evidence_file": "results/occupational_benchmark_v4_template_perturbation_all_models/effect_sizes/v4_cramers_v_effect_sizes.csv",
        "supporting_result": "docs/occupational_scope/v4_effect_size_analysis_summary.md",
        "claim_type": "effect_size_result",
    },
    {
        "claim_id": "CL9",
        "claim": "Stereotype label is not significant after balancing in v4.",
        "evidence": "v4 chi-square tests show stereotype_label is not statistically significant.",
        "evidence_file": "results/occupational_benchmark_v4_template_perturbation_all_models/statistical_tests/v4_overall_chi_square_tests.csv",
        "supporting_result": "results/occupational_benchmark_v4_template_perturbation_all_models/effect_sizes/v4_cramers_v_effect_sizes.csv",
        "claim_type": "statistical_result",
    },
    {
        "claim_id": "CL10",
        "claim": "Explicit job-title contexts behave differently from broader occupational templates.",
        "evidence": "v5 job-title benchmark and v4-v5 comparison show near-balanced or weak masculine results for quick models.",
        "evidence_file": "data/occupational_benchmark/occupational_bias_v5_job_titles.csv",
        "supporting_result": "docs/occupational_scope/v4_v5_job_title_context_comparison.md",
        "claim_type": "context_result",
    },
    {
        "claim_id": "CL11",
        "claim": "Arabic occupational bias measurement is context-sensitive.",
        "evidence": "Context Sensitivity Index combines template volatility, dialect shift, and v4-to-v5 job-title context shift.",
        "evidence_file": "results/final_package/context_sensitivity_index_quick_models.csv",
        "supporting_result": "docs/occupational_scope/context_sensitivity_index_summary.md",
        "claim_type": "methodological_result",
    },
    {
        "claim_id": "CL12",
        "claim": "The benchmark suite includes quality-control layers.",
        "evidence": "Counterfactual pair integrity audit, benchmark quality checks, artifact registry, and completeness checks.",
        "evidence_file": "results/final_package/counterfactual_pair_integrity_summary.csv",
        "supporting_result": "docs/occupational_scope/counterfactual_pair_integrity_audit.md",
        "claim_type": "quality_control",
    },
    {
        "claim_id": "CL13",
        "claim": "The thesis contribution is a framework, not only a dataset.",
        "evidence": "Benchmark design taxonomy, reporting checklist, technical contribution matrix, and datasheet.",
        "evidence_file": "docs/occupational_scope/benchmark_design_taxonomy.md",
        "supporting_result": "docs/occupational_scope/final_technical_contribution_matrix.md",
        "claim_type": "contribution_claim",
    },
]


def markdown_table(df):
    cols = list(df.columns)
    lines = []
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join(["---"] * len(cols)) + " |")

    for _, row in df.iterrows():
        values = []
        for col in cols:
            value = str(row[col]).replace("\n", " ").replace("|", "/")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(CLAIMS)

    df["evidence_file_exists"] = df["evidence_file"].apply(lambda p: Path(p).exists())
    df["supporting_result_exists"] = df["supporting_result"].apply(lambda p: Path(p).exists())

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    md = []
    md.append("# Claim-to-Evidence Traceability Matrix")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append(
        "This matrix maps the main thesis claims to the files and outputs that support them."
    )
    md.append("")
    md.append(
        "It improves defense readiness by making each major claim traceable to benchmark data, "
        "result files, statistical outputs, or documentation."
    )
    md.append("")
    md.append("## Matrix")
    md.append("")
    md.append(markdown_table(df))
    md.append("")
    md.append("## Contribution")
    md.append("")
    md.append(
        "This traceability matrix strengthens the thesis package because it links claims, "
        "implementation artifacts, and empirical evidence in a transparent way."
    )
    md.append("")

    OUTPUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("Claim-to-evidence traceability matrix generated.")
    print("CSV:", OUTPUT_CSV)
    print("Markdown:", OUTPUT_MD)
    print("")
    print(df[["claim_id", "claim_type", "evidence_file_exists", "supporting_result_exists"]].to_string(index=False))


if __name__ == "__main__":
    main()