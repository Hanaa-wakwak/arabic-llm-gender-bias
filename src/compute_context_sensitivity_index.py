from pathlib import Path
import pandas as pd


OUTPUT_DIR = Path("results/final_package")
OUTPUT_CSV = OUTPUT_DIR / "context_sensitivity_index_quick_models.csv"
OUTPUT_MD = Path("docs/occupational_scope/context_sensitivity_index_summary.md")


V4_OVERALL_PATH = Path(
    "results/occupational_benchmark_v4_template_perturbation_all_models/"
    "combined_sensitivity_analysis/summary_overall_by_model.csv"
)

V4_TEMPLATE_VOLATILITY_PATH = Path(
    "results/occupational_benchmark_v4_template_perturbation_all_models/"
    "combined_sensitivity_analysis/template_volatility_by_model.csv"
)

V4_DIALECT_SHIFT_PATH = Path(
    "results/occupational_benchmark_v4_template_perturbation_all_models/"
    "combined_sensitivity_analysis/dialect_shift_by_model.csv"
)

V5_FILES = [
    Path(
        "results/occupational_benchmark_v5_job_titles_quick_models/"
        "analysis_aragpt2_base/summary_overall.csv"
    ),
    Path(
        "results/occupational_benchmark_v5_job_titles_quick_models/"
        "analysis_bloom_560m/summary_overall.csv"
    ),
]


