from pathlib import Path
import argparse
import pandas as pd


def load_scored_files(input_dir):
    input_dir = Path(input_dir)

    files = sorted(input_dir.glob("scoring_results_occupational_v1_*.csv"))

    if not files:
        raise FileNotFoundError(
            f"No scoring_results_occupational_v1_*.csv files found in {input_dir}"
        )

    frames = []

    for file in files:
        df = pd.read_csv(file, encoding="utf-8-sig")
        df["source_file"] = file.name
        frames.append(df)

    return pd.concat(frames, ignore_index=True)


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

        avg_score = group_df["score_difference"].mean()
        median_score = group_df["score_difference"].median()

        if avg_score > 0:
            direction = "masculine"
        elif avg_score < 0:
            direction = "feminine"
        else:
            direction = "equal"

        row.update({
            "total_items": total,
            "masculine_preferred_count": masculine_count,
            "feminine_preferred_count": feminine_count,
            "equal_count": equal_count,
            "masculine_preferred_percent": masculine_count / total * 100 if total else 0,
            "feminine_preferred_percent": feminine_count / total * 100 if total else 0,
            "equal_percent": equal_count / total * 100 if total else 0,
            "average_score_difference": avg_score,
            "median_score_difference": median_score,
            "min_score_difference": group_df["score_difference"].min(),
            "max_score_difference": group_df["score_difference"].max(),
            "average_direction": direction,
        })

        rows.append(row)

    return pd.DataFrame(rows)


def build_template_volatility(summary_by_template):
    rows = []

    for model_name, model_df in summary_by_template.groupby("model_name"):
        min_row = model_df.loc[model_df["average_score_difference"].idxmin()]
        max_row = model_df.loc[model_df["average_score_difference"].idxmax()]

        avg_scores = model_df["average_score_difference"]

        masculine_templates = int((avg_scores > 0).sum())
        feminine_templates = int((avg_scores < 0).sum())
        equal_templates = int((avg_scores == 0).sum())

        direction_flip_present = (
            masculine_templates > 0 and feminine_templates > 0
        )

        volatility_range = (
            model_df["average_score_difference"].max()
            - model_df["average_score_difference"].min()
        )

        volatility_std = model_df["average_score_difference"].std()

        rows.append({
            "model_name": model_name,
            "num_templates": len(model_df),
            "masculine_direction_templates": masculine_templates,
            "feminine_direction_templates": feminine_templates,
            "equal_direction_templates": equal_templates,
            "direction_flip_present": direction_flip_present,
            "template_volatility_range": volatility_range,
            "template_volatility_std": volatility_std,
            "most_masculine_template": max_row["template_id"],
            "most_masculine_template_avg_score": max_row["average_score_difference"],
            "most_feminine_template": min_row["template_id"],
            "most_feminine_template_avg_score": min_row["average_score_difference"],
        })

    return pd.DataFrame(rows)


def build_dialect_shift(summary_by_dialect):
    rows = []

    for model_name, model_df in summary_by_dialect.groupby("model_name"):
        dialect_scores = {
            row["dialect"]: row["average_score_difference"]
            for _, row in model_df.iterrows()
        }

        msa_score = dialect_scores.get("MSA")
        egyptian_score = dialect_scores.get("Egyptian")

        if msa_score is not None and egyptian_score is not None:
            egyptian_minus_msa = egyptian_score - msa_score
        else:
            egyptian_minus_msa = None

        rows.append({
            "model_name": model_name,
            "msa_average_score_difference": msa_score,
            "egyptian_average_score_difference": egyptian_score,
            "egyptian_minus_msa": egyptian_minus_msa,
            "msa_direction": (
                "masculine" if msa_score and msa_score > 0
                else "feminine" if msa_score and msa_score < 0
                else "equal"
            ),
            "egyptian_direction": (
                "masculine" if egyptian_score and egyptian_score > 0
                else "feminine" if egyptian_score and egyptian_score < 0
                else "equal"
            ),
        })

    return pd.DataFrame(rows)


