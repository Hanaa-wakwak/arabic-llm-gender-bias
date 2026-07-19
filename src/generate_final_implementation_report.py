from pathlib import Path
import pandas as pd


OUTPUT_PATH = Path("docs/occupational_scope/final_implementation_results_report.md")


PATHS = {
    "v2_overall": Path("results/occupational_benchmark_v2_all_models/combined_analysis/overall_by_model.csv"),
    "v2_family": Path("results/occupational_benchmark_v2_all_models/combined_analysis/family_summary.csv"),
    "v2_chi": Path("results/occupational_benchmark_v2_all_models/combined_analysis/chi_square_model_family.csv"),

    "v3_balanced_quality": Path("results/occupational_benchmark_v3_balanced_quality/v3_balanced_quality_issues.csv"),
    "v3_balanced_stereotype_rows": Path("results/occupational_benchmark_v3_balanced_quality/v3_balanced_stereotype_label_counts.csv"),
    "v3_balanced_stereotype_occupations": Path("results/occupational_benchmark_v3_balanced_quality/v3_balanced_stereotype_occupation_counts.csv"),
    "v3_aragpt2": Path("results/occupational_benchmark_v3_balanced_quick_models/analysis_aragpt2_base/summary_overall.csv"),
    "v3_bloom": Path("results/occupational_benchmark_v3_balanced_quick_models/analysis_bloom_560m/summary_overall.csv"),

    "v4_quality": Path("results/occupational_benchmark_v4_template_perturbation_quality/v4_template_perturbation_quality_issues.csv"),
    "v4_overall": Path("results/occupational_benchmark_v4_template_perturbation_all_models/combined_sensitivity_analysis/summary_overall_by_model.csv"),
    "v4_volatility": Path("results/occupational_benchmark_v4_template_perturbation_all_models/combined_sensitivity_analysis/template_volatility_by_model.csv"),
    "v4_dialect": Path("results/occupational_benchmark_v4_template_perturbation_all_models/combined_sensitivity_analysis/dialect_shift_by_model.csv"),
    "v4_chi": Path("results/occupational_benchmark_v4_template_perturbation_all_models/statistical_tests/v4_overall_chi_square_tests.csv"),
    "v4_effect": Path("results/occupational_benchmark_v4_template_perturbation_all_models/effect_sizes/v4_cramers_v_effect_sizes.csv"),
        "v5_aragpt2": Path("results/occupational_benchmark_v5_job_titles_quick_models/analysis_aragpt2_base/summary_overall.csv"),
    "v5_bloom": Path("results/occupational_benchmark_v5_job_titles_quick_models/analysis_bloom_560m/summary_overall.csv"),
    "v4_v5_comparison": Path("results/v4_v5_job_title_comparison/v4_v5_quick_model_comparison.csv"),
}


def read_csv_optional(path):
    if not path.exists():
        return None

    try:
        return pd.read_csv(path, encoding="utf-8-sig")
    except Exception as e:
        print(f"Could not read {path}: {e}")
        return None


def format_number(value):
    if pd.isna(value):
        return ""

    if isinstance(value, float):
        if abs(value) < 0.0001 and value != 0:
            return f"{value:.2e}"
        return f"{value:.4f}"

    return str(value)


