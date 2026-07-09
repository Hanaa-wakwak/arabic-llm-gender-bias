from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/occupational_benchmark/occupational_bias_v4_template_perturbation.csv")
OUTPUT_DIR = Path("results/occupational_benchmark_v4_template_perturbation_quality")


REQUIRED_COLUMNS = [
    "id",
    "benchmark_version",
    "balanced_occupation_id",
    "occupation_key",
    "occupation_en",
    "field",
    "stereotype_label",
    "source_version",
    "template_id",
    "template_type",
    "semantic_frame",
    "dialect",
    "grammatical_gender_marker",
    "masculine_occupation",
    "feminine_occupation",
    "workplace",
    "masculine_sentence",
    "feminine_sentence",
]


EXPECTED_TOTAL_ROWS = 720
EXPECTED_OCCUPATIONS = 90
EXPECTED_TEMPLATES = 8
EXPECTED_ROWS_PER_STEREOTYPE = 240
EXPECTED_OCCUPATIONS_PER_STEREOTYPE = 30


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


def save_counts(df, column_name, output_dir):
    counts_df = (
        df[column_name]
        .value_counts()
        .rename_axis(column_name)
        .reset_index(name="count")
    )

    counts_df.to_csv(
        output_dir / f"v4_{column_name}_counts.csv",
        index=False,
        encoding="utf-8-sig",
    )

    return counts_df


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

    if len(df) != EXPECTED_TOTAL_ROWS:
        add_issue(
            issues,
            "unexpected_row_count",
            f"expected {EXPECTED_TOTAL_ROWS}, found {len(df)}",
            len(df),
        )

    for col in REQUIRED_COLUMNS:
        if col in df.columns:
            null_count = int(df[col].isna().sum())

            if null_count > 0:
                add_issue(issues, "missing_values", col, null_count)

            blank_count = int(df[col].astype(str).str.strip().eq("").sum())

            if blank_count > 0:
                add_issue(issues, "blank_values", col, blank_count)

    if "id" in df.columns and df["id"].duplicated().any():
        add_issue(
            issues,
            "duplicate_ids",
            "duplicate id values found",
            int(df["id"].duplicated().sum()),
        )

    if "balanced_occupation_id" in df.columns:
        unique_occupations = df["balanced_occupation_id"].nunique()

        if unique_occupations != EXPECTED_OCCUPATIONS:
            add_issue(
                issues,
                "unexpected_unique_occupation_count",
                f"expected {EXPECTED_OCCUPATIONS}, found {unique_occupations}",
                unique_occupations,
            )

    if "template_id" in df.columns:
        unique_templates = df["template_id"].nunique()

        if unique_templates != EXPECTED_TEMPLATES:
            add_issue(
                issues,
                "unexpected_template_count",
                f"expected {EXPECTED_TEMPLATES}, found {unique_templates}",
                unique_templates,
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

        row_counts = df["stereotype_label"].value_counts().to_dict()

        for label in ALLOWED_STEREOTYPE_LABELS:
            count = row_counts.get(label, 0)

            if count != EXPECTED_ROWS_PER_STEREOTYPE:
                add_issue(
                    issues,
                    "unbalanced_stereotype_rows",
                    f"{label}: expected {EXPECTED_ROWS_PER_STEREOTYPE}, found {count}",
                    count,
                )

        occupation_counts = (
            df[["balanced_occupation_id", "stereotype_label"]]
            .drop_duplicates()
            ["stereotype_label"]
            .value_counts()
            .to_dict()
        )

        for label in ALLOWED_STEREOTYPE_LABELS:
            count = occupation_counts.get(label, 0)

            if count != EXPECTED_OCCUPATIONS_PER_STEREOTYPE:
                add_issue(
                    issues,
                    "unbalanced_stereotype_occupations",
                    f"{label}: expected {EXPECTED_OCCUPATIONS_PER_STEREOTYPE}, found {count}",
                    count,
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
        identical_pairs = df[df["masculine_sentence"] == df["feminine_sentence"]]

        if len(identical_pairs) > 0:
            add_issue(
                issues,
                "identical_sentence_pairs",
                "masculine_sentence equals feminine_sentence",
                len(identical_pairs),
            )

    if {"masculine_occupation", "masculine_sentence"}.issubset(df.columns):
        missing_masc_occ = df[
            ~df.apply(
                lambda row: str(row["masculine_occupation"]).strip()
                in str(row["masculine_sentence"]),
                axis=1,
            )
        ]

        if len(missing_masc_occ) > 0:
            add_issue(
                issues,
                "masculine_occupation_missing_from_sentence",
                "masculine occupation not found in masculine sentence",
                len(missing_masc_occ),
            )

    if {"feminine_occupation", "feminine_sentence"}.issubset(df.columns):
        missing_fem_occ = df[
            ~df.apply(
                lambda row: str(row["feminine_occupation"]).strip()
                in str(row["feminine_sentence"]),
                axis=1,
            )
        ]

        if len(missing_fem_occ) > 0:
            add_issue(
                issues,
                "feminine_occupation_missing_from_sentence",
                "feminine occupation not found in feminine sentence",
                len(missing_fem_occ),
            )

    if not issues:
        add_issue(
            issues,
            "no_issues_found",
            "v4 template perturbation benchmark passed quality checks",
            0,
        )

    issues_df = pd.DataFrame(issues)

    summary_df = pd.DataFrame([
        {"metric": "total_rows", "value": len(df)},
        {"metric": "unique_occupations", "value": df["balanced_occupation_id"].nunique()},
        {"metric": "unique_fields", "value": df["field"].nunique()},
        {"metric": "unique_templates", "value": df["template_id"].nunique()},
        {"metric": "unique_semantic_frames", "value": df["semantic_frame"].nunique()},
        {"metric": "unique_stereotype_labels", "value": df["stereotype_label"].nunique()},
        {"metric": "unique_dialects", "value": df["dialect"].nunique()},
    ])

    issues_df.to_csv(
        OUTPUT_DIR / "v4_template_perturbation_quality_issues.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary_df.to_csv(
        OUTPUT_DIR / "v4_template_perturbation_quality_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    for col in [
        "field",
        "stereotype_label",
        "template_id",
        "template_type",
        "semantic_frame",
        "dialect",
        "source_version",
    ]:
        if col in df.columns:
            save_counts(df, col, OUTPUT_DIR)

    occupation_stereotype_counts = (
        df[["balanced_occupation_id", "stereotype_label"]]
        .drop_duplicates()
        ["stereotype_label"]
        .value_counts()
        .rename_axis("stereotype_label")
        .reset_index(name="occupation_count")
    )

    occupation_stereotype_counts.to_csv(
        OUTPUT_DIR / "v4_stereotype_occupation_counts.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("v4 template perturbation quality check completed.")

    print("\nIssues:")
    print(issues_df.to_string(index=False))

    print("\nSummary:")
    print(summary_df.to_string(index=False))

    print("\nRows by semantic frame:")
    print(
        df["semantic_frame"]
        .value_counts()
        .rename_axis("semantic_frame")
        .reset_index(name="count")
        .to_string(index=False)
    )

    print("\nRows by stereotype label:")
    print(
        df["stereotype_label"]
        .value_counts()
        .rename_axis("stereotype_label")
        .reset_index(name="count")
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()