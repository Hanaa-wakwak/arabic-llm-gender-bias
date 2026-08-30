from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/occupational_benchmark/occupational_bias_v6_job_roles_departments.csv")
OUTPUT_DIR = Path("results/occupational_benchmark_v6_job_roles_quality")
SUMMARY_PATH = OUTPUT_DIR / "v6_quality_summary.csv"
ISSUES_PATH = OUTPUT_DIR / "v6_quality_issues.csv"
DOC_PATH = Path("docs/occupational_scope/v6_quality_summary.md")


REQUIRED_COLUMNS = [
    "id",
    "benchmark_version",
    "role_id",
    "department",
    "job_family",
    "role_key",
    "seniority_level",
    "job_role_type",
    "workplace_context",
    "masculine_occupation",
    "feminine_occupation",
    "template_id",
    "template_type",
    "semantic_frame",
    "dialect",
    "masculine_sentence",
    "feminine_sentence",
]


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Missing v6 benchmark: {INPUT_PATH}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")
    issues = []

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            issues.append({
                "issue_type": "missing_required_column",
                "details": col,
                "count": 1,
            })

    if "id" in df.columns:
        duplicate_ids = df["id"].duplicated().sum()
        if duplicate_ids > 0:
            issues.append({
                "issue_type": "duplicate_pair_ids",
                "details": "id",
                "count": int(duplicate_ids),
            })

    for col in REQUIRED_COLUMNS:
        if col in df.columns:
            missing = df[col].isna().sum() + (df[col].astype(str).str.strip() == "").sum()
            if missing > 0:
                issues.append({
                    "issue_type": "missing_or_empty_values",
                    "details": col,
                    "count": int(missing),
                })

    if "masculine_sentence" in df.columns and "feminine_sentence" in df.columns:
        identical_sentences = (df["masculine_sentence"] == df["feminine_sentence"]).sum()
        if identical_sentences > 0:
            issues.append({
                "issue_type": "identical_masculine_feminine_sentence",
                "details": "sentence_pair",
                "count": int(identical_sentences),
            })

    if "masculine_occupation" in df.columns and "feminine_occupation" in df.columns:
        identical_titles = (df["masculine_occupation"] == df["feminine_occupation"]).sum()
        if identical_titles > 0:
            issues.append({
                "issue_type": "identical_masculine_feminine_title",
                "details": "job_title_pair",
                "count": int(identical_titles),
            })

    summary_rows = [
        {"metric": "total_rows", "value": len(df)},
        {"metric": "unique_roles", "value": df["role_id"].nunique() if "role_id" in df.columns else None},
        {"metric": "unique_departments", "value": df["department"].nunique() if "department" in df.columns else None},
        {"metric": "unique_job_families", "value": df["job_family"].nunique() if "job_family" in df.columns else None},
        {"metric": "unique_role_types", "value": df["job_role_type"].nunique() if "job_role_type" in df.columns else None},
        {"metric": "unique_templates", "value": df["template_id"].nunique() if "template_id" in df.columns else None},
        {"metric": "unique_dialects", "value": df["dialect"].nunique() if "dialect" in df.columns else None},
        {"metric": "quality_issues_found", "value": len(issues)},
    ]

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(SUMMARY_PATH, index=False, encoding="utf-8-sig")

    if issues:
        issues_df = pd.DataFrame(issues)
    else:
        issues_df = pd.DataFrame([{
            "issue_type": "no_issues_found",
            "details": "v6 benchmark passed basic quality checks",
            "count": 0,
        }])

    issues_df.to_csv(ISSUES_PATH, index=False, encoding="utf-8-sig")

    doc = []
    doc.append("# v6 Quality Summary")
    doc.append("")
    doc.append("## Summary")
    doc.append("")
    for row in summary_rows:
        doc.append(f"- {row['metric']}: {row['value']}")
    doc.append("")
    doc.append("## Issues")
    doc.append("")
    for _, row in issues_df.iterrows():
        doc.append(f"- {row['issue_type']}: {row['details']} ({row['count']})")
    doc.append("")
    doc.append("## Thesis Use")
    doc.append("")
    doc.append("This quality check verifies that the expanded v6 benchmark has complete metadata, non-empty sentence pairs, unique pair identifiers, and non-identical masculine/feminine variants.")

    DOC_PATH.write_text("\n".join(doc), encoding="utf-8")

    print("v6 quality check completed.")
    print("Summary:", SUMMARY_PATH)
    print("Issues:", ISSUES_PATH)
    print("Doc:", DOC_PATH)
    print("")
    print(summary_df.to_string(index=False))
    print("")
    print(issues_df.to_string(index=False))


if __name__ == "__main__":
    main()