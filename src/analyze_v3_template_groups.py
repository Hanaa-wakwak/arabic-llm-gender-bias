from pathlib import Path
import argparse
import pandas as pd


OLD_TEMPLATES = {
    "msa_demonstrative_workplace",
    "msa_said_professional",
    "egy_direct_workplace",
    "egy_said_role",
}


NEW_TEMPLATES = {
    "msa_achievement",
    "egy_skill_evaluation",
}


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


def template_group(template_id):
    if template_id in OLD_TEMPLATES:
        return "old_v2_template"
    if template_id in NEW_TEMPLATES:
        return "new_v3_template"
    return "unknown_template"


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Scored v3 occupational CSV.",
    )

    parser.add_argument(
        "--output_dir",
        required=True,
        help="Directory to save diagnostic outputs.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    required = [
        "model_name",
        "template_id",
        "preferred_gender",
        "score_difference",
    ]

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}\n"
            f"Available columns: {list(df.columns)}"
        )

    df["template_group"] = df["template_id"].apply(template_group)

    summary_by_template_group = summarize_group(
        df,
        ["model_name", "template_group"],
    )

    summary_by_template = summarize_group(
        df,
        ["model_name", "template_group", "template_id"],
    )

    summary_by_template_group.to_csv(
        output_dir / "summary_by_template_group.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary_by_template.to_csv(
        output_dir / "summary_by_template_diagnostic.csv",
        index=False,
        encoding="utf-8-sig",
    )

    df.to_csv(
        output_dir / "v3_scored_with_template_group.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("v3 template group diagnostic completed.")
    print("Input:", input_path)
    print("Output:", output_dir)

    print("\nSummary by template group:")
    print(summary_by_template_group.to_string(index=False))

    print("\nSummary by template:")
    print(summary_by_template.to_string(index=False))


if __name__ == "__main__":
    main()