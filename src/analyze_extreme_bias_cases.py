from pathlib import Path
import pandas as pd


OUTPUT_DIR = Path("results/final_package")
OUTPUT_DETAILED_CSV = OUTPUT_DIR / "extreme_bias_cases_detailed.csv"
OUTPUT_SUMMARY_MD = Path("docs/occupational_scope/extreme_bias_case_analysis.md")


SEARCH_DIRS = [
    Path("results/occupational_benchmark_v2_all_models"),
    Path("results/occupational_benchmark_v3_balanced_quick_models"),
    Path("results/occupational_benchmark_v4_template_perturbation_all_models"),
    Path("results/occupational_benchmark_v5_job_titles_quick_models"),
]


REQUIRED_COLUMNS = [
    "model_name",
    "masculine_sentence",
    "feminine_sentence",
    "score_difference",
]


OPTIONAL_COLUMNS = [
    "id",
    "benchmark_version",
    "field",
    "dialect",
    "template_id",
    "semantic_frame",
    "stereotype_label",
    "masculine_score",
    "feminine_score",
    "preferred_gender",
]


TOP_K = 5


def infer_benchmark_from_path(path):
    path_text = str(path).lower()

    if "v5" in path_text:
        return "v5"
    if "v4" in path_text:
        return "v4"
    if "v3_balanced" in path_text:
        return "v3_balanced"
    if "v2" in path_text:
        return "v2"

    return "unknown"


def is_scored_results_file(path):
    if path.suffix.lower() != ".csv":
        return False

    name = path.name.lower()

    if "summary" in name:
        return False
    if "counts" in name:
        return False
    if "quality" in name:
        return False
    if "chi_square" in name:
        return False
    if "effect" in name:
        return False
    if "volatility" in name:
        return False
    if "dialect_shift" in name:
        return False

    return True


def read_candidate_file(path):
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
    except Exception:
        return None

    if not all(col in df.columns for col in REQUIRED_COLUMNS):
        return None

    df = df.copy()
    df["source_file"] = str(path)
    df["benchmark_inferred"] = infer_benchmark_from_path(path)

    for col in OPTIONAL_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df["score_difference"] = pd.to_numeric(df["score_difference"], errors="coerce")
    df = df.dropna(subset=["score_difference"])

    return df


def collect_scored_results():
    frames = []

    for search_dir in SEARCH_DIRS:
        if not search_dir.exists():
            print(f"Skipping missing directory: {search_dir}")
            continue

        for path in search_dir.rglob("*.csv"):
            if not is_scored_results_file(path):
                continue

            df = read_candidate_file(path)
            if df is not None and not df.empty:
                frames.append(df)

    if not frames:
        raise ValueError("No scored result files found with required columns.")

    combined = pd.concat(frames, ignore_index=True)
    combined = combined.drop_duplicates(
        subset=[
            "benchmark_inferred",
            "model_name",
            "id",
            "masculine_sentence",
            "feminine_sentence",
            "score_difference",
        ],
        keep="first",
    )

    return combined


def select_extreme_cases(df):
    rows = []

    group_cols = ["benchmark_inferred", "model_name"]

    for (benchmark, model), group in df.groupby(group_cols):
        group = group.copy()

        strongest_masculine = group.sort_values(
            "score_difference",
            ascending=False,
        ).head(TOP_K)

        strongest_feminine = group.sort_values(
            "score_difference",
            ascending=True,
        ).head(TOP_K)

        near_neutral = group.assign(
            abs_score_difference=group["score_difference"].abs()
        ).sort_values(
            "abs_score_difference",
            ascending=True,
        ).head(TOP_K)

        for case_type, case_df in [
            ("strongest_masculine_preference", strongest_masculine),
            ("strongest_feminine_preference", strongest_feminine),
            ("near_neutral_cases", near_neutral),
        ]:
            for rank, (_, row) in enumerate(case_df.iterrows(), start=1):
                rows.append({
                    "benchmark": benchmark,
                    "model_name": model,
                    "case_type": case_type,
                    "rank": rank,
                    "score_difference": row["score_difference"],
                    "masculine_score": row.get("masculine_score", ""),
                    "feminine_score": row.get("feminine_score", ""),
                    "preferred_gender": row.get("preferred_gender", ""),
                    "field": row.get("field", ""),
                    "dialect": row.get("dialect", ""),
                    "template_id": row.get("template_id", ""),
                    "semantic_frame": row.get("semantic_frame", ""),
                    "stereotype_label": row.get("stereotype_label", ""),
                    "masculine_sentence": row["masculine_sentence"],
                    "feminine_sentence": row["feminine_sentence"],
                    "source_file": row["source_file"],
                })

    return pd.DataFrame(rows)


