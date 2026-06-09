from pathlib import Path
import argparse

import pandas as pd


def summarize_group(df: pd.DataFrame, group_cols):
    grouped = []

    for group_values, group_df in df.groupby(group_cols):
        if not isinstance(group_values, tuple):
            group_values = (group_values,)

        row = {}

        for col, value in zip(group_cols, group_values):
            row[col] = value

        total_items = len(group_df)

        masculine_count = (group_df["preferred_gender"] == "masculine").sum()
        feminine_count = (group_df["preferred_gender"] == "feminine").sum()
        equal_count = (group_df["preferred_gender"] == "equal").sum()

        row["total_items"] = total_items
        row["masculine_preferred_count"] = masculine_count
        row["feminine_preferred_count"] = feminine_count
        row["equal_count"] = equal_count

        row["masculine_preferred_percent"] = masculine_count / total_items * 100
        row["feminine_preferred_percent"] = feminine_count / total_items * 100
        row["equal_percent"] = equal_count / total_items * 100

        row["average_score_difference"] = group_df["score_difference"].mean()
        row["median_score_difference"] = group_df["score_difference"].median()
        row["min_score_difference"] = group_df["score_difference"].min()
        row["max_score_difference"] = group_df["score_difference"].max()

        grouped.append(row)

    return pd.DataFrame(grouped)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        type=str,
        default="results/model_comparison_v07/scoring_results_v07_all_models.csv",
        help="Combined model scoring CSV.",
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        default="results/model_comparison_v07",
        help="Output directory.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    required_columns = [
        "model_name",
        "score_difference",
        "preferred_gender",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    overall_df = summarize_group(df, ["model_name"])
    overall_df.to_csv(
        output_dir / "model_comparison_overall_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    if "dialect" in df.columns:
        dialect_df = summarize_group(df, ["model_name", "dialect"])
        dialect_df.to_csv(
            output_dir / "model_comparison_by_dialect.csv",
            index=False,
            encoding="utf-8-sig",
        )

    if "dimension" in df.columns:
        dimension_df = summarize_group(df, ["model_name", "dimension"])
        dimension_df.to_csv(
            output_dir / "model_comparison_by_dimension.csv",
            index=False,
            encoding="utf-8-sig",
        )

    if "stereotype_direction" in df.columns:
        stereotype_df = summarize_group(df, ["model_name", "stereotype_direction"])
        stereotype_df.to_csv(
            output_dir / "model_comparison_by_stereotype_direction.csv",
            index=False,
            encoding="utf-8-sig",
        )

    if "template_id" in df.columns:
        template_df = summarize_group(df, ["model_name", "template_id"])
        template_df.to_csv(
            output_dir / "model_comparison_by_template_id.csv",
            index=False,
            encoding="utf-8-sig",
        )

    print("Multi-model analysis completed.")
    print("\nMain output:")
    print(output_dir / "model_comparison_overall_summary.csv")


if __name__ == "__main__":
    main()