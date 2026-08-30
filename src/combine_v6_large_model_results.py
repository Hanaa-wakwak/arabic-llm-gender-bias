from pathlib import Path
import pandas as pd


BASE_DIR = Path("results/occupational_benchmark_v6_job_roles_large_all_models")
OUTPUT_DIR = BASE_DIR / "combined_analysis"
OUTPUT_PATH = OUTPUT_DIR / "v6_overall_by_model.csv"
DOC_PATH = Path("docs/occupational_scope/v6_large_all_models_result_summary.md")


def classify_direction(avg_score):
    if avg_score > 0.05:
        return "masculine"
    if avg_score < -0.05:
        return "feminine"
    return "near_neutral_or_mixed"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    summary_files = list(BASE_DIR.glob("analysis_*/summary_overall.csv"))

    if not summary_files:
        raise RuntimeError("No summary_overall.csv files found under analysis folders.")

    frames = []

    for path in summary_files:
        print(f"Reading: {path}")
        df = pd.read_csv(path, encoding="utf-8-sig")
        df["source_file"] = str(path)
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)

    combined["v6_direction"] = combined["average_score_difference"].apply(classify_direction)

    combined = combined.sort_values("model_name")
    combined.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    doc = []
    doc.append("# v6 Large Job Roles Benchmark — All Models Result Summary")
    doc.append("")
    doc.append("## Dataset")
    doc.append("")
    doc.append("- Benchmark: v6 expanded job roles and departments")
    doc.append("- Total pairs per completed model: 2,880")
    doc.append("- Structure: 120 job roles × 24 templates")
    doc.append("- Dialects: MSA and Egyptian Arabic")
    doc.append("")
    doc.append("## Overall Results")
    doc.append("")

    for _, row in combined.iterrows():
        doc.append(f"### {row['model_name']}")
        doc.append("")
        doc.append(f"- Total items: {row['total_items']}")
        doc.append(f"- Masculine preferred: {row['masculine_preferred_count']} ({row['masculine_preferred_percent']}%)")
        doc.append(f"- Feminine preferred: {row['feminine_preferred_count']} ({row['feminine_preferred_percent']}%)")
        doc.append(f"- Equal: {row['equal_count']} ({row['equal_percent']}%)")
        doc.append(f"- Average score difference: {row['average_score_difference']}")
        doc.append(f"- Median score difference: {row['median_score_difference']}")
        doc.append(f"- Direction: {row['v6_direction']}")
        doc.append("")

    doc.append("## Interpretation")
    doc.append("")
    doc.append(
        "The v6 benchmark evaluates Arabic occupational gender preference across expanded "
        "job-role, department, workplace, seniority, and job-title contexts. Negative average "
        "score differences indicate higher likelihood for feminine variants, while positive "
        "values indicate higher likelihood for masculine variants."
    )
    doc.append("")
    doc.append("## Note")
    doc.append("")
    doc.append(
        "Only models with completed analysis folders are included in this combined summary. "
        "If a model did not generate a scoring CSV, it is skipped automatically."
    )

    DOC_PATH.write_text("\n".join(doc), encoding="utf-8")

    print("")
    print("Combined v6 summary created successfully.")
    print("CSV:", OUTPUT_PATH)
    print("DOC:", DOC_PATH)
    print("")
    print(combined.to_string(index=False))


if __name__ == "__main__":
    main()