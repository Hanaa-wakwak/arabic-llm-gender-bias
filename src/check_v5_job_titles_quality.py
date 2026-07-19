from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/occupational_benchmark/occupational_bias_v5_job_titles.csv")
OUTPUT_DIR = Path("results/occupational_benchmark_v5_job_titles_quality")

QUALITY_SUMMARY_PATH = OUTPUT_DIR / "v5_job_titles_quality_summary.csv"
DIALECT_COUNTS_PATH = OUTPUT_DIR / "v5_job_titles_dialect_counts.csv"
TEMPLATE_COUNTS_PATH = OUTPUT_DIR / "v5_job_titles_template_counts.csv"
SEMANTIC_FRAME_COUNTS_PATH = OUTPUT_DIR / "v5_job_titles_semantic_frame_counts.csv"
STEREOTYPE_ROW_COUNTS_PATH = OUTPUT_DIR / "v5_job_titles_stereotype_label_counts.csv"
FIELD_COUNTS_PATH = OUTPUT_DIR / "v5_job_titles_field_counts.csv"


REQUIRED_COLUMNS = [
    "id",
    "benchmark_version",
    "occupation_id",
    "field",
    "occupation_key",
    "occupation_en",
    "masculine_occupation",
    "feminine_occupation",
    "stereotype_label",
    "dialect",
    "template_id",
    "template_type",
    "semantic_frame",
    "grammatical_gender_marker",
    "masculine_sentence",
    "feminine_sentence",
]


def add_issue(issues, issue_type, details, count):
    issues.append({
        "issue_type": issue_type,
        "details": details,
        "count": count,
    })


def save_counts(df, column, output_path):
    counts_df = (
        df[column]
        .value_counts()
        .rename_axis(column)
        .reset_index(name="count")
    )
    counts_df.to_csv(output_path, index=False, encoding="utf-8-sig")


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input benchmark not found: {INPUT_PATH}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")
    issues = []

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        add_issue(
            issues,
            "missing_columns",
            ",".join(missing_columns),
            len(missing_columns),
        )

    if df["id"].duplicated().any():
        add_issue(
            issues,
            "duplicate_ids",
            "duplicate benchmark item ids found",
            int(df["id"].duplicated().sum()),
        )

    null_counts = df[REQUIRED_COLUMNS].isna().sum()
    for col, count in null_counts.items():
        if count > 0:
            add_issue(
                issues,
                "missing_values",
                f"column={col}",
                int(count),
            )

    identical_sentence_count = int(
        (df["masculine_sentence"] == df["feminine_sentence"]).sum()
    )
    if identical_sentence_count > 0:
        add_issue(
            issues,
            "identical_sentence_pairs",
            "masculine_sentence equals feminine_sentence",
            identical_sentence_count,
        )

    if df["occupation_id"].nunique() != 90:
        add_issue(
            issues,
            "unexpected_occupation_count",
            "expected 90 unique occupations",
            int(df["occupation_id"].nunique()),
        )

    if df["template_id"].nunique() != 6:
        add_issue(
            issues,
            "unexpected_template_count",
            "expected 6 unique templates",
            int(df["template_id"].nunique()),
        )

    if df["dialect"].nunique() != 2:
        add_issue(
            issues,
            "unexpected_dialect_count",
            "expected 2 dialects",
            int(df["dialect"].nunique()),
        )

    expected_rows = df["occupation_id"].nunique() * df["template_id"].nunique()
    if len(df) != expected_rows:
        add_issue(
            issues,
            "unexpected_row_count",
            f"expected {expected_rows} rows",
            len(df),
        )

    stereotype_occ_counts = (
        df[["occupation_id", "stereotype_label"]]
        .drop_duplicates()
        ["stereotype_label"]
        .value_counts()
    )

    expected_stereotype_labels = {
        "male_stereotyped",
        "female_stereotyped",
        "neutral",
    }

    actual_stereotype_labels = set(df["stereotype_label"].dropna().unique())
    if actual_stereotype_labels != expected_stereotype_labels:
        add_issue(
            issues,
            "unexpected_stereotype_labels",
            f"actual={sorted(actual_stereotype_labels)}",
            len(actual_stereotype_labels),
        )

    for label in expected_stereotype_labels:
        count = int(stereotype_occ_counts.get(label, 0))
        if count != 30:
            add_issue(
                issues,
                "unbalanced_stereotype_occupation_count",
                f"{label} expected 30 occupations",
                count,
            )

    if issues:
        quality_df = pd.DataFrame(issues)
    else:
        quality_df = pd.DataFrame([
            {
                "issue_type": "no_issues_found",
                "details": "v5 job-title benchmark passed quality checks",
                "count": 0,
            },
            {
                "issue_type": "metric",
                "details": "total_rows",
                "count": len(df),
            },
            {
                "issue_type": "metric",
                "details": "unique_occupations",
                "count": df["occupation_id"].nunique(),
            },
            {
                "issue_type": "metric",
                "details": "unique_templates",
                "count": df["template_id"].nunique(),
            },
            {
                "issue_type": "metric",
                "details": "unique_dialects",
                "count": df["dialect"].nunique(),
            },
            {
                "issue_type": "metric",
                "details": "unique_semantic_frames",
                "count": df["semantic_frame"].nunique(),
            },
        ])

    quality_df.to_csv(QUALITY_SUMMARY_PATH, index=False, encoding="utf-8-sig")

    save_counts(df, "dialect", DIALECT_COUNTS_PATH)
    save_counts(df, "template_id", TEMPLATE_COUNTS_PATH)
    save_counts(df, "semantic_frame", SEMANTIC_FRAME_COUNTS_PATH)
    save_counts(df, "stereotype_label", STEREOTYPE_ROW_COUNTS_PATH)
    save_counts(df, "field", FIELD_COUNTS_PATH)

    print("v5 job-title quality check completed.")
    print("Input:", INPUT_PATH)
    print("Output dir:", OUTPUT_DIR)
    print("")
    print(quality_df.to_string(index=False))


if __name__ == "__main__":
    main()