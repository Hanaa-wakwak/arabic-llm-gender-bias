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
                add_issue(issues, "missing_values", col, null_count)

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

    if not issues:
        add_issue(
            issues,
            "no_issues_found",
            "v3 balanced candidate passed quality checks",
            0,
        )

    issues_df = pd.DataFrame(issues)

    summary_df = pd.DataFrame([
        {"metric": "total_rows", "value": len(df)},
        {"metric": "unique_occupations", "value": df["candidate_occupation_id"].nunique()},
        {"metric": "unique_fields", "value": df["field"].nunique()},
        {"metric": "unique_templates", "value": df["template_id"].nunique()},
        {"metric": "unique_stereotype_labels", "value": df["stereotype_label"].nunique()},
        {"metric": "unique_source_versions", "value": df["source_version"].nunique()},
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

    df["field"].value_counts().reset_index().rename(
        columns={"index": "field", "field": "count"}
    ).to_csv(
        OUTPUT_DIR / "v3_balanced_candidate_field_counts.csv",
        index=False,
        encoding="utf-8-sig",
    )

    df["stereotype_label"].value_counts().reset_index().rename(
        columns={"index": "stereotype_label", "stereotype_label": "count"}
    ).to_csv(
        OUTPUT_DIR / "v3_balanced_candidate_stereotype_counts.csv",
        index=False,
        encoding="utf-8-sig",
    )

    df["source_version"].value_counts().reset_index().rename(
        columns={"index": "source_version", "source_version": "count"}
    ).to_csv(
        OUTPUT_DIR / "v3_balanced_candidate_source_counts.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("v3 balanced candidate quality check completed.")

    print("\nIssues:")
    print(issues_df.to_string(index=False))

    print("\nSummary:")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()