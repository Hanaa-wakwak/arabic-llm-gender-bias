from pathlib import Path
import pandas as pd


OUTPUT_DIR = Path("results/final_package")
OUTPUT_CSV = OUTPUT_DIR / "final_technical_contribution_matrix.csv"
OUTPUT_MD = Path("docs/occupational_scope/final_technical_contribution_matrix.md")


CONTRIBUTIONS = [
    {
        "id": "C1",
        "technical_contribution": "v2 main validated benchmark",
        "description": "A controlled Arabic occupational gender-bias benchmark with 60 occupations, 4 templates, and 240 masculine-feminine sentence pairs.",
        "evidence_file": "data/occupational_benchmark/occupational_bias_v2.csv",
        "result_file": "results/occupational_benchmark_v2_all_models/combined_analysis/overall_by_model.csv",
        "thesis_value": "Provides the main validated empirical benchmark.",
    },
    {
        "id": "C2",
        "technical_contribution": "Six-model causal LM evaluation",
        "description": "Evaluation of Arabic-specific and non-Arabic-specific causal language models using likelihood-based paired-sentence scoring.",
        "evidence_file": "results/occupational_benchmark_v2_all_models/combined_analysis/overall_by_model.csv",
        "result_file": "results/occupational_benchmark_v2_all_models/combined_analysis/family_summary.csv",
        "thesis_value": "Shows model-family differences in measured occupational gender preference.",
    },
    {
        "id": "C3",
        "technical_contribution": "v3 expansion sensitivity benchmark",
        "description": "Expanded benchmark testing whether measured bias remains stable after increasing occupations and templates.",
        "evidence_file": "data/occupational_benchmark/occupational_bias_v3.csv",
        "result_file": "results/occupational_benchmark_v3_quick_models",
        "thesis_value": "Shows benchmark expansion can change measured bias direction.",
    },
    {
        "id": "C4",
        "technical_contribution": "v3 controlled diagnostic benchmark",
        "description": "Diagnostic benchmark using expanded occupations with original v2-style templates.",
        "evidence_file": "data/occupational_benchmark/occupational_bias_v3_controlled.csv",
        "result_file": "results/occupational_benchmark_v3_controlled_quick_models",
        "thesis_value": "Separates occupation expansion effects from template expansion effects.",
    },
    {
        "id": "C5",
        "technical_contribution": "v3 balanced stereotype-balanced benchmark",
        "description": "Balanced benchmark with 90 occupations: 30 male-stereotyped, 30 female-stereotyped, and 30 neutral occupations.",
        "evidence_file": "data/occupational_benchmark/occupational_bias_v3_balanced.csv",
        "result_file": "results/occupational_benchmark_v3_balanced_quick_models",
        "thesis_value": "Tests whether stereotype balancing stabilizes measured bias direction.",
    },
    {
        "id": "C6",
        "technical_contribution": "v4 template perturbation benchmark",
        "description": "A template-perturbation benchmark with 90 balanced occupations, 8 templates, 6 semantic frames, 2 dialects, and 720 sentence pairs.",
        "evidence_file": "data/occupational_benchmark/occupational_bias_v4_template_perturbation.csv",
        "result_file": "results/occupational_benchmark_v4_template_perturbation_all_models",
        "thesis_value": "Tests template, semantic-frame, and dialect sensitivity.",
    },
    {
        "id": "C7",
        "technical_contribution": "Template-Induced Bias Direction Volatility",
        "description": "A model-level diagnostic showing whether bias direction flips across templates.",
        "evidence_file": "results/occupational_benchmark_v4_template_perturbation_all_models/combined_sensitivity_analysis/template_volatility_by_model.csv",
        "result_file": "results/occupational_benchmark_v4_template_perturbation_all_models/combined_sensitivity_analysis/template_volatility_by_model.csv",
        "thesis_value": "Shows all tested models can change gender-preference direction across templates.",
    },
    {
        "id": "C8",
        "technical_contribution": "Dialect sensitivity analysis",
        "description": "Comparison of MSA and Egyptian Arabic contexts across models.",
        "evidence_file": "results/occupational_benchmark_v4_template_perturbation_all_models/combined_sensitivity_analysis/dialect_shift_by_model.csv",
        "result_file": "results/occupational_benchmark_v4_template_perturbation_all_models/combined_sensitivity_analysis/dialect_shift_by_model.csv",
        "thesis_value": "Shows Arabic bias measurement can differ by dialect.",
    },
    {
        "id": "C9",
        "technical_contribution": "Statistical testing and effect-size analysis",
        "description": "Chi-square tests and Cramér’s V effect sizes for model, model family, template, semantic frame, dialect, field, and stereotype label.",
        "evidence_file": "results/occupational_benchmark_v4_template_perturbation_all_models/statistical_tests/v4_overall_chi_square_tests.csv",
        "result_file": "results/occupational_benchmark_v4_template_perturbation_all_models/effect_sizes/v4_cramers_v_effect_sizes.csv",
        "thesis_value": "Shows template ID has the strongest practical effect in v4.",
    },
    {
        "id": "C10",
        "technical_contribution": "External dataset pilot integration",
        "description": "APGC and ArGAN pilot experiments for external Arabic gender-bias dataset enrichment.",
        "evidence_file": "data/external_datasets",
        "result_file": "results/external_datasets",
        "thesis_value": "Shows extensibility beyond the manually constructed benchmark.",
    },
    {
        "id": "C11",
        "technical_contribution": "v5 job-title-specific benchmark",
        "description": "A job-title-specific benchmark with 90 balanced occupations, 6 templates, 2 dialects, and 540 sentence pairs.",
        "evidence_file": "data/occupational_benchmark/occupational_bias_v5_job_titles.csv",
        "result_file": "results/occupational_benchmark_v5_job_titles_quick_models",
        "thesis_value": "Separates explicit job-title preference from broader occupational sentence-context preference.",
    },
    {
        "id": "C12",
        "technical_contribution": "v4-v5 context comparison",
        "description": "Comparison between broader v4 occupational sentence contexts and explicit v5 job-title contexts.",
        "evidence_file": "results/v4_v5_job_title_comparison/v4_v5_quick_model_comparison.csv",
        "result_file": "docs/occupational_scope/v4_v5_job_title_context_comparison.md",
        "thesis_value": "Strengthens the claim that measured bias changes with benchmark context.",
    },
        {
        "id": "C17",
        "technical_contribution": "Counterfactual pair integrity audit",
        "description": "A benchmark-wide audit checking whether masculine and feminine sentence pairs are structurally comparable in character length, word count, occupation presence, and identical-pair errors.",
        "evidence_file": "results/final_package/counterfactual_pair_integrity_summary.csv",
        "result_file": "docs/occupational_scope/counterfactual_pair_integrity_audit.md",
        "thesis_value": "Adds a quality-control layer validating the counterfactual paired-sentence design.",
    },
        {
        "id": "C18",
        "technical_contribution": "Benchmark datasheet",
        "description": "A structured benchmark datasheet documenting the purpose, construction, intended use, limitations, scoring method, quality controls, and ethical considerations of the Arabic occupational gender-bias evaluation suite.",
        "evidence_file": "docs/occupational_scope/benchmark_datasheet.md",
        "result_file": "docs/occupational_scope/benchmark_datasheet.md",
        "thesis_value": "Improves transparency, reproducibility, and responsible benchmark documentation.",
    },
        {
        "id": "C19",
        "technical_contribution": "Threats to validity and mitigation map",
        "description": "A structured validity analysis identifying construct, internal, external, statistical, reliability, and reproducibility threats, with the mitigation layer used for each.",
        "evidence_file": "docs/occupational_scope/threats_to_validity_and_mitigation_map.md",
        "result_file": "docs/occupational_scope/threats_to_validity_and_mitigation_map.md",
        "thesis_value": "Strengthens methodological rigor by explicitly linking limitations to mitigation strategies.",
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
            value = str(row[col]).replace("\n", " ")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(CONTRIBUTIONS)

    df["evidence_exists"] = df["evidence_file"].apply(lambda p: Path(p).exists())
    df["result_exists"] = df["result_file"].apply(lambda p: Path(p).exists())

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    md = []
    md.append("# Final Technical Contribution Matrix")
    md.append("")
    md.append("This matrix summarizes the main technical contributions of the thesis implementation.")
    md.append("")
    md.append("## Contribution Summary")
    md.append("")
    md.append(f"- Total technical contributions: {len(df)}")
    md.append(f"- Contributions with evidence files present: {int(df['evidence_exists'].sum())}")
    md.append(f"- Contributions with result files present: {int(df['result_exists'].sum())}")
    md.append("")
    md.append("## Matrix")
    md.append("")
    md.append(markdown_table(df))
    md.append("")
    md.append("## Final Technical Claim")
    md.append("")
    md.append(
        "The thesis contributes a robustness-oriented Arabic occupational gender-bias "
        "evaluation suite. It does not only measure model-level bias; it also evaluates "
        "whether the measurement remains stable across occupation coverage, templates, "
        "semantic frames, dialects, stereotype balancing, and explicit job-title contexts."
    )
    md.append("")

    OUTPUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("Final technical contribution matrix generated.")
    print("CSV:", OUTPUT_CSV)
    print("Markdown:", OUTPUT_MD)
    print("")
    print(df[["id", "technical_contribution", "evidence_exists", "result_exists"]].to_string(index=False))


if __name__ == "__main__":
    main()