def markdown_case_table(df, max_rows=40):
    display_cols = [
        "benchmark",
        "model_name",
        "case_type",
        "rank",
        "score_difference",
        "field",
        "dialect",
        "template_id",
        "semantic_frame",
        "masculine_sentence",
        "feminine_sentence",
    ]

    df = df[display_cols].head(max_rows).copy()

    lines = []
    lines.append("| " + " | ".join(display_cols) + " |")
    lines.append("| " + " | ".join(["---"] * len(display_cols)) + " |")

    for _, row in df.iterrows():
        values = []
        for col in display_cols:
            value = row[col]
            if isinstance(value, float):
                value = f"{value:.4f}"
            value = str(value).replace("\n", " ").replace("|", "/")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_SUMMARY_MD.parent.mkdir(parents=True, exist_ok=True)

    combined_df = collect_scored_results()
    cases_df = select_extreme_cases(combined_df)

    cases_df.to_csv(OUTPUT_DETAILED_CSV, index=False, encoding="utf-8-sig")

    summary_rows = []

    for (benchmark, model), group in combined_df.groupby(["benchmark_inferred", "model_name"]):
        summary_rows.append({
            "benchmark": benchmark,
            "model_name": model,
            "total_scored_items_found": len(group),
            "max_masculine_score_difference": group["score_difference"].max(),
            "max_feminine_score_difference": group["score_difference"].min(),
            "average_score_difference": group["score_difference"].mean(),
            "median_score_difference": group["score_difference"].median(),
        })

    summary_df = pd.DataFrame(summary_rows)

    md = []
    md.append("# Extreme Bias Case Analysis")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append(
        "This analysis extracts qualitative examples from the scored benchmark results."
    )
    md.append("")
    md.append(
        "It identifies the strongest masculine-preferred cases, strongest feminine-preferred cases, "
        "and near-neutral cases for each available model and benchmark."
    )
    md.append("")
    md.append("## Why This Matters")
    md.append("")
    md.append(
        "Aggregate statistics such as averages and percentages are useful, but they do not show "
        "which sentence pairs drive the strongest model preferences."
    )
    md.append("")
    md.append(
        "This contribution adds an interpretability layer by connecting numerical bias scores "
        "to concrete Arabic sentence-pair examples."
    )
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append(summary_df.to_markdown(index=False))
    md.append("")
    md.append("## Example Extreme Cases")
    md.append("")
    md.append(markdown_case_table(cases_df))
    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append(
        "Strong positive score differences indicate cases where the model strongly preferred "
        "the masculine sentence variant."
    )
    md.append("")
    md.append(
        "Strong negative score differences indicate cases where the model strongly preferred "
        "the feminine sentence variant."
    )
    md.append("")
    md.append(
        "Near-neutral cases show sentence pairs where the model assigned almost equal likelihood "
        "to both gendered variants."
    )
    md.append("")
    md.append("## Contribution")
    md.append("")
    md.append(
        "This analysis widens the thesis contribution by adding qualitative interpretability "
        "to the benchmark results."
    )
    md.append("")
    md.append(
        "It helps explain not only how much bias was measured, but which occupational sentence "
        "pairs produced the strongest measured preferences."
    )
    md.append("")

    OUTPUT_SUMMARY_MD.write_text("\n".join(md), encoding="utf-8")

    print("Extreme bias case analysis created.")
    print("Detailed CSV:", OUTPUT_DETAILED_CSV)
    print("Markdown:", OUTPUT_SUMMARY_MD)
    print("")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()