from pathlib import Path
import pandas as pd


OUTPUT_DIR = Path("results/final_package")
OUTPUT_CSV = OUTPUT_DIR / "final_artifact_registry.csv"
OUTPUT_MD = Path("docs/occupational_scope/final_artifact_registry.md")


ARTIFACTS = [
    # Data benchmarks
    ("data", "v2 main benchmark", "data/occupational_benchmark/occupational_bias_v2.csv"),
    ("data", "v3 experimental benchmark", "data/occupational_benchmark/occupational_bias_v3.csv"),
    ("data", "v3 controlled benchmark", "data/occupational_benchmark/occupational_bias_v3_controlled.csv"),
    ("data", "v3 balanced lexicon", "data/occupational_benchmark/occupations_fields_v3_balanced.csv"),
    ("data", "v3 balanced benchmark", "data/occupational_benchmark/occupational_bias_v3_balanced.csv"),
    ("data", "v4 template perturbation benchmark", "data/occupational_benchmark/occupational_bias_v4_template_perturbation.csv"),

    # Quality
    ("quality", "v2 quality summary", "results/occupational_benchmark_quality/occupational_bias_v2_quality_summary.csv"),
    ("quality", "v3 quality summary", "results/occupational_benchmark_v3_quality/occupational_bias_v3_quality_summary.csv"),
    ("quality", "v3 balanced quality issues", "results/occupational_benchmark_v3_balanced_quality/v3_balanced_quality_issues.csv"),
    ("quality", "v4 quality issues", "results/occupational_benchmark_v4_template_perturbation_quality/v4_template_perturbation_quality_issues.csv"),

    # v2 final results
    ("result", "v2 overall by model", "results/occupational_benchmark_v2_all_models/combined_analysis/overall_by_model.csv"),
    ("result", "v2 family summary", "results/occupational_benchmark_v2_all_models/combined_analysis/family_summary.csv"),
    ("result", "v2 chi-square test", "results/occupational_benchmark_v2_all_models/combined_analysis/chi_square_model_family.csv"),

    # v3 sensitivity
    ("result", "v3 balanced AraGPT2-base overall", "results/occupational_benchmark_v3_balanced_quick_models/analysis_aragpt2_base/summary_overall.csv"),
    ("result", "v3 balanced BLOOM-560m overall", "results/occupational_benchmark_v3_balanced_quick_models/analysis_bloom_560m/summary_overall.csv"),

    # v4 final results
    ("result", "v4 all-model overall", "results/occupational_benchmark_v4_template_perturbation_all_models/combined_sensitivity_analysis/summary_overall_by_model.csv"),
    ("result", "v4 template volatility", "results/occupational_benchmark_v4_template_perturbation_all_models/combined_sensitivity_analysis/template_volatility_by_model.csv"),
    ("result", "v4 dialect shift", "results/occupational_benchmark_v4_template_perturbation_all_models/combined_sensitivity_analysis/dialect_shift_by_model.csv"),
    ("result", "v4 semantic frame summary", "results/occupational_benchmark_v4_template_perturbation_all_models/combined_sensitivity_analysis/summary_by_model_semantic_frame.csv"),
    ("result", "v4 chi-square tests", "results/occupational_benchmark_v4_template_perturbation_all_models/statistical_tests/v4_overall_chi_square_tests.csv"),
    ("result", "v4 Cramér's V effect sizes", "results/occupational_benchmark_v4_template_perturbation_all_models/effect_sizes/v4_cramers_v_effect_sizes.csv"),

    # External pilots
    ("external", "APGC pilot summary", "docs/occupational_scope/apgc_pilot_external_dataset_summary.md"),
    ("external", "ArGAN final enrichment summary", "docs/occupational_scope/final_external_dataset_enrichment_summary.md"),

    # Docs
    ("doc", "Chapter 3 methodology draft", "docs/occupational_scope/chapter_3_methodology_draft.md"),
    ("doc", "Chapter 4 results draft", "docs/occupational_scope/chapter_4_results_draft.md"),
    ("doc", "Chapter 5 discussion draft", "docs/occupational_scope/chapter_5_discussion_draft.md"),
    ("doc", "Chapter 6 conclusion draft", "docs/occupational_scope/chapter_6_conclusion_future_work_draft.md"),
    ("doc", "Final contribution statement", "docs/occupational_scope/final_contribution_statement.md"),
    ("doc", "Final technical contribution table", "docs/occupational_scope/final_technical_contribution_table.md"),
    ("doc", "Doctor explanation script", "docs/occupational_scope/doctor_explanation_script.md"),
    ("doc", "Final viva questions and answers", "docs/occupational_scope/final_viva_questions_and_answers.md"),
]


def count_rows_if_csv(path):
    if not path.exists() or path.suffix.lower() != ".csv":
        return None

    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
        return len(df)
    except Exception:
        return None


def count_columns_if_csv(path):
    if not path.exists() or path.suffix.lower() != ".csv":
        return None

    try:
        df = pd.read_csv(path, encoding="utf-8-sig", nrows=1)
        return len(df.columns)
    except Exception:
        return None


def markdown_table(df):
    cols = list(df.columns)
    lines = []

    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join(["---"] * len(cols)) + " |")

    for _, row in df.iterrows():
        values = []
        for col in cols:
            value = row[col]
            if pd.isna(value):
                value = ""
            values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for artifact_type, description, raw_path in ARTIFACTS:
        path = Path(raw_path)
        exists = path.exists()

        rows.append({
            "artifact_type": artifact_type,
            "description": description,
            "path": raw_path,
            "exists": exists,
            "rows_if_csv": count_rows_if_csv(path),
            "columns_if_csv": count_columns_if_csv(path),
        })

    registry_df = pd.DataFrame(rows)

    registry_df.to_csv(
        OUTPUT_CSV,
        index=False,
        encoding="utf-8-sig",
    )

    missing_df = registry_df[registry_df["exists"] == False].copy()

    md = []
    md.append("# Final Artifact Registry")
    md.append("")
    md.append("This file lists the main implementation artifacts generated by the thesis project.")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append(f"- Total artifacts tracked: {len(registry_df)}")
    md.append(f"- Existing artifacts: {int(registry_df['exists'].sum())}")
    md.append(f"- Missing artifacts: {len(missing_df)}")
    md.append("")
    md.append("## Artifact Table")
    md.append("")
    md.append(markdown_table(registry_df))
    md.append("")

    if len(missing_df) > 0:
        md.append("## Missing Artifacts")
        md.append("")
        md.append(markdown_table(missing_df))
        md.append("")
    else:
        md.append("## Missing Artifacts")
        md.append("")
        md.append("No missing tracked artifacts.")
        md.append("")

    OUTPUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("Final artifact registry created.")
    print("CSV:", OUTPUT_CSV)
    print("Markdown:", OUTPUT_MD)
    print("Tracked artifacts:", len(registry_df))
    print("Missing artifacts:", len(missing_df))

    if len(missing_df) > 0:
        print("\nMissing:")
        print(missing_df[["artifact_type", "description", "path"]].to_string(index=False))


if __name__ == "__main__":
    main()