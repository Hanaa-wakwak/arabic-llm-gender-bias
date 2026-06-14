from pathlib import Path
import argparse
import pandas as pd


def summarize_group(df, group_cols):
    rows = []

    for group_values, group_df in df.groupby(group_cols):
        if not isinstance(group_values, tuple):
            group_values = (group_values,)

        row = {}

        for col, value in zip(group_cols, group_values):
            row[col] = value

        total = len(group_df)
        masculine_count = int((group_df["preferred_gender"] == "masculine").sum())
        feminine_count = int((group_df["preferred_gender"] == "feminine").sum())
        equal_count = int((group_df["preferred_gender"] == "equal").sum())

        row.update({
            "total_items": total,
            "masculine_preferred_count": masculine_count,
            "feminine_preferred_count": feminine_count,
            "equal_count": equal_count,
            "masculine_preferred_percent": masculine_count / total * 100 if total else 0,
            "feminine_preferred_percent": feminine_count / total * 100 if total else 0,
            "equal_percent": equal_count / total * 100 if total else 0,
            "average_score_difference": group_df["score_difference"].mean(),
            "median_score_difference": group_df["score_difference"].median(),
            "min_score_difference": group_df["score_difference"].min(),
            "max_score_difference": group_df["score_difference"].max(),
        })

        rows.append(row)

    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Scored APGC-format gender-pair CSV file.",
    )

    parser.add_argument(
        "--output_dir",
        required=True,
        help="Directory to save APGC analysis outputs.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    required_columns = [
        "id",
        "masculine_sentence",
        "feminine_sentence",
        "gender_context",
        "masculine_score",
        "feminine_score",
        "score_difference",
        "preferred_gender",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    overall_df = summarize_group(df, ["model_name"])
    by_context_df = summarize_group(df, ["model_name", "gender_context"])

    if "source_dataset" in df.columns:
        by_source_df = summarize_group(df, ["model_name", "source_dataset"])
    else:
        by_source_df = pd.DataFrame()

    overall_df.to_csv(
        output_dir / "apgc_summary_overall.csv",
        index=False,
        encoding="utf-8-sig",
    )

    by_context_df.to_csv(
        output_dir / "apgc_summary_by_gender_context.csv",
        index=False,
        encoding="utf-8-sig",
    )

    if not by_source_df.empty:
        by_source_df.to_csv(
            output_dir / "apgc_summary_by_source_dataset.csv",
            index=False,
            encoding="utf-8-sig",
        )

    df.to_csv(
        output_dir / "apgc_scored_results_with_analysis.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("APGC gender analysis completed.")
    print("Input:", input_path)
    print("Outputs saved to:", output_dir)

    print("\nOverall summary:")
    print(overall_df)

    print("\nSummary by gender context:")
    print(by_context_df)


if __name__ == "__main__":
    main()