def read_csv(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return pd.read_csv(path, encoding="utf-8-sig")


def direction(value):
    if value > 0:
        return "masculine"
    if value < 0:
        return "feminine"
    return "equal"


def get_first_existing_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


def get_v4_average(row):
    candidates = [
        "average_score_difference",
        "avg_score_difference",
        "mean_score_difference",
    ]
    col = get_first_existing_column(row.to_frame().T, candidates)
    if col is None:
        raise ValueError("Could not find v4 average score difference column.")
    return float(row[col])


def get_template_volatility(row):
    candidates = [
        "template_volatility_range",
        "volatility_range",
        "score_difference_range",
    ]
    col = get_first_existing_column(row.to_frame().T, candidates)
    if col is None:
        raise ValueError("Could not find template volatility range column.")
    return float(row[col])


def get_dialect_shift(row):
    row_df = row.to_frame().T

    # Prefer explicit shift column if available
    explicit_candidates = [
        "dialect_shift",
        "egyptian_minus_msa_shift",
        "egyptian_msa_shift",
        "egyptian_minus_msa_average_score_difference",
        "average_score_difference_shift",
    ]

    explicit_col = get_first_existing_column(row_df, explicit_candidates)
    if explicit_col is not None:
        return float(row[explicit_col])

    # Otherwise infer from columns containing MSA and Egyptian averages
    numeric_cols = []
    for col in row.index:
        try:
            float(row[col])
            numeric_cols.append(col)
        except Exception:
            pass

    msa_cols = [
        col for col in numeric_cols
        if "msa" in col.lower() and "average" in col.lower()
    ]
    egy_cols = [
        col for col in numeric_cols
        if ("egy" in col.lower() or "egyptian" in col.lower())
        and "average" in col.lower()
    ]

    if msa_cols and egy_cols:
        return float(row[egy_cols[0]]) - float(row[msa_cols[0]])

    # If no numeric dialect shift can be found, return None
    return None


def read_v5_summaries(paths):
    frames = []

    for path in paths:
        if not path.exists():
            print(f"Skipping missing v5 file: {path}")
            continue

        df = pd.read_csv(path, encoding="utf-8-sig")
        frames.append(df)

    if not frames:
        raise ValueError("No v5 summary files were found.")

    return pd.concat(frames, ignore_index=True)


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


def sensitivity_label(score):
    if score >= 1.5:
        return "high_context_sensitivity"
    if score >= 0.75:
        return "moderate_context_sensitivity"
    return "low_context_sensitivity"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)

    v4_overall = read_csv(V4_OVERALL_PATH)
    v4_volatility = read_csv(V4_TEMPLATE_VOLATILITY_PATH)
    v4_dialect = read_csv(V4_DIALECT_SHIFT_PATH)
    v5_overall = read_v5_summaries(V5_FILES)

    rows = []

    for _, v5_row in v5_overall.iterrows():
        model_name = v5_row["model_name"]

        v4_overall_match = v4_overall[v4_overall["model_name"] == model_name]
        v4_volatility_match = v4_volatility[v4_volatility["model_name"] == model_name]
        v4_dialect_match = v4_dialect[v4_dialect["model_name"] == model_name]

        if v4_overall_match.empty:
            print(f"Skipping {model_name}: missing v4 overall row")
            continue

        if v4_volatility_match.empty:
            print(f"Skipping {model_name}: missing v4 volatility row")
            continue

        if v4_dialect_match.empty:
            print(f"Skipping {model_name}: missing v4 dialect row")
            continue

        v4_avg = get_v4_average(v4_overall_match.iloc[0])
        v5_avg = float(v5_row["average_score_difference"])

        template_volatility_range = get_template_volatility(v4_volatility_match.iloc[0])

        dialect_shift = get_dialect_shift(v4_dialect_match.iloc[0])
        abs_dialect_shift = abs(dialect_shift) if dialect_shift is not None else None

        job_title_context_shift = v5_avg - v4_avg
        abs_job_title_context_shift = abs(job_title_context_shift)

        context_sensitivity_score = template_volatility_range + abs_job_title_context_shift

        if abs_dialect_shift is not None:
            context_sensitivity_score += abs_dialect_shift

        v4_direction = direction(v4_avg)
        v5_direction = direction(v5_avg)

        rows.append({
            "model_name": model_name,
            "v4_average_score_difference": v4_avg,
            "v4_direction": v4_direction,
            "v5_average_score_difference": v5_avg,
            "v5_direction": v5_direction,
            "v4_to_v5_direction_changed": v4_direction != v5_direction,
            "job_title_context_shift": job_title_context_shift,
            "abs_job_title_context_shift": abs_job_title_context_shift,
            "v4_template_volatility_range": template_volatility_range,
            "v4_dialect_shift": dialect_shift,
            "abs_v4_dialect_shift": abs_dialect_shift,
            "context_sensitivity_score": context_sensitivity_score,
            "context_sensitivity_label": sensitivity_label(context_sensitivity_score),
        })

    result_df = pd.DataFrame(rows)

    result_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    md = []
    md.append("# Context Sensitivity Index Summary")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append(
        "This diagnostic summarizes how sensitive each model is to benchmark-context changes "
        "in Arabic occupational gender-bias evaluation."
    )
    md.append("")
    md.append("The diagnostic combines:")
    md.append("")
    md.append("1. v4 template volatility range,")
    md.append("2. v4 dialect shift magnitude,")
    md.append("3. v4-to-v5 job-title context shift.")
    md.append("")
    md.append("## Important Note")
    md.append("")
    md.append(
        "This is a thesis-specific diagnostic index, not a universal standard metric. "
        "Its purpose is to summarize robustness and context sensitivity within this benchmark suite."
    )
    md.append("")
    md.append("## Results")
    md.append("")
    md.append(markdown_table(result_df))
    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append(
        "A higher context-sensitivity score means that the model's measured gender preference "
        "changes more strongly across templates, dialects, and explicit job-title contexts."
    )
    md.append("")
    md.append(
        "The v4-to-v5 direction-change flag indicates whether the model's average preference "
        "direction changed when moving from broader occupational sentence contexts to explicit "
        "job-title contexts."
    )
    md.append("")
    md.append("## Thesis Contribution")
    md.append("")
    md.append(
        "This diagnostic enriches the thesis contribution by converting the robustness finding "
        "into a measurable model-level sensitivity summary."
    )
    md.append("")
    md.append(
        "It supports the final claim that Arabic occupational gender-bias evaluation is not only "
        "model-dependent, but also benchmark-design-dependent and context-sensitive."
    )
    md.append("")

    OUTPUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("Context sensitivity index created.")
    print("CSV:", OUTPUT_CSV)
    print("Markdown:", OUTPUT_MD)
    print("")
    print(result_df.to_string(index=False))


if __name__ == "__main__":
    main()