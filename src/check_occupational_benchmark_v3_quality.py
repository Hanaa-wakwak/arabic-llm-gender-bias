from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/occupational_benchmark/occupational_bias_v3.csv")
OUTPUT_DIR = Path("results/occupational_benchmark_v3_quality")


REQUIRED_COLUMNS = [
    "id",
    "benchmark_version",
    "occupation_id",
    "occupation_key",
    "occupation_en",
    "field",
    "stereotype_label",
    "template_id",
    "template_type",
    "dialect",
    "grammatical_gender_marker",
    "masculine_occupation",
    "feminine_occupation",
    "masculine_sentence",
    "feminine_sentence",
]


ALLOWED_STEREOTYPE_LABELS = {
    "male_stereotyped",
    "female_stereotyped",
    "neutral",
}


ALLOWED_DIALECTS = {
    "MSA",
    "Egyptian",
}


def add_issue(issues, issue_type, details, count):
    issues.append({
        "issue_type": issue_type,
        "details": details,
        "count": count,
    })


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

    issues = []

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_columns:
        add_issue(
            issues,
            "missing_required_columns",
            ",".join(missing_columns),
            len(missing_columns),
        )

    if len(df) != 540:
        add_issue(
            issues,
            "unexpected_row_count",
            f"expected 540 rows, found {len(df)}",
            len(df),
        )

    if "id" in df.columns and df["id"].duplicated().any():
        add_issue(
            issues,
            "duplicate_ids",
            "id column contains duplicates",
            int(df["id"].duplicated().sum()),
        )

    for col in REQUIRED_COLUMNS:
        if col in df.columns:
            null_count = int(df[col].isna().sum())
            if null_count > 0:
                add_issue(
                    issues,
                    "missing_values",
                    col,
                    null_count,
                )

    if "stereotype_label" in df.columns:
        invalid_labels = sorted(set(df["stereotype_label"]) - ALLOWED_STEREOTYPE_LABELS)
        if invalid_labels:
            add_issue(
                issues,
                "invalid_stereotype_labels",
                ",".join(invalid_labels),
                len(invalid_labels),
            )

    if "dialect" in df.columns:
        invalid_dialects = sorted(set(df["dialect"]) - ALLOWED_DIALECTS)
        if invalid_dialects:
            add_issue(
                issues,
                "invalid_dialects",
                ",".join(invalid_dialects),
                len(invalid_dialects),
            )

    if {"masculine_sentence", "feminine_sentence"}.issubset(df.columns):
        equal_sentences = df[df["masculine_sentence"] == df["feminine_sentence"]]
        if len(equal_sentences) > 0:
            add_issue(
                issues,
                "identical_masculine_feminine_sentences",
                "masculine_sentence equals feminine_sentence",
                len(equal_sentences),
            )

    if {"masculine_occupation", "masculine_sentence"}.issubset(df.columns):
        missing_masc_occ = df[
            ~df.apply(
                lambda row: str(row["masculine_occupation"]) in str(row["masculine_sentence"]),
                axis=1,
            )
        ]
        if len(missing_masc_occ) > 0:
            add_issue(
                issues,
                "masculine_occupation_missing_from_sentence",
                "masculine occupation not found inside masculine sentence",
                len(missing_masc_occ),
            )

    if {"feminine_occupation", "feminine_sentence"}.issubset(df.columns):
        missing_fem_occ = df[
            ~df.apply(
                lambda row: str(row["feminine_occupation"]) in str(row["feminine_sentence"]),
                axis=1,
            )
        ]
        if len(missing_fem_occ) > 0:
            add_issue(
                issues,
                "feminine_occupation_missing_from_sentence",
                "feminine occupation not found inside feminine sentence",
                len(missing_fem_occ),
            )

    summary_rows = []

    summary_rows.append({
        "metric": "total_rows",
        "value": len(df),
    })

    summary_rows.append({
        "metric": "unique_occupations",
        "value": df["occupation_id"].nunique() if "occupation_id" in df.columns else None,
    })

    summary_rows.append({
        "metric": "unique_fields",
        "value": df["field"].nunique() if "field" in df.columns else None,
    })

    summary_rows.append({
        "metric": "unique_templates",
        "value": df["template_id"].nunique() if "template_id" in df.columns else None,
    })

    summary_rows.append({
        "metric": "unique_stereotype_labels",
        "value": df["stereotype_label"].nunique() if "stereotype_label" in df.columns else None,
    })

    if not issues:
        add_issue(
            issues,
            "no_issues_found",
            "benchmark passed v3 quality checks",
            0,
        )

    issues_df = pd.DataFrame(issues)
    summary_df = pd.DataFrame(summary_rows)

    field_counts = df["field"].value_counts().reset_index()
    field_counts.columns = ["field", "count"]

    template_counts = df["template_id"].value_counts().reset_index()
    template_counts.columns = ["template_id", "count"]

    stereotype_counts = df["stereotype_label"].value_counts().reset_index()
    stereotype_counts.columns = ["stereotype_label", "count"]

    issues_df.to_csv(
        OUTPUT_DIR / "occupational_bias_v3_quality_issues.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary_df.to_csv(
        OUTPUT_DIR / "occupational_bias_v3_quality_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    field_counts.to_csv(
        OUTPUT_DIR / "occupational_bias_v3_field_counts.csv",
        index=False,
        encoding="utf-8-sig",
    )

    template_counts.to_csv(
        OUTPUT_DIR / "occupational_bias_v3_template_counts.csv",
        index=False,
        encoding="utf-8-sig",
    )

    stereotype_counts.to_csv(
        OUTPUT_DIR / "occupational_bias_v3_stereotype_counts.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("v3 quality check completed.")
    print("Issues:")
    print(issues_df.to_string(index=False))

    print("\nSummary:")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()