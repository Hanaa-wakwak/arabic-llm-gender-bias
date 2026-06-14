from pathlib import Path
import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Benchmark CSV file to check.",
    )

    parser.add_argument(
        "--output_dir",
        default="results/occupational_benchmark_quality",
        help="Output directory.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    required_columns = [
        "id",
        "field",
        "occupation_id",
        "occupation_m",
        "occupation_f",
        "workplace",
        "dialect",
        "template_id",
        "masculine_sentence",
        "feminine_sentence",
        "stereotype_direction",
        "notes",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    issues = []

    if missing_columns:
        issues.append({
            "issue_type": "missing_columns",
            "details": "|".join(missing_columns),
            "count": len(missing_columns),
        })

    for col in required_columns:
        if col in df.columns:
            missing_count = int(df[col].isna().sum())
            if missing_count > 0:
                issues.append({
                    "issue_type": "missing_values",
                    "details": col,
                    "count": missing_count,
                })

    if "id" in df.columns:
        duplicated_id_count = int(df["id"].duplicated().sum())
        if duplicated_id_count > 0:
            issues.append({
                "issue_type": "duplicate_ids",
                "details": "id",
                "count": duplicated_id_count,
            })

    if "masculine_sentence" in df.columns and "feminine_sentence" in df.columns:
        identical_count = int((df["masculine_sentence"] == df["feminine_sentence"]).sum())
        if identical_count > 0:
            issues.append({
                "issue_type": "identical_masculine_feminine_sentence",
                "details": "masculine_sentence == feminine_sentence",
                "count": identical_count,
            })

        duplicated_pair_count = int(
            df.duplicated(subset=["masculine_sentence", "feminine_sentence"]).sum()
        )
        if duplicated_pair_count > 0:
            issues.append({
                "issue_type": "duplicate_sentence_pairs",
                "details": "masculine_sentence + feminine_sentence",
                "count": duplicated_pair_count,
            })

    summary_rows = []

    summary_rows.append({
        "metric": "total_rows",
        "value": len(df),
    })

    for col in ["field", "dialect", "template_id", "stereotype_direction"]:
        if col in df.columns:
            counts = df[col].value_counts().sort_index()
            for value, count in counts.items():
                summary_rows.append({
                    "metric": f"count_by_{col}",
                    "value": f"{value}: {count}",
                })

    issues_df = pd.DataFrame(issues)
    summary_df = pd.DataFrame(summary_rows)

    if issues_df.empty:
        issues_df = pd.DataFrame([{
            "issue_type": "no_issues_found",
            "details": "benchmark passed basic checks",
            "count": 0,
        }])

    output_stem = input_path.stem

    summary_df.to_csv(
        output_dir / f"{output_stem}_quality_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    issues_df.to_csv(
        output_dir / f"{output_stem}_quality_issues.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("Benchmark quality check completed.")
    print("Input:", input_path)
    print("Rows:", len(df))
    print("\nIssues:")
    print(issues_df)
    print("\nOutputs saved to:")
    print(output_dir)


if __name__ == "__main__":
    main()