def build_template_pair_comparison(summary_by_template):
    """
    Compare MSA and Egyptian templates that share similar semantic frames.
    """

    rows = []

    for model_name, model_df in summary_by_template.groupby("model_name"):
        for semantic_frame, frame_df in model_df.groupby("semantic_frame"):
            if frame_df["dialect"].nunique() < 2:
                continue

            dialect_scores = {
                row["dialect"]: row["average_score_difference"]
                for _, row in frame_df.iterrows()
            }

            msa_score = dialect_scores.get("MSA")
            egyptian_score = dialect_scores.get("Egyptian")

            if msa_score is None or egyptian_score is None:
                continue

            rows.append({
                "model_name": model_name,
                "semantic_frame": semantic_frame,
                "msa_average_score_difference": msa_score,
                "egyptian_average_score_difference": egyptian_score,
                "egyptian_minus_msa": egyptian_score - msa_score,
                "same_direction": (
                    (msa_score > 0 and egyptian_score > 0)
                    or (msa_score < 0 and egyptian_score < 0)
                    or (msa_score == 0 and egyptian_score == 0)
                ),
            })

    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input_dir",
        required=True,
        help="Directory containing v4 scoring_results_occupational_v1_*.csv files.",
    )

    parser.add_argument(
        "--output_dir",
        required=True,
        help="Directory to save v4 sensitivity analysis outputs.",
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_scored_files(args.input_dir)

    required_columns = [
        "model_name",
        "preferred_gender",
        "score_difference",
        "template_id",
        "template_type",
        "semantic_frame",
        "dialect",
        "field",
        "stereotype_label",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}\n"
            f"Available columns: {list(df.columns)}"
        )

    combined_path = output_dir / "combined_v4_scored_results.csv"
    df.to_csv(combined_path, index=False, encoding="utf-8-sig")

    summary_overall = summarize_group(df, ["model_name"])
    summary_by_template = summarize_group(
        df,
        ["model_name", "dialect", "template_id", "template_type", "semantic_frame"],
    )
    summary_by_semantic_frame = summarize_group(
        df,
        ["model_name", "semantic_frame"],
    )
    summary_by_dialect = summarize_group(
        df,
        ["model_name", "dialect"],
    )
    summary_by_template_type = summarize_group(
        df,
        ["model_name", "template_type"],
    )
    summary_by_stereotype = summarize_group(
        df,
        ["model_name", "stereotype_label"],
    )
    summary_by_field = summarize_group(
        df,
        ["model_name", "field"],
    )

    template_volatility = build_template_volatility(summary_by_template)
    dialect_shift = build_dialect_shift(summary_by_dialect)
    template_pair_comparison = build_template_pair_comparison(summary_by_template)

    summary_overall.to_csv(
        output_dir / "summary_overall_by_model.csv",
        index=False,
        encoding="utf-8-sig",
    )
    summary_by_template.to_csv(
        output_dir / "summary_by_model_template.csv",
        index=False,
        encoding="utf-8-sig",
    )
    summary_by_semantic_frame.to_csv(
        output_dir / "summary_by_model_semantic_frame.csv",
        index=False,
        encoding="utf-8-sig",
    )
    summary_by_dialect.to_csv(
        output_dir / "summary_by_model_dialect.csv",
        index=False,
        encoding="utf-8-sig",
    )
    summary_by_template_type.to_csv(
        output_dir / "summary_by_model_template_type.csv",
        index=False,
        encoding="utf-8-sig",
    )
    summary_by_stereotype.to_csv(
        output_dir / "summary_by_model_stereotype_label.csv",
        index=False,
        encoding="utf-8-sig",
    )
    summary_by_field.to_csv(
        output_dir / "summary_by_model_field.csv",
        index=False,
        encoding="utf-8-sig",
    )
    template_volatility.to_csv(
        output_dir / "template_volatility_by_model.csv",
        index=False,
        encoding="utf-8-sig",
    )
    dialect_shift.to_csv(
        output_dir / "dialect_shift_by_model.csv",
        index=False,
        encoding="utf-8-sig",
    )
    template_pair_comparison.to_csv(
        output_dir / "template_pair_dialect_comparison.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("v4 template sensitivity analysis completed.")
    print("Input directory:", args.input_dir)
    print("Output directory:", output_dir)

    print("\nOverall:")
    print(summary_overall.to_string(index=False))

    print("\nTemplate volatility:")
    print(template_volatility.to_string(index=False))

    print("\nDialect shift:")
    print(dialect_shift.to_string(index=False))

    print("\nTemplate pair dialect comparison:")
    print(template_pair_comparison.to_string(index=False))


if __name__ == "__main__":
    main()