def markdown_table(df, max_rows=None, selected_columns=None):
    if df is None:
        return "_File not found or could not be read._"

    if selected_columns:
        existing = [col for col in selected_columns if col in df.columns]
        df = df[existing].copy()

    if max_rows is not None:
        df = df.head(max_rows).copy()

    cols = list(df.columns)
    lines = []

    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join(["---"] * len(cols)) + " |")

    for _, row in df.iterrows():
        values = [format_number(row[col]) for col in cols]
        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = {name: read_csv_optional(path) for name, path in PATHS.items()}

    md = []

    md.append("# Final Implementation Results Report")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append(
        "This report consolidates the main technical outputs of the Arabic occupational "
        "gender-bias evaluation suite."
    )
    md.append("")
    md.append("The final implementation includes:")
    md.append("")
    md.append("1. v2 main validated benchmark,")
    md.append("2. v3 sensitivity benchmarks,")
    md.append("3. v3 balanced benchmark,")
    md.append("4. v4 template perturbation benchmark,")
    md.append("5. statistical tests,")
    md.append("6. effect-size analysis.")
    md.append("")

    md.append("## v2 Main Validated Benchmark")
    md.append("")
    md.append("The v2 benchmark remains the main validated benchmark.")
    md.append("")
    md.append("### v2 Overall by Model")
    md.append("")
    md.append(markdown_table(data["v2_overall"]))
    md.append("")

    md.append("### v2 Model-Family Summary")
    md.append("")
    md.append(markdown_table(data["v2_family"]))
    md.append("")

    md.append("### v2 Chi-Square Test")
    md.append("")
    md.append(markdown_table(data["v2_chi"]))
    md.append("")

    md.append("## v3 Balanced Sensitivity Benchmark")
    md.append("")
    md.append(
        "The v3 balanced benchmark was created to test whether stereotype balancing "
        "stabilizes the measured bias direction."
    )
    md.append("")
    md.append("### Quality Check")
    md.append("")
    md.append(markdown_table(data["v3_balanced_quality"]))
    md.append("")

    md.append("### Stereotype Row Counts")
    md.append("")
    md.append(markdown_table(data["v3_balanced_stereotype_rows"]))
    md.append("")

    md.append("### Stereotype Occupation Counts")
    md.append("")
    md.append(markdown_table(data["v3_balanced_stereotype_occupations"]))
    md.append("")

    md.append("### v3 Balanced Quick Model Results")
    md.append("")
    md.append("AraGPT2-base:")
    md.append("")
    md.append(markdown_table(data["v3_aragpt2"]))
    md.append("")
    md.append("BLOOM-560m:")
    md.append("")
    md.append(markdown_table(data["v3_bloom"]))
    md.append("")

    md.append("## v4 Template Perturbation Benchmark")
    md.append("")
    md.append(
        "The v4 benchmark tests template, semantic-frame, and dialect sensitivity "
        "using 90 balanced occupations and 8 templates."
    )
    md.append("")
    md.append("### Quality Check")
    md.append("")
    md.append(markdown_table(data["v4_quality"]))
    md.append("")

    md.append("### v4 Overall by Model")
    md.append("")
    md.append(markdown_table(
        data["v4_overall"],
        selected_columns=[
            "model_name",
            "total_items",
            "masculine_preferred_count",
            "feminine_preferred_count",
            "equal_count",
            "average_score_difference",
            "average_direction",
        ],
    ))
    md.append("")

    md.append("### v4 Template Volatility by Model")
    md.append("")
    md.append(markdown_table(
        data["v4_volatility"],
        selected_columns=[
            "model_name",
            "num_templates",
            "masculine_direction_templates",
            "feminine_direction_templates",
            "direction_flip_present",
            "template_volatility_range",
            "most_masculine_template",
            "most_feminine_template",
        ],
    ))
    md.append("")

    md.append("### v4 Dialect Shift")
    md.append("")
    md.append(markdown_table(data["v4_dialect"]))
    md.append("")

    md.append("### v4 Chi-Square Tests")
    md.append("")
    md.append(markdown_table(data["v4_chi"]))
    md.append("")

    md.append("### v4 Effect Sizes")
    md.append("")
    md.append(markdown_table(data["v4_effect"]))
    md.append("")

    md.append("## Final Technical Conclusion")
    md.append("")
    md.append(
        "The final implementation shows that Arabic occupational gender-bias evaluation "
        "is both model-dependent and benchmark-design-dependent."
    )
    md.append("")
    md.append(
        "The v2 benchmark provides the main validated model-family result. "
        "The v3 and v3 balanced benchmarks demonstrate sensitivity to occupation "
        "coverage and lexical formulation. The v4 benchmark demonstrates that template "
        "formulation, semantic frame, and dialect can significantly affect measured "
        "gender preference."
    )
    md.append("")
    md.append(
        "The strongest practical factor in v4 was template ID, based on Cramér's V effect-size analysis."
    )
    md.append("")
    md.append("## v5 Job-Title Benchmark")
    md.append("")
    md.append(
        "The v5 benchmark isolates occupations as explicit job titles in CV, job advertisement, "
        "HR record, and professional profile contexts."
    )
    md.append("")
    md.append("### AraGPT2-base v5 Result")
    md.append("")
    md.append(markdown_table(data["v5_aragpt2"]))
    md.append("")
    md.append("### BLOOM-560m v5 Result")
    md.append("")
    md.append(markdown_table(data["v5_bloom"]))
    md.append("")
    md.append("### v4-v5 Context Comparison")
    md.append("")
    md.append(markdown_table(data["v4_v5_comparison"]))
    md.append("")
    md.append(
        "The v5 results show that explicit job-title contexts can behave differently from "
        "broader occupational sentence templates. This further supports the claim that "
        "Arabic occupational gender-bias measurement is benchmark-design-dependent."
    )
    md.append("")

    OUTPUT_PATH.write_text("\n".join(md), encoding="utf-8")

    print("Final implementation report generated.")
    print("Output:", OUTPUT_PATH)


if __name__ == "__main__":
    main()