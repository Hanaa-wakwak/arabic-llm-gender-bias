import argparse
from pathlib import Path

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze Arabic gender minimal-pair scoring results."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to scoring results CSV file.",
    )

    parser.add_argument(
        "--output_dir",
        default="results",
        help="Directory where analysis files will be saved.",
    )

    parser.add_argument(
        "--prefix",
        required=True,
        help="Prefix for output analysis files, e.g. v01 or template_test_v01.",
    )

    return parser.parse_args()


def create_overall_summary(df):
    total_items = len(df)

    masculine_preferred = int((df["preferred_gender"] == "masculine").sum())
    feminine_preferred = int((df["preferred_gender"] == "feminine").sum())
    equal_preferred = int((df["preferred_gender"] == "equal").sum())

    summary = pd.DataFrame([{
        "total_items": total_items,
        "masculine_preferred_count": masculine_preferred,
        "feminine_preferred_count": feminine_preferred,
        "equal_count": equal_preferred,
        "masculine_preferred_percent": masculine_preferred / total_items * 100,
        "feminine_preferred_percent": feminine_preferred / total_items * 100,
        "equal_percent": equal_preferred / total_items * 100,
        "average_score_difference": df["score_difference"].mean(),
        "median_score_difference": df["score_difference"].median(),
        "min_score_difference": df["score_difference"].min(),
        "max_score_difference": df["score_difference"].max(),
    }])

    return summary


def group_analysis(df, group_col):
    grouped = (
        df.groupby(group_col)
        .agg(
            total_items=("score_difference", "count"),
            average_score_difference=("score_difference", "mean"),
            median_score_difference=("score_difference", "median"),
            min_score_difference=("score_difference", "min"),
            max_score_difference=("score_difference", "max"),
            masculine_preferred_count=("preferred_gender", lambda x: (x == "masculine").sum()),
            feminine_preferred_count=("preferred_gender", lambda x: (x == "feminine").sum()),
            equal_count=("preferred_gender", lambda x: (x == "equal").sum()),
        )
        .reset_index()
    )

    grouped["masculine_preferred_percent"] = (
        grouped["masculine_preferred_count"] / grouped["total_items"] * 100
    )

    grouped["feminine_preferred_percent"] = (
        grouped["feminine_preferred_count"] / grouped["total_items"] * 100
    )

    grouped["equal_percent"] = (
        grouped["equal_count"] / grouped["total_items"] * 100
    )

    return grouped


def main():
    args = parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    required_columns = ["score_difference", "preferred_gender"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    print("=" * 70)
    print("Arabic Gender Minimal Pair Analysis")
    print("=" * 70)
    print(f"Input: {input_path}")
    print(f"Rows: {len(df)}")

    # Overall summary
    summary = create_overall_summary(df)
    summary_path = output_dir / f"analysis_summary_{args.prefix}.csv"
    summary.to_csv(summary_path, index=False, encoding="utf-8-sig")

    print("\nOverall summary:")
    print(summary)

    print("\nSaved:")
    print(summary_path)

    # Optional grouped analyses
    possible_group_cols = [
        "dialect",
    "dimension",
    "stereotype_direction",
    "template_type",
    "template_id",
    "concept_id",
    ]

    for col in possible_group_cols:
        if col in df.columns:
            grouped = group_analysis(df, col)
            output_path = output_dir / f"analysis_by_{col}_{args.prefix}.csv"
            grouped.to_csv(output_path, index=False, encoding="utf-8-sig")

            print(f"\nAnalysis by {col}:")
            print(grouped)

            print("\nSaved:")
            print(output_path)

    # Detailed analysis if these columns exist
    detailed_cols = [
          col for col in [
        "dialect",
        "dimension",
        "stereotype_direction",
        "template_type",
        "template_id",
        "concept_id",
    ]
    if col in df.columns
    ]

    if len(detailed_cols) >= 2:
        detailed = (
            df.groupby(detailed_cols)
            .agg(
                total_items=("score_difference", "count"),
                average_score_difference=("score_difference", "mean"),
                median_score_difference=("score_difference", "median"),
                masculine_preferred_count=("preferred_gender", lambda x: (x == "masculine").sum()),
                feminine_preferred_count=("preferred_gender", lambda x: (x == "feminine").sum()),
                equal_count=("preferred_gender", lambda x: (x == "equal").sum()),
            )
            .reset_index()
        )

        detailed["masculine_preferred_percent"] = (
            detailed["masculine_preferred_count"] / detailed["total_items"] * 100
        )

        detailed["feminine_preferred_percent"] = (
            detailed["feminine_preferred_count"] / detailed["total_items"] * 100
        )

        detailed_path = output_dir / f"analysis_detailed_{args.prefix}.csv"
        detailed.to_csv(detailed_path, index=False, encoding="utf-8-sig")

        print("\nDetailed analysis:")
        print(detailed)

        print("\nSaved:")
        print(detailed_path)

    print("\nDone.")


if __name__ == "__main__":
    main()