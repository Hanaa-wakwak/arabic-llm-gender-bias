from pathlib import Path
import pandas as pd


OUTPUT_DIR = Path("results/v4_v5_job_title_comparison")
OUTPUT_CSV = OUTPUT_DIR / "v4_v5_quick_model_comparison.csv"
OUTPUT_MD = Path("docs/occupational_scope/v4_v5_job_title_context_comparison.md")


FILES = {
    "v4_aragpt2_base": Path(
        "results/occupational_benchmark_v4_template_perturbation_quick_models/"
        "analysis_aragpt2_base/summary_overall.csv"
    ),
    "v4_bloom_560m": Path(
        "results/occupational_benchmark_v4_template_perturbation_quick_models/"
        "analysis_bloom_560m/summary_overall.csv"
    ),
    "v5_aragpt2_base": Path(
        "results/occupational_benchmark_v5_job_titles_quick_models/"
        "analysis_aragpt2_base/summary_overall.csv"
    ),
    "v5_bloom_560m": Path(
        "results/occupational_benchmark_v5_job_titles_quick_models/"
        "analysis_bloom_560m/summary_overall.csv"
    ),
}


def read_summary(path):
    if not path.exists():
        print(f"Missing file: {path}")
        return None

    return pd.read_csv(path, encoding="utf-8-sig")


def direction_from_average(avg):
    if avg > 0:
        return "masculine"
    if avg < 0:
        return "feminine"
    return "equal"


def direction_from_counts(row):
    m = row["masculine_preferred_count"]
    f = row["feminine_preferred_count"]

    if m > f:
        return "masculine"
    if f > m:
        return "feminine"
    return "equal"


def add_version_rows(rows, version_label, benchmark_role, df):
    if df is None:
        return

    for _, row in df.iterrows():
        avg = float(row["average_score_difference"])
        rows.append({
            "benchmark": version_label,
            "benchmark_role": benchmark_role,
            "model_name": row["model_name"],
            "total_items": int(row["total_items"]),
            "masculine_preferred_count": int(row["masculine_preferred_count"]),
            "feminine_preferred_count": int(row["feminine_preferred_count"]),
            "equal_count": int(row["equal_count"]),
            "masculine_preferred_percent": float(row["masculine_preferred_percent"]),
            "feminine_preferred_percent": float(row["feminine_preferred_percent"]),
            "average_score_difference": avg,
            "median_score_difference": float(row["median_score_difference"]),
            "direction_by_average": direction_from_average(avg),
            "direction_by_count": direction_from_counts(row),
        })


def markdown_table(df):
    cols = list(df.columns)
    lines = []
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join(["---"] * len(cols)) + " |")

    for _, row in df.iterrows():
        values = []
        for col in cols:
            value = row[col]
            if isinstance(value, float):
                value = f"{value:.4f}"
            values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)

    v4_aragpt2 = read_summary(FILES["v4_aragpt2_base"])
    v4_bloom = read_summary(FILES["v4_bloom_560m"])
    v5_aragpt2 = read_summary(FILES["v5_aragpt2_base"])
    v5_bloom = read_summary(FILES["v5_bloom_560m"])

    rows = []

    add_version_rows(
        rows,
        "v4",
        "template_perturbation_broader_sentence_contexts",
        v4_aragpt2,
    )
    add_version_rows(
        rows,
        "v4",
        "template_perturbation_broader_sentence_contexts",
        v4_bloom,
    )
    add_version_rows(
        rows,
        "v5",
        "explicit_job_title_context",
        v5_aragpt2,
    )
    add_version_rows(
        rows,
        "v5",
        "explicit_job_title_context",
        v5_bloom,
    )

    comparison_df = pd.DataFrame(rows)

    if comparison_df.empty:
        raise ValueError("No comparison rows created. Check input summary files.")

    comparison_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    pivot_df = comparison_df[[
        "benchmark",
        "model_name",
        "total_items",
        "masculine_preferred_count",
        "feminine_preferred_count",
        "equal_count",
        "average_score_difference",
        "median_score_difference",
        "direction_by_average",
        "direction_by_count",
    ]].copy()

    md = []

    md.append("# v4 vs v5 Job-Title Context Comparison")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append(
        "This comparison tests whether explicit job-title contexts behave differently "
        "from broader occupational sentence templates."
    )
    md.append("")
    md.append("v4 evaluates occupations inside broader semantic frames such as workplace presence, "
              "experience, competence, leadership, achievement, and responsibility.")
    md.append("")
    md.append("v5 isolates the occupation as an explicit job title in CV, job advertisement, "
              "HR record, and professional profile contexts.")
    md.append("")
    md.append("## Comparison Table")
    md.append("")
    md.append(markdown_table(pivot_df))
    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append(
        "The v5 benchmark shows that explicit job-title contexts can produce weaker "
        "or different gender-preference directions compared with broader v4 sentence contexts."
    )
    md.append("")
    md.append(
        "AraGPT2-base is near-balanced in v5, while BLOOM-560m shows weak masculine preference. "
        "This contrasts with the broader v4 setting, where both models showed overall feminine preference."
    )
    md.append("")
    md.append("## Thesis Relevance")
    md.append("")
    md.append(
        "This comparison strengthens the thesis claim that Arabic occupational gender-bias "
        "measurement is benchmark-design-dependent. The measured direction can change when "
        "the occupation is presented as a direct job title rather than embedded in a broader "
        "occupational sentence frame."
    )
    md.append("")

    OUTPUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("v4-v5 job-title context comparison created.")
    print("CSV:", OUTPUT_CSV)
    print("Markdown:", OUTPUT_MD)
    print("")
    print(pivot_df.to_string(index=False))


if __name__ == "__main__":
    main()