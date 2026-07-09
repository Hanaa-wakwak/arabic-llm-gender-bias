from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/occupational_benchmark/occupational_bias_v3_balanced_candidate.csv")
OUTPUT_DIR = Path("results/occupational_benchmark_v3_balanced_candidate_quality")


REQUIRED_COLUMNS = [
    "id",
    "benchmark_version",
    "candidate_occupation_id",
    "occupation_key",
    "field",
    "stereotype_label",
    "source_version",
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


ALLOWED_SOURCE_VERSIONS = {
    "v2_preserved",
    "v3_candidate_addition",
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


def save_value_counts(df, column_name, output_path):
    counts_df = (
        df[column_name]
        .value_counts()
        .rename_axis(column_name)
        .reset_index(name="count")
    )

    counts_df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
    )


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

    if len(df) != 360:
        add_issue(
            issues,
            "unexpected_row_count",
            f"expected 360 rows, found {len(df)}",
            len(df),
        )

    if "id" in df.columns and df["id"].duplicated().any():
        add_issue(
            issues,
            "duplicate_ids",
            "id contains duplicated values",
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

    if "source_version" in df.columns:
        invalid_sources = sorted(set(df["source_version"]) - ALLOWED_SOURCE_VERSIONS)

        if invalid_sources:
            add_issue(
                issues,
                "invalid_source_versions",
                ",".join(invalid_sources),
                len(invalid_sources),
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
                "identical_sentence_pairs",
                "masculine_sentence equals feminine_sentence",
                len(equal_sentences),
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
            "v3 balanced candidate passed quality checks",
            0,
        )

    issues_df = pd.DataFrame(issues)

    summary_df = pd.DataFrame([
        {
            "metric": "total_rows",
            "value": len(df),
        },
        {
            "metric": "unique_occupations",
            "value": df["candidate_occupation_id"].nunique()
            if "candidate_occupation_id" in df.columns
            else None,
        },
        {
            "metric": "unique_fields",
            "value": df["field"].nunique()
            if "field" in df.columns
            else None,
        },
        {
            "metric": "unique_templates",
            "value": df["template_id"].nunique()
            if "template_id" in df.columns
            else None,
        },
        {
            "metric": "unique_stereotype_labels",
            "value": df["stereotype_label"].nunique()
            if "stereotype_label" in df.columns
            else None,
        },
        {
            "metric": "unique_source_versions",
            "value": df["source_version"].nunique()
            if "source_version" in df.columns
            else None,
        },
    ])

    issues_df.to_csv(
        OUTPUT_DIR / "v3_balanced_candidate_quality_issues.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary_df.to_csv(
        OUTPUT_DIR / "v3_balanced_candidate_quality_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    if "field" in df.columns:
        save_value_counts(
            df,
            "field",
            OUTPUT_DIR / "v3_balanced_candidate_field_counts.csv",
        )

    if "stereotype_label" in df.columns:
        save_value_counts(
            df,
            "stereotype_label",
            OUTPUT_DIR / "v3_balanced_candidate_stereotype_counts.csv",
        )

    if "source_version" in df.columns:
        save_value_counts(
            df,
            "source_version",
            OUTPUT_DIR / "v3_balanced_candidate_source_counts.csv",
        )

    if "template_id" in df.columns:
        save_value_counts(
            df,
            "template_id",
            OUTPUT_DIR / "v3_balanced_candidate_template_counts.csv",
        )

    if "dialect" in df.columns:
        save_value_counts(
            df,
            "dialect",
            OUTPUT_DIR / "v3_balanced_candidate_dialect_counts.csv",
        )

    print("v3 balanced candidate quality check completed.")

    print("\nIssues:")
    print(issues_df.to_string(index=False))

    print("\nSummary:")
    print(summary_df.to_string(index=False))

    if "stereotype_label" in df.columns:
        print("\nStereotype counts:")
        print(
            df["stereotype_label"]
            .value_counts()
            .rename_axis("stereotype_label")
            .reset_index(name="count")
            .to_string(index=False)
        )

    if "source_version" in df.columns:
        print("\nSource counts:")
        print(
            df["source_version"]
            .value_counts()
            .rename_axis("source_version")
            .reset_index(name="count")
            .to_string(index=False)
        )


if __name__ == "__main__":
    main()