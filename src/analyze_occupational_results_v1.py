from pathlib import Path
import argparse
import pandas as pd


def normalize_columns(df):
    """
    Make analyzer compatible with old and new benchmark column names.

    Old names:
    occupation_m, occupation_f, stereotype_direction

    New names:
    masculine_occupation, feminine_occupation, stereotype_label
    """

    rename_map = {
        "occupation_m": "masculine_occupation",
        "occupation_f": "feminine_occupation",
        "stereotype_direction": "stereotype_label",
    }

    for old_col, new_col in rename_map.items():
        if old_col in df.columns and new_col not in df.columns:
            df[new_col] = df[old_col]

    return df


def summarize_group(df, group_cols):
    rows = []

    for group_values, group_df in df.groupby(group_cols, dropna=False):
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


def validate_required_columns(df):
    required_columns = [
        "id",
        "model_name",
        "field",
        "dialect",
        "template_id",
        "masculine_sentence",
        "feminine_sentence",
        "masculine_score",
        "feminine_score",
        "score_difference",
        "preferred_gender",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}\n"
            f"Available columns: {list(df.columns)}"
        )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Scored occupational result CSV file.",
    )

    parser.add_argument(
        "--output_dir",
        required=True,
        help="Directory to save analysis outputs.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, encoding="utf-8-sig")
    df = normalize_columns(df)

    validate_required_columns(df)

    # Main summaries
    summary_overall = summarize_group(df, ["model_name"])
    summary_by_field = summarize_group(df, ["model_name", "field"])
    summary_by_dialect = summarize_group(df, ["model_name", "dialect"])
    summary_by_template = summarize_group(df, ["model_name", "template_id"])

    summary_overall.to_csv(
        output_dir / "summary_overall.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary_by_field.to_csv(
        output_dir / "summary_by_field.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary_by_dialect.to_csv(
        output_dir / "summary_by_dialect.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary_by_template.to_csv(
        output_dir / "summary_by_template.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # v3-specific summaries if columns exist
    if "stereotype_label" in df.columns:
        summary_by_stereotype = summarize_group(
            df,
            ["model_name", "stereotype_label"],
        )

        summary_by_stereotype.to_csv(
            output_dir / "summary_by_stereotype_label.csv",
            index=False,
            encoding="utf-8-sig",
        )

    if "template_type" in df.columns:
        summary_by_template_type = summarize_group(
            df,
            ["model_name", "template_type"],
        )

        summary_by_template_type.to_csv(
            output_dir / "summary_by_template_type.csv",
            index=False,
            encoding="utf-8-sig",
        )

    if "grammatical_gender_marker" in df.columns:
        summary_by_gender_marker = summarize_group(
            df,
            ["model_name", "grammatical_gender_marker"],
        )

        summary_by_gender_marker.to_csv(
            output_dir / "summary_by_grammatical_gender_marker.csv",
            index=False,
            encoding="utf-8-sig",
        )

    # Save full scored file copy
    df.to_csv(
        output_dir / "scored_results_with_analysis.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("Occupational result analysis completed.")
    print("Input:", input_path)
    print("Outputs saved to:", output_dir)

    print("\nOverall summary:")
    print(summary_overall.to_string(index=False))

    print("\nSummary by field:")
    print(summary_by_field.to_string(index=False))

    if "stereotype_label" in df.columns:
        print("\nSummary by stereotype label:")
        print(summary_by_stereotype.to_string(index=False))


if __name__ == "__main__":
    main()